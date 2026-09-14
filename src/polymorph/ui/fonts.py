from __future__ import annotations

import lzma

from PySide6.QtCore import QByteArray
from PySide6.QtGui import QFont, QFontDatabase
from PySide6.QtWidgets import QApplication

from ..resources import asset_path

_FONT_FILES = {
    "Polymorph Regular": ("fonts/Polymorph-Regular.ttf.xz", True),
    "Polymorph Bold": ("fonts/Polymorph-Bold.ttf.xz", True),
    "Cinzel": ("fonts/Cinzel-wght.ttf", False),
    "Inter": ("fonts/Inter-opsz-wght.ttf", False),
}


def _register_font(relative_path: str, compressed: bool) -> list[str]:
    path = asset_path(relative_path)
    if not path.is_file():
        return []

    try:
        if compressed:
            font_data = lzma.decompress(path.read_bytes())
            font_id = QFontDatabase.addApplicationFontFromData(QByteArray(font_data))
        else:
            font_id = QFontDatabase.addApplicationFont(str(path))
    except (OSError, lzma.LZMAError):
        return []

    if font_id < 0:
        return []
    return list(QFontDatabase.applicationFontFamilies(font_id))


def load_brand_fonts(app: QApplication | None = None) -> dict[str, str]:
    """Register Polymorph's packaged display/body fonts before the UI is built.

    Packaged builds carry Amanda's Polymorph Regular/Bold faces as losslessly
    compressed assets and register the exact decompressed font bytes directly
    with Qt. Inter remains the body/UI face; Cinzel is an emergency fallback if
    the branded display assets cannot be loaded.
    """
    loaded: dict[str, str] = {}
    for logical_name, (relative_path, compressed) in _FONT_FILES.items():
        families = _register_font(relative_path, compressed)
        if families:
            loaded[logical_name] = families[0]

    bundled_regular = loaded.get("Polymorph Regular")
    bundled_bold = loaded.get("Polymorph Bold")
    display_regular = bundled_regular or loaded.get("Cinzel", "Cinzel")
    display_bold = bundled_bold or bundled_regular or loaded.get("Cinzel", "Cinzel")
    display_source = (
        "bundled-polymorph"
        if bundled_regular and bundled_bold
        else "partial-polymorph"
        if bundled_regular or bundled_bold
        else "cinzel-fallback"
    )

    if app is not None:
        body_family = loaded.get("Inter")
        if body_family:
            font = QFont(body_family)
            font.setPointSizeF(10.5)
            app.setFont(font)
        app.setProperty("polymorphFontsLoaded", ",".join(sorted(loaded)))
        app.setProperty("polymorphDisplayFont", display_regular)
        app.setProperty("polymorphDisplayBoldFont", display_bold)
        app.setProperty("polymorphDisplaySource", display_source)

    return loaded
