from __future__ import annotations

import sys
from pathlib import Path

from PySide6.QtWidgets import QApplication

from .ui.adaptive_main_window import MainWindow
from .ui.styles import apply_brand_skin


def main() -> int:
    app = QApplication(sys.argv)
    app.setApplicationName("Polymorph")
    app.setOrganizationName("Knight Witch")

    if "--smoke-test" in sys.argv:
        index = sys.argv.index("--smoke-test")
        if index + 1 >= len(sys.argv):
            return 2
        from .smoke_test import run_packaged_smoke_test

        return run_packaged_smoke_test(app, Path(sys.argv[index + 1]))

    window = MainWindow()
    apply_brand_skin(window)
    window.show()

    # Dragging files onto the installed EXE/shortcut passes them as command-line args.
    cli_files = [Path(arg) for arg in sys.argv[1:] if Path(arg).suffix.lower() == ".webp"]
    if cli_files:
        window._add_files(cli_files)
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
