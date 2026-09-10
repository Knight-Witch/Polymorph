import math
import unittest

from polymorph.size_optimizer import (
    choose_reference_next_scale,
    minimum_scale_for_long_edge,
    reference_thresholds,
)


class ReferenceOptimizerTests(unittest.TestCase):
    def test_reference_thresholds_match_patched_99mb_constants(self):
        self.assertEqual(reference_thresholds(99_000_000), (97_000_000, 93_000_000))

    def test_thresholds_scale_with_user_ceiling(self):
        target, accept = reference_thresholds(50_000_000)
        self.assertEqual(target, 48_989_898)
        self.assertEqual(accept, 46_969_696)

    def test_failure_uses_reference_area_prediction_and_safety(self):
        scale = choose_reference_next_scale(
            current_scale=1.0,
            current_size=120_000_000,
            max_bytes=99_000_000,
            failed_scale=1.0,
            passed_scale=None,
        )
        expected = min(math.sqrt(97_000_000 / 120_000_000) * 0.985, 0.96)
        self.assertAlmostEqual(scale, expected)

    def test_failure_after_pass_bisects_reference_bracket(self):
        scale = choose_reference_next_scale(
            current_scale=0.8,
            current_size=110_000_000,
            max_bytes=99_000_000,
            failed_scale=0.8,
            passed_scale=0.7,
        )
        self.assertEqual(scale, 0.75)

    def test_pass_in_acceptance_band_stops(self):
        self.assertIsNone(
            choose_reference_next_scale(
                current_scale=0.7,
                current_size=93_000_000,
                max_bytes=99_000_000,
                failed_scale=0.8,
                passed_scale=0.7,
            )
        )

    def test_low_pass_with_known_failure_reclaims_resolution(self):
        scale = choose_reference_next_scale(
            current_scale=0.7,
            current_size=90_000_000,
            max_bytes=99_000_000,
            failed_scale=0.8,
            passed_scale=0.7,
        )
        self.assertEqual(scale, 0.75)

    def test_full_size_pass_cannot_reclaim_above_native(self):
        self.assertIsNone(
            choose_reference_next_scale(
                current_scale=1.0,
                current_size=80_000_000,
                max_bytes=99_000_000,
                failed_scale=None,
                passed_scale=1.0,
            )
        )

    def test_emergency_floor_never_upscales(self):
        self.assertAlmostEqual(minimum_scale_for_long_edge(4096, 4096), 128 / 4096)
        self.assertEqual(minimum_scale_for_long_edge(64, 64), 1.0)


if __name__ == "__main__":
    unittest.main()
