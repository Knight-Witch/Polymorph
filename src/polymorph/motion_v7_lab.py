from __future__ import annotations

import argparse
import sys

from PySide6.QtCore import QTimer
from PySide6.QtWidgets import QApplication

from . import motion_lab as base_lab
from .motion_v7_history import V7HistoryMixin
from .motion_v7_render import ExtendedArcaneLoader
from .motion_v7_state import ExtendedEditorState
from .motion_v7_ui_build import V7UIBuildMixin
from .motion_v7_ui_dialogs import V7UIDialogMixin
from .ui.fonts import load_brand_fonts


class ExtendedMotionLab(V7HistoryMixin, V7UIDialogMixin, V7UIBuildMixin, base_lab.MotionLab):
    def __init__(self) -> None:
        self._history_suspended = False
        self._undo_stack: list[dict] = []
        self._redo_stack: list[dict] = []
        self._history_current: dict | None = None
        self._history_merge_key: str | None = None
        self._history_merge_timer: QTimer | None = None

        base_lab.MotionEditorState = ExtendedEditorState
        base_lab.ArcaneLoader = ExtendedArcaneLoader
        super().__init__()
        self.setWindowTitle("Polymorph Motion Lab — Scene Builder v7")
        self._history_merge_timer = QTimer(self)
        self._history_merge_timer.setSingleShot(True)
        self._history_merge_timer.timeout.connect(self._clear_history_merge)
        self._history_current = self.capture_workspace()
        self._install_history_shortcuts()
        self._apply_v7_tooltips()
        self._update_history_buttons()


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--smoke-test", action="store_true")
    args = parser.parse_args(argv)
    app = QApplication(sys.argv[:1])
    load_brand_fonts(app)
    window = ExtendedMotionLab()
    window.show()
    if args.smoke_test:
        window.loader.set_progress(0.62)
        window.loader.editor.set_value("triangle", "static", True)
        window.loader.editor.set_value("middle_runes", "rune_render_mode", "Solid")
        window.loader.editor.set_value("middle_runes", "rune_weight", "Bold")
        window.loader.editor.set_value("progress_outer", "loader_ring_type", "Gradient Tail")
        window.loader.editor.set_value("tracers", "tracer_length", 0.85)
        window.button.forced = "hover"
        QTimer.singleShot(320, app.quit)
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
