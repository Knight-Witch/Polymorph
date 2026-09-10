from __future__ import annotations

import os
import time
import traceback
from pathlib import Path

from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication

from .resources import asset_path
from .tools import find_toolchain
from .ui.main_window import MainWindow

_ASSETS = ("update.svg", "github.svg", "kofi.svg", "patreon.svg", "discord.svg")


def _write_log(lines: list[str]) -> None:
    log_path = os.environ.get("POLYMORPH_SMOKE_LOG")
    if not log_path:
        return
    path = Path(log_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def run_packaged_smoke_test(app: QApplication, sample: Path) -> int:
    """Exercise the frozen application without exposing a user-facing test mode."""
    lines: list[str] = []
    window: MainWindow | None = None
    try:
        sample = sample.resolve()
        if not sample.is_file():
            raise RuntimeError(f"Smoke-test WebP is missing: {sample}")

        tools = find_toolchain()
        for name, path in (
            ("ffmpeg", tools.ffmpeg),
            ("ffprobe", tools.ffprobe),
            ("gifski", tools.gifski),
        ):
            if not path.is_file():
                raise RuntimeError(f"Bundled {name} was not found: {path}")
        lines.append("PASS bundled conversion tools")

        for name in _ASSETS:
            path = asset_path(name)
            if not path.is_file():
                raise RuntimeError(f"Packaged UI resource is missing: {path}")
            if QIcon(str(path)).isNull():
                raise RuntimeError(f"Packaged UI resource could not be loaded: {path}")
        lines.append("PASS packaged footer SVG resources")

        window = MainWindow()
        if window.converter is None:
            raise RuntimeError("Main window could not resolve the bundled conversion toolchain")
        window._add_files([sample])
        app.processEvents()

        if window.file_list.count() != 1:
            raise RuntimeError("Main window did not accept the smoke-test WebP")

        movie = window.preview._movie
        if movie is None or not movie.isValid():
            raise RuntimeError("Qt could not initialize animated WebP playback")
        if not movie.jumpToFrame(0):
            raise RuntimeError("Qt could not decode the first animated WebP frame")

        deadline = time.monotonic() + 2.0
        while window.preview._pixmap.isNull() and time.monotonic() < deadline:
            app.processEvents()
            time.sleep(0.02)
        if window.preview._pixmap.isNull():
            raise RuntimeError("Live preview did not produce a renderable WebP frame")
        lines.append("PASS animated WebP live preview")

        window.frame_mode.setCurrentIndex(1)  # Crop to ratio
        window.ratio_combo.setCurrentText("16:9")
        app.processEvents()
        window.res_radio.setChecked(True)
        window.width_spin.setValue(64)
        app.processEvents()
        if (window.width_spin.value(), window.height_spin.value()) != (64, 36):
            raise RuntimeError(
                "Linked resolution controls failed for 16:9: "
                f"{window.width_spin.value()}x{window.height_spin.value()}"
            )
        lines.append("PASS linked 16:9 resolution controls")

        lines.append("PACKAGED POLYMORPH SMOKE TEST PASSED")
        _write_log(lines)
        return 0
    except Exception as exc:
        lines.append(f"FAIL {exc}")
        lines.append(traceback.format_exc())
        _write_log(lines)
        return 1
    finally:
        if window is not None:
            window.close()
        app.processEvents()
