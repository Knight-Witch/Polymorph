from __future__ import annotations

import math

# Ratios are taken directly from the user-tested patched Python converter:
# LIMIT=99,000,000; TARGET=97,000,000; ACCEPT_LOW=93,000,000.
_REFERENCE_LIMIT = 99
_REFERENCE_TARGET = 97
_REFERENCE_ACCEPT_LOW = 93
GIF_MIN_LONG_EDGE = 128


def reference_thresholds(max_bytes: int) -> tuple[int, int]:
    """Scale the patched converter's 97/99 target and 93/99 acceptance floor."""
    if max_bytes <= 0:
        raise ValueError("Maximum byte size must be positive")
    target_bytes = max_bytes * _REFERENCE_TARGET // _REFERENCE_LIMIT
    accept_low_bytes = max_bytes * _REFERENCE_ACCEPT_LOW // _REFERENCE_LIMIT
    return target_bytes, accept_low_bytes


def choose_reference_next_scale(
    *,
    current_scale: float,
    current_size: int,
    max_bytes: int,
    failed_scale: float | None,
    passed_scale: float | None,
) -> float | None:
    """Port the patched standalone smart-fit scale selection exactly.

    Only the byte thresholds are generalized from the standalone's fixed 99 MB
    ceiling to the user's selected ceiling. Encoder quality and timing are not
    part of this function.
    """
    target_bytes, accept_low_bytes = reference_thresholds(max_bytes)

    if current_size > max_bytes:
        ratio = math.sqrt(target_bytes / current_size)
        proposed = current_scale * ratio * 0.985

        # Preserve the standalone's guaranteed meaningful downward move.
        proposed = min(proposed, current_scale * 0.96)

        if passed_scale is not None:
            proposed = (passed_scale + current_scale) / 2.0

        return proposed

    if current_size >= accept_low_bytes:
        return None

    if failed_scale is None:
        # A full-size pass cannot be improved by increasing resolution.
        return None

    # Reclaim resolution without crossing the known failing scale.
    ratio = math.sqrt(target_bytes / max(current_size, 1))
    predicted = current_scale * ratio * 0.985
    midpoint = (current_scale + failed_scale) / 2.0

    proposed = max(predicted, midpoint)
    proposed = min(proposed, failed_scale * 0.995)

    if proposed <= current_scale * 1.01:
        return None

    return proposed


def minimum_scale_for_long_edge(width: int, height: int) -> float:
    """Return the standalone 128 px emergency floor without ever upscaling."""
    longest = max(width, height)
    if longest <= 0:
        raise ValueError("Dimensions must be positive")
    return min(1.0, GIF_MIN_LONG_EDGE / longest)
