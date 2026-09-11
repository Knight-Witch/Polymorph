from __future__ import annotations

import math
from dataclasses import dataclass

from .size_optimizer import reference_thresholds

PREFERRED_LONG_EDGE = 2048
MIN_ADAPTIVE_FPS = 100.0 / 6.0  # 16.666... FPS / 60 ms GIF cadence.
MIN_LINEAR_GAIN = 0.08


@dataclass(frozen=True, slots=True)
class GifMotionPlan:
    source_fps: float
    target_fps: float
    delay_centiseconds: int | None
    preferred_long_edge: int
    predicted_long_edge: int
    sample_size_bytes: int | None = None

    @property
    def resample(self) -> bool:
        return self.delay_centiseconds is not None and self.target_fps < self.source_fps - 1e-6


def preferred_long_edge(native_long_edge: int, preferred: int = PREFERRED_LONG_EDGE) -> int:
    if native_long_edge <= 0:
        return 0
    return min(native_long_edge, preferred)


def uniform_gif_fps_candidates(
    source_fps: float,
    min_fps: float = MIN_ADAPTIVE_FPS,
) -> list[tuple[float, int]]:
    """Return lower, uniform GIF-friendly rates ordered nearest the source first.

    GIF frame delays are centiseconds. Restricting adaptive candidates to 100/N FPS
    gives every output frame the same duration instead of alternating short/long
    delays that create a visible cadence wobble.
    """
    if source_fps <= 0 or min_fps <= 0 or source_fps <= min_fps + 1e-6:
        return []

    max_delay = max(1, int(math.floor(100.0 / min_fps + 1e-9)))
    candidates: list[tuple[float, int]] = []
    for delay_cs in range(1, max_delay + 1):
        fps = 100.0 / delay_cs
        if fps >= source_fps - 1e-6:
            continue
        if fps < min_fps - 1e-6:
            continue
        candidates.append((fps, delay_cs))
    candidates.sort(key=lambda item: item[0], reverse=True)
    return candidates


def predicted_long_edge(
    full_fps_long_edge: int,
    source_fps: float,
    target_fps: float,
    native_long_edge: int,
) -> int:
    """Ideal frame-count-only spatial prediction used only as a cheap upper bound."""
    if full_fps_long_edge <= 0 or source_fps <= 0 or target_fps <= 0:
        return max(0, full_fps_long_edge)
    predicted = full_fps_long_edge * math.sqrt(source_fps / target_fps)
    return min(native_long_edge, max(full_fps_long_edge, int(round(predicted))))


def evaluate_measured_candidate(
    *,
    source_fps: float,
    target_fps: float,
    delay_centiseconds: int,
    baseline_long_edge: int,
    native_long_edge: int,
    sample_size_bytes: int,
    max_bytes: int,
    preferred: int = PREFERRED_LONG_EDGE,
    min_linear_gain: float = MIN_LINEAR_GAIN,
) -> GifMotionPlan | None:
    """Accept a reduced-FPS candidate only when a real encoded sample earns it.

    The sample is encoded at the already-fitted Preserve-motion dimensions. This
    measures the actual gifski cost of motion-interpolated frames, which can differ
    substantially from the naive frame-count ratio. The patched-Python 97/99 target
    is then used to estimate how much spatial resolution that measured byte cost can
    realistically buy before a full adaptive size search is attempted.
    """
    if (
        source_fps <= 0
        or target_fps <= 0
        or target_fps >= source_fps - 1e-6
        or baseline_long_edge <= 0
        or native_long_edge <= 0
        or sample_size_bytes <= 0
        or max_bytes <= 0
    ):
        return None

    spatial_target = preferred_long_edge(native_long_edge, preferred)
    if baseline_long_edge >= spatial_target:
        return None

    target_bytes, _ = reference_thresholds(max_bytes)
    predicted = baseline_long_edge * math.sqrt(target_bytes / sample_size_bytes)
    predicted_edge = min(
        spatial_target,
        native_long_edge,
        max(baseline_long_edge, int(round(predicted))),
    )
    gain = predicted_edge / baseline_long_edge - 1.0
    if gain + 1e-9 < min_linear_gain:
        return None

    return GifMotionPlan(
        source_fps=source_fps,
        target_fps=target_fps,
        delay_centiseconds=delay_centiseconds,
        preferred_long_edge=spatial_target,
        predicted_long_edge=predicted_edge,
        sample_size_bytes=sample_size_bytes,
    )


def actual_gain_is_worthwhile(
    *,
    baseline_long_edge: int,
    adaptive_long_edge: int,
    min_linear_gain: float = MIN_LINEAR_GAIN,
) -> bool:
    if baseline_long_edge <= 0 or adaptive_long_edge <= baseline_long_edge:
        return False
    return adaptive_long_edge / baseline_long_edge - 1.0 + 1e-9 >= min_linear_gain


def expected_uniform_frame_count(duration_s: float, fps: float) -> int:
    if duration_s <= 0 or fps <= 0:
        return 0
    return max(1, int(math.floor(duration_s * fps + 0.5)))
