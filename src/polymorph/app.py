from __future__ import annotations

import sys
from pathlib import Path

from PySide6.QtWidgets import QApplication

from .ui.visual_patch import install_visual_patch
from .ui.button_motion_patch import install_button_motion_patch
from .ui.button_motion import install_button_motion
from .ui.compact_status_patch import install_compact_status_patch
from .ui.final_polish_patch import install_final_polish_patch

install_visual_patch()
install_button_motion_patch()
install_button_motion()
install_compact_status_patch()
install_final_polish_patch()

from .ui.adaptive_main_window import MainWindow
from .ui.branded_layout import rebuild_brand_layout
from .ui.fonts import load_brand_fonts
from .ui.styles import apply_brand_skin


def main() -> int:
    app = QApplication(sys.argv)
    app.setApplicationName("Polymorph")
    app.setOrganizationName("Knight Witch")
    load_brand_fonts(app)

    window = MainWindow()
    rebuild_brand_layout(window)
    apply_brand_skin(window)
    window.show()

    cli_files = [Path(arg) for arg in sys.argv[1:] if Path(arg).suffix.lower() == ".webp"]
    if cli_files:
        window._add_files(cli_files)
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
