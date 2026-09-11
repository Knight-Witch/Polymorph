import unittest

from polymorph.motion_planner import (
    choose_favor_resolution_plan,
    expected_uniform_frame_count,
    uniform_gif_fps_candidates,
)


class MotionPlannerTests(unittest.TestCase):
    def test_25fps_only_steps_to_uniform_20fps(self):
        self.assertEqual(uniform_gif_fps_candidates(25.0), [(20.0, 5)])

    def test_60fps_candidates_stay_uniform_and_nearest_first(self):
        self.assertEqual(
            uniform_gif_fps_candidates(60.0),
            [(50.0, 2), (100.0 / 3.0, 3), (25.0, 4), (20.0, 5)],
        )

    def test_viper_like_case_selects_20fps(self):
        plan = choose_favor_resolution_plan(
            source_fps=25.0,
            full_fps_long_edge=1552,
            native_long_edge=2048,
        )
        self.assertTrue(plan.resample)
        self.assertAlmostEqual(plan.target_fps, 20.0)
        self.assertEqual(plan.delay_centiseconds, 5)
        self.assertGreater(plan.predicted_long_edge, 1700)

    def test_native_resolution_never_sacrifices_frames(self):
        plan = choose_favor_resolution_plan(
            source_fps=25.0,
            full_fps_long_edge=1024,
            native_long_edge=1024,
        )
        self.assertFalse(plan.resample)
        self.assertEqual(plan.target_fps, 25.0)

    def test_trivial_gain_preserves_motion(self):
        plan = choose_favor_resolution_plan(
            source_fps=25.0,
            full_fps_long_edge=1950,
            native_long_edge=2048,
        )
        self.assertFalse(plan.resample)

    def test_higher_fps_uses_highest_uniform_rate_near_target(self):
        plan = choose_favor_resolution_plan(
            source_fps=60.0,
            full_fps_long_edge=1500,
            native_long_edge=3072,
        )
        self.assertTrue(plan.resample)
        self.assertAlmostEqual(plan.target_fps, 100.0 / 3.0)
        self.assertEqual(plan.delay_centiseconds, 3)

    def test_expected_viper_frame_count(self):
        self.assertEqual(expected_uniform_frame_count(15.0, 20.0), 300)


if __name__ == "__main__":
    unittest.main()
