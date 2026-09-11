import tempfile
import unittest
from pathlib import Path

from polymorph.gif_timing import patch_last_frame_delay, read_frame_delays_cs


def _frame(delay_cs: int) -> bytes:
    # Minimal timed image block. The parser only needs structurally valid GIF
    # extension/image sub-block boundaries for this pure timing test.
    gce = bytes([
        0x21, 0xF9, 0x04, 0x00,
        delay_cs & 0xFF, (delay_cs >> 8) & 0xFF,
        0x00, 0x00,
    ])
    descriptor = bytes([
        0x2C,
        0, 0, 0, 0,
        1, 0, 1, 0,
        0x00,
    ])
    image_data = bytes([0x02, 0x02, 0x4C, 0x01, 0x00])
    return gce + descriptor + image_data


def _gif(delays: list[int]) -> bytes:
    header = b"GIF89a"
    logical_screen = bytes([
        1, 0, 1, 0,
        0x00,
        0x00,
        0x00,
    ])
    return header + logical_screen + b"".join(_frame(delay) for delay in delays) + b"\x3b"


class GifTimingTests(unittest.TestCase):
    def test_patch_changes_only_final_delay(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "test.gif"
            original = _gif([8, 8, 8])
            path.write_bytes(original)

            patch_last_frame_delay(path, 4)

            patched = path.read_bytes()
            self.assertEqual(len(patched), len(original))
            self.assertEqual(read_frame_delays_cs(path), [8, 8, 4])

            differences = [
                index for index, (before, after) in enumerate(zip(original, patched))
                if before != after
            ]
            self.assertEqual(len(differences), 1)

    def test_multi_byte_delay_round_trip(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "test.gif"
            path.write_bytes(_gif([8, 8]))
            patch_last_frame_delay(path, 300)
            self.assertEqual(read_frame_delays_cs(path), [8, 300])


if __name__ == "__main__":
    unittest.main()
