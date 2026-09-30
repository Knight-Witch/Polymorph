from __future__ import annotations

from .models import MediaInfo


class IntegrityError(RuntimeError):
    pass


def validate_output_integrity(
    source: MediaInfo,
    output: MediaInfo,
    *,
    expected_width: int | None = None,
    expected_height: int | None = None,
    expected_frame_count: int | None = None,
    expected_fps: float | None = None,
) -> None:
    """Reject silent spatial or temporal degradation after encoding.

    Expected output dimensions and frame count are exact. Duration gets a small
    tolerance because GIF timing is quantized and container timestamps can differ
    slightly without changing the visible animation cadence.
    """
    if expected_width is not None and expected_height is not None:
        if output.width != expected_width or output.height != expected_height:
            raise IntegrityError(
                f"Dimension verification failed: requested {expected_width}x{expected_height}, "
                f"output is {output.width}x{output.height}."
            )

    frames = source.frame_count if expected_frame_count is None else expected_frame_count
    if output.frame_count != frames:
        raise IntegrityError(
            f"Frame verification failed: expected {frames} frames, "
            f"output has {output.frame_count}."
        )

    if source.duration_s <= 0 or output.duration_s <= 0:
        return

    fps = expected_fps if expected_fps and expected_fps > 0 else source.fps
    frame_time = 1.0 / fps if fps > 0 else 0.05
    tolerance = max(0.05, frame_time * 2.0)
    delta = abs(output.duration_s - source.duration_s)
    if delta > tolerance:
        raise IntegrityError(
            f"Timing verification failed: source duration is {source.duration_s:.3f}s, "
            f"output duration is {output.duration_s:.3f}s."
        )
