from __future__ import annotations

import shutil
import subprocess
import tempfile
from dataclasses import replace
from pathlib import Path

from .converter import ConversionCancelled, ConversionError, Converter, ProgressCallback
from .geometry import native_geometry
from .integrity import IntegrityError, validate_output_integrity
from .models import ConversionResult, ConversionSettings, GifMotionMode, MediaInfo, OutputFormat, SizingMode
from .motion_planner import choose_favor_resolution_plan, expected_uniform_frame_count
from .probe import ProbeError, probe_media
from .size_units import mb_to_bytes


class AdaptiveConverter(Converter):
    """Experimental GIF motion/resolution balancing layered over proven Converter behavior.

    Preserve-motion conversions call the production Converter unchanged. The adaptive
    path first measures the full-frame result, then only resamples if the pure motion
    planner predicts a worthwhile spatial gain.
    """

    def __init__(self, tools) -> None:
        super().__init__(tools)
        self._adaptive_target_fps: float | None = None
        self._adaptive_expected_frames: int | None = None

    def convert(
        self,
        source: Path,
        settings: ConversionSettings,
        progress: ProgressCallback | None = None,
    ) -> ConversionResult:
        if not (
            settings.output_format is OutputFormat.GIF
            and settings.sizing_mode is SizingMode.FILE_SIZE
            and settings.gif_motion_mode is GifMotionMode.FAVOR_RESOLUTION
        ):
            self._clear_adaptive_state()
            return super().convert(source, settings, progress)

        self.reset_cancel()
        info = self.probe(source)
        native = native_geometry(info, settings.framing)
        max_bytes = mb_to_bytes(settings.max_mb)
        if max_bytes <= 0:
            raise ConversionError("Maximum file size must be greater than zero")

        output_dir = Path(settings.output_dir or source.parent)
        output_dir.mkdir(parents=True, exist_ok=True)
        output = self._available_output_path(output_dir, source.stem, "gif")

        with tempfile.TemporaryDirectory(prefix="polymorph-motion-plan-") as temp_dir_str:
            baseline_output = Path(temp_dir_str) / "baseline.gif"
            self._clear_adaptive_state()

            baseline_progress = None
            if progress:
                baseline_progress = lambda fraction, _label: progress(
                    min(0.45, max(0.0, fraction) * 0.45),
                    "Planning motion / resolution",
                )

            baseline = self._encode_gif_to_size(
                info,
                settings,
                baseline_output,
                native.width,
                native.height,
                max_bytes,
                baseline_progress,
            )

            plan = choose_favor_resolution_plan(
                source_fps=info.fps,
                full_fps_long_edge=max(baseline.width, baseline.height),
                native_long_edge=max(native.width, native.height),
            )

            if not plan.resample:
                if output.exists():
                    output.unlink()
                shutil.copy2(baseline.output, output)
                if progress:
                    progress(1.0, "Preserving original motion")
                return replace(baseline, output=output)

            expected_frames = expected_uniform_frame_count(info.duration_s, plan.target_fps)
            if expected_frames <= 0:
                raise ConversionError("Could not determine an even target frame count.")

            self._adaptive_target_fps = plan.target_fps
            self._adaptive_expected_frames = expected_frames
            try:
                adaptive_progress = None
                if progress:
                    adaptive_progress = lambda fraction, _label: progress(
                        0.45 + min(0.55, max(0.0, fraction) * 0.55),
                        f"Favoring resolution at {plan.target_fps:.2f} FPS",
                    )

                result = self._encode_gif_to_size(
                    info,
                    settings,
                    output,
                    native.width,
                    native.height,
                    max_bytes,
                    adaptive_progress,
                )
                return replace(result, passes=baseline.passes + result.passes)
            finally:
                self._clear_adaptive_state()

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
        if self._adaptive_target_fps is None:
            return super()._encode_gif(info, settings, output, width, height, progress, label)

        if info.frame_durations_ms:
            shortest = min(info.frame_durations_ms)
            longest = max(info.frame_durations_ms)
            if longest - shortest > 1:
                raise ConversionError(
                    "Favor resolution currently requires a constant-frame-rate animated WebP."
                )

        source_fps = info.fps
        target_fps = self._adaptive_target_fps
        expected_frames = self._adaptive_expected_frames
        if source_fps <= 0 or target_fps <= 0 or expected_frames is None:
            raise ConversionError("Could not determine adaptive GIF timing.")
        if target_fps >= source_fps - 1e-6:
            raise ConversionError("Adaptive GIF target must be lower than the source frame rate.")

        # Keep the proven spatial/framing filter untouched, then motion-resample the
        # already-scaled frames. Padding supplies minterpolate with end-of-stream
        # lookahead; trimming makes the uniform output frame count exact.
        from .filters import build_video_filter

        base_filter, _ = build_video_filter(info, settings.framing, width, height)
        pad_seconds = max(2.0 / source_fps, 2.0 / target_fps)
        filter_graph = (
            f"{base_filter},"
            f"tpad=stop_mode=clone:stop_duration={pad_seconds:.6f},"
            f"minterpolate=fps={target_fps:.9f}:mi_mode=mci:mc_mode=aobmc:"
            "me_mode=bidir:vsbmc=1,"
            f"trim=end_frame={expected_frames},setpts=PTS-STARTPTS"
        )

        ffmpeg_cmd = self._base_ffmpeg(info, filter_graph) + [
            "-fps_mode",
            "passthrough",
            "-pix_fmt",
            "yuv420p",
            "-progress",
            "pipe:2",
            "-f",
            "yuv4mpegpipe",
            "pipe:1",
        ]
        gifski_cmd = [
            str(self.tools.gifski),
            "--fps",
            f"{target_fps:.6f}",
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
                raise ConversionError(
                    details or f"Adaptive GIF encoding failed (ffmpeg={ffmpeg_rc}, gifski={gifski_rc})"
                )
        finally:
            try:
                gifski_log_path.unlink(missing_ok=True)
            except OSError:
                pass

    def _verify_output(
        self,
        source_info: MediaInfo,
        output: Path,
        expected_width: int,
        expected_height: int,
    ) -> None:
        if self._adaptive_expected_frames is None or self._adaptive_target_fps is None:
            return super()._verify_output(source_info, output, expected_width, expected_height)

        try:
            output_info = probe_media(self.tools.ffprobe, output)
            validate_output_integrity(
                source_info,
                output_info,
                expected_width=expected_width,
                expected_height=expected_height,
                expected_frame_count=self._adaptive_expected_frames,
                expected_fps=self._adaptive_target_fps,
            )
        except (ProbeError, IntegrityError) as exc:
            try:
                output.unlink(missing_ok=True)
            except OSError:
                pass
            raise ConversionError(f"Adaptive output integrity verification failed. {exc}") from exc

    def _result(
        self,
        info: MediaInfo,
        output: Path,
        width: int,
        height: int,
        passes: int,
    ) -> ConversionResult:
        result = super()._result(info, output, width, height, passes)
        if self._adaptive_expected_frames is not None:
            return replace(result, frames=self._adaptive_expected_frames)
        return result

    def _clear_adaptive_state(self) -> None:
        self._adaptive_target_fps = None
        self._adaptive_expected_frames = None
