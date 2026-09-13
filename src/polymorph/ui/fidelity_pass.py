from __future__ import annotations

from PySide6.QtCore import QSize
from PySide6.QtWidgets import QLabel, QLayout, QRadioButton, QToolButton, QWidget


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


def apply_mockup_fidelity(window) -> None:
    """Tighten branded composition to the approved mockup without changing state."""
    window.setProperty("polymorphFidelity", "mockup-v1")

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

    # Busy cards use one clean content column underneath their icon/title.
    for title in ("OUTPUT FORMAT", "SIZING", "ASPECT RATIO"):
        card = _card_for_heading(window, title)
        content = _nested_layout(card, 2)
        if content is not None:
            content.setContentsMargins(21, 0, 0, 0)

    # GIF priority is a vertical list rather than a nested grid. Give its radios
    # and helper copy the same left-column treatment without disturbing the header.
    priority = _card_for_heading(window, "GIF PRIORITY")
    if priority is not None:
        for radio in priority.findChildren(QRadioButton):
            radio.setProperty("mockupIndented", True)
        for label in priority.findChildren(QLabel, "SecondaryText"):
            label.setProperty("mockupIndentedNote", True)

    # Framing is the three-choice exception from the alignment rule, but make the
    # row occupy its card evenly so the bubbles do not bunch against the left edge.
    framing = _card_for_heading(window, "FRAMING")
    framing_row = _nested_layout(framing, 2)
    if framing_row is not None:
        framing_row.setContentsMargins(8, 0, 2, 0)
        framing_row.setSpacing(8)

    # Crop Zoom and Output Folder intentionally stay divider-free and use more of
    # the card width, matching the simpler mockup panels.
    for title in ("CROP ZOOM", "OUTPUT FOLDER"):
        card = _card_for_heading(window, title)
        content = _nested_layout(card, 1)
        if content is not None:
            content.setContentsMargins(21, 0, 0, 0)

    # File-row overflow affordance should read as an obvious menu, not punctuation.
    for button in window.findChildren(QToolButton, "QueueMenuButton"):
        button.setMinimumWidth(30)
        button.setAccessibleName("File actions")

    # Footer links need the airy, separated rhythm of the mockup.
    status_card = window.findChild(QWidget, "StatusCard")
    if status_card is not None and status_card.layout() is not None:
        top_row = status_card.layout().itemAt(0).layout()
        if top_row is not None:
            top_row.setSpacing(11)
    for button in window.findChildren(QToolButton, "FooterLink"):
        button.setIconSize(QSize(14, 14))
        button.setProperty("mockupFooter", True)
