from __future__ import annotations

from PySide6.QtWidgets import QLabel, QPushButton, QSplitter


BASE_STYLESHEET = r"""
QMainWindow {
    background: #070809;
    color: #f2ece3;
}
QWidget {
    color: #f2ece3;
    font-family: "Segoe UI", "Arial", sans-serif;
    font-size: 11pt;
}
QWidget#AppRoot {
    background: #090a0b;
}
QFrame#Card {
    background: #101112;
    border: 1px solid #3d3428;
    border-radius: 10px;
}
QLabel#Muted {
    color: #9b968c;
}
QLabel#Title {
    color: #f7f1e7;
    font-family: "Georgia", "Times New Roman", serif;
    font-size: 24pt;
    font-weight: 600;
}
QLabel#Subtitle {
    color: #c9a869;
    font-size: 10pt;
    font-weight: 700;
}
QLabel#FooterVersion {
    color: #766f65;
    font-size: 9pt;
}
QLabel#PreviewMeta {
    color: #a7a197;
    font-size: 9pt;
    padding-top: 3px;
}
QLabel#StatusLabel {
    color: #e9e0d3;
    font-size: 10pt;
    font-weight: 600;
}
QLabel#PathText {
    color: #d5cec2;
    background: #090a0b;
    border: 1px solid #393126;
    border-radius: 6px;
    padding: 7px 8px;
}
QLabel#Section {
    min-height: 22px;
    color: #d1af72;
    font-size: 10pt;
    font-weight: 700;
    border-bottom: 1px solid #413625;
    padding-bottom: 5px;
}
QRadioButton {
    min-height: 23px;
    spacing: 8px;
    background: transparent;
}
QRadioButton::indicator {
    width: 15px;
    height: 15px;
    border: 1px solid #71695f;
    border-radius: 8px;
    background: #08090a;
}
QRadioButton::indicator:hover {
    border-color: #c9a869;
}
QRadioButton::indicator:checked {
    border: 1px solid #d3b477;
    background: qradialgradient(
        cx: 0.5, cy: 0.5, radius: 0.5,
        fx: 0.5, fy: 0.5,
        stop: 0 #d42b34,
        stop: 0.38 #d42b34,
        stop: 0.39 #08090a,
        stop: 1 #08090a
    );
}
QRadioButton::indicator:disabled {
    border-color: #4a4742;
    background: #151617;
}
QRadioButton::indicator:checked:disabled {
    border-color: #5d554a;
    background: qradialgradient(
        cx: 0.5, cy: 0.5, radius: 0.5,
        fx: 0.5, fy: 0.5,
        stop: 0 #7b4448,
        stop: 0.38 #7b4448,
        stop: 0.39 #151617,
        stop: 1 #151617
    );
}
QRadioButton:disabled {
    color: #68645e;
}
QPushButton, QToolButton, QComboBox, QSpinBox, QDoubleSpinBox {
    color: #e9e2d8;
    background: #151617;
    border: 1px solid #443b30;
    border-radius: 7px;
    padding: 7px 10px;
}
QPushButton, QToolButton {
    min-height: 22px;
}
QComboBox, QSpinBox, QDoubleSpinBox {
    min-height: 24px;
    background: #0b0c0d;
}
QPushButton:hover, QToolButton:hover, QComboBox:hover, QSpinBox:hover, QDoubleSpinBox:hover {
    color: #fff7ec;
    background: #1d1a18;
    border-color: #806a47;
}
QPushButton:focus, QToolButton:focus, QComboBox:focus, QSpinBox:focus, QDoubleSpinBox:focus {
    border-color: #c9a869;
}
QPushButton:pressed, QToolButton:pressed {
    background: #241013;
    border-color: #a92831;
}
QPushButton:disabled, QToolButton:disabled,
QComboBox:disabled, QSpinBox:disabled, QDoubleSpinBox:disabled {
    color: #66625d;
    background: #141516;
    border-color: #2b2926;
}
QPushButton#HeaderAction {
    color: #e9d3aa;
    background: #11100f;
    border: 1px solid #8a7048;
    font-weight: 600;
    padding-left: 14px;
    padding-right: 14px;
}
QPushButton#HeaderAction:hover {
    color: #fff4de;
    background: #1a1612;
    border-color: #d1af72;
}
QPushButton#Primary {
    min-height: 52px;
    color: #fff3e5;
    background: qlineargradient(
        x1: 0, y1: 0, x2: 1, y2: 0,
        stop: 0 #370a0d,
        stop: 0.5 #72141b,
        stop: 1 #370a0d
    );
    border: 1px solid #c9a869;
    border-radius: 9px;
    font-family: "Georgia", "Times New Roman", serif;
    font-size: 13pt;
    font-weight: 700;
    padding: 10px 18px;
}
QPushButton#Primary:hover {
    color: #ffffff;
    background: qlineargradient(
        x1: 0, y1: 0, x2: 1, y2: 0,
        stop: 0 #481015,
        stop: 0.5 #8b1b23,
        stop: 1 #481015
    );
    border-color: #efd096;
}
QPushButton#Primary:pressed {
    background: qlineargradient(
        x1: 0, y1: 0, x2: 1, y2: 0,
        stop: 0 #25070a,
        stop: 0.5 #5e1016,
        stop: 1 #25070a
    );
    border-color: #f7dca7;
}
QPushButton#Primary:disabled {
    color: #746b61;
    background: #211416;
    border-color: #493c2f;
}
QToolButton#FooterIcon {
    background: transparent;
    border: 1px solid transparent;
    padding: 5px;
}
QToolButton#FooterIcon:hover {
    background: #17130f;
    border-color: #6e5739;
}
QLineEdit {
    color: #eee6db;
    background: #090a0b;
    border: 1px solid #3b342b;
    border-radius: 7px;
    padding: 7px;
}
QLineEdit:hover, QLineEdit:focus {
    border-color: #9c7d50;
}
QListWidget {
    color: #ddd7cd;
    background: #090a0b;
    border: 1px solid #292722;
    border-radius: 7px;
    outline: none;
    padding: 3px;
}
QListWidget::item {
    padding: 9px;
    margin: 2px;
    border: 1px solid transparent;
    border-radius: 6px;
}
QListWidget::item:hover {
    background: #171616;
    border-color: #40372c;
}
QListWidget::item:selected {
    color: #fff7ef;
    background: #260c10;
    border: 1px solid #8b2028;
}
QComboBox QAbstractItemView {
    color: #eee6db;
    background: #0d0e0f;
    border: 1px solid #5d4d36;
    selection-color: #ffffff;
    selection-background-color: #5f141a;
    outline: none;
}
QComboBox::drop-down {
    width: 24px;
    border: none;
}
QSlider::groove:horizontal {
    height: 5px;
    background: #08090a;
    border: 1px solid #2d2923;
    border-radius: 3px;
}
QSlider::sub-page:horizontal {
    background: #a61e27;
    border-radius: 3px;
}
QSlider::handle:horizontal {
    width: 15px;
    margin: -6px 0;
    background: #d2b174;
    border: 1px solid #f0d196;
    border-radius: 8px;
}
QSlider::handle:horizontal:hover {
    background: #efd49f;
}
QSlider::groove:horizontal:disabled,
QSlider::sub-page:horizontal:disabled {
    background: #202122;
    border-color: #2a2927;
}
QSlider::handle:horizontal:disabled {
    background: #55514a;
    border-color: #625b51;
}
QProgressBar {
    color: #d9d0c4;
    background: #070809;
    border: 1px solid #3b3023;
    border-radius: 5px;
    height: 9px;
    text-align: center;
}
QProgressBar::chunk {
    background: qlineargradient(
        x1: 0, y1: 0, x2: 1, y2: 0,
        stop: 0 #8e171f,
        stop: 0.75 #c42731,
        stop: 1 #d0ad70
    );
    border-radius: 4px;
}
QSplitter::handle {
    background: #16130f;
}
QSplitter::handle:hover {
    background: #6f5738;
}
QScrollBar:vertical {
    width: 9px;
    background: transparent;
}
QScrollBar::handle:vertical {
    background: #403a32;
    border-radius: 4px;
    min-height: 26px;
}
QScrollBar::handle:vertical:hover {
    background: #69573f;
}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical,
QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
    background: transparent;
    border: none;
}
QToolTip {
    color: #f5ede2;
    background: #0c0d0e;
    border: 1px solid #6b563a;
    padding: 6px 7px;
}
"""


