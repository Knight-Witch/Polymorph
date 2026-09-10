import unittest
from pathlib import Path

from polymorph.integrity import IntegrityError, validate_output_integrity
from polymorph.models import MediaInfo


class IntegrityTests(unittest.TestCase):
    def info(self, frames=180, duration=6.0):
        return MediaInfo(Path("x"), 2048, 2048, frames, duration, nominal_fps=30.0)

    def test_exact_frame_count_and_close_duration_pass(self):
        validate_output_integrity(self.info(), self.info(duration=6.03))

    def test_lost_frame_fails(self):
        with self.assertRaises(IntegrityError):
            validate_output_integrity(self.info(), self.info(frames=179))

    def test_large_timing_drift_fails(self):
        with self.assertRaises(IntegrityError):
            validate_output_integrity(self.info(), self.info(duration=6.5))


if __name__ == "__main__":
    unittest.main()
