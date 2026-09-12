from __future__ import annotations

from PySide6.QtGui import QFont, QFontDatabase
from PySide6.QtWidgets import QApplication

from ..resources import asset_path

_FONT_FILES = {
    "Cinzel": "fonts/Cinzel-wght.ttf",
    "Inter": "fonts/Inter-opsz-wght.ttf",
}


def load_brand_fonts(app: QApplication | None = None) -> dict[str, str]:
    """Load bundled UI fonts when available and return resolved family names.

    Development checkouts may omit the binary font assets; packaged builds fetch
    and bundle the pinned files during CI. Missing fonts therefore degrade to the
    stylesheet fallback stack rather than preventing Polymorph from starting.
    """
    loaded: dict[str, str] = {}
    for logical_name, relative_path in _FONT_FILES.items():
        path = asset_path(relative_path)
        if not path.is_file():
            continue
        font_id = QFontDatabase.addApplicationFont(str(path))
        if font_id < 0:
            continue
        families = QFontDatabase.applicationFontFamilies(font_id)
        if families:
            loaded[logical_name] = families[0]

    if app is not None:
        body_family = loaded.get("Inter")
        if body_family:
            font = QFont(body_family)
            font.setPointSizeF(11.0)
            app.setFont(font)
        app.setProperty("polymorphFontsLoaded", ",".join(sorted(loaded)))

    return loaded
