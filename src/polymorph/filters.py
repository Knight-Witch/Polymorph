from __future__ import annotations

from .geometry import FrameGeometry, even, native_geometry
from .models import FramingMode, FramingSettings, MediaInfo


def _safe_color(value: str) -> str:
    value = value.strip().lstrip("#")
    if len(value) not in {6, 8} or any(ch not in "0123456789abcdefABCDEF" for ch in value):
        return "000000"
    return value[:6]


def build_video_filter(
    info: MediaInfo,
    framing: FramingSettings,
    output_width: int,
    output_height: int,
) -> tuple[str, FrameGeometry]:
    native = native_geometry(info, framing)
    filters: list[str] = []

    if framing.mode is FramingMode.CROP and native.crop_width and native.crop_height:
        filters.append(
            f"crop={native.crop_width}:{native.crop_height}:{native.crop_x}:{native.crop_y}"
        )
    elif framing.mode is FramingMode.FIT and framing.ratio:
        filters.append(
            f"pad={native.width}:{native.height}:{native.pad_x}:{native.pad_y}:color=0x{_safe_color(framing.background)}"
        )

    output_width = even(output_width)
    output_height = even(output_height)
    if output_width != native.width or output_height != native.height:
        filters.append(f"scale={output_width}:{output_height}:flags=lanczos")

    filters.append("setsar=1")
    return ",".join(filters), native
