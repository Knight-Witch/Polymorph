from __future__ import annotations

import json
import struct
import subprocess
from pathlib import Path

from .models import MediaInfo


class ProbeError(RuntimeError):
    pass


def _u24le(data: bytes) -> int:
    return data[0] | (data[1] << 8) | (data[2] << 16)


def probe_webp_riff(path: Path) -> tuple[int, int, list[int]]:
    """Read animated WebP canvas size and ANMF frame durations directly.

    HeroForge animated WebPs have historically exposed unreliable dimensions in
    some ffprobe builds, so this parser is retained as a first-class fallback.
    """
    raw = path.read_bytes()
    if len(raw) < 12 or raw[:4] != b"RIFF" or raw[8:12] != b"WEBP":
        raise ProbeError("Not a RIFF WebP file")

    width = height = 0
    durations: list[int] = []
    pos = 12
    n = len(raw)

    while pos + 8 <= n:
        chunk_id = raw[pos : pos + 4]
        size = struct.unpack_from("<I", raw, pos + 4)[0]
        payload_start = pos + 8
        payload_end = min(payload_start + size, n)
        payload = raw[payload_start:payload_end]

        if chunk_id == b"VP8X" and len(payload) >= 10:
            width = 1 + _u24le(payload[4:7])
            height = 1 + _u24le(payload[7:10])
        elif chunk_id == b"ANMF" and len(payload) >= 16:
            durations.append(_u24le(payload[12:15]))

        pos = payload_start + size + (size & 1)

    return width, height, durations


def _ffprobe_json(ffprobe: Path, path: Path) -> dict:
    cmd = [
        str(ffprobe),
        "-v",
        "error",
        "-count_frames",
        "-select_streams",
        "v:0",
        "-show_entries",
        "stream=width,height,nb_read_frames,nb_frames,avg_frame_rate,r_frame_rate,duration:format=duration",
        "-of",
        "json",
        str(path),
    ]
    proc = subprocess.run(cmd, capture_output=True, text=True, check=False)
    if proc.returncode != 0:
        raise ProbeError(proc.stderr.strip() or "ffprobe failed")
    try:
        return json.loads(proc.stdout)
    except json.JSONDecodeError as exc:
        raise ProbeError("ffprobe returned invalid JSON") from exc


def _parse_fraction(value: str | None) -> float:
    if not value or value in {"0/0", "N/A"}:
        return 0.0
    if "/" in value:
        a, b = value.split("/", 1)
        try:
            denom = float(b)
            return float(a) / denom if denom else 0.0
        except ValueError:
            return 0.0
    try:
        return float(value)
    except ValueError:
        return 0.0


def probe_media(ffprobe: Path, path: Path) -> MediaInfo:
    path = Path(path)
    if not path.exists():
        raise ProbeError(f"Input does not exist: {path}")

    riff_width = riff_height = 0
    riff_durations: list[int] = []
    if path.suffix.lower() == ".webp":
        try:
            riff_width, riff_height, riff_durations = probe_webp_riff(path)
        except ProbeError:
            pass

    ffprobe_error: ProbeError | None = None
    try:
        data = _ffprobe_json(ffprobe, path)
    except ProbeError as exc:
        ffprobe_error = exc
        data = {}

    streams = data.get("streams") or []
    stream = streams[0] if streams else {}
    fmt = data.get("format") or {}

    width = int(stream.get("width") or 0) or riff_width
    height = int(stream.get("height") or 0) or riff_height

    frame_count = 0
    for key in ("nb_read_frames", "nb_frames"):
        value = stream.get(key)
        if value and value != "N/A":
            try:
                frame_count = int(value)
                break
            except ValueError:
                pass
    if not frame_count and riff_durations:
        frame_count = len(riff_durations)

    duration_s = 0.0
    if riff_durations:
        duration_s = sum(max(1, d) for d in riff_durations) / 1000.0
    if duration_s <= 0:
        for candidate in (stream.get("duration"), fmt.get("duration")):
            try:
                duration_s = float(candidate or 0)
            except (TypeError, ValueError):
                duration_s = 0.0
            if duration_s > 0:
                break

    nominal_fps = _parse_fraction(stream.get("avg_frame_rate")) or _parse_fraction(stream.get("r_frame_rate"))
    if duration_s <= 0 and frame_count and nominal_fps > 0:
        duration_s = frame_count / nominal_fps
    if nominal_fps <= 0 and frame_count > 0 and duration_s > 0:
        nominal_fps = frame_count / duration_s

    if width <= 0 or height <= 0 or frame_count <= 0 or duration_s <= 0:
        if ffprobe_error and not (riff_width and riff_height and riff_durations):
            raise ffprobe_error
        if width <= 0 or height <= 0:
            raise ProbeError("Could not determine source dimensions")
        if frame_count <= 0:
            raise ProbeError("Could not determine source frame count")
        raise ProbeError("Could not determine source duration")

    return MediaInfo(
        path=path,
        width=width,
        height=height,
        frame_count=frame_count,
        duration_s=duration_s,
        frame_durations_ms=riff_durations,
        nominal_fps=nominal_fps,
    )
