from __future__ import annotations

from PySide6.QtGui import QFont, QFontDatabase
from PySide6.QtWidgets import QApplication

from ..resources import asset_path

_FONT_FILES = {
    "Cinzel": "fonts/Cinzel-wght.ttf",
    "Inter": "fonts/Inter-opsz-wght.ttf",
}
_OPTIONAL_TRAJAN_FILES = (
    "fonts/Trajan-Regular.ttf",
    "fonts/Trajan-Bold.otf",
)


def load_brand_fonts(app: QApplication | None = None) -> dict[str, str]:
    """Load packaged UI fonts and prefer legally installed Trajan Pro when present.

    Polymorph's public repository bundles only redistributable Cinzel/Inter assets.
    If Trajan Pro is installed on the user's Windows system (or supplied locally in
    an untracked development assets folder), Qt will use it automatically.
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

    # Development-only/private local convenience: register Trajan if a legal
    # local copy exists beside the other assets. These files are not committed.
    for relative_path in _OPTIONAL_TRAJAN_FILES:
        path = asset_path(relative_path)
        if not path.is_file():
            continue
        font_id = QFontDatabase.addApplicationFont(str(path))
        if font_id >= 0:
            families = QFontDatabase.applicationFontFamilies(font_id)
            if families:
                loaded["Trajan Pro"] = families[0]

    families = set(QFontDatabase.families())
    display = "Trajan Pro" if "Trajan Pro" in families else loaded.get("Cinzel", "Cinzel")

    if app is not None:
        body_family = loaded.get("Inter")
        if body_family:
            font = QFont(body_family)
            font.setPointSizeF(10.5)
            app.setFont(font)
        app.setProperty("polymorphFontsLoaded", ",".join(sorted(loaded)))
        app.setProperty("polymorphDisplayFont", display)

    return loaded
