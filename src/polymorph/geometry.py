from __future__ import annotations

from dataclasses import dataclass

from .models import FramingMode, FramingSettings, MediaInfo


MIN_FRAMING_ZOOM = 1.0
MAX_FRAMING_ZOOM = 4.0


@dataclass(frozen=True, slots=True)
class FrameGeometry:
    width: int
    height: int
    crop_x: int = 0
    crop_y: int = 0
    crop_width: int | None = None
    crop_height: int | None = None
    pad_x: int = 0
    pad_y: int = 0
    content_width: int | None = None
    content_height: int | None = None


@dataclass(frozen=True, slots=True)
class ContentPlacement:
    """Aspect-preserving source placement inside a framing canvas.

    x/y are relative to the canvas and may be negative when zoom/cover causes the
    source to extend beyond an edge. width/height always preserve source aspect.
    """

    x: float
    y: float
    width: float
    height: float


def even(value: float | int, minimum: int = 2) -> int:
    n = max(minimum, int(round(value)))
    return n if n % 2 == 0 else n - 1 if n > minimum else n + 1


def clamp_framing_zoom(value: float) -> float:
    return max(MIN_FRAMING_ZOOM, min(MAX_FRAMING_ZOOM, float(value)))


def _clamp_offset(value: float) -> float:
    return max(-1.0, min(1.0, float(value)))


def _axis_position(extra: int, offset: float) -> int:
    if extra <= 0:
        return 0
    normalized = _clamp_offset(offset)
    return int(round((normalized + 1.0) * 0.5 * extra))


def _placed_axis_origin(canvas_size: float, content_size: float, offset: float) -> float:
    """Place content within/over a canvas using the same -1..+1 position model.

    When content is smaller than the canvas, -1/+1 align to the near/far padded
    edge. When content is larger, -1/+1 reveal the near/far cropped edge.
    """

    normalized = _clamp_offset(offset)
    travel = abs(canvas_size - content_size)
    fraction = (normalized + 1.0) * 0.5
    if content_size <= canvas_size:
        return travel * fraction
    return -travel * fraction


def content_placement(
    source_width: float,
    source_height: float,
    canvas_width: float,
    canvas_height: float,
    framing: FramingSettings,
) -> ContentPlacement:
    """Return aspect-preserving content placement for Crop/Fit preview + encode.

    Crop starts at the minimum scale that covers the canvas; Fit starts at the
    maximum scale that contains the whole source. Manual zoom multiplies that base
    scale while position offsets choose which padded/cropped edge is visible.
    """

    sw = max(1.0, float(source_width))
    sh = max(1.0, float(source_height))
    cw = max(1.0, float(canvas_width))
    ch = max(1.0, float(canvas_height))

    if framing.mode is FramingMode.CROP:
        base_scale = max(cw / sw, ch / sh)
    else:
        # FIT is the only other caller in normal use. ORIGINAL also behaves as a
        # contain operation here so the helper remains safe in isolation.
        base_scale = min(cw / sw, ch / sh)

    zoom = clamp_framing_zoom(framing.zoom)
    width = sw * base_scale * zoom
    height = sh * base_scale * zoom
    x = _placed_axis_origin(cw, width, framing.offset_x)
    y = _placed_axis_origin(ch, height, framing.offset_y)
    return ContentPlacement(x=x, y=y, width=width, height=height)


def native_geometry(info: MediaInfo, framing: FramingSettings) -> FrameGeometry:
    sw, sh = info.width, info.height
    if framing.mode is FramingMode.ORIGINAL or not framing.ratio:
        return FrameGeometry(width=even(sw), height=even(sh), content_width=even(sw), content_height=even(sh))

    ratio = max(0.05, framing.ratio)
    source_ratio = sw / sh

    # Native canvas dimensions intentionally remain independent of manual zoom.
    # Zoom changes composition inside this canvas; it never silently raises the
    # user's output-resolution ceiling.
    if framing.mode is FramingMode.CROP:
        if source_ratio > ratio:
            ch = sh
            cw = min(sw, even(sh * ratio))
            cx = _axis_position(sw - cw, framing.offset_x)
            cy = 0
        else:
            cw = sw
            ch = min(sh, even(sw / ratio))
            cx = 0
            cy = _axis_position(sh - ch, framing.offset_y)
        return FrameGeometry(
            width=even(cw),
            height=even(ch),
            crop_x=cx,
            crop_y=cy,
            crop_width=even(cw),
            crop_height=even(ch),
            content_width=even(sw),
            content_height=even(sh),
        )

    if source_ratio < ratio:
        canvas_h = sh
        canvas_w = even(sh * ratio)
        px = _axis_position(canvas_w - sw, framing.offset_x)
        py = 0
    else:
        canvas_w = sw
        canvas_h = even(sw / ratio)
        px = 0
        py = _axis_position(canvas_h - sh, framing.offset_y)

    return FrameGeometry(
        width=even(canvas_w),
        height=even(canvas_h),
        pad_x=px,
        pad_y=py,
        content_width=even(sw),
        content_height=even(sh),
    )


def scaled_dimensions(native: FrameGeometry, scale: float) -> tuple[int, int]:
    scale = max(0.01, min(1.0, scale))
    return even(native.width * scale), even(native.height * scale)


def linked_dimensions(native_width: int, native_height: int, value: int, driver: str) -> tuple[int, int]:
    """Return no-upscale even dimensions locked to the framed native ratio."""
    native_width = even(native_width)
    native_height = even(native_height)
    if native_width <= 0 or native_height <= 0:
        raise ValueError("Native dimensions must be positive")

    if driver == "width":
        width = even(min(max(2, value), native_width))
        height = even(width * native_height / native_width)
        if height > native_height:
            height = native_height
            width = even(height * native_width / native_height)
        return width, height

    if driver == "height":
        height = even(min(max(2, value), native_height))
        width = even(height * native_width / native_height)
        if width > native_width:
            width = native_width
            height = even(width * native_height / native_width)
        return width, height

    raise ValueError("driver must be 'width' or 'height'")


def validate_requested_resolution(native: FrameGeometry, width: int, height: int) -> float:
    if width <= 0 or height <= 0:
        raise ValueError("Resolution must be positive")
    sx = width / native.width
    sy = height / native.height
    if sx > 1.0001 or sy > 1.0001:
        raise ValueError(
            f"Requested {width}x{height} would upscale the source. "
            f"Maximum framed size is {native.width}x{native.height}."
        )
    if abs(sx - sy) > 0.02:
        raise ValueError(
            f"Requested resolution must preserve the selected framing ratio. "
            f"Try {even(native.width * min(sx, sy))}x{even(native.height * min(sx, sy))}."
        )
    return min(sx, sy)
