from __future__ import annotations

import json
import subprocess
import tempfile
from pathlib import Path
from typing import Callable

from . import converter as _converter
from .filters import build_video_filter
from .gif_timing import GifTimingError, patch_last_frame_delay, read_frame_delays_cs
from .models import ConversionSettings, MediaInfo


_INSTALLED = False
_ORIGINAL_BASE_ENCODE_GIF = _converter.Converter._encode_gif
_ORIGINAL_ADAPTIVE_ENCODE_GIF: Callable | None = None


def _fallback_input_matrix(info: MediaInfo) -> str:
    # Base this decision on the ORIGINAL source, not the resized GIF dimensions.
    # HD video is overwhelmingly BT.709; SD video is the legacy BT.601 case.
    return "bt601" if info.width <= 720 and info.height <= 576 else "bt709"


def _probe_input_matrix(ffprobe: Path, info: MediaInfo) -> str:
    fallback = _fallback_input_matrix(info)
    try:
        proc = subprocess.run(
            [
                str(ffprobe),
                "-v",
                "error",
                "-select_streams",
                "v:0",
                "-show_entries",
                "stream=color_space",
                "-of",
                "json",
                str(info.path),
            ],
            capture_output=True,
            check=False,
            text=True,
            creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0),
        )
        if proc.returncode != 0:
            return fallback
        payload = json.loads(proc.stdout or "{}")
        streams = payload.get("streams") or []
        if not streams:
            return fallback
        color_space = str(streams[0].get("color_space") or "").strip().lower()
    except (OSError, TypeError, ValueError, json.JSONDecodeError):
        return fallback

    if color_space == "bt709":
        return "bt709"
    if color_space in {"smpte170m", "bt470bg", "bt601"}:
        return "bt601"
    return fallback


def _normalize_mp4_filter(filter_graph: str, input_matrix: str) -> str:
    # gifski 1.32's Y4M C444 decoder expects full-range BT.709. Normalize MP4
    # frames explicitly into that representation so source colors remain stable
    # even when an HD BT.709 source is resized to an SD-sized GIF.
    color_filter = (
        f"scale=in_color_matrix={input_matrix}:out_color_matrix=bt709:"
        "in_range=auto:out_range=full,format=yuv444p"
    )
    return f"{filter_graph},{color_filter}" if filter_graph else color_filter


def _run_mp4_gif_stream(
    self: _converter.Converter,
    info: MediaInfo,
    output: Path,
    filter_graph: str,
    width: int,
    fps: float,
    progress: _converter.ProgressCallback | None,
    label: str,
) -> None:
    input_matrix = _probe_input_matrix(self.tools.ffprobe, info)
    normalized_filter = _normalize_mp4_filter(filter_graph, input_matrix)

    ffmpeg_cmd = self._base_ffmpeg(info, normalized_filter) + [
        "-fps_mode",
        "passthrough",
        "-pix_fmt",
        "yuv444p",
        "-color_range",
        "pc",
        "-colorspace",
        "bt709",
        "-progress",
        "pipe:2",
        "-f",
        "yuv4mpegpipe",
        "pipe:1",
    ]
    gifski_cmd = [
        str(self.tools.gifski),
        "--fps",
        f"{fps:.6f}",
        "--quality",
        "100",
        "--extra",
        "--repeat",
        "0",
        "--width",
        str(width),
        "-o",
        str(output),
        "-",
    ]

    with tempfile.NamedTemporaryFile(mode="w+b", delete=False) as gifski_log:
        gifski_log_path = Path(gifski_log.name)
    try:
        ffmpeg = subprocess.Popen(
            ffmpeg_cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            stdin=subprocess.DEVNULL,
            creationflags=self._creation_flags(),
        )
        assert ffmpeg.stdout is not None
        gifski_log_handle = open(gifski_log_path, "wb")
        try:
            gifski = subprocess.Popen(
                gifski_cmd,
                stdin=ffmpeg.stdout,
                stdout=subprocess.DEVNULL,
                stderr=gifski_log_handle,
                creationflags=self._creation_flags(),
            )
        finally:
            gifski_log_handle.close()
        ffmpeg.stdout.close()
        self._register(ffmpeg, gifski)
        try:
            self._consume_progress(ffmpeg, info.duration_s, progress, label)
            ffmpeg_rc = ffmpeg.wait()
            gifski_rc = gifski.wait()
        finally:
            self._unregister(ffmpeg, gifski)

        if self._cancel.is_set():
            raise _converter.ConversionCancelled()
        if ffmpeg_rc != 0 or gifski_rc != 0 or not output.exists():
            details = gifski_log_path.read_text(errors="replace").strip()
            raise _converter.ConversionError(
                details or f"MP4 GIF encoding failed (ffmpeg={ffmpeg_rc}, gifski={gifski_rc})"
            )
    finally:
        try:
            gifski_log_path.unlink(missing_ok=True)
        except OSError:
            pass


