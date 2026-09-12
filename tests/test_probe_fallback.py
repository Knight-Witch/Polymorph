import os
import struct
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from polymorph.probe import ProbeError, _creation_flags, probe_media


def u24(value: int) -> bytes:
    return bytes((value & 255, (value >> 8) & 255, (value >> 16) & 255))


def chunk(kind: bytes, payload: bytes) -> bytes:
    out = kind + struct.pack("<I", len(payload)) + payload
    return out + (b"\0" if len(payload) & 1 else b"")


class ProbeFallbackTests(unittest.TestCase):
    def test_riff_metadata_survives_ffprobe_failure(self):
        vp8x = bytes([0x02, 0, 0, 0]) + u24(999) + u24(999)
        anmf = u24(0) + u24(0) + u24(999) + u24(999) + u24(50) + b"\0"
        body = b"WEBP" + chunk(b"VP8X", vp8x) + chunk(b"ANMF", anmf) + chunk(b"ANMF", anmf)
        data = b"RIFF" + struct.pack("<I", len(body)) + body
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "fallback.webp"
            path.write_bytes(data)
            with patch("polymorph.probe._ffprobe_json", side_effect=ProbeError("decoder failure")):
                info = probe_media(Path("ffprobe"), path)
        self.assertEqual((info.width, info.height), (1000, 1000))
        self.assertEqual(info.frame_count, 2)
        self.assertAlmostEqual(info.duration_s, 0.1)
        self.assertAlmostEqual(info.fps, 20.0)

    def test_windows_ffprobe_uses_no_console_window_flag(self):
        if os.name == "nt":
            self.assertEqual(_creation_flags(), subprocess.CREATE_NO_WINDOW)
        else:
            self.assertEqual(_creation_flags(), 0)


if __name__ == "__main__":
    unittest.main()
