import unittest

from polymorph.motion_planner import (
    actual_gain_is_worthwhile,
    evaluate_measured_candidate,
    expected_uniform_frame_count,
    predicted_long_edge,
    uniform_gif_fps_candidates,
)


class MotionPlannerTests(unittest.TestCase):
    def test_25fps_has_uniform_candidates_down_to_12_5(self):
        candidates = uniform_gif_fps_candidates(25.0)
        self.assertEqual(len(candidates), 4)
        self.assertEqual(candidates[0], (20.0, 5))
        self.assertAlmostEqual(candidates[1][0], 100.0 / 6.0)
        self.assertEqual(candidates[1][1], 6)
        self.assertAlmostEqual(candidates[2][0], 100.0 / 7.0)
        self.assertEqual(candidates[2][1], 7)
        self.assertEqual(candidates[3], (12.5, 8))

    def test_60fps_candidates_stay_uniform_and_nearest_first(self):
        self.assertEqual(
            uniform_gif_fps_candidates(60.0),
            [
                (50.0, 2),
                (100.0 / 3.0, 3),
                (25.0, 4),
                (20.0, 5),
                (100.0 / 6.0, 6),
                (100.0 / 7.0, 7),
                (12.5, 8),
            ],
        )

    def test_viper_20fps_sample_can_be_rejected_by_real_byte_cost(self):
        # Dev.9 reported 1552px and displayed ~89.2 MiB, which is roughly
        # 93.5 decimal MB. At that measured cost, 20 FPS cannot buy an 8%
        # linear spatial gain even though frame-count-only math predicted it could.
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

    def test_lower_uniform_candidate_is_accepted_when_measured_cost_earns_gain(self):
        plan = evaluate_measured_candidate(
            source_fps=25.0,
            target_fps=100.0 / 7.0,
            delay_centiseconds=7,
            baseline_long_edge=1552,
            native_long_edge=2048,
            sample_size_bytes=78_000_000,
            max_bytes=99_000_000,
        )
        self.assertIsNotNone(plan)
        assert plan is not None
        self.assertAlmostEqual(plan.target_fps, 100.0 / 7.0)
        self.assertEqual(plan.delay_centiseconds, 7)
        self.assertGreaterEqual(plan.predicted_long_edge, 1700)

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

    def test_frame_count_only_prediction_remains_an_optimistic_screen(self):
        predicted = predicted_long_edge(1552, 25.0, 20.0, 2048)
        self.assertGreater(predicted, 1700)

    def test_expected_uniform_frame_counts(self):
        self.assertEqual(expected_uniform_frame_count(15.0, 20.0), 300)
        self.assertEqual(expected_uniform_frame_count(15.0, 100.0 / 6.0), 250)
        self.assertEqual(expected_uniform_frame_count(15.0, 100.0 / 7.0), 214)
        self.assertEqual(expected_uniform_frame_count(15.0, 12.5), 188)


if __name__ == "__main__":
    unittest.main()
