import unittest
from pathlib import Path

from polymorph.filters import build_video_filter
from polymorph.models import FramingMode, FramingSettings, MediaInfo


class FilterTests(unittest.TestCase):
    def setUp(self):
        self.info = MediaInfo(Path("sample.webp"), 2048, 2048, 180, 6.0)

    def test_crop_16_9_crops_without_stretching(self):
        framing = FramingSettings(mode=FramingMode.CROP, ratio=16 / 9)
        graph, native = build_video_filter(self.info, framing, 2048, 1152)
        self.assertEqual((native.width, native.height), (2048, 1152))
        self.assertEqual(graph, "crop=2048:1152:0:448,setsar=1")

    def test_fit_16_9_pads_without_stretching(self):
        framing = FramingSettings(mode=FramingMode.FIT, ratio=16 / 9)
        graph, native = build_video_filter(self.info, framing, 3640, 2048)
        self.assertEqual((native.width, native.height), (3640, 2048))
        self.assertEqual(graph, "pad=3640:2048:796:0:color=0x000000,setsar=1")

    def test_crop_zoom_scales_then_crops_aspect_preserved_content(self):
        framing = FramingSettings(mode=FramingMode.CROP, ratio=16 / 9, zoom=2.0)
        graph, _ = build_video_filter(self.info, framing, 2048, 1152)
        self.assertEqual(
            graph,
            "scale=4096:4096:flags=lanczos,crop=2048:1152:1024:1472,setsar=1",
        )

    def test_fit_zoom_can_crop_and_pad_without_ratio_distortion(self):
        framing = FramingSettings(mode=FramingMode.FIT, ratio=16 / 9, zoom=1.5)
        graph, _ = build_video_filter(self.info, framing, 3640, 2048)
        self.assertEqual(
            graph,
            "scale=3072:3072:flags=lanczos,crop=3072:2048:0:512,"
            "pad=3640:2048:284:0:color=0x000000,setsar=1",
        )

    def test_final_output_scale_happens_after_framing(self):
        framing = FramingSettings(mode=FramingMode.CROP, ratio=16 / 9)
        graph, _ = build_video_filter(self.info, framing, 1280, 720)
        self.assertEqual(
            graph,
            "crop=2048:1152:0:448,scale=1280:720:flags=lanczos,setsar=1",
        )


if __name__ == "__main__":
    unittest.main()
