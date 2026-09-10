from __future__ import annotations

import math
import os
import shutil
import subprocess
import tempfile
import threading
from pathlib import Path
from typing import Callable

from .constants import FILE_SIZE_HEADROOM, MAX_SIZE_PASSES, MIN_SCALE
from .filters import build_video_filter
from .geometry import native_geometry, scaled_dimensions, validate_requested_resolution
from .integrity import IntegrityError, validate_output_integrity
from .models import ConversionResult, ConversionSettings, MediaInfo, OutputFormat, SizingMode
from .probe import ProbeError, probe_media
from .tools import Toolchain

ProgressCallback = Callable[[float, str], None]


class ConversionCancelled(RuntimeError):
    pass


class ConversionError(RuntimeError):
    pass


class Converter:
    """Quality-first conversion engine, intentionally independent of the GUI."""

    def __init__(self, tools: Toolchain) -> None:
        self.tools = tools
        self._cancel = threading.Event()
        self._process_lock = threading.Lock()
        self._active_processes: list[subprocess.Popen] = []

    def cancel(self) -> None:
        self._cancel.set()
        with self._process_lock:
            for proc in self._active_processes:
                try:
                    proc.terminate()
                except OSError:
                    pass

    def reset_cancel(self) -> None:
        self._cancel.clear()

    def probe(self, path: Path) -> MediaInfo:
        return probe_media(self.tools.ffprobe, Path(path))

    @staticmethod
    def _available_output_path(output_dir: Path, stem: str, extension: str) -> Path:
        base = output_dir / f"{stem}_POLYMORPH.{extension}"
        if not base.exists():
            return base
        index = 2
        while True:
            candidate = output_dir / f"{stem}_POLYMORPH_{index}.{extension}"
            if not candidate.exists():
                return candidate
            index += 1

    def convert(
        self,
        source: Path,
        settings: ConversionSettings,
        progress: ProgressCallback | None = None,
    ) -> ConversionResult:
        self.reset_cancel()
        info = self.probe(source)
        native = native_geometry(info, settings.framing)
        output_dir = Path(settings.output_dir or source.parent)
        output_dir.mkdir(parents=True, exist_ok=True)
        extension = settings.output_format.value
        output = self._available_output_path(output_dir, source.stem, extension)

        if settings.sizing_mode is SizingMode.RESOLUTION:
            if not settings.requested_width or not settings.requested_height:
                raise ConversionError("Resolution mode requires width and height")
            scale = validate_requested_resolution(
                native, settings.requested_width, settings.requested_height
            )
            width, height = scaled_dimensions(native, scale)
            self._encode_once(info, settings, output, width, height, progress, "Encoding")
            return self._result(info, output, width, height, 1)

        max_bytes = int(settings.max_mb * 1024 * 1024)
        if max_bytes <= 0:
            raise ConversionError("Maximum file size must be greater than zero")
        return self._encode_to_size(info, settings, output, native.width, native.height, max_bytes, progress)

    def _encode_to_size(
        self,
        info: MediaInfo,
        settings: ConversionSettings,
        output: Path,
        native_width: int,
        native_height: int,
        max_bytes: int,
        progress: ProgressCallback | None,
    ) -> ConversionResult:
        target_bytes = int(max_bytes * FILE_SIZE_HEADROOM)
        high_fail = 1.0
        low_good = 0.0
        scale = 1.0
        best: tuple[Path, int, int, float] | None = None
        passes = 0

        with tempfile.TemporaryDirectory(prefix="polymorph-") as temp_dir_str:
            temp_dir = Path(temp_dir_str)
            for pass_index in range(MAX_SIZE_PASSES):
                if self._cancel.is_set():
                    raise ConversionCancelled()
                passes += 1
                width = max(2, int(round(native_width * scale)))
                height = max(2, int(round(native_height * scale)))
                width -= width % 2
                height -= height % 2
                candidate = temp_dir / f"candidate-{pass_index}.{settings.output_format.value}"
                label = "Encoding" if pass_index == 0 else "Optimizing size"
                self._encode_once(info, settings, candidate, width, height, progress, label)
                size = candidate.stat().st_size

                if size <= max_bytes:
                    low_good = max(low_good, scale)
                    best = (candidate, width, height, scale)
                    if size >= target_bytes * 0.94 or high_fail - scale < 0.025:
                        break
                    next_scale = min(high_fail * 0.995, (scale + high_fail) / 2)
                    if next_scale <= scale + 0.01:
                        break
                    scale = next_scale
                    continue

                high_fail = min(high_fail, scale)
                estimated = scale * math.sqrt(target_bytes / max(size, 1)) * 0.985
                if low_good > 0:
                    estimated = max(estimated, (low_good + high_fail) / 2)
                scale = max(MIN_SCALE, min(high_fail * 0.985, estimated))

            if best is None:
                raise ConversionError(
                    f"Could not fit output under {settings.max_mb:.1f} MB without scaling below the supported minimum."
                )

            candidate, width, height, _ = best
            output.parent.mkdir(parents=True, exist_ok=True)
            if output.exists():
                output.unlink()
            shutil.copy2(candidate, output)

        return self._result(info, output, width, height, passes)

    def _result(self, info: MediaInfo, output: Path, width: int, height: int, passes: int) -> ConversionResult:
        return ConversionResult(
            source=info.path,
            output=output,
            width=width,
            height=height,
            size_bytes=output.stat().st_size,
            frames=info.frame_count,
            duration_s=info.duration_s,
            passes=passes,
        )

    def _encode_once(
        self,
        info: MediaInfo,
        settings: ConversionSettings,
        output: Path,
        width: int,
        height: int,
        progress: ProgressCallback | None,
        label: str,
    ) -> None:
        if settings.output_format is OutputFormat.GIF:
            self._encode_gif(info, settings, output, width, height, progress, label)
        else:
            self._encode_mp4(info, settings, output, width, height, progress, label)

        self._verify_output(info, output, width, height)
        if progress:
            progress(1.0, label)

    def _verify_output(
        self,
        source_info: MediaInfo,
        output: Path,
        expected_width: int,
        expected_height: int,
    ) -> None:
        try:
            output_info = probe_media(self.tools.ffprobe, output)
            validate_output_integrity(
                source_info,
                output_info,
                expected_width=expected_width,
                expected_height=expected_height,
            )
        except (ProbeError, IntegrityError) as exc:
            try:
                output.unlink(missing_ok=True)
            except OSError:
                pass
            raise ConversionError(f"Output integrity verification failed. {exc}") from exc

    def _base_ffmpeg(self, info: MediaInfo, filter_graph: str) -> list[str]:
        return [
            str(self.tools.ffmpeg),
            "-hide_banner",
            "-loglevel",
            "error",
            "-i",
            str(info.path),
            "-map",
            "0:v:0",
            "-an",
            "-vf",
            filter_graph,
        ]

    def _encode_gif(
        self,
        info: MediaInfo,
        settings: ConversionSettings,
        output: Path,
        width: int,
        height: int,
        progress: ProgressCallback | None,
        label: str,
    ) -> None:
        filter_graph, _ = build_video_filter(info, settings.framing, width, height)
        ffmpeg_cmd = self._base_ffmpeg(info, filter_graph) + [
            "-fps_mode",
            "passthrough",
            # The validated standalone pipeline negotiated a 4:2:0 Y4M handoff.
            # Pin yuv420p here because the bundled FFmpeg 9.0.1 build can otherwise
            # choose a non-Y4M-compatible source format and fail before gifski.
            "-pix_fmt",
            "yuv420p",
            "-progress",
            "pipe:2",
            "-f",
            "yuv4mpegpipe",
            "pipe:1",
        ]
        if info.frame_durations_ms:
            shortest = min(info.frame_durations_ms)
            longest = max(info.frame_durations_ms)
            if longest - shortest > 1:
                raise ConversionError(
                    "This animated WebP uses variable frame durations. The current GIF path "
                    "cannot preserve those timings exactly, so Polymorph will not silently resample it."
                )

        source_fps = info.fps
        if source_fps <= 0:
            raise ConversionError("Could not determine source frame rate for GIF timing.")
        if source_fps > 100:
            raise ConversionError(
                f"Source is {source_fps:.3f} FPS, above gifski's 100 FPS limit. "
                "Polymorph will not silently reduce frame rate."
            )

        gifski_cmd = [
            str(self.tools.gifski),
            "--fps",
            f"{source_fps:.6f}",
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
                raise ConversionCancelled()
            if ffmpeg_rc != 0 or gifski_rc != 0 or not output.exists():
                details = gifski_log_path.read_text(errors="replace").strip()
                raise ConversionError(details or f"GIF encoding failed (ffmpeg={ffmpeg_rc}, gifski={gifski_rc})")
        finally:
            try:
                gifski_log_path.unlink(missing_ok=True)
            except OSError:
                pass

    def _encode_mp4(
        self,
        info: MediaInfo,
        settings: ConversionSettings,
        output: Path,
        width: int,
        height: int,
        progress: ProgressCallback | None,
        label: str,
    ) -> None:
        filter_graph, _ = build_video_filter(info, settings.framing, width, height)
        cmd = self._base_ffmpeg(info, filter_graph) + [
            "-fps_mode",
            "passthrough",
            "-c:v",
            "libx264",
            "-preset",
            "slow",
            "-crf",
            "16",
            "-pix_fmt",
            "yuv420p",
            "-movflags",
            "+faststart",
            "-progress",
            "pipe:2",
            "-y",
            str(output),
        ]
        proc = subprocess.Popen(
            cmd,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.PIPE,
            stdin=subprocess.DEVNULL,
            creationflags=self._creation_flags(),
        )
        self._register(proc)
        try:
            self._consume_progress(proc, info.duration_s, progress, label)
            rc = proc.wait()
        finally:
            self._unregister(proc)

        if self._cancel.is_set():
            raise ConversionCancelled()
        if rc != 0 or not output.exists():
            raise ConversionError(f"MP4 encoding failed (ffmpeg={rc})")

    def _consume_progress(
        self,
        proc: subprocess.Popen,
        duration_s: float,
        callback: ProgressCallback | None,
        label: str,
    ) -> None:
        if proc.stderr is None:
            return
        while True:
            if self._cancel.is_set():
                try:
                    proc.terminate()
                except OSError:
                    pass
                return
            raw = proc.stderr.readline()
            if not raw:
                break
            line = raw.decode("utf-8", errors="replace").strip()
            if "=" not in line:
                continue
            key, value = line.split("=", 1)
            if key not in {"out_time_us", "out_time_ms"}:
                continue
            try:
                seconds = int(value) / 1_000_000.0
            except ValueError:
                continue
            fraction = min(0.995, seconds / duration_s) if duration_s > 0 else 0.0
            if callback:
                callback(max(0.0, fraction), label)

    def _register(self, *processes: subprocess.Popen) -> None:
        with self._process_lock:
            self._active_processes.extend(processes)

    def _unregister(self, *processes: subprocess.Popen) -> None:
        with self._process_lock:
            for proc in processes:
                if proc in self._active_processes:
                    self._active_processes.remove(proc)

    @staticmethod
    def _creation_flags() -> int:
        return getattr(subprocess, "CREATE_NO_WINDOW", 0) if os.name == "nt" else 0
