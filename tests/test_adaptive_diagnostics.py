import json
import tempfile
import unittest
from pathlib import Path

from polymorph.diagnostic_adaptive_converter import DiagnosticAdaptiveConverter
from polymorph.models import ConversionResult


class AdaptiveDiagnosticTests(unittest.TestCase):
    def _converter(self) -> DiagnosticAdaptiveConverter:
        converter = DiagnosticAdaptiveConverter(None)
        converter._diagnostic_baseline_edge = 1552
        converter._diagnostic_native_edge = 2048
        converter._diagnostic_max_bytes = 99_000_000
        converter._diagnostic_candidates = {
            2: {
                "stride": 2,
                "nominal_fps": 12.5,
                "effective_fps": 12.5333333333,
                "expected_frames": 188,
                "delay_centiseconds": 8,
                "final_delay_centiseconds": 4,
            }
        }
        return converter

    def test_classifies_measured_gain_rejection(self):
        converter = self._converter()
        converter._diagnostic_events = [
            {
                "event": "encode_result",
                "phase": "sample_probe",
                "stride": 2,
                "width": 1552,
                "height": 1552,
                "size_bytes": 90_000_000,
            },
            {
                "event": "final_result",
                "width": 1552,
                "height": 1552,
                "size_bytes": 93_630_962,
                "frames": 375,
            },
        ]

        summary = converter._candidate_summary()[0]
        self.assertEqual(summary["outcome"], "measured_gain_below_threshold")
        self.assertLess(summary["predicted_linear_gain"], 0.08)

    def test_classifies_selected_candidate_and_writes_sidecar(self):
        converter = self._converter()
        converter._diagnostic_events = [
            {
                "event": "encode_result",
                "phase": "sample_probe",
                "stride": 2,
                "width": 1552,
                "height": 1552,
                "size_bytes": 50_000_000,
            },
            {
                "event": "fit_result",
                "phase": "adaptive_fit",
                "stride": 2,
                "width": 1800,
                "height": 1800,
                "size_bytes": 96_000_000,
                "frames": 188,
                "passes": 3,
            },
            {
                "event": "final_result",
                "width": 1800,
                "height": 1800,
                "size_bytes": 96_000_000,
                "frames": 188,
            },
        ]

        summary = converter._candidate_summary()[0]
        self.assertEqual(summary["outcome"], "selected")
        self.assertGreaterEqual(summary["actual_linear_gain"], 0.08)

        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "trace.json"
            result = ConversionResult(
                source=Path("source.webp"),
                output=Path("output.gif"),
                width=1800,
                height=1800,
                size_bytes=96_000_000,
                frames=188,
                duration_s=15.0,
                passes=4,
            )
            converter._write_diagnostic(path, result)
            payload = json.loads(path.read_text(encoding="utf-8"))
            self.assertEqual(payload["final"]["frames"], 188)
            self.assertEqual(payload["candidates"][0]["outcome"], "selected")
            self.assertEqual(converter.last_diagnostic_path, path)


if __name__ == "__main__":
    unittest.main()
