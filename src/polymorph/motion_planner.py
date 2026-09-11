from __future__ import annotations

import math
from dataclasses import dataclass

PREFERRED_LONG_EDGE = 2048
MIN_ADAPTIVE_FPS = 20.0
MIN_LINEAR_GAIN = 0.08
SOFT_TARGET_RATIO = 0.95


@dataclass(frozen=True, slots=True)
class GifMotionPlan:
    source_fps: float
    target_fps: float
    delay_centiseconds: int | None
    preferred_long_edge: int
    predicted_long_edge: int

    @property
    def resample(self) -> bool:
        return self.delay_centiseconds is not None and self.target_fps < self.source_fps - 1e-6


def uniform_gif_fps_candidates(source_fps: float, min_fps: float = MIN_ADAPTIVE_FPS) -> list[tuple[float, int]]:
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
    if full_fps_long_edge <= 0 or source_fps <= 0 or target_fps <= 0:
        return max(0, full_fps_long_edge)
    predicted = full_fps_long_edge * math.sqrt(source_fps / target_fps)
    return min(native_long_edge, max(full_fps_long_edge, int(round(predicted))))


def choose_favor_resolution_plan(
    *,
    source_fps: float,
    full_fps_long_edge: int,
    native_long_edge: int,
    preferred_long_edge: int = PREFERRED_LONG_EDGE,
    min_fps: float = MIN_ADAPTIVE_FPS,
    min_linear_gain: float = MIN_LINEAR_GAIN,
    soft_target_ratio: float = SOFT_TARGET_RATIO,
) -> GifMotionPlan:
    preferred = min(native_long_edge, preferred_long_edge)
    preserve = GifMotionPlan(
        source_fps=source_fps,
        target_fps=source_fps,
        delay_centiseconds=None,
        preferred_long_edge=preferred,
        predicted_long_edge=full_fps_long_edge,
    )

    if source_fps <= 0 or full_fps_long_edge <= 0 or native_long_edge <= 0:
        return preserve
    if full_fps_long_edge >= preferred:
        return preserve

    viable: list[GifMotionPlan] = []
    for fps, delay_cs in uniform_gif_fps_candidates(source_fps, min_fps):
        predicted = predicted_long_edge(
            full_fps_long_edge,
            source_fps,
            fps,
            native_long_edge,
        )
        gain = predicted / full_fps_long_edge - 1.0
        if gain + 1e-9 < min_linear_gain:
            continue

        plan = GifMotionPlan(
            source_fps=source_fps,
            target_fps=fps,
            delay_centiseconds=delay_cs,
            preferred_long_edge=preferred,
            predicted_long_edge=predicted,
        )
        viable.append(plan)

        # Prefer the highest FPS that gets reasonably close to the soft spatial
        # target. We only move farther down the cadence ladder when necessary.
        if predicted >= preferred * soft_target_ratio:
            return plan

    # If no candidate reaches the soft target, the lowest permitted viable FPS
    # gives the best spatial recovery while respecting the automatic floor.
    return viable[-1] if viable else preserve


def expected_uniform_frame_count(duration_s: float, fps: float) -> int:
    if duration_s <= 0 or fps <= 0:
        return 0
    return max(1, int(math.floor(duration_s * fps + 0.5)))
