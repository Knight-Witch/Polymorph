from __future__ import annotations

import sys
from pathlib import Path

from PySide6.QtWidgets import QApplication

from .ui.main_window import MainWindow


def main() -> int:
    app = QApplication(sys.argv)
    app.setApplicationName("Polymorph")
    app.setOrganizationName("Knight Witch")
    window = MainWindow()
    window.show()

    # Dragging files onto the installed EXE/shortcut passes them as command-line args.
    cli_files = [Path(arg) for arg in sys.argv[1:] if Path(arg).suffix.lower() == ".webp"]
    if cli_files:
        window._add_files(cli_files)
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
