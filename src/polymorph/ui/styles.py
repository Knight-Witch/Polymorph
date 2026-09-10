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
QLabel#Section { font-size: 10pt; font-weight: 600; color: #d9dee5; }
QPushButton, QToolButton, QComboBox, QSpinBox, QDoubleSpinBox {
    background: #262a31;
    border: 1px solid rgba(255,255,255,0.10);
    border-radius: 7px;
    padding: 7px 10px;
}
QPushButton:hover, QToolButton:hover, QComboBox:hover, QSpinBox:hover, QDoubleSpinBox:hover {
    background: #2d323a;
    border-color: rgba(255,255,255,0.18);
}
QPushButton:pressed, QToolButton:pressed { background: #20242a; }
QPushButton:disabled, QToolButton:disabled { color: #666d77; background: #202329; }
QPushButton#Primary {
    background: #e8ebef;
    color: #15171a;
    font-weight: 700;
    padding: 10px 18px;
}
QPushButton#Primary:hover { background: #ffffff; }
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
    padding: 5px;
}
"""
