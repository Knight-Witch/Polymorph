from __future__ import annotations

from PySide6.QtCore import QEvent, QObject, QSize, Qt, QTimer
from PySide6.QtGui import QColor, QIcon
from PySide6.QtWidgets import (
    QApplication,
    QLabel,
    QLayout,
    QPushButton,
    QRadioButton,
    QToolButton,
    QWidget,
)

from .brand_widgets import TintIconLabel, tinted_icon_pixmap, tracked_font


_CARD_ICONS = {
    "FILES": "files.svg",
    "OUTPUT FORMAT": "output-format.svg",
    "SIZING": "sizing.svg",
    "GIF PRIORITY": "gif-priority.svg",
    "FRAMING": "framing.svg",
    "ASPECT RATIO": "aspect-ratio-clean.svg",
    "CROP ZOOM": "crop-zoom.svg",
    "OUTPUT FOLDER": "output-folder.svg",
}

_MOCKUP_OVERRIDE_MARKER = "/* POLYMORPH_MOCKUP_V3_OVERRIDES */"


def _card_for_heading(window, title: str):
    for heading in window.findChildren(QLabel, "CardHeading"):
        if heading.text() == title:
            return heading.parentWidget()
    return None


def _nested_layout(card, index: int) -> QLayout | None:
    if card is None or card.layout() is None or card.layout().count() <= index:
        return None
    return card.layout().itemAt(index).layout()


def _remove_spacer_between(layout: QLayout, first: QWidget, second: QWidget) -> None:
    first_index = layout.indexOf(first)
    second_index = layout.indexOf(second)
    if first_index < 0 or second_index <= first_index:
        return
    for index in range(second_index - 1, first_index, -1):
        item = layout.itemAt(index)
        if item is not None and item.spacerItem() is not None:
            layout.takeAt(index)


def _qss_family(family: str) -> str:
    return family.replace("\\", "\\\\").replace('"', '\\"')


def _icon_size(scale: float) -> int:
    return max(13, round(18 * scale))


def _section_axis(scale: float) -> int:
    # Icon width + header gap. Content text should visually start on this axis.
    return max(17, round(24 * scale))


def _radio_nudge(scale: float) -> int:
    # Radio label begins after indicator+spacing, so only a small widget nudge is needed.
    return max(2, round(4 * scale))


def _set_card_icon(window, title: str, asset: str, scale: float) -> None:
    card = _card_for_heading(window, title)
    header = _nested_layout(card, 0)
    if header is None or header.count() == 0:
        return
    icon = header.itemAt(0).widget()
    if not isinstance(icon, QLabel):
        return
    size = _icon_size(scale)
    header.setSpacing(max(4, round(6 * scale)))
    if isinstance(icon, TintIconLabel):
        icon._asset = asset
        icon._icon_size = 18
        icon.refresh(scale)
        return
    icon.setText("")
    icon.setFixedSize(size, size)
    icon.setPixmap(tinted_icon_pixmap(asset, size))


def _apply_heading_typography(window, scale: float) -> None:
    app = QApplication.instance()
    family = "Polymorph"
    if app is not None:
        family = str(app.property("polymorphDisplayBoldFont") or family).strip() or family
    point_size = max(6.8, 8.45 * scale)
    spacing = max(0.45, 0.78 * scale)
    for heading in window.findChildren(QLabel, "CardHeading"):
        heading.setStyleSheet(
            f'font-family: "{_qss_family(family)}"; '
            f"font-size: {point_size:.2f}pt; font-weight: 700; "
            "color: #c9a666; background: transparent;"
        )
        heading.setFont(
            tracked_font(
                point_size,
                spacing,
                bold=True,
                family=family,
            )
        )


