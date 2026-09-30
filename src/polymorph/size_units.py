from __future__ import annotations

DECIMAL_MB_BYTES = 1_000_000


def mb_to_bytes(value: float) -> int:
    """Convert user-facing decimal megabytes to bytes."""
    return int(round(value * DECIMAL_MB_BYTES))


def bytes_to_mb(value: int) -> float:
    """Convert bytes to user-facing decimal megabytes."""
    return value / DECIMAL_MB_BYTES
