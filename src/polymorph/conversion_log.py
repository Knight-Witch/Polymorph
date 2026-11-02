"""Per-batch conversion diagnostics stored locally, never uploaded."""
from __future__ import annotations

import os
import uuid
from datetime import datetime, timezone
from pathlib import Path

from .models import ConversionSettings


def logs_directory() -> Path:
    """Outside the installed application and any output media directories."""
    if os.name == "nt":
        home = Path(os.environ.get("LOCALAPPDATA") or (Path.home() / "AppData" / "Local"))
    else:
        home = Path(os.environ.get("XDG_STATE_HOME") or (Path.home() / ".local" / "state"))
    return home / "Polymorph" / "logs"


def latest_log(directory: Path | None = None) -> tuple[Path | None, str]:
    directory = directory if directory is not None else logs_directory()
    try:
        candidates = sorted(
            (p for p in directory.glob("conversion-*.log") if p.is_file()),
            key=lambda p: p.name, reverse=True,
        )
        if not candidates:
            return None, "No conversion logs yet. Start a conversion to create one."
        path = candidates[0]
        return path, path.read_text(encoding="utf-8", errors="replace")
    except OSError as exc:
        return None, f"Could not read the conversion log: {exc}"


class ConversionLog:
    """Write every result immediately; keep memory copy if disk is not writable."""

    def __init__(
        self, files: list[Path], settings: ConversionSettings, version: str,
        directory: Path | None = None,
    ) -> None:
        self._lines: list[str] = []
        self.write_error: str | None = None
        root = directory if directory is not None else logs_directory()
        self.path = root / (
            "conversion-" + datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
            + "-" + uuid.uuid4().hex[:8] + ".log"
        )
        self._append("POLYMORPH CONVERSION LOG")
        self._append(f"Version: {version}")
        self._append(f"Session (UTC): {datetime.now(timezone.utc).isoformat()}")
        self._append(f"Input count: {len(files)}")
        self._append(f"Output format: {settings.output_format.value}")
        self._append(f"Sizing mode: {settings.sizing_mode.value}")
        self._append(f"File size target (decimal MB): {settings.max_mb}")
        self._append(f"Resolution: {settings.requested_width} x {settings.requested_height}")
        self._append(f"Output folder: {settings.output_dir}")
        self._append(f"Framing: {settings.framing!r}")
        self._append(f"GIF motion mode: {settings.gif_motion_mode.value}")
        self._append(f"Lossless WebP: {settings.webp_lossless}")
        self._append("Private local log: paths and error details are never uploaded.")
        for file in files:
            self._append(f"QUEUED {file}")
        self._append("-" * 64)

    @property
    def text(self) -> str:
        data = "\n".join(self._lines) + "\n"
        return f"Unable to save log to disk: {self.write_error}\n\n{data}" if self.write_error else data

    def _append(self, text: str) -> None:
        entry = f"[{datetime.now(timezone.utc).strftime('%H:%M:%S.%f')[:-3]} UTC] {text}"
        self._lines.append(entry)
        if self.write_error is not None:
            return
        try:
            self.path.parent.mkdir(parents=True, exist_ok=True)
            with self.path.open("a", encoding="utf-8") as stream:
                stream.write(entry + "\n")
        except OSError as exc:
            self.write_error = str(exc)

    def planned(self, path: str, settings: ConversionSettings) -> None:
        """Record the actual settings snapshot for this source."""
        self._append(
            f"PLAN   {path} | format={settings.output_format.value} "
            f"sizing={settings.sizing_mode.value} "
            f"max_mb={settings.max_mb} "
            f"dimensions={settings.requested_width}x{settings.requested_height} "
            f"framing={settings.framing!r} "
            f"webp_lossless={settings.webp_lossless} "
            f"gif_motion={settings.gif_motion_mode.value}"
        )

    def started(self, path: str) -> None:
        self._append(f"START  {path}")

    def saved(self, source: str, output: str, summary: str) -> None:
        self._append(f"SAVED  {source}\n        -> {output} ({summary})")

    def failed(self, path: str, reason: str, traceback_text: str = "") -> None:
        self._append(f"FAILED {path}\n        Reason: {reason}")
        if traceback_text.strip():
            self._append("Exception traceback:\n" + traceback_text.rstrip())

    def finished(self, saved: int, failed: int) -> None:
        self._append(f"COMPLETE  {saved} saved, {failed} failed")