def _apply_mockup_palette_and_body(window, scale: float) -> None:
    sheet = window.styleSheet()
    if _MOCKUP_OVERRIDE_MARKER in sheet:
        sheet = sheet.split(_MOCKUP_OVERRIDE_MARKER, 1)[0].rstrip()

    radio_size = max(7.0, 8.05 * scale)
    helper_size = max(6.35, 7.15 * scale)
    control_size = max(7.0, 8.15 * scale)
    queue_size = max(7.0, 8.15 * scale)
    footer_size = max(6.6, 7.45 * scale)
    small_size = max(6.4, 7.20 * scale)
    footer_height = max(18, round(26 * scale))

    overrides = f"""
{_MOCKUP_OVERRIDE_MARKER}
QWidget#AppRoot QRadioButton {{
    font-family: "Inter", "Segoe UI", sans-serif;
    font-size: {radio_size:.2f}pt;
    color: #ddd7cf;
}}
QWidget#AppRoot QComboBox,
QWidget#AppRoot QSpinBox,
QWidget#AppRoot QDoubleSpinBox,
QWidget#AppRoot QPushButton {{
    font-family: "Inter", "Segoe UI", sans-serif;
    font-size: {control_size:.2f}pt;
    color: #dcd5cc;
}}
QLabel#SecondaryText {{
    font-family: "Inter", "Segoe UI", sans-serif;
    font-size: {helper_size:.2f}pt;
    color: #827d75;
}}
QLabel#QueueFileName {{
    font-family: "Inter", "Segoe UI", sans-serif;
    font-size: {queue_size:.2f}pt;
    color: #e7e0d7;
}}
QLabel#QueueMeta,
QLabel#FileCount,
QLabel#FooterMeta {{
    font-family: "Inter", "Segoe UI", sans-serif;
    font-size: {small_size:.2f}pt;
    color: #777168;
}}
QLabel#StatusLabel {{
    font-family: "Inter", "Segoe UI", sans-serif;
    font-size: {max(7.2, 8.35 * scale):.2f}pt;
    color: #e7e0d6;
}}
QLabel#StatusDetail {{
    font-family: "Inter", "Segoe UI", sans-serif;
    font-size: {helper_size:.2f}pt;
    color: #7f7a72;
}}
QLabel#UnitLabel,
QLabel#TimesLabel,
QLabel#ZoomValue,
QLabel#PlaybackTime {{
    font-family: "Inter", "Segoe UI", sans-serif;
    font-size: {helper_size:.2f}pt;
    color: #938b80;
}}
QLabel#PathText {{
    font-family: "Inter", "Segoe UI", sans-serif;
    font-size: {max(6.8, 7.75 * scale):.2f}pt;
    color: #d3ccc2;
    background: #070707;
    border-color: #3d3226;
}}
QPushButton#HeaderAction {{
    font-size: {max(6.9, 7.85 * scale):.2f}pt;
    color: #e2c996;
    background: #0c0b0a;
    border-color: #735b3d;
}}
QPushButton#BrowseButton {{
    font-size: {max(6.8, 7.55 * scale):.2f}pt;
    color: #cfbea1;
    background: #0c0b0a;
    border-color: #5f4b34;
}}
QToolButton#FooterLink {{
    font-family: "Inter", "Segoe UI", sans-serif;
    font-size: {footer_size:.2f}pt;
    color: #aaa39a;
    min-height: {footer_height}px;
    padding: 2px 7px 2px 4px;
}}
QToolButton#FooterLink:hover {{ color: #e7ddd0; }}
QFrame#CardSeparator,
QFrame#PreviewMetaSeparator,
QFrame#FooterSeparator {{
    color: #342b21;
    background: #342b21;
}}
QFrame#VerticalSeparator {{
    color: #342d25;
    background: #342d25;
}}
QRadioButton::indicator {{
    border-color: #696259;
    background: #050506;
}}
QRadioButton::indicator:hover {{ border-color: #bb965e; }}
QRadioButton::indicator:checked {{
    border-color: #c5a164;
    background: qradialgradient(
        cx: 0.5, cy: 0.5, radius: 0.5,
        fx: 0.5, fy: 0.5,
        stop: 0 #df2d36,
        stop: 0.35 #df2d36,
        stop: 0.36 #050506,
        stop: 1 #050506
    );
}}
QComboBox,
QSpinBox,
QDoubleSpinBox {{
    background: #080809;
    border-color: #3b3127;
}}
QComboBox:hover,
QSpinBox:hover,
QDoubleSpinBox:hover {{
    background: #11100f;
    border-color: #7a6040;
}}
"""
    window.setStyleSheet(sheet + "\n" + overrides)


