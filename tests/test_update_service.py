import hashlib
import io
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from polymorph.update_service import (
    _download_to_path,
    _is_allowed_release_asset_url,
    _parse_checksum,
    _select_release_assets,
    is_newer,
)


class UpdateVersionTests(unittest.TestCase):
    def test_newer_release(self):
        self.assertTrue(is_newer("1.0.0", "0.1.0-dev.1"))

    def test_same_release(self):
        self.assertFalse(is_newer("1.2.3", "1.2.3"))

    def test_older_release(self):
        self.assertFalse(is_newer("1.2.2", "1.2.3"))


class ReleaseAssetTests(unittest.TestCase):
    def test_only_exact_installer_and_companion_checksum_are_selected(self):
        base = "https://github.com/Knight-Witch/Polymorph/releases/download/v1.2.3/"
        payload = {
            "assets": [
                {"name": "Polymorph_Setup_v1.2.3.exe", "browser_download_url": base + "Polymorph_Setup_v1.2.3.exe"},
                {"name": "Polymorph_Setup_v1.2.3.exe.sha256", "browser_download_url": base + "Polymorph_Setup_v1.2.3.exe.sha256"},
                {"name": "Polymorph-dev.zip.sha256", "browser_download_url": base + "Polymorph-dev.zip.sha256"},
            ]
        }
        installer, checksum = _select_release_assets(payload, "1.2.3")
        self.assertEqual(installer, base + "Polymorph_Setup_v1.2.3.exe")
        self.assertEqual(checksum, base + "Polymorph_Setup_v1.2.3.exe.sha256")

    def test_mismatched_checksum_asset_is_not_accepted(self):
        base = "https://github.com/Knight-Witch/Polymorph/releases/download/v1.2.3/"
        payload = {
            "assets": [
                {"name": "Polymorph_Setup_v1.2.3.exe", "browser_download_url": base + "Polymorph_Setup_v1.2.3.exe"},
                {"name": "Polymorph_v1.2.3.sha256", "browser_download_url": base + "Polymorph_v1.2.3.sha256"},
            ]
        }
        installer, checksum = _select_release_assets(payload, "1.2.3")
        self.assertIsNotNone(installer)
        self.assertIsNone(checksum)

    def test_only_official_repo_release_urls_are_allowed(self):
        valid = "https://github.com/Knight-Witch/Polymorph/releases/download/v1.2.3/Polymorph_Setup_v1.2.3.exe"
        evil = "https://example.com/Knight-Witch/Polymorph/releases/download/v1.2.3/Polymorph_Setup_v1.2.3.exe"
        sibling = "https://github.com/Other/Polymorph/releases/download/v1.2.3/Polymorph_Setup_v1.2.3.exe"
        self.assertTrue(_is_allowed_release_asset_url(valid))
        self.assertFalse(_is_allowed_release_asset_url(evil))
        self.assertFalse(_is_allowed_release_asset_url(sibling))


class ChecksumTests(unittest.TestCase):
    def test_checksum_accepts_exact_installer_filename(self):
        digest = "a" * 64
        self.assertEqual(
            _parse_checksum(f"{digest}  Polymorph_Setup_v1.2.3.exe\n", "Polymorph_Setup_v1.2.3.exe"),
            digest,
        )

    def test_checksum_rejects_different_filename(self):
        digest = "b" * 64
        with self.assertRaises(RuntimeError):
            _parse_checksum(f"{digest}  Other.exe\n", "Polymorph_Setup_v1.2.3.exe")

    def test_checksum_rejects_malformed_digest(self):
        with self.assertRaises(RuntimeError):
            _parse_checksum("not-a-sha256  Polymorph_Setup_v1.2.3.exe\n", "Polymorph_Setup_v1.2.3.exe")


class _FakeResponse(io.BytesIO):
    def __init__(self, data: bytes, declared_length: int | None = None):
        super().__init__(data)
        self.headers = {
            "Content-Length": str(len(data) if declared_length is None else declared_length)
        }

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        self.close()
        return False


class StreamingDownloadTests(unittest.TestCase):
    def test_download_streams_to_disk_and_returns_sha256(self):
        data = (b"polymorph-update-test" * 1000)
        expected = hashlib.sha256(data).hexdigest()
        url = "https://github.com/Knight-Witch/Polymorph/releases/download/v1.2.3/Polymorph_Setup_v1.2.3.exe"
        with tempfile.TemporaryDirectory() as tmp:
            destination = Path(tmp) / "installer.exe"
            with patch("polymorph.update_service.urllib.request.urlopen", return_value=_FakeResponse(data)):
                actual = _download_to_path(url, destination, max_bytes=len(data) + 1)
            self.assertEqual(actual, expected)
            self.assertEqual(destination.read_bytes(), data)

    def test_download_rejects_declared_oversize_asset(self):
        data = b"small"
        url = "https://github.com/Knight-Witch/Polymorph/releases/download/v1.2.3/Polymorph_Setup_v1.2.3.exe"
        with tempfile.TemporaryDirectory() as tmp:
            destination = Path(tmp) / "installer.exe"
            with patch(
                "polymorph.update_service.urllib.request.urlopen",
                return_value=_FakeResponse(data, declared_length=1000),
            ):
                with self.assertRaises(RuntimeError):
                    _download_to_path(url, destination, max_bytes=100)
            self.assertFalse(destination.exists())


if __name__ == "__main__":
    unittest.main()
