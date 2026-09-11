from __future__ import annotations

import shutil
import subprocess
import tempfile
from dataclasses import replace
from pathlib import Path

from .converter import ConversionCancelled, ConversionError, Converter, ProgressCallback
from .geometry import native_geometry
from .gif_timing import GifTimingError, patch_last_frame_delay, read_frame_delays_cs
from .integrity import IntegrityError, validate_output_integrity
from .models import ConversionResult, ConversionSettings, GifMotionMode, MediaInfo, OutputFormat, SizingMode
from .motion_planner import (
    MIN_LINEAR_GAIN,
    DecimationCandidate,
    actual_gain_is_worthwhile,
    evaluate_measured_decimation,
    predicted_decimated_long_edge,
    preferred_long_edge,
    source_decimation_candidates,
)
from .probe import ProbeError, probe_media
from .size_units import mb_to_bytes


class AdaptiveConverter(Converter):
    """GIF motion/resolution balancing layered over the proven Converter behavior.

    Preserve-motion conversions call the production Converter unchanged. Favor
    resolution first produces the proven full-FPS result, then tests exact source-
    frame decimation. No synthetic intermediate frames are created in dev.13.
    """

    def __init__(self, tools) -> None:
        super().__init__(tools)
        self._adaptive_stride: int | None = None
        self._adaptive_target_fps: float | None = None
        self._adaptive_effective_fps: float | None = None
        self._adaptive_expected_frames: int | None = None
        self._adaptive_delay_cs: int | None = None
        self._adaptive_final_delay_cs: int | None = None

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
                    min(0.30, max(0.0, fraction) * 0.30),
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

            if baseline_edge >= preferred_long_edge(native_edge):
                return self._commit_baseline(baseline, output, baseline.passes, progress)

            source_delay_cs = self._source_delay_centiseconds(info)
            if source_delay_cs is None:
                return self._commit_baseline(baseline, output, baseline.passes, progress)

            candidates: list[DecimationCandidate] = []
            for candidate in source_decimation_candidates(
                source_fps=info.fps,
                source_frame_count=info.frame_count,
                source_delay_centiseconds=source_delay_cs,
            ):
                ideal_edge = predicted_decimated_long_edge(
                    baseline_edge,
                    info.frame_count,
                    candidate.expected_frames,
                    native_edge,
                )
                ideal_gain = ideal_edge / baseline_edge - 1.0
                if ideal_gain + 1e-9 >= MIN_LINEAR_GAIN:
                    candidates.append(candidate)

            if not candidates:
                return self._commit_baseline(baseline, output, baseline.passes, progress)

            total_passes = baseline.passes
            slot_span = 0.70 / len(candidates)

            # Important: do not stop after a predicted candidate fails its full fit.
            # Dev.10-dev.12 could select a higher-FPS probe, fail the final gain veto,
            # then immediately return the baseline without ever testing deeper plans.
            # Each candidate now gets its own measured probe and, when justified, a
            # full fit before the next lower-motion plan is considered.
            for index, candidate in enumerate(candidates):
                slot_start = 0.30 + index * slot_span
                self._set_decimation_state(candidate)
                sample_output = temp_dir / f"probe-stride-{candidate.stride}.gif"

                sample_progress = None
                if progress:
                    sample_progress = lambda fraction, _label, start=slot_start: progress(
                        start + min(slot_span * 0.35, max(0.0, fraction) * slot_span * 0.35),
                        f"Measuring frame stride {candidate.stride}",
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
                    self._clear_adaptive_state()
                    continue

                total_passes += 1
                plan = evaluate_measured_decimation(
                    source_fps=info.fps,
                    candidate=candidate,
                    baseline_long_edge=baseline_edge,
                    native_long_edge=native_edge,
                    sample_size_bytes=sample_output.stat().st_size,
                    max_bytes=max_bytes,
                )
                if plan is None:
                    self._clear_adaptive_state()
                    continue

                adaptive_output = temp_dir / f"adaptive-stride-{candidate.stride}.gif"
                adaptive_progress = None
                if progress:
                    adaptive_progress = lambda fraction, _label, start=slot_start: progress(
                        start + slot_span * 0.35 + min(
                            slot_span * 0.65,
                            max(0.0, fraction) * slot_span * 0.65,
                        ),
                        f"Favoring resolution with every {candidate.stride}th source frame",
                    )

                try:
                    result = self._encode_gif_to_size(
                        info,
                        settings,
                        adaptive_output,
                        native.width,
                        native.height,
                        max_bytes,
                        adaptive_progress,
                    )
                except ConversionCancelled:
                    raise
                except ConversionError:
                    self._clear_adaptive_state()
                    continue

                total_passes += result.passes
                if not actual_gain_is_worthwhile(
                    baseline_long_edge=baseline_edge,
                    adaptive_long_edge=max(result.width, result.height),
                ):
                    self._clear_adaptive_state()
                    continue

                if output.exists():
                    output.unlink()
                shutil.copy2(result.output, output)
                effective_fps = candidate.effective_fps
                self._clear_adaptive_state()
                if progress:
                    progress(1.0, f"Favoring resolution at {effective_fps:.2f} FPS")
                return replace(result, output=output, passes=total_passes)

            self._clear_adaptive_state()
            return self._commit_baseline(baseline, output, total_passes, progress)

    @staticmethod
    def _source_delay_centiseconds(info: MediaInfo) -> int | None:
        if not info.frame_durations_ms:
            return None
        shortest = min(info.frame_durations_ms)
        longest = max(info.frame_durations_ms)
        if longest - shortest > 1:
            return None
        average_ms = sum(info.frame_durations_ms) / len(info.frame_durations_ms)
        delay_cs = int(round(average_ms / 10.0))
        if delay_cs <= 0 or abs(average_ms - delay_cs * 10.0) > 0.5:
            return None
        expected_fps = 100.0 / delay_cs
        if info.fps <= 0 or abs(info.fps - expected_fps) > 0.05:
            return None
        return delay_cs

    def _set_decimation_state(self, candidate: DecimationCandidate) -> None:
        self._adaptive_stride = candidate.stride
        self._adaptive_target_fps = candidate.nominal_fps
        self._adaptive_effective_fps = candidate.effective_fps
        self._adaptive_expected_frames = candidate.expected_frames
        self._adaptive_delay_cs = candidate.delay_centiseconds
        self._adaptive_final_delay_cs = candidate.final_delay_centiseconds

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
        if self._adaptive_stride is None:
            return super()._encode_gif(info, settings, output, width, height, progress, label)

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
            raise ConversionError("Could not determine exact source-frame decimation timing.")

        from .filters import build_video_filter

        base_filter, _ = build_video_filter(info, settings.framing, width, height)
        # Keep every Nth original decoded frame. setpts + fps establishes a clean Y4M
        # cadence for gifski without inventing intermediate image content.
        filter_graph = (
            f"{base_filter},"
            f"select='not(mod(n\\,{stride}))',"
            f"setpts=N/({target_fps:.9f}*TB),"
            f"fps={target_fps:.9f}"
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

            # A source loop is not always divisible by the decimation stride. Keep
            # every retained image at its exact source position, then shorten only
            # the final GIF delay to the source-frame remainder. For Viper stride 2,
            # this means 187 x 80 ms intervals plus one 40 ms closure interval: the
            # original 15.0 s rotation and constant angular speed are preserved.
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
                raise ConversionError(f"Could not finalize adaptive GIF timing. {exc}") from exc
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
        if self._adaptive_expected_frames is None or self._adaptive_stride is None:
            return super()._verify_output(source_info, output, expected_width, expected_height)

        expected_frames = self._adaptive_expected_frames
        effective_fps = self._adaptive_effective_fps
        regular_delay_cs = self._adaptive_delay_cs
        final_delay_cs = self._adaptive_final_delay_cs
        if effective_fps is None or regular_delay_cs is None or final_delay_cs is None:
            raise ConversionError("Adaptive timing state is incomplete.")

        try:
            delays = read_frame_delays_cs(output)
            if len(delays) != expected_frames:
                raise IntegrityError(
                    f"Frame verification failed: expected {expected_frames} frames, output has {len(delays)}."
                )
            if any(delay != regular_delay_cs for delay in delays[:-1]):
                raise IntegrityError("Adaptive GIF contains an unexpected internal frame delay.")
            if delays[-1] != final_delay_cs:
                raise IntegrityError(
                    f"Adaptive GIF closure delay is {delays[-1]} cs; expected {final_delay_cs} cs."
                )

            output_info = probe_media(self.tools.ffprobe, output)
            validate_output_integrity(
                source_info,
                output_info,
                expected_width=expected_width,
                expected_height=expected_height,
                expected_frame_count=expected_frames,
                expected_fps=effective_fps,
            )
        except (ProbeError, IntegrityError, GifTimingError) as exc:
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
        self._adaptive_stride = None
        self._adaptive_target_fps = None
        self._adaptive_effective_fps = None
        self._adaptive_expected_frames = None
        self._adaptive_delay_cs = None
        self._adaptive_final_delay_cs = None