def _apply_container_geometry(window, scale: float) -> None:
    # The accepted minimum-size compaction is protected; do not overwrite its rail budget.
    if scale <= 0.76:
        return

    card_h = max(8, round(11 * scale))
    card_top = max(6, round(8 * scale))
    card_bottom = max(7, round(9 * scale))
    card_spacing = max(4, round(6 * scale))

    for card in window.findChildren(QWidget, "ControlCard"):
        layout = card.layout()
        if layout is not None:
            layout.setContentsMargins(card_h, card_top, card_h, card_bottom)
            layout.setSpacing(card_spacing)

    file_card = window.findChild(QWidget, "FileCard")
    if file_card is not None and file_card.layout() is not None:
        file_card.layout().setContentsMargins(card_h, card_top, card_h, max(6, round(8 * scale)))
        file_card.layout().setSpacing(max(4, round(6 * scale)))

    rail = window.findChild(QWidget, "ControlRailContent")
    if rail is not None and rail.layout() is not None:
        rail.layout().setSpacing(max(5, round(7 * scale)))

    status_card = window.findChild(QWidget, "StatusCard")
    if status_card is not None and status_card.layout() is not None:
        status_card.layout().setContentsMargins(
            max(8, round(12 * scale)),
            max(5, round(7 * scale)),
            max(8, round(12 * scale)),
            max(5, round(7 * scale)),
        )
        status_card.layout().setSpacing(max(4, round(5 * scale)))
        top_row = status_card.layout().itemAt(0).layout()
        if top_row is not None:
            top_row.setSpacing(max(8, round(12 * scale)))


def _apply_content_alignment(window, scale: float) -> None:
    axis = _section_axis(scale)
    radio_pad = _radio_nudge(scale)

    # Full-width radio sections: the visible radio LABEL starts on the same vertical
    # axis as the card title; helper copy begins on that exact axis too.
    for title in ("OUTPUT FORMAT", "SIZING", "GIF PRIORITY"):
        card = _card_for_heading(window, title)
        if card is None:
            continue
        for radio in card.findChildren(QRadioButton):
            radio.setProperty("mockupIndented", False)
            radio.setStyleSheet(f"padding-left: {radio_pad}px;")

    for title in ("OUTPUT FORMAT", "GIF PRIORITY"):
        card = _card_for_heading(window, title)
        if card is None:
            continue
        for label in card.findChildren(QLabel, "SecondaryText"):
            label.setProperty("mockupIndentedNote", False)
            label.setStyleSheet("padding-left: 0px;")
            label.setContentsMargins(axis, 0, 0, 0)

    # Paired Framing card: first radio label follows the same title axis.
    framing = _card_for_heading(window, "FRAMING")
    framing_row = _nested_layout(framing, 2)
    if framing_row is not None:
        framing_row.setContentsMargins(radio_pad, 0, 0, 0)
        framing_row.setSpacing(max(5, round(7 * scale)))

    # Input/slider rows without radio indicators start directly under the title text.
    for title, layout_index in (
        ("ASPECT RATIO", 2),
        ("CROP ZOOM", 1),
        ("OUTPUT FOLDER", 1),
    ):
        card = _card_for_heading(window, title)
        content = _nested_layout(card, layout_index)
        if content is not None:
            content.setContentsMargins(axis, 0, 0, 0)


def _apply_button_typography(window, scale: float) -> None:
    browse = window.findChild(QPushButton, "BrowseButton")
    if browse is not None:
        browse.setStyleSheet(f"font-size: {max(6.8, 7.55 * scale):.2f}pt;")
    add_files = window.findChild(QPushButton, "HeaderAction")
    if add_files is not None:
        add_files.setStyleSheet(f"font-size: {max(6.9, 7.85 * scale):.2f}pt;")


