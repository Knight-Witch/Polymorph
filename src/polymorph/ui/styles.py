from __future__ import annotations


BASE_STYLESHEET = r"""
QMainWindow {
    background: #050607;
    color: #f2ece2;
}
QWidget {
    color: #f2ece2;
    font-family: "Inter", "Segoe UI", sans-serif;
    font-size: 10.2pt;
}
QWidget#AppRoot,
QWidget#Workspace,
QWidget#ControlRailContent {
    background: #070809;
}
QScrollArea#ControlRail,
QScrollArea#ControlRail > QWidget > QWidget {
    background: transparent;
    border: none;
}

/* Brand header */
QLabel#BrandTitle {
    color: #f3ede3;
}
QLabel#BrandSubtitle {
    color: #c9a766;
}
QLabel#HeaderVersion {
    color: #6f6a62;
    font-size: 8.5pt;
    padding-bottom: 3px;
}
QLabel#FooterVersion {
    color: #625e58;
    font-size: 8.2pt;
}

/* Main cards */
QFrame#FileCard,
QFrame#PreviewCard,
QFrame#ControlCard,
QFrame#StatusCard {
    background: qlineargradient(
        x1: 0, y1: 0, x2: 1, y2: 1,
        stop: 0 #0d0f10,
        stop: 0.55 #0b0c0d,
        stop: 1 #10100f
    );
    border: 1px solid #3b3125;
    border-radius: 8px;
}
QFrame#FileCard {
    border-color: #4a3a27;
}
QFrame#PreviewCard {
    background: qlineargradient(
        x1: 0, y1: 0, x2: 0, y2: 1,
        stop: 0 #090a0b,
        stop: 1 #0d0f10
    );
    border-color: #57442d;
}
QFrame#StatusCard {
    border-color: #342b20;
    background: #090a0b;
}
QLabel#CardHeading {
    color: #cfad6a;
    font-family: "Cinzel", "Georgia", serif;
    font-size: 8.6pt;
    font-weight: 700;
}
QFrame#CardSeparator {
    color: #3a3125;
    background: #3a3125;
    border: none;
    max-height: 1px;
}
QFrame#VerticalSeparator {
    color: #3a342c;
    background: #3a342c;
    border: none;
    max-width: 1px;
}
QLabel#SecondaryText {
    color: #817d77;
    font-size: 8.2pt;
}
QLabel#FileCount {
    color: #827d75;
    font-size: 8.2pt;
}
QLabel#PreviewMeta {
    color: #969087;
    font-size: 8.5pt;
    padding-top: 1px;
}
QLabel#StatusLabel {
    color: #ebe4da;
    font-size: 9.5pt;
    font-weight: 650;
}
QLabel#StatusDetail {
    color: #817b72;
    font-size: 8.1pt;
}
QLabel#UnitLabel,
QLabel#TimesLabel,
QLabel#ZoomValue {
    color: #928a7d;
    font-size: 8.5pt;
}
QLabel#PathText {
    color: #cfc8bd;
    background: #070809;
    border: 1px solid #342e26;
    border-radius: 5px;
    padding: 5px 7px;
    font-size: 8.7pt;
}

/* File queue */
QListWidget#QueueList {
    background: #070809;
    border: 1px solid #25231f;
    border-radius: 6px;
    outline: none;
    padding: 3px;
}
QListWidget#QueueList::item {
    padding: 0;
    margin: 0;
    border: none;
    background: transparent;
}
QFrame#QueueRow {
    background: qlineargradient(
        x1: 0, y1: 0, x2: 1, y2: 0,
        stop: 0 #0e1011,
        stop: 1 #11100f
    );
    border: 1px solid #2f2a24;
    border-radius: 5px;
}
QFrame#QueueRow:hover {
    border-color: #665136;
    background: #141312;
}
QFrame#QueueRow[selected="true"] {
    background: qlineargradient(
        x1: 0, y1: 0, x2: 1, y2: 0,
        stop: 0 #21090c,
        stop: 0.15 #180b0d,
        stop: 1 #11100f
    );
    border-color: #9d232b;
}
QLabel#QueueThumb {
    background: #050607;
    border: 1px solid #3b3329;
    border-radius: 3px;
    color: #756f67;
    font-size: 7.5pt;
}
QLabel#QueueFileName {
    color: #ece5db;
    font-size: 9.2pt;
    font-weight: 600;
}
QLabel#QueueMeta {
    color: #77726b;
    font-size: 7.8pt;
}
QToolButton#QueueMenuButton {
    color: #aaa39a;
    background: transparent;
    border: none;
    font-size: 15pt;
    min-width: 24px;
    max-width: 24px;
    padding: 0;
}
QToolButton#QueueMenuButton:hover {
    color: #f0d297;
    background: #1b1713;
}

/* Radios */
QRadioButton {
    min-height: 19px;
    spacing: 6px;
    background: transparent;
    font-size: 9pt;
}
QRadioButton::indicator {
    width: 12px;
    height: 12px;
    border: 1px solid #71695f;
    border-radius: 7px;
    background: #060708;
}
QRadioButton::indicator:hover {
    border-color: #d2b16f;
}
QRadioButton::indicator:checked {
    border-color: #d3b371;
    background: qradialgradient(
        cx: 0.5, cy: 0.5, radius: 0.5,
        fx: 0.5, fy: 0.5,
        stop: 0 #e0323b,
        stop: 0.36 #e0323b,
        stop: 0.37 #060708,
        stop: 1 #060708
    );
}
QRadioButton::indicator:disabled {
    border-color: #46433e;
    background: #131415;
}
QRadioButton::indicator:checked:disabled {
    border-color: #5d5449;
    background: qradialgradient(
        cx: 0.5, cy: 0.5, radius: 0.5,
        fx: 0.5, fy: 0.5,
        stop: 0 #774147,
        stop: 0.36 #774147,
        stop: 0.37 #131415,
        stop: 1 #131415
    );
}
QRadioButton:disabled {
    color: #5e5a54;
}

/* Inputs and buttons */
QPushButton,
QToolButton,
QComboBox,
QSpinBox,
QDoubleSpinBox {
    color: #e9e1d5;
    background: #0b0c0d;
    border: 1px solid #3b3329;
    border-radius: 5px;
    padding: 4px 7px;
}
QPushButton,
QToolButton {
    min-height: 20px;
}
QComboBox,
QSpinBox,
QDoubleSpinBox {
    min-height: 21px;
}
QPushButton:hover,
QToolButton:hover,
QComboBox:hover,
QSpinBox:hover,
QDoubleSpinBox:hover {
    color: #fff5e7;
    background: #171411;
    border-color: #7e633f;
}
QPushButton:focus,
QToolButton:focus,
QComboBox:focus,
QSpinBox:focus,
QDoubleSpinBox:focus {
    border-color: #b89459;
}
QPushButton:pressed,
QToolButton:pressed {
    background: #240d10;
    border-color: #a82b33;
}
QPushButton:disabled,
QToolButton:disabled,
QComboBox:disabled,
QSpinBox:disabled,
QDoubleSpinBox:disabled {
    color: #595650;
    background: #111213;
    border-color: #262521;
}

QAbstractSpinBox::up-button,
QAbstractSpinBox::down-button {
    width: 0px;
    height: 0px;
    border: none;
}
QAbstractSpinBox::up-arrow,
QAbstractSpinBox::down-arrow {
    width: 0px;
    height: 0px;
}

QPushButton#HeaderAction {
    color: #e9d3aa;
    background: #11100e;
    border-color: #856a42;
    font-weight: 600;
    padding-left: 10px;
    padding-right: 10px;
}
QPushButton#HeaderAction:hover {
    color: #fff2dc;
    border-color: #d0aa68;
}
QToolButton#HeaderTrash {
    background: transparent;
    border: none;
    min-width: 24px;
    max-width: 24px;
    padding: 2px;
}
QToolButton#HeaderTrash:hover {
    background: #1a1512;
    border: 1px solid #6e5538;
}
QPushButton#ClearAllLink {
    color: #8a847b;
    background: transparent;
    border: none;
    min-height: 18px;
    padding: 2px 3px;
    font-size: 8.5pt;
}
QPushButton#ClearAllLink:hover {
    color: #e13b43;
}
QPushButton#BrowseButton {
    color: #d8c39d;
    background: #11100e;
    border-color: #6f5838;
    min-width: 62px;
}
QPushButton#TinyAction,
QPushButton#FitColorButton {
    color: #a9a198;
    background: #0b0c0d;
    border-color: #3a3229;
    padding: 2px 5px;
}
QPushButton#TinyAction:hover,
QPushButton#FitColorButton:hover {
    color: #f0d49a;
    border-color: #806744;
}
QToolButton#InfoButton {
    min-width: 25px;
    max-width: 25px;
    padding-left: 2px;
    padding-right: 2px;
}

/* Cast button */
QPushButton#Primary {
    min-height: 62px;
    background: qlineargradient(
        x1: 0, y1: 0, x2: 1, y2: 0,
        stop: 0 #1d080a,
        stop: 0.2 #3c0b10,
        stop: 0.5 #74151c,
        stop: 0.8 #3c0b10,
        stop: 1 #1d080a
    );
    border: 1px solid #b88f4d;
    border-radius: 8px;
    padding: 0;
}
QPushButton#Primary:hover {
    background: qlineargradient(
        x1: 0, y1: 0, x2: 1, y2: 0,
        stop: 0 #26090c,
        stop: 0.2 #501018,
        stop: 0.5 #8d2028,
        stop: 0.8 #501018,
        stop: 1 #26090c
    );
    border-color: #e1bd79;
}
QPushButton#Primary:pressed {
    background: #470d12;
    border-color: #f0cf8c;
}
QPushButton#Primary:disabled {
    background: #1a1112;
    border-color: #41372c;
}
QLabel#CastTitle {
    color: #f1ddba;
    font-family: "Cinzel", "Georgia", serif;
    font-size: 11pt;
    font-weight: 700;
}
QLabel#CastSubtitle {
    color: #9f8d71;
    font-family: "Inter", sans-serif;
    font-size: 7pt;
    font-weight: 600;
}
QLabel#CastDash {
    color: #8f6f42;
    font-size: 12pt;
}

/* Combo popup */
QComboBox QAbstractItemView {
    color: #ece4d8;
    background: #0c0d0e;
    border: 1px solid #57462f;
    selection-color: #ffffff;
    selection-background-color: #61151b;
    outline: none;
}
QComboBox::drop-down {
    width: 20px;
    border: none;
}

/* Slider */
QSlider::groove:horizontal {
    height: 4px;
    background: #050607;
    border: 1px solid #28241f;
    border-radius: 2px;
}
QSlider::sub-page:horizontal {
    background: qlineargradient(
        x1: 0, y1: 0, x2: 1, y2: 0,
        stop: 0 #991820,
        stop: 1 #d12a33
    );
    border-radius: 2px;
}
QSlider::handle:horizontal {
    width: 12px;
    margin: -5px 0;
    background: #c9a663;
    border: 1px solid #ebca87;
    border-radius: 7px;
}
QSlider::handle:horizontal:hover {
    background: #e1c17d;
}
QSlider::groove:horizontal:disabled,
QSlider::sub-page:horizontal:disabled {
    background: #1c1d1e;
    border-color: #25241f;
}
QSlider::handle:horizontal:disabled {
    background: #4f4b45;
    border-color: #5d564d;
}

/* Progress */
QProgressBar#InlineProgress {
    background: #050607;
    border: 1px solid #31291f;
    border-radius: 3px;
    height: 5px;
}
QProgressBar#InlineProgress::chunk {
    background: qlineargradient(
        x1: 0, y1: 0, x2: 1, y2: 0,
        stop: 0 #9d1821,
        stop: 0.75 #cf2a34,
        stop: 1 #c9a463
    );
    border-radius: 2px;
}

/* Footer */
QToolButton#FooterLink {
    color: #8e8982;
    background: transparent;
    border: none;
    min-height: 22px;
    padding: 2px 5px;
    font-size: 8.2pt;
}
QToolButton#FooterLink:hover {
    color: #e3d7c6;
    background: transparent;
}

/* Splitter / scrollbars / menus / tooltips */
QSplitter#BrandMainSplitter::handle {
    background: #16120f;
}
QSplitter#BrandMainSplitter::handle:hover {
    background: #6d5638;
}
QScrollBar:vertical {
    width: 7px;
    background: transparent;
}
QScrollBar::handle:vertical {
    background: #38342e;
    border-radius: 3px;
    min-height: 24px;
}
QScrollBar::handle:vertical:hover {
    background: #66543c;
}
QScrollBar::add-line:vertical,
QScrollBar::sub-line:vertical,
QScrollBar::add-page:vertical,
QScrollBar::sub-page:vertical {
    background: transparent;
    border: none;
}
QMenu {
    color: #e8e0d5;
    background: #0d0e0f;
    border: 1px solid #4d3e2c;
    padding: 4px;
}
QMenu::item {
    padding: 5px 22px 5px 8px;
}
QMenu::item:selected {
    background: #3f1015;
}
QToolTip {
    color: #f1e9dd;
    background: #0b0c0d;
    border: 1px solid #665137;
    padding: 5px 6px;
}
"""


def apply_brand_skin(window) -> None:
    """Apply the compact concept-matched Polymorph presentation."""
    window.resize(1260, 820)
    window.setMinimumSize(1080, 700)

    window.convert_btn.setAccessibleName("Cast Polymorph")
    window.dimensions_label.setObjectName("PreviewMeta")
    window.status_label.setObjectName("StatusLabel")
    window.output_path.setObjectName("PathText")

    window.setProperty("polymorphSkin", "occult-gold-v3")
    window.setStyleSheet(BASE_STYLESHEET)
