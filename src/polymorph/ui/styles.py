from __future__ import annotations

from PySide6.QtWidgets import QFrame, QLabel, QPushButton


BASE_STYLESHEET = r"""
QMainWindow {
    background: #060708;
    color: #f3eee6;
}
QWidget {
    color: #f3eee6;
    font-family: "Inter", "Segoe UI", "Arial", sans-serif;
    font-size: 11pt;
}
QWidget#AppRoot,
QWidget#Workspace,
QWidget#ControlRailContent {
    background: #08090a;
}
QScrollArea#ControlRail {
    background: transparent;
    border: none;
}
QScrollArea#ControlRail > QWidget > QWidget {
    background: transparent;
}

/* Brand header */
QLabel#BrandTitle {
    color: #f7f0e5;
    font-family: "Cinzel", "Georgia", "Times New Roman", serif;
    font-size: 28pt;
    font-weight: 650;
}
QLabel#BrandSubtitle {
    color: #c9a86b;
    font-family: "Inter", "Segoe UI", sans-serif;
    font-size: 10.5pt;
    font-weight: 650;
}
QLabel#HeaderVersion {
    color: #756f66;
    font-size: 9.5pt;
    padding-bottom: 4px;
}
QLabel#FooterVersion {
    color: #6e6962;
    font-size: 9pt;
}

/* Panels */
QFrame#FileCard,
QFrame#PreviewCard,
QFrame#ControlCard,
QFrame#StatusCard {
    background: #0e1011;
    border: 1px solid #3f3528;
    border-radius: 10px;
}
QFrame#PreviewCard {
    background: #0a0b0c;
    border-color: #59472f;
}
QFrame#StatusCard {
    background: #0b0c0d;
    border-color: #302a22;
}
QLabel#CardHeading {
    color: #d4b474;
    font-family: "Cinzel", "Georgia", serif;
    font-size: 10.5pt;
    font-weight: 700;
    padding-bottom: 5px;
    border-bottom: 1px solid #473a29;
}
QLabel#SecondaryText {
    color: #8f8a82;
    font-size: 9.3pt;
}
QLabel#FileCount {
    color: #938d84;
    font-size: 9.5pt;
}
QLabel#PreviewMeta {
    color: #aaa39a;
    font-size: 9.5pt;
    padding-top: 3px;
}
QLabel#StatusLabel {
    color: #e8dfd3;
    font-size: 10.3pt;
    font-weight: 600;
}
QLabel#CastHint {
    color: #766f67;
    font-size: 8.9pt;
    padding: 1px 8px 0 8px;
}
QLabel#TimesLabel {
    color: #8b847a;
    padding-left: 1px;
    padding-right: 1px;
}
QLabel#PathText {
    color: #ddd5ca;
    background: #08090a;
    border: 1px solid #3a3228;
    border-radius: 7px;
    padding: 8px 9px;
}

/* Radios */
QRadioButton {
    min-height: 24px;
    spacing: 8px;
    background: transparent;
}
QRadioButton::indicator {
    width: 15px;
    height: 15px;
    border: 1px solid #736a5e;
    border-radius: 8px;
    background: #070809;
}
QRadioButton::indicator:hover {
    border-color: #d0ad6e;
}
QRadioButton::indicator:checked {
    border: 1px solid #d7b777;
    background: qradialgradient(
        cx: 0.5, cy: 0.5, radius: 0.5,
        fx: 0.5, fy: 0.5,
        stop: 0 #d12a33,
        stop: 0.36 #d12a33,
        stop: 0.37 #070809,
        stop: 1 #070809
    );
}
QRadioButton::indicator:disabled {
    border-color: #494640;
    background: #151617;
}
QRadioButton::indicator:checked:disabled {
    border-color: #5b5348;
    background: qradialgradient(
        cx: 0.5, cy: 0.5, radius: 0.5,
        fx: 0.5, fy: 0.5,
        stop: 0 #774249,
        stop: 0.36 #774249,
        stop: 0.37 #151617,
        stop: 1 #151617
    );
}
QRadioButton:disabled {
    color: #66625c;
}

/* Buttons and fields */
QPushButton,
QToolButton,
QComboBox,
QSpinBox,
QDoubleSpinBox {
    color: #ede5d9;
    background: #151617;
    border: 1px solid #443a2f;
    border-radius: 7px;
    padding: 7px 10px;
}
QPushButton,
QToolButton {
    min-height: 24px;
}
QComboBox,
QSpinBox,
QDoubleSpinBox {
    min-height: 25px;
    background: #090a0b;
}
QSpinBox,
QDoubleSpinBox {
    selection-background-color: #6e171d;
}
QPushButton:hover,
QToolButton:hover,
QComboBox:hover,
QSpinBox:hover,
QDoubleSpinBox:hover {
    color: #fff8ee;
    background: #1d1a17;
    border-color: #8a7048;
}
QPushButton:focus,
QToolButton:focus,
QComboBox:focus,
QSpinBox:focus,
QDoubleSpinBox:focus {
    border-color: #c9a869;
}
QPushButton:pressed,
QToolButton:pressed {
    background: #251014;
    border-color: #a82a32;
}
QPushButton:disabled,
QToolButton:disabled,
QComboBox:disabled,
QSpinBox:disabled,
QDoubleSpinBox:disabled {
    color: #65615b;
    background: #131415;
    border-color: #292824;
}

QPushButton#HeaderAction {
    color: #f0dbb0;
    background: #12100e;
    border-color: #907447;
    font-weight: 650;
    padding-left: 14px;
    padding-right: 14px;
}
QPushButton#HeaderAction:hover {
    color: #fff3dc;
    background: #1d1812;
    border-color: #d1af72;
}
QPushButton#QuietAction {
    color: #aaa39a;
    background: #0c0d0e;
    border-color: #35302a;
}
QPushButton#QuietAction:hover {
    color: #e9dfd0;
    border-color: #66533b;
}
QToolButton#InfoButton,
QToolButton#BrowseButton {
    min-width: 30px;
    max-width: 36px;
    padding-left: 5px;
    padding-right: 5px;
}

QPushButton#Primary {
    min-height: 58px;
    color: #fff5e8;
    background: qlineargradient(
        x1: 0, y1: 0, x2: 1, y2: 0,
        stop: 0 #2a080b,
        stop: 0.18 #4a0c11,
        stop: 0.5 #77161d,
        stop: 0.82 #4a0c11,
        stop: 1 #2a080b
    );
    border: 1px solid #c8a768;
    border-radius: 9px;
    font-family: "Cinzel", "Georgia", serif;
    font-size: 14pt;
    font-weight: 700;
    padding: 10px 18px;
}
QPushButton#Primary:hover {
    color: #ffffff;
    background: qlineargradient(
        x1: 0, y1: 0, x2: 1, y2: 0,
        stop: 0 #390b0f,
        stop: 0.18 #5e1117,
        stop: 0.5 #921f27,
        stop: 0.82 #5e1117,
        stop: 1 #390b0f
    );
    border-color: #efd296;
}
QPushButton#Primary:pressed {
    background: qlineargradient(
        x1: 0, y1: 0, x2: 1, y2: 0,
        stop: 0 #210609,
        stop: 0.5 #5d1016,
        stop: 1 #210609
    );
    border-color: #f7dda9;
}
QPushButton#Primary:disabled {
    color: #746b61;
    background: #201315;
    border-color: #493c2f;
}

/* Lists */
QListWidget {
    color: #ddd6cc;
    background: #08090a;
    border: 1px solid #2b2925;
    border-radius: 7px;
    outline: none;
    padding: 3px;
}
QListWidget::item {
    min-height: 26px;
    padding: 8px 10px;
    margin: 2px;
    border: 1px solid transparent;
    border-radius: 6px;
}
QListWidget::item:hover {
    background: #171515;
    border-color: #40372c;
}
QListWidget::item:selected {
    color: #fff8ef;
    background: #260c10;
    border-color: #92232b;
}

/* Combos */
QComboBox QAbstractItemView {
    color: #eee6db;
    background: #0d0e0f;
    border: 1px solid #5e4c35;
    selection-color: #ffffff;
    selection-background-color: #65151c;
    outline: none;
}
QComboBox::drop-down {
    width: 24px;
    border: none;
}

/* Sliders */
QSlider::groove:horizontal {
    height: 5px;
    background: #070809;
    border: 1px solid #302a22;
    border-radius: 3px;
}
QSlider::sub-page:horizontal {
    background: #a81e27;
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
    background: #f0d49d;
}
QSlider::groove:horizontal:disabled,
QSlider::sub-page:horizontal:disabled {
    background: #202122;
    border-color: #292824;
}
QSlider::handle:horizontal:disabled {
    background: #55514a;
    border-color: #625b51;
}

/* Progress */
QProgressBar {
    color: #d8d0c5;
    background: #070809;
    border: 1px solid #3a3024;
    border-radius: 4px;
    height: 7px;
    text-align: center;
}
QProgressBar::chunk {
    background: qlineargradient(
        x1: 0, y1: 0, x2: 1, y2: 0,
        stop: 0 #85151d,
        stop: 0.78 #c62832,
        stop: 1 #d1ae70
    );
    border-radius: 3px;
}

/* Footer */
QToolButton#FooterIcon {
    background: transparent;
    border: 1px solid transparent;
    padding: 5px;
}
QToolButton#FooterIcon:hover {
    background: #17130f;
    border-color: #6d5739;
}

/* Splitter, scrollbars, tooltips */
QSplitter#BrandMainSplitter::handle {
    background: #15120f;
}
QSplitter#BrandMainSplitter::handle:hover {
    background: #735b3a;
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
QScrollBar::add-line:vertical,
QScrollBar::sub-line:vertical,
QScrollBar::add-page:vertical,
QScrollBar::sub-page:vertical {
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
    """Apply the branded presentation after the functional window is built."""
    window.resize(1280, 880)
    window.setMinimumSize(1020, 720)

    window.convert_btn.setText("Cast Polymorph")
    window.convert_btn.setAccessibleName("Cast Polymorph")
    window.dimensions_label.setObjectName("PreviewMeta")
    window.status_label.setObjectName("StatusLabel")
    window.output_path.setObjectName("PathText")

    # Reuse the validated object names/controls while making the new layout
    # visually explicit for smoke tests and later animation work.
    window.setProperty("polymorphSkin", "occult-gold-v2")
    window.setStyleSheet(BASE_STYLESHEET)
