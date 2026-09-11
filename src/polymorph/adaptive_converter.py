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
from .motion_planner import (
    MIN_LINEAR_GAIN,
    actual_gain_is_worthwhile,
    evaluate_measured_candidate,
    expected_uniform_frame_count,
    predicted_long_edge,
    preferred_long_edge,
    uniform_gif_fps_candidates,
)
from .probe import ProbeError, probe_media
from .size_units import mb_to_bytes


class AdaptiveConverter(Converter):
    """GIF motion/resolution balancing layered over the proven Converter behavior.

    Preserve-motion conversions call the production Converter unchanged. Favor
    resolution first produces the proven full-FPS result, then measures real gifski
    cost at lower uniform cadences before deciding whether any FPS sacrifice buys a
    meaningful spatial improvement.
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
            temp_dir = Path(temp_dir_str)
            baseline_output = temp_dir / "baseline.gif"
            self._clear_adaptive_state()

            baseline_progress = None
            if progress:
                baseline_progress = lambda fraction, _label: progress(
                    min(0.35, max(0.0, fraction) * 0.35),
                    "Measuring original motion",
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
            baseline_edge = max(baseline.width, baseline.height)
            native_edge = max(native.width, native.height)

            # Do not sacrifice motion when the full-FPS result already reaches the
            # useful/native spatial target.
            if baseline_edge >= preferred_long_edge(native_edge):
                return self._commit_baseline(baseline, output, baseline.passes, progress)

            candidates: list[tuple[float, int]] = []
            for candidate_fps, delay_cs in uniform_gif_fps_candidates(info.fps):
                # Skip rates that cannot possibly reach the minimum gain even under
                # the optimistic frame-count-only model. Real encoded sampling below
                # is the authority for candidates that survive this cheap screen.
                ideal_edge = predicted_long_edge(
                    baseline_edge,
                    info.fps,
                    candidate_fps,
                    native_edge,
                )
                ideal_gain = ideal_edge / baseline_edge - 1.0
                if ideal_gain + 1e-9 >= MIN_LINEAR_GAIN:
                    candidates.append((candidate_fps, delay_cs))

            if not candidates:
                return self._commit_baseline(baseline, output, baseline.passes, progress)

            selected_plan = None
            probe_passes = 0
            probe_span = 0.20 / len(candidates)

            for index, (candidate_fps, delay_cs) in enumerate(candidates):
                expected_frames = expected_uniform_frame_count(info.duration_s, candidate_fps)
                if expected_frames <= 0:
                    continue

                self._adaptive_target_fps = candidate_fps
                self._adaptive_expected_frames = expected_frames
                sample_output = temp_dir / f"probe-{delay_cs}cs.gif"

                sample_progress = None
                if progress:
                    start = 0.35 + index * probe_span
                    sample_progress = lambda fraction, _label, start=start: progress(
                        start + min(probe_span, max(0.0, fraction) * probe_span),
                        f"Measuring {candidate_fps:.2f} FPS tradeoff",
                    )

                try:
                    self._encode_once(
                        info,
                        settings,
                        sample_output,
                        baseline.width,
                        baseline.height,
                        sample_progress,
                        "Measuring adaptive cadence",
                    )
                except ConversionCancelled:
                    raise
                except ConversionError:
                    # Favor resolution is optional. A failed experimental cadence
                    # must never make an otherwise valid Preserve-motion conversion
                    # fail; simply try the next clean cadence or fall back.
                    self._clear_adaptive_state()
                    continue

                probe_passes += 1
                selected_plan = evaluate_measured_candidate(
                    source_fps=info.fps,
                    target_fps=candidate_fps,
                    delay_centiseconds=delay_cs,
                    baseline_long_edge=baseline_edge,
                    native_long_edge=native_edge,
                    sample_size_bytes=sample_output.stat().st_size,
                    max_bytes=max_bytes,
                )
                if selected_plan is not None:
                    break
                self._clear_adaptive_state()

            if selected_plan is None:
                self._clear_adaptive_state()
                return self._commit_baseline(
                    baseline,
                    output,
                    baseline.passes + probe_passes,
                    progress,
                )

            expected_frames = expected_uniform_frame_count(
                info.duration_s,
                selected_plan.target_fps,
            )
            self._adaptive_target_fps = selected_plan.target_fps
            self._adaptive_expected_frames = expected_frames

            adaptive_output = temp_dir / "adaptive.gif"
            try:
                adaptive_progress = None
                if progress:
                    adaptive_progress = lambda fraction, _label: progress(
                        0.55 + min(0.45, max(0.0, fraction) * 0.45),
                        f"Favoring resolution at {selected_plan.target_fps:.2f} FPS",
                    )

                result = self._encode_gif_to_size(
                    info,
                    settings,
                    adaptive_output,
                    native.width,
                    native.height,
                    max_bytes,
                    adaptive_progress,
                )
                total_passes = baseline.passes + probe_passes + result.passes

                # Planning is deliberately conservative, but the final measured
                # result still has veto power. Never keep a lower-FPS output unless
                # it actually earns the same meaningful spatial gain promised to the
                # user by Favor resolution.
                if not actual_gain_is_worthwhile(
                    baseline_long_edge=baseline_edge,
                    adaptive_long_edge=max(result.width, result.height),
                ):
                    return self._commit_baseline(
                        baseline,
                        output,
                        total_passes,
                        progress,
                    )

                if output.exists():
                    output.unlink()
                shutil.copy2(result.output, output)
                if progress:
                    progress(1.0, f"Favoring resolution at {selected_plan.target_fps:.2f} FPS")
                return replace(result, output=output, passes=total_passes)
            finally:
                self._clear_adaptive_state()

    def _commit_baseline(
        self,
        baseline: ConversionResult,
        output: Path,
        passes: int,
        progress: ProgressCallback | None,
    ) -> ConversionResult:
        self._clear_adaptive_state()
        if output.exists():
            output.unlink()
        shutil.copy2(baseline.output, output)
        if progress:
            progress(1.0, "Preserving original motion — no worthwhile resolution gain")
        return replace(baseline, output=output, passes=passes)

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
