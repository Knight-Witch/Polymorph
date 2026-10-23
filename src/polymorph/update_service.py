from __future__ import annotations

import hashlib
import json
import os
import re
import shutil
import subprocess
import tempfile
import urllib.request
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import urlsplit

from .constants import APP_VERSION, LATEST_RELEASE_API, REPO_URL

_VERSION_RE = re.compile(r"(?:polymorph-)?v?(\d+)\.(\d+)\.(\d+)", re.IGNORECASE)
_SHA256_RE = re.compile(r"^[0-9a-fA-F]{64}$")
_RELEASE_ASSET_PATH_PREFIX = "/Knight-Witch/Polymorph/releases/download/"
_DOWNLOAD_CHUNK_BYTES = 1024 * 1024
_MAX_CHECKSUM_BYTES = 4096
_MAX_INSTALLER_BYTES = 750_000_000
_DOWNLOAD_TIMEOUT = 30.0


@dataclass(frozen=True, slots=True)
class ReleaseInfo:
    version: str
    page_url: str
    installer_url: str | None
    checksum_url: str | None
    notes: str
    kind: str = "installer"
    run_id: int | None = None
    artifact_name: str | None = None
    delta_url: str | None = None
    delta_checksum_url: str | None = None


def _version_tuple(value: str) -> tuple[int, int, int]:
    match = _VERSION_RE.search(value)
    return tuple(map(int, match.groups())) if match else (0, 0, 0)


def is_newer(candidate: str, current: str = APP_VERSION) -> bool:
    # Prerelease revisions share a three-part base version; compare the Dev
    # counter rather than treating every prerelease build as equal.
    dev = re.compile(r"^(\d+)\.(\d+)\.(\d+)-dev\.(\d+)$")
    newer_dev, old_dev = dev.fullmatch(candidate), dev.fullmatch(current)
    if newer_dev and old_dev:
        return tuple(map(int, newer_dev.groups())) > tuple(map(int, old_dev.groups()))
    return _version_tuple(candidate) > _version_tuple(current)


def _asset_names(version: str) -> tuple[str, str]:
    installer = f"Polymorph_Setup_v{version}.exe"
    return installer, f"{installer}.sha256"


def _is_allowed_release_asset_url(url: str) -> bool:
    try:
        parsed = urlsplit(url)
    except ValueError:
        return False
    return (
        parsed.scheme.lower() == "https"
        and parsed.netloc.lower() == "github.com"
        and parsed.path.casefold().startswith(_RELEASE_ASSET_PATH_PREFIX.casefold())
    )


def _select_release_assets(payload: dict, version: str) -> tuple[str | None, str | None]:
    installer_name, checksum_name = _asset_names(version)
    expected_installer = installer_name.casefold()
    expected_checksum = checksum_name.casefold()
    installer_url = None
    checksum_url = None

    for asset in payload.get("assets") or []:
        name = str(asset.get("name") or "")
        url = str(asset.get("browser_download_url") or "")
        if not _is_allowed_release_asset_url(url):
            continue
        folded = name.casefold()
        if folded == expected_installer:
            installer_url = url
        elif folded == expected_checksum:
            checksum_url = url

    return installer_url, checksum_url


def _select_release_delta_assets(payload: dict, current: str, target: str) -> tuple[str | None, str | None]:
    # Only an exact-version pair hosted on the official public Release is valid.
    archive = f"Polymorph_Update_from-{current}_to-{target}.zip"
    desired = {archive.casefold(): None, (archive + ".sha256").casefold(): None}
    for asset in payload.get("assets") or []:
        name = str(asset.get("name") or "").casefold()
        url = str(asset.get("browser_download_url") or "")
        # Match both the public release *tag* and the exact asset basename.
        # Never accept a similarly named asset from a different release.
        expected_path = f"/Knight-Witch/Polymorph/releases/download/v{target}/{asset.get('name')}"
        if (name in desired and _is_allowed_release_asset_url(url)
                and urlsplit(url).path.casefold() == expected_path.casefold()):
            desired[name] = url
    return desired[archive.casefold()], desired[(archive + ".sha256").casefold()]


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
    installer_url, checksum_url = _select_release_assets(payload, version)
    delta_url, delta_checksum = (None, None)
    delta_url, delta_checksum = _select_release_delta_assets(payload, APP_VERSION, version)

    return ReleaseInfo(
        version=version,
        page_url=str(payload.get("html_url") or ""),
        installer_url=installer_url,
        checksum_url=checksum_url,
        notes=str(payload.get("body") or ""),
        kind="stable_delta" if delta_url and delta_checksum else "installer",
        delta_url=delta_url,
        delta_checksum_url=delta_checksum,
    )


