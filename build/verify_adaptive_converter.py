from __future__ import annotations

import json
import random
import tempfile
from pathlib import Path

from PIL import Image

from polymorph.adaptive_converter import AdaptiveConverter
from polymorph.converter import Converter
from polymorph.models import ConversionSettings, GifMotionMode, OutputFormat, SizingMode
from polymorph.motion_planner import source_decimation_candidates
from polymorph.tools import Toolchain


WIDTH = 192
HEIGHT = 192
FRAME_COUNT = 30
FRAME_MS = 40


def make_source(path: Path) -> None:
    frames: list[Image.Image] = []
    pixel_count = WIDTH * HEIGHT * 3
    for index in range(FRAME_COUNT):
        rng = random.Random(0xC0FFEE + index)
        frames.append(Image.frombytes("RGB", (WIDTH, HEIGHT), rng.randbytes(pixel_count)))
    frames[0].save(
        path,
        save_all=True,
        append_images=frames[1:],
        duration=[FRAME_MS] * FRAME_COUNT,
        loop=0,
        lossless=True,
        format="WEBP",
    )


def verify(tools: Toolchain, report_path: Path | None = None) -> None:
    with tempfile.TemporaryDirectory(prefix="polymorph-adaptive-integration-") as tmp:
        root = Path(tmp)
        source = root / "adaptive-source.webp"
        make_source(source)

        preserve_converter = Converter(tools)
        adaptive_converter = AdaptiveConverter(tools)
        info = adaptive_converter.probe(source)
        if info.frame_count != FRAME_COUNT or abs(info.fps - 25.0) > 0.05:
            raise RuntimeError(
                f"Adaptive fixture probe mismatch: {info.frame_count} frames at {info.fps:.4f} FPS"
            )

        full_dir = root / "full"
        full_dir.mkdir()
        full_settings = ConversionSettings(
            output_format=OutputFormat.GIF,
            sizing_mode=SizingMode.RESOLUTION,
            requested_width=WIDTH,
            requested_height=HEIGHT,
            output_dir=full_dir,
        )
        full = preserve_converter.convert(source, full_settings)

        source_delay_cs = adaptive_converter._source_delay_centiseconds(info)
        if source_delay_cs is None:
            raise RuntimeError("Adaptive fixture timing was not representable in GIF centiseconds")
        candidates = source_decimation_candidates(
            source_fps=info.fps,
            source_frame_count=info.frame_count,
            source_delay_centiseconds=source_delay_cs,
        )
        if not candidates or candidates[0].stride != 2:
            raise RuntimeError("Adaptive fixture did not produce the expected stride-2 candidate")

        stride2 = candidates[0]
        adaptive_converter._set_decimation_state(stride2)
        stride2_path = root / "stride2-full.gif"
        try:
            adaptive_converter._encode_once(
                info,
                ConversionSettings(output_format=OutputFormat.GIF),
                stride2_path,
                WIDTH,
                HEIGHT,
                None,
                "Adaptive integration probe",
            )
        finally:
            adaptive_converter._clear_adaptive_state()

        full_size = full.size_bytes
        stride2_size = stride2_path.stat().st_size
        ratio = stride2_size / full_size
        if ratio >= 0.80:
            raise RuntimeError(
                "Adaptive integration fixture is not discriminating enough: "
                f"stride-2/full byte ratio is {ratio:.4f}"
            )

        cap_bytes = int(full_size * 0.80)
        cap_mb = cap_bytes / 1_000_000.0

        preserve_dir = root / "preserve"
        favor_dir = root / "favor"
        preserve_dir.mkdir()
        favor_dir.mkdir()

        preserve_settings = ConversionSettings(
            output_format=OutputFormat.GIF,
            sizing_mode=SizingMode.FILE_SIZE,
            max_mb=cap_mb,
            output_dir=preserve_dir,
            gif_motion_mode=GifMotionMode.PRESERVE,
        )
        favor_settings = ConversionSettings(
            output_format=OutputFormat.GIF,
            sizing_mode=SizingMode.FILE_SIZE,
            max_mb=cap_mb,
            output_dir=favor_dir,
            gif_motion_mode=GifMotionMode.FAVOR_RESOLUTION,
        )

        preserve = preserve_converter.convert(source, preserve_settings)
        favor = adaptive_converter.convert(source, favor_settings)

        gain = max(favor.width, favor.height) / max(preserve.width, preserve.height) - 1.0
        if favor.frames >= preserve.frames:
            raise RuntimeError(
                f"Favor-resolution integration stayed at {favor.frames} frames; expected decimation below {preserve.frames}"
            )
        if gain < 0.08 - 1e-9:
            raise RuntimeError(
                f"Favor-resolution integration gained only {gain:.4%}: "
                f"preserve={preserve.width}x{preserve.height}, favor={favor.width}x{favor.height}"
            )
        if favor.size_bytes > cap_bytes:
            raise RuntimeError(
                f"Favor-resolution integration exceeded cap: {favor.size_bytes} > {cap_bytes}"
            )

        report = {
            "source": {
                "width": info.width,
                "height": info.height,
                "frames": info.frame_count,
                "fps": info.fps,
            },
            "full_resolution_bytes": full_size,
            "stride2_full_resolution_bytes": stride2_size,
            "stride2_full_ratio": ratio,
            "cap_bytes": cap_bytes,
            "preserve": {
                "width": preserve.width,
                "height": preserve.height,
                "bytes": preserve.size_bytes,
                "frames": preserve.frames,
            },
            "favor": {
                "width": favor.width,
                "height": favor.height,
                "bytes": favor.size_bytes,
                "frames": favor.frames,
            },
            "linear_gain": gain,
        }
        if report_path is not None:
            report_path.parent.mkdir(parents=True, exist_ok=True)
            report_path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")

        print(
            "Adaptive converter integration passed: "
            f"full={full_size} bytes, stride2={stride2_size} bytes, "
            f"preserve={preserve.width}x{preserve.height}/{preserve.frames}f, "
            f"favor={favor.width}x{favor.height}/{favor.frames}f, gain={gain:.2%}"
        )


def main() -> int:
    import sys

    root = Path(sys.argv[1] if len(sys.argv) > 1 else "tools")
    report = Path(sys.argv[2]) if len(sys.argv) > 2 else None
    suffix = ".exe" if sys.platform.startswith("win") else ""
    verify(
        Toolchain(
            ffmpeg=root / f"ffmpeg{suffix}",
            ffprobe=root / f"ffprobe{suffix}",
            gifski=root / f"gifski{suffix}",
        ),
        report,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
