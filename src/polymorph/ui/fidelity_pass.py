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


def _set_card_icon(window, title: str, asset: str, scale: float) -> None:
    card = _card_for_heading(window, title)
    header = _nested_layout(card, 0)
    if header is None or header.count() == 0:
        return
    icon = header.itemAt(0).widget()
    if not isinstance(icon, QLabel):
        return
    if isinstance(icon, TintIconLabel):
        icon._asset = asset
        icon.refresh(scale)
        return
    size = max(10, round(15 * scale))
    icon.setText("")
    icon.setFixedSize(size, size)
    icon.setPixmap(tinted_icon_pixmap(asset, size))


def _apply_heading_typography(window, scale: float) -> None:
    app = QApplication.instance()
    family = "Polymorph"
    if app is not None:
        family = str(app.property("polymorphDisplayBoldFont") or family).strip() or family
    point_size = max(7.0, 9.2 * scale)
    spacing = max(0.5, 0.9 * scale)
    for heading in window.findChildren(QLabel, "CardHeading"):
        heading.setStyleSheet(
            f'font-family: "{_qss_family(family)}"; '
            f"font-size: {point_size:.2f}pt; font-weight: 700; "
            "color: #d8b872; background: transparent;"
        )
        heading.setFont(
            tracked_font(
                point_size,
                spacing,
                bold=True,
                family=family,
            )
        )


def _apply_content_alignment(window, scale: float) -> None:
    radio_indent = max(12, round(21 * scale))
    note_indent = max(25, round(39 * scale))

    for title in ("OUTPUT FORMAT", "SIZING", "GIF PRIORITY"):
        card = _card_for_heading(window, title)
        if card is None:
            continue
        for radio in card.findChildren(QRadioButton):
            radio.setProperty("mockupIndented", True)
            radio.setStyleSheet(f"padding-left: {radio_indent}px;")

    for title in ("OUTPUT FORMAT", "GIF PRIORITY"):
        card = _card_for_heading(window, title)
        if card is None:
            continue
        for label in card.findChildren(QLabel, "SecondaryText"):
            label.setContentsMargins(0, 0, 0, 0)
            label.setProperty("mockupIndentedNote", True)
            label.setStyleSheet(f"padding-left: {note_indent}px;")


def _apply_button_typography(window, scale: float) -> None:
    browse = window.findChild(QPushButton, "BrowseButton")
    if browse is not None:
        browse.setStyleSheet(f"font-size: {max(7.0, 8.0 * scale):.2f}pt;")
    add_files = window.findChild(QPushButton, "HeaderAction")
    if add_files is not None:
        add_files.setStyleSheet(f"font-size: {max(7.2, 8.4 * scale):.2f}pt;")


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
    _apply_heading_typography(window, scale)
    _apply_content_alignment(window, scale)
    _apply_button_typography(window, scale)
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
    window.setProperty("polymorphFidelity", "mockup-v2")

    # FILES: title + count belong together; actions belong together at the right.
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

    # Framing is the three-choice exception from the aligned content-column rule.
    framing = _card_for_heading(window, "FRAMING")
    framing_row = _nested_layout(framing, 2)
    if framing_row is not None:
        framing_row.setContentsMargins(8, 0, 2, 0)
        framing_row.setSpacing(8)

    # File-row overflow affordance should read as an obvious menu, not punctuation.
    for button in window.findChildren(QToolButton, "QueueMenuButton"):
        button.setMinimumWidth(30)
        button.setAccessibleName("File actions")

    # Footer links keep the airy, separated rhythm of the mockup.
    status_card = window.findChild(QWidget, "StatusCard")
    if status_card is not None and status_card.layout() is not None:
        top_row = status_card.layout().itemAt(0).layout()
        if top_row is not None:
            top_row.setSpacing(11)
    for button in window.findChildren(QToolButton, "FooterLink"):
        button.setIconSize(QSize(14, 14))
        button.setProperty("mockupFooter", True)

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