def apply_brand_skin(window) -> None:
    """Apply the first presentation-only Polymorph skin after the functional UI is built."""
    window.resize(1180, 840)
    window.setMinimumSize(940, 700)

    root = window.centralWidget()
    if root is not None:
        root.setObjectName("AppRoot")

    section_names = {
        "output": "OUTPUT FORMAT",
        "sizing": "SIZING",
        "gif priority": "GIF PRIORITY",
        "framing": "FRAMING",
        "output folder": "OUTPUT FOLDER",
    }
    for label in window.findChildren(QLabel):
        text = label.text().strip()
        lowered = text.lower()
        if text in {"Media Transmutation Utility", "MEDIA CONVERSION MAGIC"}:
            label.setText("MEDIA CONVERSION MAGIC")
            label.setObjectName("Subtitle")
        elif label.objectName() == "Section":
            label.setText(section_names.get(lowered, text.upper()))
        elif text == "Files":
            label.setText("FILES")
            label.setObjectName("Section")
        elif text.startswith("Polymorph v"):
            label.setObjectName("FooterVersion")

    for button in window.findChildren(QPushButton):
        if button.text() in {"Add Files", "+ Add Files"}:
            button.setText("+ Add Files")
            button.setObjectName("HeaderAction")

    window.convert_btn.setText("Cast Polymorph")
    window.convert_btn.setAccessibleName("Cast Polymorph")
    window.dimensions_label.setObjectName("PreviewMeta")
    window.status_label.setObjectName("StatusLabel")
    window.output_path.setObjectName("PathText")

    splitter = window.findChild(QSplitter)
    if splitter is not None:
        splitter.setHandleWidth(5)
        splitter.setSizes([220, 620, 330])

    window.file_list.setSpacing(2)
    window.setProperty("polymorphSkin", "occult-gold-v1")

    # Object names above are used by the stylesheet, so re-apply after naming.
    window.setStyleSheet(BASE_STYLESHEET)
