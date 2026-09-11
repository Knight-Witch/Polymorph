import tempfile
import unittest
from pathlib import Path

from polymorph.adaptive_converter import AdaptiveConverter
from polymorph.models import (
    ConversionResult,
    ConversionSettings,
    GifMotionMode,
    MediaInfo,
    OutputFormat,
    SizingMode,
)


class _FakeAdaptiveConverter(AdaptiveConverter):
    def __init__(self, root: Path) -> None:
        super().__init__(None)
        self.root = root
        self.full_fit_strides: list[int] = []
        self.sample_strides: list[int] = []
        self.info = MediaInfo(
            path=root / "source.webp",
            width=2048,
            height=2048,
            frame_count=375,
            duration_s=15.0,
            frame_durations_ms=[40] * 375,
            nominal_fps=25.0,
        )

    def probe(self, path: Path) -> MediaInfo:
        return self.info

    def _encode_once(self, info, settings, output, width, height, progress, label) -> None:
        assert self._adaptive_stride is not None
        self.sample_strides.append(self._adaptive_stride)
        output.parent.mkdir(parents=True, exist_ok=True)
        # Small relative to a 1 MB test ceiling, so each stride clears the measured
        # prediction gate and the test specifically exercises the final-gain veto.
        with output.open("wb") as handle:
            handle.truncate(500_000)

    def _encode_gif_to_size(
        self,
        info,
        settings,
        output,
        native_width,
        native_height,
        max_bytes,
        progress,
    ) -> ConversionResult:
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_bytes(b"gif")

        if self._adaptive_stride is None:
            width = height = 1552
            frames = 375
        elif self._adaptive_stride == 2:
            self.full_fit_strides.append(2)
            width = height = 1600  # <8% gain: must continue, not fall back.
            frames = 188
        else:
            self.full_fit_strides.append(self._adaptive_stride)
            width = height = 1800  # >=8% gain: accept this deeper candidate.
            frames = 125

        return ConversionResult(
            source=info.path,
            output=output,
            width=width,
            height=height,
            size_bytes=output.stat().st_size,
            frames=frames,
            duration_s=15.0,
            passes=1,
        )


class AdaptiveConverterTests(unittest.TestCase):
    def test_failed_high_candidate_continues_to_deeper_decimation(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = root / "source.webp"
            source.write_bytes(b"source")
            converter = _FakeAdaptiveConverter(root)
            settings = ConversionSettings(
                output_format=OutputFormat.GIF,
                sizing_mode=SizingMode.FILE_SIZE,
                max_mb=1.0,
                output_dir=root,
                gif_motion_mode=GifMotionMode.FAVOR_RESOLUTION,
            )

            result = converter.convert(source, settings)

            self.assertEqual(converter.sample_strides[:2], [2, 3])
            self.assertEqual(converter.full_fit_strides, [2, 3])
            self.assertEqual((result.width, result.height), (1800, 1800))
            self.assertEqual(result.frames, 125)


if __name__ == "__main__":
    unittest.main()
