from __future__ import annotations

import hashlib
import json
import os
import re
import subprocess
import tempfile
import urllib.request
from dataclasses import dataclass
from pathlib import Path

from .constants import APP_VERSION, LATEST_RELEASE_API

_VERSION_RE = re.compile(r"(?:polymorph-)?v?(\d+)\.(\d+)\.(\d+)", re.IGNORECASE)


@dataclass(frozen=True, slots=True)
class ReleaseInfo:
    version: str
    page_url: str
    installer_url: str | None
    checksum_url: str | None
    notes: str


def _version_tuple(value: str) -> tuple[int, int, int]:
    match = _VERSION_RE.search(value)
    return tuple(map(int, match.groups())) if match else (0, 0, 0)


def is_newer(candidate: str, current: str = APP_VERSION) -> bool:
    return _version_tuple(candidate) > _version_tuple(current)


def fetch_latest_release(timeout: float = 5.0) -> ReleaseInfo | None:
    request = urllib.request.Request(
        LATEST_RELEASE_API,
        headers={"Accept": "application/vnd.github+json", "User-Agent": f"Polymorph/{APP_VERSION}"},
    )
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            payload = json.load(response)
    except Exception:
        return None

    tag = str(payload.get("tag_name") or "")
    if "polymorph" not in tag.lower() and not tag.lower().startswith("v"):
        return None
    version_match = _VERSION_RE.search(tag)
    if not version_match:
        return None
    version = ".".join(version_match.groups())

    installer_url = None
    checksum_url = None
    for asset in payload.get("assets") or []:
        name = str(asset.get("name") or "")
        url = asset.get("browser_download_url")
        lower = name.lower()
        if lower.endswith(".exe") and "setup" in lower and "polymorph" in lower:
            installer_url = url
        elif lower.endswith(".sha256") and "polymorph" in lower:
            checksum_url = url

    return ReleaseInfo(
        version=version,
        page_url=str(payload.get("html_url") or ""),
        installer_url=installer_url,
        checksum_url=checksum_url,
        notes=str(payload.get("body") or ""),
    )


def download_and_verify_installer(release: ReleaseInfo) -> Path:
    if not release.installer_url or not release.checksum_url:
        raise RuntimeError("This release does not include both an installer and checksum.")

    temp_dir = Path(tempfile.mkdtemp(prefix="polymorph-update-"))
    installer = temp_dir / f"Polymorph_Setup_v{release.version}.exe"
    checksum_file = temp_dir / f"Polymorph_Setup_v{release.version}.exe.sha256"
    urllib.request.urlretrieve(release.installer_url, installer)
    urllib.request.urlretrieve(release.checksum_url, checksum_file)

    expected = checksum_file.read_text(encoding="utf-8", errors="replace").strip().split()[0].lower()
    actual = hashlib.sha256(installer.read_bytes()).hexdigest().lower()
    if not expected or actual != expected:
        raise RuntimeError("Downloaded update failed SHA-256 verification.")
    return installer


def launch_installer(installer: Path) -> None:
    if os.name != "nt":
        raise RuntimeError("Automatic installation is currently Windows-only.")
    subprocess.Popen([str(installer)], close_fds=True)