def _fidelity_base_encode_gif(
    self: _converter.Converter,
    info: MediaInfo,
    settings: ConversionSettings,
    output: Path,
    width: int,
    height: int,
    progress: _converter.ProgressCallback | None,
    label: str,
) -> None:
    if info.path.suffix.lower() != ".mp4":
        # Protected boundary: animated WebP -> GIF remains on the existing
        # production implementation without flag/timing changes.
        return _ORIGINAL_BASE_ENCODE_GIF(
            self, info, settings, output, width, height, progress, label
        )

    filter_graph, _ = build_video_filter(info, settings.framing, width, height)
    source_fps = info.fps
    if source_fps <= 0:
        raise _converter.ConversionError("Could not determine source frame rate for GIF timing.")
    if source_fps > 100:
        raise _converter.ConversionError(
            f"Source is {source_fps:.3f} FPS, above gifski's 100 FPS limit. "
            "Polymorph will not silently reduce frame rate."
        )
    _run_mp4_gif_stream(
        self,
        info,
        output,
        filter_graph,
        width,
        source_fps,
        progress,
        label,
    )


def _fidelity_adaptive_encode_gif(
    self,
    info: MediaInfo,
    settings: ConversionSettings,
    output: Path,
    width: int,
    height: int,
    progress: _converter.ProgressCallback | None,
    label: str,
) -> None:
    if _ORIGINAL_ADAPTIVE_ENCODE_GIF is None:
        raise RuntimeError("Adaptive GIF fidelity patch was not initialized")

    if info.path.suffix.lower() != ".mp4" or self._adaptive_stride is None:
        # Preserve the existing adaptive implementation. When stride is None,
        # its super() call resolves to the patched base MP4 path above.
        return _ORIGINAL_ADAPTIVE_ENCODE_GIF(
            self, info, settings, output, width, height, progress, label
        )

    source_delay_cs = self._source_delay_centiseconds(info)
    stride = self._adaptive_stride
    target_fps = self._adaptive_target_fps
    expected_frames = self._adaptive_expected_frames
    regular_delay_cs = self._adaptive_delay_cs
    final_delay_cs = self._adaptive_final_delay_cs
    if (
        source_delay_cs is None
        or target_fps is None
        or expected_frames is None
        or regular_delay_cs is None
        or final_delay_cs is None
    ):
        raise _converter.ConversionError(
            "Could not determine exact source-frame decimation timing."
        )

    base_filter, _ = build_video_filter(info, settings.framing, width, height)
    filter_graph = (
        f"{base_filter},"
        f"select='not(mod(n\\,{stride}))',"
        f"setpts=N/({target_fps:.9f}*TB),"
        f"fps={target_fps:.9f}"
    )
    _run_mp4_gif_stream(
        self,
        info,
        output,
        filter_graph,
        width,
        target_fps,
        progress,
        label,
    )

    try:
        delays = read_frame_delays_cs(output)
        if len(delays) != expected_frames:
            raise GifTimingError(
                f"Expected {expected_frames} GIF frames, found {len(delays)}."
            )
        if any(delay != regular_delay_cs for delay in delays):
            raise GifTimingError(
                "gifski did not produce the expected uniform pre-patch cadence."
            )
        if final_delay_cs != regular_delay_cs:
            patch_last_frame_delay(output, final_delay_cs)
    except GifTimingError as exc:
        try:
            output.unlink(missing_ok=True)
        except OSError:
            pass
        raise _converter.ConversionError(
            f"Could not finalize adaptive GIF timing. {exc}"
        ) from exc


def install_gif_fidelity_patch() -> None:
    global _INSTALLED, _ORIGINAL_ADAPTIVE_ENCODE_GIF
    if _INSTALLED:
        return

    # Lazy import avoids touching Qt/UI modules and keeps startup ordering
    # independent from the visual preload repair.
    from .adaptive_converter import AdaptiveConverter

    _ORIGINAL_ADAPTIVE_ENCODE_GIF = AdaptiveConverter._encode_gif
    _converter.Converter._encode_gif = _fidelity_base_encode_gif
    AdaptiveConverter._encode_gif = _fidelity_adaptive_encode_gif
    _INSTALLED = True
