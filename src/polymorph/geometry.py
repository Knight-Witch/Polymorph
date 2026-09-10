from __future__ import annotations

from dataclasses import dataclass

from .models import FramingMode, FramingSettings, MediaInfo


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


def even(value: float | int, minimum: int = 2) -> int:
    n = max(minimum, int(round(value)))
    return n if n % 2 == 0 else n - 1 if n > minimum else n + 1


def _axis_position(extra: int, offset: float) -> int:
    if extra <= 0:
        return 0
    normalized = max(-1.0, min(1.0, offset))
    return int(round((normalized + 1.0) * 0.5 * extra))


def native_geometry(info: MediaInfo, framing: FramingSettings) -> FrameGeometry:
    sw, sh = info.width, info.height
    if framing.mode is FramingMode.ORIGINAL or not framing.ratio:
        return FrameGeometry(width=even(sw), height=even(sh), content_width=even(sw), content_height=even(sh))

    ratio = max(0.05, framing.ratio)
    source_ratio = sw / sh

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
            content_width=even(cw),
            content_height=even(ch),
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
