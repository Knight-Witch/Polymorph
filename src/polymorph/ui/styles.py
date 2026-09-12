BASE_STYLESHEET = r"""
QMainWindow, QWidget {
    background: #17191d;
    color: #edf0f4;
    font-family: "Segoe UI", system-ui, sans-serif;
    font-size: 10pt;
}
QFrame#Card {
    background: #1e2126;
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 12px;
}
QLabel#Muted { color: #9aa2ad; }
QLabel#Title { font-size: 18pt; font-weight: 600; }
QLabel#Section {
    min-height: 18px;
    font-size: 10pt;
    font-weight: 600;
    color: #d9dee5;
}
QRadioButton {
    min-height: 20px;
    spacing: 7px;
}
QRadioButton::indicator {
    width: 13px;
    height: 13px;
    border-radius: 7px;
    border: 1px solid #707985;
    background: #111317;
}
QRadioButton::indicator:checked {
    border: 2px solid #eef1f5;
    background: #eef1f5;
}
QRadioButton::indicator:disabled {
    border-color: #4b525c;
    background: #202329;
}
QRadioButton::indicator:checked:disabled {
    border-color: #69717d;
    background: #69717d;
}
QPushButton, QToolButton, QComboBox, QSpinBox, QDoubleSpinBox {
    background: #262a31;
    border: 1px solid rgba(255,255,255,0.10);
    border-radius: 7px;
    padding: 7px 10px;
}
QComboBox, QSpinBox, QDoubleSpinBox {
    min-height: 20px;
}
QPushButton:hover, QToolButton:hover, QComboBox:hover, QSpinBox:hover, QDoubleSpinBox:hover {
    background: #2d323a;
    border-color: rgba(255,255,255,0.18);
}
QPushButton:pressed, QToolButton:pressed { background: #20242a; }
QPushButton:disabled, QToolButton:disabled,
QComboBox:disabled, QSpinBox:disabled, QDoubleSpinBox:disabled {
    color: #69717d;
    background: #202329;
    border-color: rgba(255,255,255,0.06);
}
QRadioButton:disabled { color: #69717d; }
QSlider::groove:horizontal {
    height: 4px;
    background: #111317;
    border-radius: 2px;
}
QSlider::sub-page:horizontal {
    background: #858e9a;
    border-radius: 2px;
}
QSlider::handle:horizontal {
    width: 14px;
    margin: -5px 0;
    border-radius: 7px;
    background: #e8ebef;
}
QSlider::groove:horizontal:disabled,
QSlider::sub-page:horizontal:disabled {
    background: #202329;
}
QSlider::handle:horizontal:disabled { background: #69717d; }
QPushButton#Primary {
    background: #e8ebef;
    color: #15171a;
    font-weight: 700;
    padding: 10px 18px;
}
QPushButton#Primary:hover { background: #ffffff; }
QToolButton#FooterIcon {
    background: transparent;
    border: 1px solid transparent;
    padding: 5px;
}
QToolButton#FooterIcon:hover {
    background: #24282e;
    border-color: rgba(255,255,255,0.10);
}
QLineEdit {
    background: #14161a;
    border: 1px solid rgba(255,255,255,0.10);
    border-radius: 7px;
    padding: 7px;
}
QListWidget {
    background: transparent;
    border: none;
    outline: none;
}
QListWidget::item {
    padding: 8px;
    border-radius: 7px;
}
QListWidget::item:selected { background: #2a2f37; }
QProgressBar {
    background: #111317;
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 5px;
    height: 8px;
    text-align: center;
}
QProgressBar::chunk { background: #d5dae1; border-radius: 4px; }
QScrollBar:vertical { width: 8px; background: transparent; }
QScrollBar::handle:vertical { background: #3a4049; border-radius: 4px; min-height: 24px; }
QToolTip {
    background: #0f1114;
    color: #f1f3f5;
    border: 1px solid #3a4048;
    padding: 6px 7px;
}
"""
