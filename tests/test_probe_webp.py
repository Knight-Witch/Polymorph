import struct
import tempfile
import unittest
from pathlib import Path

from polymorph.probe import probe_webp_riff


def u24(value: int) -> bytes:
    return bytes((value & 255, (value >> 8) & 255, (value >> 16) & 255))


def chunk(kind: bytes, payload: bytes) -> bytes:
    out = kind + struct.pack("<I", len(payload)) + payload
    return out + (b"\0" if len(payload) & 1 else b"")


class WebPRiffTests(unittest.TestCase):
    def test_vp8x_and_anmf_metadata(self):
        vp8x = bytes([0x02, 0, 0, 0]) + u24(2047) + u24(2047)
        # ANMF header: x(3), y(3), width-1(3), height-1(3), duration(3), flags(1)
        anmf_a = u24(0) + u24(0) + u24(2047) + u24(2047) + u24(33) + b"\0"
        anmf_b = u24(0) + u24(0) + u24(2047) + u24(2047) + u24(34) + b"\0"
        body = b"WEBP" + chunk(b"VP8X", vp8x) + chunk(b"ANMF", anmf_a) + chunk(b"ANMF", anmf_b)
        data = b"RIFF" + struct.pack("<I", len(body)) + body
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "test.webp"
            path.write_bytes(data)
            width, height, durations = probe_webp_riff(path)
        self.assertEqual((width, height), (2048, 2048))
        self.assertEqual(durations, [33, 34])


if __name__ == "__main__":
    unittest.main()
