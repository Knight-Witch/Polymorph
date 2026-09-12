from __future__ import annotations

import json
import math
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .adaptive_converter import AdaptiveConverter
from .constants import APP_VERSION
from .geometry import native_geometry
from .models import ConversionResult, ConversionSettings, GifMotionMode, OutputFormat, SizingMode
from .motion_planner import MIN_LINEAR_GAIN, DecimationCandidate, preferred_long_edge
from .size_optimizer import reference_thresholds
from .size_units import mb_to_bytes


class DiagnosticAdaptiveConverter(AdaptiveConverter):
    """Development-only trace wrapper around the experimental adaptive converter.

    The wrapped conversion decisions are unchanged. Favor-resolution jobs additionally
    emit a compact JSON sidecar that records every real encode attempt and enough
    measured data to explain why each source-frame stride was selected or rejected.
    """

    def __init__(self, tools) -> None:
        super().__init__(tools)
        self.last_diagnostic_path: Path | None = None
        self._diagnostic_events: list[dict[str, Any]] = []
        self._diagnostic_candidates: dict[int, dict[str, Any]] = {}
        self._diagnostic_baseline_edge = 0
        self._diagnostic_native_edge = 0
        self._diagnostic_max_bytes = 0

    def convert(self, source: Path, settings: ConversionSettings, progress=None) -> ConversionResult:
        adaptive = (
            settings.output_format is OutputFormat.GIF
            and settings.sizing_mode is SizingMode.FILE_SIZE
            and settings.gif_motion_mode is GifMotionMode.FAVOR_RESOLUTION
        )
        if not adaptive:
            self._reset_diagnostic()
            return super().convert(source, settings, progress)

        self._reset_diagnostic()
        source = Path(source)
        info = self.probe(source)
        native = native_geometry(info, settings.framing)
        self._diagnostic_native_edge = max(native.width, native.height)
        self._diagnostic_max_bytes = mb_to_bytes(settings.max_mb)
        self._record(
            "start",
            source=str(source),
            source_width=info.width,
            source_height=info.height,
            source_frames=info.frame_count,
            source_duration_s=info.duration_s,
            source_fps=info.fps,
            native_width=native.width,
            native_height=native.height,
            max_bytes=self._diagnostic_max_bytes,
        )

        try:
            result = super().convert(source, settings, progress)
        except Exception as exc:
            self._record("fatal_error", error_type=type(exc).__name__, error=str(exc))
            self._write_diagnostic(
                self._failure_diagnostic_path(source, settings),
                final_result=None,
            )
            raise

        self._record(
            "final_result",
            width=result.width,
            height=result.height,
            size_bytes=result.size_bytes,
            frames=result.frames,
            duration_s=result.duration_s,
            passes=result.passes,
        )
        self._write_diagnostic(
            result.output.with_name(f"{result.output.stem}_ADAPTIVE_DIAGNOSTIC.json"),
            final_result=result,
        )
        return result

    def _encode_gif_to_size(
        self,
        info,
        settings,
        output,
        native_width,
        native_height,
        max_bytes,
        progress,
    ) -> ConversionResult:
        stride = self._adaptive_stride
        phase = "baseline_fit" if stride is None else "adaptive_fit"
        self._record(
            "fit_start",
            phase=phase,
            stride=stride,
            native_width=native_width,
            native_height=native_height,
            max_bytes=max_bytes,
        )
        try:
            result = super()._encode_gif_to_size(
                info,
                settings,
                output,
                native_width,
                native_height,
                max_bytes,
                progress,
            )
        except Exception as exc:
            self._record(
                "fit_error",
                phase=phase,
                stride=stride,
                error_type=type(exc).__name__,
                error=str(exc),
            )
            raise

        if stride is None:
            self._diagnostic_baseline_edge = max(result.width, result.height)
        self._record(
            "fit_result",
            phase=phase,
            stride=stride,
            width=result.width,
            height=result.height,
            size_bytes=result.size_bytes,
            frames=result.frames,
            passes=result.passes,
        )
        return result

    def _encode_once(self, info, settings, output, width, height, progress, label) -> None:
        stride = self._adaptive_stride
        phase = "sample_probe" if Path(output).name.startswith("probe-stride-") else "encode_pass"
        try:
            super()._encode_once(info, settings, output, width, height, progress, label)
        except Exception as exc:
            self._record(
                "encode_error",
                phase=phase,
                stride=stride,
                width=width,
                height=height,
                label=label,
                output_name=Path(output).name,
                error_type=type(exc).__name__,
                error=str(exc),
            )
            raise

        size_bytes = Path(output).stat().st_size if Path(output).exists() else None
        self._record(
            "encode_result",
            phase=phase,
            stride=stride,
            width=width,
            height=height,
            label=label,
            output_name=Path(output).name,
            size_bytes=size_bytes,
        )

    def _set_decimation_state(self, candidate: DecimationCandidate) -> None:
        self._diagnostic_candidates[candidate.stride] = {
            "stride": candidate.stride,
            "nominal_fps": candidate.nominal_fps,
            "effective_fps": candidate.effective_fps,
            "expected_frames": candidate.expected_frames,
            "delay_centiseconds": candidate.delay_centiseconds,
            "final_delay_centiseconds": candidate.final_delay_centiseconds,
        }
        self._record("candidate_start", **self._diagnostic_candidates[candidate.stride])
        super()._set_decimation_state(candidate)

    def _commit_baseline(self, baseline, output, passes, progress):
        self._record(
            "fallback_to_baseline",
            width=baseline.width,
            height=baseline.height,
            size_bytes=baseline.size_bytes,
            frames=baseline.frames,
            passes=passes,
        )
        return super()._commit_baseline(baseline, output, passes, progress)

    def _record(self, event: str, **details: Any) -> None:
        self._diagnostic_events.append({"event": event, **details})

    def _reset_diagnostic(self) -> None:
        self.last_diagnostic_path = None
        self._diagnostic_events = []
        self._diagnostic_candidates = {}
        self._diagnostic_baseline_edge = 0
        self._diagnostic_native_edge = 0
        self._diagnostic_max_bytes = 0

    def _candidate_summary(self) -> list[dict[str, Any]]:
        if self._diagnostic_baseline_edge <= 0 or self._diagnostic_max_bytes <= 0:
            return []

        target_bytes, _ = reference_thresholds(self._diagnostic_max_bytes)
        spatial_target = preferred_long_edge(self._diagnostic_native_edge)
        summaries: list[dict[str, Any]] = []
        final_event = next(
            (event for event in reversed(self._diagnostic_events) if event["event"] == "final_result"),
            None,
        )
        final_frames = int(final_event["frames"]) if final_event else None

        for stride in sorted(self._diagnostic_candidates):
            data = dict(self._diagnostic_candidates[stride])
            stride_events = [
                event for event in self._diagnostic_events if event.get("stride") == stride
            ]
            sample = next(
                (
                    event
                    for event in stride_events
                    if event["event"] == "encode_result" and event.get("phase") == "sample_probe"
                ),
                None,
            )
            sample_error = next(
                (
                    event
                    for event in stride_events
                    if event["event"] == "encode_error" and event.get("phase") == "sample_probe"
                ),
                None,
            )
            fit = next(
                (
                    event
                    for event in reversed(stride_events)
                    if event["event"] == "fit_result" and event.get("phase") == "adaptive_fit"
                ),
                None,
            )
            fit_error = next(
                (
                    event
                    for event in reversed(stride_events)
                    if event["event"] == "fit_error" and event.get("phase") == "adaptive_fit"
                ),
                None,
            )

            if sample and sample.get("size_bytes"):
                sample_size = int(sample["size_bytes"])
                predicted = self._diagnostic_baseline_edge * math.sqrt(target_bytes / sample_size)
                predicted_edge = min(
                    spatial_target,
                    self._diagnostic_native_edge,
                    max(self._diagnostic_baseline_edge, int(round(predicted))),
                )
                predicted_gain = predicted_edge / self._diagnostic_baseline_edge - 1.0
                data.update(
                    sample_size_bytes=sample_size,
                    predicted_long_edge=predicted_edge,
                    predicted_linear_gain=predicted_gain,
                )
            else:
                predicted_gain = None

            if fit:
                fit_edge = max(int(fit["width"]), int(fit["height"]))
                actual_gain = fit_edge / self._diagnostic_baseline_edge - 1.0
                data.update(
                    fit_width=int(fit["width"]),
                    fit_height=int(fit["height"]),
                    fit_size_bytes=int(fit["size_bytes"]),
                    actual_linear_gain=actual_gain,
                )
            else:
                actual_gain = None

            if final_frames == data["expected_frames"]:
                outcome = "selected"
            elif sample_error:
                outcome = "sample_encode_error"
                data["error"] = sample_error.get("error")
            elif sample is None:
                outcome = "sample_not_completed"
            elif predicted_gain is not None and predicted_gain + 1e-9 < MIN_LINEAR_GAIN:
                outcome = "measured_gain_below_threshold"
            elif fit_error:
                outcome = "adaptive_fit_error"
                data["error"] = fit_error.get("error")
            elif fit is not None and actual_gain is not None and actual_gain + 1e-9 < MIN_LINEAR_GAIN:
                outcome = "final_gain_below_threshold"
            elif fit is not None:
                outcome = "fit_completed_but_not_selected"
            else:
                outcome = "measurement_passed_no_fit_result"

            data["outcome"] = outcome
            summaries.append(data)

        return summaries

    def _write_diagnostic(self, path: Path, final_result: ConversionResult | None) -> None:
        payload: dict[str, Any] = {
            "schema": 1,
            "polymorph_version": APP_VERSION,
            "created_utc": datetime.now(timezone.utc).isoformat(),
            "minimum_linear_gain": MIN_LINEAR_GAIN,
            "baseline_long_edge": self._diagnostic_baseline_edge,
            "native_long_edge": self._diagnostic_native_edge,
            "max_bytes": self._diagnostic_max_bytes,
            "candidates": self._candidate_summary(),
            "events": self._diagnostic_events,
        }
        if final_result is not None:
            payload["final"] = {
                "output": str(final_result.output),
                "width": final_result.width,
                "height": final_result.height,
                "size_bytes": final_result.size_bytes,
                "frames": final_result.frames,
                "duration_s": final_result.duration_s,
                "passes": final_result.passes,
            }

        try:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
            self.last_diagnostic_path = path
        except OSError:
            self.last_diagnostic_path = None

    @staticmethod
    def _failure_diagnostic_path(source: Path, settings: ConversionSettings) -> Path:
        output_dir = Path(settings.output_dir or source.parent)
        return output_dir / f"{source.stem}_POLYMORPH_ADAPTIVE_DIAGNOSTIC.json"