def _apply_footer_polish(window, scale: float) -> None:
    size = max(13, round(18 * scale))
    for button in window.findChildren(QToolButton, "FooterLink"):
        base = button.property("polymorphFooterBaseText")
        if not base:
            base = button.text().replace("\u00a0", " ").strip()
            button.setProperty("polymorphFooterBaseText", base)
        button.setText(f"\u00a0\u00a0{base}")
        button.setIconSize(QSize(size, size))
        button.setProperty("mockupFooter", True)
        if base == "Check for Updates":
            button.setIcon(QIcon(tinted_icon_pixmap("update.svg", size, QColor("#c8c2b9"))))


def _apply_playback_icon(window, scale: float) -> None:
    button = window.findChild(QToolButton, "PlaybackButton")
    if button is None:
        return
    playing = bool(button.property("polymorphPlaying"))
    asset = "pause.svg" if playing else "play.svg"
    size = max(12, round(15 * scale))
    button.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonIconOnly)
    button.setText("")
    button.setIcon(QIcon(tinted_icon_pixmap(asset, size, QColor("#e9d5ad"))))
    button.setIconSize(QSize(size, size))
    button.setAccessibleName("Pause preview" if playing else "Play preview")


def _apply_visual_polish(window) -> None:
    scale = float(window.property("brandScale") or 1.0)
    _apply_mockup_palette_and_body(window, scale)
    _apply_container_geometry(window, scale)
    _apply_heading_typography(window, scale)
    _apply_content_alignment(window, scale)
    _apply_button_typography(window, scale)
    _apply_footer_polish(window, scale)
    _apply_playback_icon(window, scale)
    for title, asset in _CARD_ICONS.items():
        _set_card_icon(window, title, asset, scale)


class _VisualPolishController(QObject):
    """Reapply optical-only adjustments after the responsive registry finishes."""

    def __init__(self, window) -> None:
        super().__init__(window)
        self.window = window
        self._pending = False
        window.installEventFilter(self)

    def eventFilter(self, watched, event) -> bool:
        if watched is self.window and event.type() in (QEvent.Type.Resize, QEvent.Type.Show):
            if not self._pending:
                self._pending = True
                QTimer.singleShot(1, self.refresh)
        return super().eventFilter(watched, event)

    def refresh(self) -> None:
        self._pending = False
        _apply_visual_polish(self.window)


def apply_mockup_fidelity(window) -> None:
    """Tighten branded composition to the approved mockup without changing state."""
    # Keep the smoke-compatible fidelity generation tag; record the newer optical
    # revision separately so this presentation-only pass does not disturb proven gates.
    window.setProperty("polymorphFidelity", "mockup-v2")
    window.setProperty("polymorphOpticalRevision", "mockup-v3-alignment-icons")

    file_card = window.findChild(QWidget, "FileCard")
    file_count = window.findChild(QLabel, "FileCount")
    if file_card is not None and file_card.layout() is not None and file_count is not None:
        header = file_card.layout().itemAt(0).layout()
        if header is not None:
            heading = None
            for index in range(header.count()):
                widget = header.itemAt(index).widget()
                if isinstance(widget, QLabel) and widget.objectName() == "CardHeading":
                    heading = widget
                    break
            if heading is not None:
                _remove_spacer_between(header, heading, file_count)
                file_count.setContentsMargins(4, 0, 0, 0)
            header.setSpacing(7)

    for button in window.findChildren(QToolButton, "QueueMenuButton"):
        button.setMinimumWidth(30)
        button.setAccessibleName("File actions")

    playback = window.findChild(QToolButton, "PlaybackButton")
    if playback is not None:
        playback.setProperty("polymorphPlaying", False)

        def sync_playback_state(_index, _total, _current_s, _total_s, playing: bool) -> None:
            playback.setProperty("polymorphPlaying", bool(playing))
            _apply_playback_icon(window, float(window.property("brandScale") or 1.0))

        window.preview.playbackChanged.connect(sync_playback_state)

    controller = _VisualPolishController(window)
    window._brand_visual_polish_controller = controller
    QTimer.singleShot(0, controller.refresh)