def _download_to_path(
    url: str,
    destination: Path,
    *,
    timeout: float = _DOWNLOAD_TIMEOUT,
    max_bytes: int,
) -> str:
    if not _is_allowed_release_asset_url(url):
        raise RuntimeError("Update asset URL is not an official Polymorph GitHub release URL.")

    request = urllib.request.Request(url, headers={"User-Agent": f"Polymorph/{APP_VERSION}"})
    hasher = hashlib.sha256()
    total = 0
    destination.parent.mkdir(parents=True, exist_ok=True)

    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            length = response.headers.get("Content-Length")
            if length:
                try:
                    declared = int(length)
                except ValueError:
                    declared = 0
                if declared > max_bytes:
                    raise RuntimeError("Update asset is larger than the allowed download limit.")

            with destination.open("wb") as output:
                while True:
                    chunk = response.read(_DOWNLOAD_CHUNK_BYTES)
                    if not chunk:
                        break
                    total += len(chunk)
                    if total > max_bytes:
                        raise RuntimeError("Update asset exceeded the allowed download limit.")
                    output.write(chunk)
                    hasher.update(chunk)
    except Exception:
        try:
            destination.unlink(missing_ok=True)
        except OSError:
            pass
        raise

    if total == 0:
        try:
            destination.unlink(missing_ok=True)
        except OSError:
            pass
        raise RuntimeError("Update asset download was empty.")
    return hasher.hexdigest().lower()


def _parse_checksum(text: str, expected_filename: str) -> str:
    first_line = next((line.strip() for line in text.splitlines() if line.strip()), "")
    if not first_line:
        raise RuntimeError("Update checksum file is empty.")

    parts = first_line.split(maxsplit=1)
    digest = parts[0].lower()
    if not _SHA256_RE.fullmatch(digest):
        raise RuntimeError("Update checksum file does not contain a valid SHA-256 digest.")

    if len(parts) == 2:
        named_file = parts[1].strip()
        if named_file.startswith("*"):
            named_file = named_file[1:]
        named_file = named_file.replace("\\", "/").rsplit("/", 1)[-1]
        if named_file.casefold() != expected_filename.casefold():
            raise RuntimeError("Update checksum refers to a different installer file.")
    return digest


def download_and_verify_installer(release: ReleaseInfo) -> Path:
    if not release.installer_url or not release.checksum_url:
        raise RuntimeError("This release does not include the exact Polymorph installer and checksum pair.")

    installer_name, checksum_name = _asset_names(release.version)
    temp_dir = Path(tempfile.mkdtemp(prefix="polymorph-update-"))
    installer = temp_dir / installer_name
    checksum_file = temp_dir / checksum_name

    try:
        _download_to_path(
            release.checksum_url,
            checksum_file,
            max_bytes=_MAX_CHECKSUM_BYTES,
        )
        expected = _parse_checksum(
            checksum_file.read_text(encoding="utf-8", errors="replace"),
            installer_name,
        )
        actual = _download_to_path(
            release.installer_url,
            installer,
            max_bytes=_MAX_INSTALLER_BYTES,
        )
        if actual != expected:
            raise RuntimeError("Downloaded update failed SHA-256 verification.")
        try:
            checksum_file.unlink(missing_ok=True)
        except OSError:
            pass
        return installer
    except Exception:
        shutil.rmtree(temp_dir, ignore_errors=True)
        raise


def download_and_stage_public_delta(release: ReleaseInfo, install_dir: Path) -> Path:
    """Use official public release SHA-256 pair; never fetch from private Dev."""
    if release.kind != "stable_delta" or not release.delta_url or not release.delta_checksum_url:
        raise RuntimeError("No verified official public incremental update is available")
    from .delta_update import sha256, stage_delta
    archive_name = f"Polymorph_Update_from-{APP_VERSION}_to-{release.version}.zip"
    work = Path(tempfile.mkdtemp(prefix="polymorph-public-patch-"))
    try:
        checksum_file = work / (archive_name + ".sha256")
        package = work / archive_name
        _download_to_path(release.delta_checksum_url, checksum_file, max_bytes=_MAX_CHECKSUM_BYTES)
        expected = _parse_checksum(checksum_file.read_text(encoding="utf-8"), archive_name)
        _download_to_path(release.delta_url, package, max_bytes=100_000_000)
        if sha256(package) != expected:
            raise RuntimeError("Public incremental update SHA-256 mismatch")
        return stage_delta(package, install_dir, APP_VERSION, channel="stable")
    finally:
        shutil.rmtree(work, ignore_errors=True)


def launch_installer(installer: Path) -> None:
    if os.name != "nt":
        raise RuntimeError("Automatic installation is currently Windows-only.")
    subprocess.Popen([str(installer)], close_fds=True)



def fetch_latest_for_channel() -> ReleaseInfo | None:
    """Stable checks only the official public GitHub Release."""
    return fetch_latest_release()
