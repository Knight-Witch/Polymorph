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
    allow_encoder_frame_merging: bool = False,
) -> None:
    """Reject silent spatial or temporal degradation after encoding.

    Exact stored-frame counts remain required unless a known output encoder
    consolidates duplicate displayed frames. Those outputs must retain valid,
    positive presentation delays and their original total playback duration.
    """
    if expected_width is not None and expected_height is not None:
        if output.width != expected_width or output.height != expected_height:
            raise IntegrityError(
                f"Dimension verification failed: requested {expected_width}x{expected_height}, "
                f"output is {output.width}x{output.height}."
            )

    frames = source.frame_count if expected_frame_count is None else expected_frame_count
    if output.frame_count != frames:
        # gifski and libwebp_anim can coalesce visually identical frames
        # and transfer their display time to the surviving image. Preserve
        # the full animation timeline rather than requiring one storage image
        # for every decoded MP4 frame. Do not relax MP4 output or non-MP4
        # source verification.
        optimized = (
            allow_encoder_frame_merging
            and expected_frame_count is None
            and source.path.suffix.lower() == ".mp4"
            and output.path.suffix.lower() in {".gif", ".webp"}
            and 1 <= output.frame_count < frames
            and (output.path.suffix.lower() == ".gif" or output.frame_count >= 2)
            and len(output.frame_durations_ms) == output.frame_count
            and all(delay > 0 for delay in output.frame_durations_ms)
            and output.duration_s > 0
            and abs(sum(output.frame_durations_ms) / 1000.0 - output.duration_s) <= 0.002
        )
        if not optimized:
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
