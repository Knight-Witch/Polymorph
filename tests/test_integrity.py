import unittest
from pathlib import Path

from polymorph.integrity import IntegrityError, validate_output_integrity
from polymorph.models import MediaInfo


class IntegrityTests(unittest.TestCase):
    def info(self, frames=180, duration=6.0, width=2048, height=2048):
        return MediaInfo(Path("x"), width, height, frames, duration, nominal_fps=30.0)

    def test_exact_frame_count_close_duration_and_dimensions_pass(self):
        validate_output_integrity(
            self.info(),
            self.info(duration=6.03, width=1400, height=1400),
            expected_width=1400,
            expected_height=1400,
        )

    def test_dimension_mismatch_fails(self):
        with self.assertRaises(IntegrityError):
            validate_output_integrity(
                self.info(),
                self.info(width=800, height=800),
                expected_width=1400,
                expected_height=1400,
            )

    def test_lost_frame_fails(self):
        with self.assertRaises(IntegrityError):
            validate_output_integrity(self.info(), self.info(frames=179))

    def test_expected_reduced_frame_count_passes(self):
        source = self.info(frames=150, duration=6.0)
        output = self.info(frames=120, duration=6.0, width=1600, height=1600)
        validate_output_integrity(
            source,
            output,
            expected_width=1600,
            expected_height=1600,
            expected_frame_count=120,
            expected_fps=20.0,
        )

    def test_wrong_reduced_frame_count_fails(self):
        with self.assertRaises(IntegrityError):
            validate_output_integrity(
                self.info(frames=150, duration=6.0),
                self.info(frames=119, duration=6.0),
                expected_frame_count=120,
                expected_fps=20.0,
            )

    def test_large_timing_drift_fails(self):
        with self.assertRaises(IntegrityError):
            validate_output_integrity(self.info(), self.info(duration=6.5))


if __name__ == "__main__":
    unittest.main()
