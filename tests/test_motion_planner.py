import unittest

from polymorph.motion_planner import (
    actual_gain_is_worthwhile,
    evaluate_measured_candidate,
    evaluate_measured_decimation,
    expected_uniform_frame_count,
    predicted_decimated_long_edge,
    predicted_long_edge,
    source_decimation_candidates,
    uniform_gif_fps_candidates,
)


class MotionPlannerTests(unittest.TestCase):
    def test_25fps_has_legacy_uniform_candidates_down_to_12_5(self):
        candidates = uniform_gif_fps_candidates(25.0)
        self.assertEqual(len(candidates), 4)
        self.assertEqual(candidates[0], (20.0, 5))
        self.assertAlmostEqual(candidates[1][0], 100.0 / 6.0)
        self.assertEqual(candidates[1][1], 6)
        self.assertAlmostEqual(candidates[2][0], 100.0 / 7.0)
        self.assertEqual(candidates[2][1], 7)
        self.assertEqual(candidates[3], (12.5, 8))

    def test_viper_exact_decimation_candidates_preserve_loop_duration(self):
        candidates = source_decimation_candidates(
            source_fps=25.0,
            source_frame_count=375,
            source_delay_centiseconds=4,
        )
        self.assertEqual([c.stride for c in candidates], [2, 3])

        stride2 = candidates[0]
        self.assertEqual(stride2.expected_frames, 188)
        self.assertAlmostEqual(stride2.nominal_fps, 12.5)
        self.assertEqual(stride2.delay_centiseconds, 8)
        self.assertEqual(stride2.final_delay_centiseconds, 4)
        self.assertAlmostEqual(stride2.effective_fps, 188 / 15.0)
        self.assertEqual(
            (stride2.expected_frames - 1) * stride2.delay_centiseconds
            + stride2.final_delay_centiseconds,
            1500,
        )

        stride3 = candidates[1]
        self.assertEqual(stride3.expected_frames, 125)
        self.assertAlmostEqual(stride3.nominal_fps, 25.0 / 3.0)
        self.assertEqual(stride3.delay_centiseconds, 12)
        self.assertEqual(stride3.final_delay_centiseconds, 12)
        self.assertAlmostEqual(stride3.effective_fps, 125 / 15.0)

    def test_decimation_prediction_uses_real_retained_frame_count(self):
        predicted = predicted_decimated_long_edge(
            1552,
            source_frame_count=375,
            output_frame_count=188,
            native_long_edge=2048,
        )
        self.assertEqual(predicted, 2048)

    def test_measured_decimation_can_reach_soft_native_target(self):
        candidate = source_decimation_candidates(
            source_fps=25.0,
            source_frame_count=375,
            source_delay_centiseconds=4,
        )[0]
        plan = evaluate_measured_decimation(
            source_fps=25.0,
            candidate=candidate,
            baseline_long_edge=1552,
            native_long_edge=2048,
            sample_size_bytes=50_000_000,
            max_bytes=99_000_000,
        )
        self.assertIsNotNone(plan)
        assert plan is not None
        self.assertEqual(plan.stride, 2)
        self.assertEqual(plan.expected_frames, 188)
        self.assertEqual(plan.final_delay_centiseconds, 4)
        self.assertEqual(plan.predicted_long_edge, 2048)

    def test_measured_decimation_still_requires_worthwhile_gain(self):
        candidate = source_decimation_candidates(
            source_fps=25.0,
            source_frame_count=375,
            source_delay_centiseconds=4,
        )[0]
        plan = evaluate_measured_decimation(
            source_fps=25.0,
            candidate=candidate,
            baseline_long_edge=1552,
            native_long_edge=2048,
            sample_size_bytes=93_500_000,
            max_bytes=99_000_000,
        )
        self.assertIsNone(plan)

    def test_viper_20fps_sample_can_be_rejected_by_real_byte_cost(self):
        plan = evaluate_measured_candidate(
            source_fps=25.0,
            target_fps=20.0,
            delay_centiseconds=5,
            baseline_long_edge=1552,
            native_long_edge=2048,
            sample_size_bytes=93_500_000,
            max_bytes=99_000_000,
        )
        self.assertIsNone(plan)

    def test_native_resolution_never_accepts_adaptive_candidate(self):
        plan = evaluate_measured_candidate(
            source_fps=25.0,
            target_fps=20.0,
            delay_centiseconds=5,
            baseline_long_edge=1024,
            native_long_edge=1024,
            sample_size_bytes=50_000_000,
            max_bytes=99_000_000,
        )
        self.assertIsNone(plan)

    def test_actual_gain_requires_same_eight_percent_floor(self):
        self.assertFalse(
            actual_gain_is_worthwhile(
                baseline_long_edge=1552,
                adaptive_long_edge=1600,
            )
        )
        self.assertTrue(
            actual_gain_is_worthwhile(
                baseline_long_edge=1552,
                adaptive_long_edge=1680,
            )
        )

    def test_frame_count_only_prediction_remains_an_optimistic_legacy_screen(self):
        predicted = predicted_long_edge(1552, 25.0, 20.0, 2048)
        self.assertGreater(predicted, 1700)

    def test_expected_uniform_frame_counts(self):
        self.assertEqual(expected_uniform_frame_count(15.0, 20.0), 300)
        self.assertEqual(expected_uniform_frame_count(15.0, 100.0 / 6.0), 250)
        self.assertEqual(expected_uniform_frame_count(15.0, 100.0 / 7.0), 214)
        self.assertEqual(expected_uniform_frame_count(15.0, 12.5), 188)


if __name__ == "__main__":
    unittest.main()
