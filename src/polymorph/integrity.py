from __future__ import annotations

from .models import MediaInfo


class IntegrityError(RuntimeError):
    pass


def validate_output_integrity(source: MediaInfo, output: MediaInfo) -> None:
    """Reject silent temporal degradation after encoding.

    Frame count is exact. Duration gets a small tolerance because GIF timing is
    quantized and container timestamps can differ slightly without changing the
    visible animation cadence.
    """
    if output.frame_count != source.frame_count:
        raise IntegrityError(
            f"Frame verification failed: source has {source.frame_count} frames, "
            f"output has {output.frame_count}."
        )

    if source.duration_s <= 0 or output.duration_s <= 0:
        return

    fps = source.fps
    frame_time = 1.0 / fps if fps > 0 else 0.05
    tolerance = max(0.05, frame_time * 2.0)
    delta = abs(output.duration_s - source.duration_s)
    if delta > tolerance:
        raise IntegrityError(
            f"Timing verification failed: source duration is {source.duration_s:.3f}s, "
            f"output duration is {output.duration_s:.3f}s."
        )
