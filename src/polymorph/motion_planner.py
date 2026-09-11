from __future__ import annotations

import math
from dataclasses import dataclass

from .size_optimizer import reference_thresholds

PREFERRED_LONG_EDGE = 2048
MIN_ADAPTIVE_FPS = 8.0
MIN_LINEAR_GAIN = 0.08


@dataclass(frozen=True, slots=True)
class GifMotionPlan:
    source_fps: float
    target_fps: float
    delay_centiseconds: int | None
    preferred_long_edge: int
    predicted_long_edge: int
    sample_size_bytes: int | None = None
    stride: int | None = None
    final_delay_centiseconds: int | None = None
    expected_frames: int | None = None
    effective_fps: float | None = None

    @property
    def resample(self) -> bool:
        return self.delay_centiseconds is not None and self.target_fps < self.source_fps - 1e-6


@dataclass(frozen=True, slots=True)
class DecimationCandidate:
    stride: int
    nominal_fps: float
    delay_centiseconds: int
    final_delay_centiseconds: int
    expected_frames: int
    effective_fps: float


def preferred_long_edge(native_long_edge: int, preferred: int = PREFERRED_LONG_EDGE) -> int:
    if native_long_edge <= 0:
        return 0
    return min(native_long_edge, preferred)


def uniform_gif_fps_candidates(
    source_fps: float,
    min_fps: float = 12.5,
) -> list[tuple[float, int]]:
    """Legacy synthetic-frame cadence candidates retained for diagnostics/history."""
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


def source_decimation_candidates(
    *,
    source_fps: float,
    source_frame_count: int,
    source_delay_centiseconds: int,
    min_fps: float = MIN_ADAPTIVE_FPS,
) -> list[DecimationCandidate]:
    """Return exact source-frame decimation plans, nearest motion retention first.

    Every candidate keeps frame 0 and then retains every Nth original frame. Most
    retained-frame delays are N * source_delay. If the source frame count is not a
    multiple of N, the final GIF frame gets the exact shorter remainder delay needed
    to close the loop at the original angular speed instead of introducing a periodic
    motion jump or a synthetic intermediate frame.
    """
    if (
        source_fps <= 0
        or source_frame_count <= 1
        or source_delay_centiseconds <= 0
        or min_fps <= 0
    ):
        return []

    candidates: list[DecimationCandidate] = []
    stride = 2
    while source_fps / stride >= min_fps - 1e-9:
        expected_frames = (source_frame_count + stride - 1) // stride
        last_index = (expected_frames - 1) * stride
        remainder_steps = source_frame_count - last_index
        if not 1 <= remainder_steps <= stride:
            break

        delay_cs = source_delay_centiseconds * stride
        final_delay_cs = source_delay_centiseconds * remainder_steps
        duration_cs = (expected_frames - 1) * delay_cs + final_delay_cs
        effective_fps = expected_frames / (duration_cs / 100.0)
        candidates.append(
            DecimationCandidate(
                stride=stride,
                nominal_fps=source_fps / stride,
                delay_centiseconds=delay_cs,
                final_delay_centiseconds=final_delay_cs,
                expected_frames=expected_frames,
                effective_fps=effective_fps,
            )
        )
        stride += 1
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


def predicted_decimated_long_edge(
    full_fps_long_edge: int,
    source_frame_count: int,
    output_frame_count: int,
    native_long_edge: int,
) -> int:
    if full_fps_long_edge <= 0 or source_frame_count <= 0 or output_frame_count <= 0:
        return max(0, full_fps_long_edge)
    predicted = full_fps_long_edge * math.sqrt(source_frame_count / output_frame_count)
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
    """Legacy synthetic-candidate measured gate retained for regression history."""
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


def evaluate_measured_decimation(
    *,
    source_fps: float,
    candidate: DecimationCandidate,
    baseline_long_edge: int,
    native_long_edge: int,
    sample_size_bytes: int,
    max_bytes: int,
    preferred: int = PREFERRED_LONG_EDGE,
    min_linear_gain: float = MIN_LINEAR_GAIN,
) -> GifMotionPlan | None:
    if (
        source_fps <= 0
        or candidate.nominal_fps <= 0
        or candidate.nominal_fps >= source_fps - 1e-6
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
        target_fps=candidate.nominal_fps,
        delay_centiseconds=candidate.delay_centiseconds,
        preferred_long_edge=spatial_target,
        predicted_long_edge=predicted_edge,
        sample_size_bytes=sample_size_bytes,
        stride=candidate.stride,
        final_delay_centiseconds=candidate.final_delay_centiseconds,
        expected_frames=candidate.expected_frames,
        effective_fps=candidate.effective_fps,
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
