"""Safely validate and stage file-level updates; only an external process applies them."""
from __future__ import annotations

import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path

from .resources import asset_path

_VERSION = re.compile(r"^\d+\.\d+\.\d+(?:-dev\.\d+)?$")
_SAFE_PATH = re.compile(r"^[A-Za-z0-9_./+\-]+$")
_SHA = re.compile(r"^[0-9a-f]{64}$")
_MAX_FILES = 500
_MAX_BYTES = 450_000_000

def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()

def safe_path(value: str) -> bool:
    return bool(value and _SAFE_PATH.fullmatch(value) and ".." not in value.split("/")
                and not value.startswith("/") and "//" not in value and "\\" not in value)

def validate_manifest(manifest: dict, from_version: str, *, channel: str) -> list[dict]:
    if not isinstance(manifest, dict) or set(manifest) != {
        "schema", "channel", "from_version", "to_version", "files"
    } or manifest["schema"] != 1:
        raise RuntimeError("Unsupported update manifest")
    if manifest["channel"] != channel or manifest["from_version"] != from_version:
        raise RuntimeError("Update does not match this installed version/channel")
    target = manifest["to_version"]
    if not isinstance(target, str) or not _VERSION.fullmatch(target):
        raise RuntimeError("Invalid target version")
    if (channel == "dev") != ("-dev." in target):
        raise RuntimeError("Update is for a different release channel")
    files = manifest["files"]
    if not isinstance(files, list) or not 0 < len(files) <= _MAX_FILES:
        raise RuntimeError("Invalid update file list")
    seen, total = set(), 0
    for item in files:
        if not isinstance(item, dict) or set(item) != {"path", "before", "after", "size"}:
            raise RuntimeError("Invalid update file metadata")
        name, before, after, size = item["path"], item["before"], item["after"], item["size"]
        if not isinstance(name, str) or not safe_path(name) or name in seen:
            raise RuntimeError("Unsafe or duplicate update path")
        # Only the known, versioned bundled updater helper is an allowed script.
        if (name.lower().endswith((".ps1", ".bat", ".cmd"))
                and name != "_internal/polymorph/assets/updater/apply_delta.ps1") or name == "Uninstall.exe":
            raise RuntimeError("Unexpected executable script or uninstaller in update")
        if before is not None and (not isinstance(before, str) or not _SHA.fullmatch(before)):
            raise RuntimeError("Invalid expected previous checksum")
        if not isinstance(after, str) or not _SHA.fullmatch(after) or type(size) is not int or size < 0:
            raise RuntimeError("Invalid update file checksum/size")
        total += size
        if total > _MAX_BYTES:
            raise RuntimeError("Update payload too large")
        seen.add(name)
    return files

def stage_delta(package: Path, install_dir: Path, from_version: str, channel: str = "dev") -> Path:
    """Verify all old/new hashes before making *any* modifications to the installation."""
    if not package.is_file() or package.stat().st_size > _MAX_BYTES:
        raise RuntimeError("Missing or oversized update archive")
    if not install_dir.is_dir():
        raise RuntimeError("Polymorph installation was not found")
    staging = Path(tempfile.mkdtemp(prefix="polymorph-delta-"))
    try:
        with zipfile.ZipFile(package) as z:
            manifest = json.loads(z.read("manifest.json"))
            files = validate_manifest(manifest, from_version, channel=channel)
            expected = {"manifest.json"} | {"payload/" + f["path"] for f in files}
            if set(z.namelist()) != expected:
                raise RuntimeError("Update archive contains unlisted or missing files")
            (staging / "payload").mkdir(parents=True, exist_ok=True)
            for item in files:
                relative = item["path"]
                current = install_dir / relative
                previous = item["before"]
                if previous is None:
                    if current.exists():
                        raise RuntimeError(f"Update destination already exists: {relative}")
                elif not current.is_file() or sha256(current) != previous:
                    raise RuntimeError(f"Installed file differs from expected base: {relative}")
                info = z.getinfo("payload/" + relative)
                if info.file_size != item["size"] or ((info.external_attr >> 16) & 0o170000) == 0o120000:
                    raise RuntimeError("Update file size or file type invalid")
                dst = staging / "payload" / relative
                dst.parent.mkdir(parents=True, exist_ok=True)
                with z.open(info) as source, dst.open("wb") as out:
                    shutil.copyfileobj(source, out, 1024 * 1024)
                if sha256(dst) != item["after"]:
                    raise RuntimeError(f"Update checksum mismatch: {relative}")
        (staging / "manifest.json").write_text(json.dumps(manifest), encoding="utf-8")
        helper = asset_path("updater/apply_delta.ps1")
        if not helper.is_file():
            raise RuntimeError("Bundled updater helper is missing")
        shutil.copy2(helper, staging / "apply_delta.ps1")
        return staging
    except Exception:
        shutil.rmtree(staging, ignore_errors=True)
        raise

def launch_staged_update(staging: Path, install_dir: Path) -> None:
    if os.name != "nt" or not getattr(sys, "frozen", False):
        raise RuntimeError("Automatic patch installation requires packaged Polymorph on Windows")
    manifest = json.loads((staging / "manifest.json").read_text(encoding="utf-8"))
    subprocess.Popen(
        ["powershell.exe", "-NoProfile", "-NonInteractive", "-ExecutionPolicy", "Bypass",
         "-WindowStyle", "Hidden", "-File", str(staging / "apply_delta.ps1"),
         "-InstallDir", str(install_dir), "-StageDir", str(staging),
         "-ParentPid", str(os.getpid()), "-BaseVersion", manifest["from_version"],
         "-TargetVersion", manifest["to_version"]],
        creationflags=subprocess.CREATE_NO_WINDOW,
        close_fds=True,
    )
