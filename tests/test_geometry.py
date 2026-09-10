import unittest
from pathlib import Path

from polymorph.geometry import linked_dimensions, native_geometry, validate_requested_resolution
from polymorph.models import FramingMode, FramingSettings, MediaInfo


class GeometryTests(unittest.TestCase):
    def setUp(self):
        self.info = MediaInfo(Path("sample.webp"), 2048, 2048, 180, 6.0)

    def test_crop_16_9(self):
        g = native_geometry(self.info, FramingSettings(mode=FramingMode.CROP, ratio=16 / 9))
        self.assertEqual((g.width, g.height), (2048, 1152))
        self.assertEqual((g.crop_x, g.crop_y), (0, 448))

    def test_fit_16_9_preserves_native_content(self):
        g = native_geometry(self.info, FramingSettings(mode=FramingMode.FIT, ratio=16 / 9))
        self.assertEqual(g.height, 2048)
        self.assertEqual(g.content_width, 2048)
        self.assertEqual(g.content_height, 2048)
        self.assertGreater(g.width, 2048)

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
