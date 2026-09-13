from __future__ import annotations

import os
import sys
from pathlib import Path

from PySide6.QtWidgets import QApplication

from .ui.adaptive_main_window import MainWindow
from .ui.branded_layout import rebuild_brand_layout
from .ui.fonts import load_brand_fonts
from .ui.styles import apply_brand_skin


def _bootstrap_log(message: str) -> None:
    """Append packaged-smoke startup checkpoints without affecting normal launches."""
    target = os.environ.get("POLYMORPH_SMOKE_LOG")
    if not target:
        return
    try:
        path = Path(target)
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("a", encoding="utf-8") as handle:
            handle.write(f"APP {message}\n")
            handle.flush()
    except Exception:
        pass


def main() -> int:
    _bootstrap_log("main entered")
    _bootstrap_log("constructing QApplication")
    app = QApplication(sys.argv)
    _bootstrap_log("QApplication constructed")
    app.setApplicationName("Polymorph")
    app.setOrganizationName("Knight Witch")
    _bootstrap_log("loading brand fonts")
    load_brand_fonts(app)
    _bootstrap_log("brand fonts loaded")

    if "--smoke-test" in sys.argv:
        _bootstrap_log("smoke-test argument detected")
        index = sys.argv.index("--smoke-test")
        if index + 1 >= len(sys.argv):
            _bootstrap_log("smoke-test sample argument missing")
            return 2
        _bootstrap_log("importing packaged smoke module")
        from .smoke_test import run_packaged_smoke_test

        _bootstrap_log("packaged smoke module imported")
        _bootstrap_log("calling packaged smoke")
        code = run_packaged_smoke_test(app, Path(sys.argv[index + 1]))
        _bootstrap_log(f"packaged smoke returned {code}")
        # The frozen smoke path is a CI probe, not an interactive Qt session.
        # Force process teardown after the probe has written its log so native
        # media/plugin teardown cannot keep Start-Process waiting indefinitely.
        try:
            sys.stdout.flush()
            sys.stderr.flush()
        finally:
            os._exit(code)

    _bootstrap_log("constructing interactive main window")
    window = MainWindow()
    rebuild_brand_layout(window)
    apply_brand_skin(window)
    window.show()

    # Dragging files onto the installed EXE/shortcut passes them as command-line args.
    cli_files = [Path(arg) for arg in sys.argv[1:] if Path(arg).suffix.lower() == ".webp"]
    if cli_files:
        window._add_files(cli_files)
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
