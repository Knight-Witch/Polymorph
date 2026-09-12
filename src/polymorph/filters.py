from __future__ import annotations

from .geometry import FrameGeometry, content_placement, even, native_geometry
from .models import FramingMode, FramingSettings, MediaInfo


def _safe_color(value: str) -> str:
    value = value.strip().lstrip("#")
    if len(value) not in {6, 8} or any(ch not in "0123456789abcdefABCDEF" for ch in value):
        return "000000"
    return value[:6]


def _visible_axis(canvas: int, content: int, origin: int) -> tuple[int, int, int]:
    """Return source crop offset, visible length, and destination pad offset."""
    crop = max(0, -origin)
    pad = max(0, origin)
    available_source = max(0, content - crop)
    available_canvas = max(0, canvas - pad)
    visible = min(available_source, available_canvas)
    return crop, max(2, visible), pad


def build_video_filter(
    info: MediaInfo,
    framing: FramingSettings,
    output_width: int,
    output_height: int,
) -> tuple[str, FrameGeometry]:
    native = native_geometry(info, framing)
    filters: list[str] = []

    if framing.mode is not FramingMode.ORIGINAL and framing.ratio:
        placement = content_placement(
            info.width,
            info.height,
            native.width,
            native.height,
            framing,
        )
        content_width = even(placement.width)
        content_height = even(placement.height)

        # Crop must cover the whole canvas. Guard against a one-pixel rounding
        # undershoot when an unusual aspect ratio lands between even dimensions.
        if framing.mode is FramingMode.CROP:
            content_width = max(native.width, content_width)
            content_height = max(native.height, content_height)

        if (content_width, content_height) != (info.width, info.height):
            filters.append(f"scale={content_width}:{content_height}:flags=lanczos")

        origin_x = int(round(placement.x))
        origin_y = int(round(placement.y))
        crop_x, visible_width, pad_x = _visible_axis(native.width, content_width, origin_x)
        crop_y, visible_height, pad_y = _visible_axis(native.height, content_height, origin_y)

        # Keep all intermediate dimensions even for yuv420p. The canvas itself is
        # even, and a one-pixel trim is preferable to chroma-format distortion.
        visible_width = min(content_width - crop_x, even(visible_width))
        visible_height = min(content_height - crop_y, even(visible_height))
        visible_width = max(2, visible_width)
        visible_height = max(2, visible_height)

        if (
            crop_x
            or crop_y
            or visible_width != content_width
            or visible_height != content_height
        ):
            filters.append(
                f"crop={visible_width}:{visible_height}:{crop_x}:{crop_y}"
            )

        if (
            pad_x
            or pad_y
            or visible_width != native.width
            or visible_height != native.height
        ):
            color = framing.background if framing.mode is FramingMode.FIT else "#000000"
            filters.append(
                f"pad={native.width}:{native.height}:{pad_x}:{pad_y}:color=0x{_safe_color(color)}"
            )

    output_width = even(output_width)
    output_height = even(output_height)
    if output_width != native.width or output_height != native.height:
        filters.append(f"scale={output_width}:{output_height}:flags=lanczos")

    filters.append("setsar=1")
    return ",".join(filters), native
