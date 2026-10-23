"""Animated WebP timing checks and minimal RIFF final-delay correction.

FFmpeg's libwebp_anim stores a default 100 ms final ANMF delay. Change only
that final three-byte duration to retain the source loop length; never change
frame count or preceding timestamps.
"""
from __future__ import annotations

import struct
from pathlib import Path

from .probe import ProbeError, probe_webp_riff


def finalize_webp_timing(output: Path, source_duration_s: float, source_durations_ms: list[int]) -> None:
    width, height, encoded = probe_webp_riff(output)
    if not width or not height or not encoded:
        raise ProbeError("Animated WebP has no animation frames")
    if source_durations_ms:
        if len(encoded) != len(source_durations_ms):
            raise ProbeError("Animated WebP lost source frames")
        if any(abs(a - b) > 2 for a, b in zip(encoded[:-1], source_durations_ms[:-1])):
            raise ProbeError("Animated WebP source frame timing was altered")
        expected_last = source_durations_ms[-1]
    else:
        expected_last = round(source_duration_s * 1000) - sum(encoded[:-1])
    if not 1 <= expected_last <= 0xFFFFFF:
        raise ProbeError("Animated WebP final frame timing cannot be represented")
    if encoded[-1] == expected_last:
        return

    # Validate RIFF chunks before editing any byte. ANMF durations are unsigned
    # 24-bit milliseconds at payload offset 12; changing them preserves length.
    with output.open("r+b") as f:
        if f.read(4) != b"RIFF":
            raise ProbeError("Not RIFF WebP")
        f.seek(8)
        if f.read(4) != b"WEBP":
            raise ProbeError("Not WebP")
        f.seek(0, 2)
        n = f.tell()
        pos, last_offset, count = 12, None, 0
        while pos + 8 <= n:
            f.seek(pos)
            name = f.read(4)
            size = struct.unpack("<I", f.read(4))[0]
            end = pos + 8 + size
            if end > n:
                raise ProbeError("Truncated WebP RIFF chunk")
            if name == b"ANMF":
                if size < 16:
                    raise ProbeError("Invalid WebP ANMF header")
                last_offset = pos + 8 + 12
                count += 1
            pos = end + (size & 1)
        if count != len(encoded) or last_offset is None:
            raise ProbeError("Animated WebP frame count mismatch")
        f.seek(last_offset)
        f.write(expected_last.to_bytes(3, "little"))

    _, _, checked = probe_webp_riff(output)
    if len(checked) != len(encoded) or sum(checked) != sum(source_durations_ms or []) and (
        source_durations_ms or abs(sum(checked) - round(source_duration_s * 1000)) > 1
    ):
        raise ProbeError("Animated WebP timing verification failed")
