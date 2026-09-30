from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QLabel, QRadioButton

from . import fidelity_pass as _fidelity


_MARKER = "/* POLYMORPH_FINAL_POLISH_V1 */"
_INSTALLED = False
_previous_palette = None
_previous_visual = None


def _card_for_heading(window, title: str):
    for heading in window.findChildren(QLabel, "CardHeading"):
        if heading.text() == title:
            return heading.parentWidget()
    return None


def _final_palette(window, scale: float) -> None:
    assert _previous_palette is not None
    _previous_palette(window, scale)

    sheet = window.styleSheet()
    if _MARKER in sheet:
        sheet = sheet.split(_MARKER, 1)[0].rstrip()

    # Human-review correction: option labels must read clearly above their helpers.
    if scale <= 0.76:
        option_size = 7.60
        helper_size = 5.80
    else:
        option_size = max(8.10, 9.25 * scale)
        helper_size = max(5.80, 6.45 * scale)
    override = f"""
{_MARKER}
QWidget#AppRoot QRadioButton {{
    font-family: "Inter", "Segoe UI", sans-serif;
    font-size: {option_size:.2f}pt;
}}
QLabel#SecondaryText {{
    font-family: "Inter", "Segoe UI", sans-serif;
    font-size: {helper_size:.2f}pt;
}}
"""
    window.setStyleSheet(sheet + "\n" + override)


def _apply_local_option_typography(window, scale: float) -> None:
    """Own the actual widgets so alignment-only local styles cannot erase hierarchy."""
    if scale <= 0.76:
        option_size = 7.60
        helper_size = 5.80
    else:
        option_size = max(8.10, 9.25 * scale)
        helper_size = max(5.80, 6.45 * scale)

    for radio in window.findChildren(QRadioButton):
        existing = radio.styleSheet().strip().rstrip(";")
        prefix = f"{existing}; " if existing else ""
        radio.setStyleSheet(
            prefix
            + 'font-family: "Inter", "Segoe UI", sans-serif; '
            + f"font-size: {option_size:.2f}pt; font-weight: 500;"
        )

    for label in window.findChildren(QLabel, "SecondaryText"):
        label.setStyleSheet(
            'padding-left: 0px; font-family: "Inter", "Segoe UI", sans-serif; '
            + f"font-size: {helper_size:.2f}pt; font-weight: 400; color: #85898d;"
        )


def _align_framing_pair(window) -> None:
    """Pin paired-card content to the top so both headers/dividers share one baseline."""
    framing = _card_for_heading(window, "FRAMING")
    aspect = _card_for_heading(window, "ASPECT RATIO")
    for card in (framing, aspect):
        if card is None or card.layout() is None:
            continue
        card.layout().setAlignment(Qt.AlignmentFlag.AlignTop)


def _final_visual(window) -> None:
    assert _previous_visual is not None
    _previous_visual(window)
    _align_framing_pair(window)
    _apply_local_option_typography(window, float(window.property("brandScale") or 1.0))


def install_final_polish_patch() -> None:
    """Apply the narrow post-stable release human-review corrections."""
    global _INSTALLED, _previous_palette, _previous_visual
    if _INSTALLED:
        return
    _INSTALLED = True

    _previous_palette = _fidelity._apply_mockup_palette_and_body
    _previous_visual = _fidelity._apply_visual_polish
    _fidelity._apply_mockup_palette_and_body = _final_palette
    _fidelity._apply_visual_polish = _final_visual
