import unittest
from pathlib import Path

from polymorph.geometry import (
    content_placement,
    linked_dimensions,
    native_geometry,
    validate_requested_resolution,
)
from polymorph.models import FramingMode, FramingSettings, MediaInfo


class GeometryTests(unittest.TestCase):
    def setUp(self):
        self.info = MediaInfo(Path("sample.webp"), 2048, 2048, 180, 6.0)

    def test_crop_16_9(self):
        framing = FramingSettings(mode=FramingMode.CROP, ratio=16 / 9)
        g = native_geometry(self.info, framing)
        self.assertEqual((g.width, g.height), (2048, 1152))
        self.assertEqual((g.crop_x, g.crop_y), (0, 448))

        p = content_placement(2048, 2048, g.width, g.height, framing)
        self.assertAlmostEqual(p.width / p.height, 1.0)
        self.assertEqual((round(p.x), round(p.y)), (0, -448))

    def test_fit_16_9_preserves_native_content(self):
        framing = FramingSettings(mode=FramingMode.FIT, ratio=16 / 9)
        g = native_geometry(self.info, framing)
        self.assertEqual(g.height, 2048)
        self.assertEqual(g.content_width, 2048)
        self.assertEqual(g.content_height, 2048)
        self.assertGreater(g.width, 2048)

        p = content_placement(2048, 2048, g.width, g.height, framing)
        self.assertAlmostEqual(p.width / p.height, 1.0)
        self.assertEqual((round(p.width), round(p.height)), (2048, 2048))
        self.assertGreater(p.x, 0)
        self.assertEqual(round(p.y), 0)

    def test_crop_zoom_preserves_source_aspect(self):
        framing = FramingSettings(mode=FramingMode.CROP, ratio=16 / 9, zoom=2.0)
        g = native_geometry(self.info, framing)
        p = content_placement(2048, 2048, g.width, g.height, framing)
        self.assertEqual((round(p.width), round(p.height)), (4096, 4096))
        self.assertAlmostEqual(p.width / p.height, 1.0)
        self.assertEqual((round(p.x), round(p.y)), (-1024, -1472))

    def test_fit_zoom_can_magnify_without_changing_canvas_ratio(self):
        framing = FramingSettings(mode=FramingMode.FIT, ratio=16 / 9, zoom=1.5)
        g = native_geometry(self.info, framing)
        p = content_placement(2048, 2048, g.width, g.height, framing)
        self.assertAlmostEqual(g.width / g.height, 16 / 9, places=3)
        self.assertEqual((round(p.width), round(p.height)), (3072, 3072))
        self.assertAlmostEqual(p.width / p.height, 1.0)

    def test_resolution_mode_rejects_upscale(self):
        g = native_geometry(self.info, FramingSettings())
        with self.assertRaises(ValueError):
            validate_requested_resolution(g, 4096, 4096)

    def test_resolution_mode_accepts_downscale(self):
        g = native_geometry(self.info, FramingSettings())
        scale = validate_requested_resolution(g, 700, 700)
        self.assertLess(scale, 1.0)

    def test_linked_width_preserves_16_9(self):
        self.assertEqual(linked_dimensions(2048, 1152, 700, "width"), (700, 394))

    def test_linked_height_preserves_16_9(self):
        self.assertEqual(linked_dimensions(2048, 1152, 700, "height"), (1244, 700))

    def test_linked_resolution_clamps_upscale(self):
        self.assertEqual(linked_dimensions(2048, 2048, 4096, "width"), (2048, 2048))


if __name__ == "__main__":
    unittest.main()
