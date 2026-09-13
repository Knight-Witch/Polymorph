from __future__ import annotations

from PySide6.QtGui import QFont, QFontDatabase
from PySide6.QtWidgets import QApplication

from ..resources import asset_path

_FONT_FILES = {
    "Trajan Regular": "fonts/Trajan-Regular.ttf",
    "Trajan Bold": "fonts/Trajan-Bold.otf",
    "Cinzel": "fonts/Cinzel-wght.ttf",
    "Inter": "fonts/Inter-opsz-wght.ttf",
}


def _installed_trajan_family() -> str | None:
    """Return a Trajan-family face only as a source-checkout fallback."""
    families = list(QFontDatabase.families())
    preferred = (
        "Trajan Pro 3",
        "Trajan Pro",
        "Trajan",
    )
    folded = {family.casefold(): family for family in families}
    for candidate in preferred:
        match = folded.get(candidate.casefold())
        if match:
            return match
    for family in families:
        if family.casefold().startswith("trajan"):
            return family
    return None


def load_brand_fonts(app: QApplication | None = None) -> dict[str, str]:
    """Register Polymorph's packaged display/body fonts before the UI is built.

    Packaged Windows builds carry the approved Trajan Regular/Bold files inside
    the application. Cinzel remains an emergency source-checkout fallback only;
    normal installed testers do not depend on any system font being present.
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

    bundled_regular = loaded.get("Trajan Regular")
    bundled_bold = loaded.get("Trajan Bold")
    installed_fallback = _installed_trajan_family()
    display_regular = bundled_regular or installed_fallback or loaded.get("Cinzel", "Cinzel")
    display_bold = bundled_bold or bundled_regular or installed_fallback or loaded.get("Cinzel", "Cinzel")
    display_source = (
        "bundled-trajan"
        if bundled_regular and bundled_bold
        else "system-trajan"
        if installed_fallback
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
