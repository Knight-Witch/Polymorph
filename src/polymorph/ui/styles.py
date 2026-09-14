from __future__ import annotations

from PySide6.QtWidgets import QApplication, QLabel

from .brand_widgets import ResponsiveBrandController, display_family, tracked_font
from .fidelity_pass import apply_mockup_fidelity


def _px(value: float, scale: float, minimum: int = 1) -> int:
    return max(minimum, round(value * scale))


def _qss_family(family: str) -> str:
    return family.replace("\\", "\\\\").replace('"', '\\"')


def _display_families() -> tuple[str, str]:
    regular = display_family()
    app = QApplication.instance()
    bold = regular
    if app is not None:
        bold = str(app.property("polymorphDisplayBoldFont") or regular).strip() or regular
    return _qss_family(regular), _qss_family(bold)


def build_brand_stylesheet(scale: float = 1.0) -> str:
    body = max(7.7, 9.5 * scale)
    small = max(6.9, 7.9 * scale)
    tiny = max(6.4, 7.2 * scale)
    title_size = max(16.5, 23.5 * scale)
    subtitle_size = max(7.2, 9.8 * scale)
    heading_size = max(8.0, 11.3 * scale)
    display_regular, display_bold = _display_families()
    control_pad_v = _px(3.5, scale, 2)
    control_pad_h = _px(7, scale, 4)
    radius = _px(4, scale, 2)
    radio = _px(12, scale, 9)
    radio_radius = max(5, radio // 2 + 1)
    slider_handle = _px(12, scale, 9)
    slider_margin = -_px(5, scale, 3)
    indent = _px(18, scale, 12)
    note_indent = _px(20, scale, 13)

    return f"""
QMainWindow {{
    background: #040506;
    color: #f2ece2;
}}
QWidget {{
    color: #f2ece2;
}}
QWidget#AppRoot,
QWidget#AppRoot QWidget {{
    font-family: "Inter", "Segoe UI", sans-serif;
    font-size: {body:.2f}pt;
}}
QWidget#AppRoot,
QWidget#Workspace,
QWidget#ControlRailContent {{
    background: #040506;
}}

/* Brand header: explicitly outrank the inherited body QSS. */
QLabel#BrandTitle {{
    color: #f5efe6;
    background: transparent;
    font-family: "{display_regular}";
    font-size: {title_size:.2f}pt;
    font-weight: 400;
}}
QLabel#BrandSubtitle {{
    color: #cdaa66;
    background: transparent;
    font-family: "{display_regular}";
    font-size: {subtitle_size:.2f}pt;
    font-weight: 400;
}}

/* Card/header text */
QLabel#CardHeading {{
    color: #d8b872;
    background: transparent;
    font-family: "{display_bold}";
    font-size: {heading_size:.2f}pt;
    font-weight: 700;
}}
QLabel#FileCount {{ color: #817b72; font-size: {small:.2f}pt; background: transparent; }}
QLabel#SecondaryText {{ color: #7e7971; font-size: {small:.2f}pt; background: transparent; }}
QLabel#PreviewMeta {{
    color: #958e84;
    font-size: {small:.2f}pt;
    background: transparent;
    padding-top: {_px(2, scale, 1)}px;
}}
QLabel#StatusLabel {{
    color: #eee6db;
    font-size: {max(7.9, 9.2*scale):.2f}pt;
    font-weight: 650;
    background: transparent;
}}
QLabel#StatusDetail {{ color: #807a72; font-size: {small:.2f}pt; background: transparent; }}
QLabel#FooterMeta {{ color: #6f6960; font-size: {tiny:.2f}pt; background: transparent; }}
QLabel#UnitLabel,
QLabel#TimesLabel,
QLabel#ZoomValue,
QLabel#PlaybackTime {{
    color: #958c7e;
    font-size: {small:.2f}pt;
    background: transparent;
}}
QLabel#PathText {{
    color: #d2c9bc;
    background: #070809;
    border: 1px solid #3b3024;
    border-radius: {radius}px;
    padding: {_px(4, scale, 3)}px {_px(7, scale, 4)}px;
    font-size: {max(7.3, 8.4*scale):.2f}pt;
}}
QFrame#CardSeparator,
QFrame#PreviewMetaSeparator,
QFrame#FooterSeparator {{
    color: #3b3022;
    background: #3b3022;
    border: none;
    max-height: 1px;
}}
QFrame#VerticalSeparator {{
    color: #3a332a;
    background: #3a332a;
    border: none;
    max-width: 1px;
}}

/* Queue */
QListWidget#QueueList {{
    background: transparent;
    border: none;
    outline: none;
    padding: 0px;
}}
QListWidget#QueueList::item {{
    padding: 0px;
    margin: 0px;
    border: none;
    background: transparent;
}}
QLabel#QueueThumb {{
    background: #050607;
    border: 1px solid #4c3d2b;
    border-radius: {_px(2, scale, 1)}px;
}}
QLabel#QueueFileName {{
    color: #eee6da;
    font-size: {max(7.7, 8.8*scale):.2f}pt;
    font-weight: 600;
    background: transparent;
}}
QLabel#QueueMeta {{ color: #79736b; font-size: {tiny:.2f}pt; background: transparent; }}
QToolButton#QueueMenuButton {{
    color: #aaa39a;
    background: transparent;
    border: none;
    font-size: {max(17.0, 23.0*scale):.2f}pt;
    font-weight: 700;
    padding: 0px;
}}
QToolButton#QueueMenuButton:hover {{ color: #efc97e; background: #1b1510; }}

/* Radios */
QRadioButton {{
    min-height: {_px(18, scale, 14)}px;
    spacing: {_px(6, scale, 4)}px;
    background: transparent;
    font-size: {max(7.5, 8.7*scale):.2f}pt;
}}
QRadioButton[mockupIndented="true"] {{ padding-left: {indent}px; }}
QLabel[mockupIndentedNote="true"] {{ padding-left: {note_indent}px; }}
QRadioButton::indicator {{
    width: {radio}px;
    height: {radio}px;
    border: 1px solid #71695f;
    border-radius: {radio_radius}px;
    background: #060708;
}}
QRadioButton::indicator:hover {{ border-color: #d2b16f; }}
QRadioButton::indicator:checked {{
    border-color: #d3b371;
    background: qradialgradient(
        cx: 0.5, cy: 0.5, radius: 0.5,
        fx: 0.5, fy: 0.5,
        stop: 0 #e0323b,
        stop: 0.35 #e0323b,
        stop: 0.36 #060708,
        stop: 1 #060708
    );
}}
QRadioButton::indicator:disabled {{ border-color: #46433e; background: #131415; }}
QRadioButton::indicator:checked:disabled {{
    border-color: #5d5449;
    background: qradialgradient(
        cx: 0.5, cy: 0.5, radius: 0.5,
        fx: 0.5, fy: 0.5,
        stop: 0 #774147,
        stop: 0.35 #774147,
        stop: 0.36 #131415,
        stop: 1 #131415
    );
}}
QRadioButton:disabled {{ color: #5d5953; }}

/* Inputs */
QPushButton,
QToolButton,
QComboBox,
QSpinBox,
QDoubleSpinBox {{
    color: #e9e1d5;
    background: #090a0b;
    border: 1px solid #3c3228;
    border-radius: {radius}px;
    padding: {control_pad_v}px {control_pad_h}px;
}}
QPushButton,
QToolButton {{ min-height: {_px(18, scale, 15)}px; }}
QComboBox,
QSpinBox,
QDoubleSpinBox {{ min-height: {_px(20, scale, 17)}px; }}
QPushButton:hover,
QToolButton:hover,
QComboBox:hover,
QSpinBox:hover,
QDoubleSpinBox:hover {{
    color: #fff5e7;
    background: #17130f;
    border-color: #876943;
}}
QPushButton:focus,
QToolButton:focus,
QComboBox:focus,
QSpinBox:focus,
QDoubleSpinBox:focus {{ border-color: #b89459; }}
QPushButton:pressed,
QToolButton:pressed {{ background: #260d10; border-color: #a82b33; }}
QPushButton:disabled,
QToolButton:disabled,
QComboBox:disabled,
QSpinBox:disabled,
QDoubleSpinBox:disabled {{
    color: #595650;
    background: #0e0f10;
    border-color: #262521;
}}
QAbstractSpinBox::up-button,
QAbstractSpinBox::down-button,
QAbstractSpinBox::up-arrow,
QAbstractSpinBox::down-arrow {{ width: 0px; height: 0px; border: none; }}

QPushButton#HeaderAction {{
    color: #edd7ac;
    background: qlineargradient(x1:0,y1:0,x2:0,y2:1, stop:0 #14120f, stop:1 #0b0b0a);
    border-color: #8d7047;
    font-weight: 600;
    padding-left: {_px(11, scale, 7)}px;
    padding-right: {_px(11, scale, 7)}px;
}}
QPushButton#HeaderAction:hover {{ color: #fff2dc; border-color: #d2aa68; background: #19140f; }}
QToolButton#HeaderTrash {{
    background: transparent;
    border: none;
    padding: {_px(2, scale, 1)}px;
}}
QToolButton#HeaderTrash:hover {{ background: #1a1512; border: 1px solid #6e5538; }}
QPushButton#ClearAllLink {{
    color: #8a847b;
    background: transparent;
    border: none;
    min-height: {_px(16, scale, 13)}px;
    padding: {_px(2, scale, 1)}px {_px(3, scale, 2)}px;
    font-size: {small:.2f}pt;
}}
QPushButton#ClearAllLink:hover {{ color: #e13b43; }}
QPushButton#BrowseButton {{
    color: #d8c39d;
    background: #11100e;
    border-color: #6f5838;
}}
QToolButton#InfoButton {{ padding-left: {_px(2, scale, 1)}px; padding-right: {_px(2, scale, 1)}px; }}

/* Playback */
QToolButton#PlaybackButton {{
    color: #e9d5ad;
    background: transparent;
    border: none;
    font-size: {max(9.0, 12.5*scale):.2f}pt;
    padding: 0px {_px(4, scale, 2)}px;
}}
QToolButton#PlaybackButton:hover {{ color: #fff2d8; background: transparent; }}

/* Combo popup */
QComboBox QAbstractItemView {{
    color: #ece4d8;
    background: #0c0d0e;
    border: 1px solid #57462f;
    selection-color: #ffffff;
    selection-background-color: #61151b;
    outline: none;
}}
QComboBox::drop-down {{ width: {_px(20, scale, 15)}px; border: none; }}

/* Sliders */
QSlider::groove:horizontal {{
    height: {_px(4, scale, 3)}px;
    background: #040506;
    border: 1px solid #2b261f;
    border-radius: 2px;
}}
QSlider::sub-page:horizontal {{
    background: qlineargradient(
        x1: 0, y1: 0, x2: 1, y2: 0,
        stop: 0 #94171f,
        stop: 0.70 #c62831,
        stop: 1 #c8a15d
    );
    border-radius: 2px;
}}
QSlider::handle:horizontal {{
    width: {slider_handle}px;
    margin: {slider_margin}px 0;
    background: qradialgradient(cx:0.42,cy:0.38,radius:0.72, stop:0 #efd08f, stop:0.55 #c9a663, stop:1 #6f5431);
    border: 1px solid #f1cf8b;
    border-radius: {max(5, slider_handle//2)}px;
}}
QSlider::handle:horizontal:hover {{ background: #e1c17d; border-color: #ffe2a4; }}
QSlider::groove:horizontal:disabled,
QSlider::sub-page:horizontal:disabled {{ background: #1c1d1e; border-color: #25241f; }}
QSlider::handle:horizontal:disabled {{ background: #4f4b45; border-color: #5d564d; }}
QSlider#CropZoomSlider::groove:horizontal {{
    height: {_px(5, scale, 3)}px;
    background: #030405;
    border: 1px solid #342a20;
}}
QSlider#CropZoomSlider::handle:horizontal {{
    width: {_px(14, scale, 10)}px;
    margin: {-_px(5, scale, 3)}px 0;
    background: qradialgradient(cx:0.4,cy:0.35,radius:0.75, stop:0 #f1d18f, stop:0.55 #c39b58, stop:1 #684d2c);
    border: 1px solid #f0cd87;
    border-radius: {_px(7, scale, 5)}px;
}}
QSlider#PlaybackTimeline::sub-page:horizontal {{
    background: qlineargradient(x1:0,y1:0,x2:1,y2:0, stop:0 #d4b47a, stop:1 #a77838);
}}

/* Inline progress */
QProgressBar#InlineProgress {{
    background: #050607;
    border: 1px solid #31291f;
    border-radius: 3px;
    height: {_px(5, scale, 3)}px;
}}
QProgressBar#InlineProgress::chunk {{
    background: qlineargradient(x1:0,y1:0,x2:1,y2:0, stop:0 #9d1821, stop:0.75 #cf2a34, stop:1 #c9a463);
    border-radius: 2px;
}}

/* Footer */
QToolButton#FooterLink {{
    color: #948d83;
    background: transparent;
    border: none;
    min-height: {_px(22, scale, 17)}px;
    padding: {_px(3, scale, 2)}px {_px(9, scale, 5)}px;
    font-size: {small:.2f}pt;
}}
QToolButton#FooterLink:hover {{ color: #eadfce; background: transparent; }}

/* Menus/tooltips */
QMenu {{ color: #e8e0d5; background: #0d0e0f; border: 1px solid #4d3e2c; padding: 4px; }}
QMenu::item {{ padding: {_px(5, scale, 3)}px {_px(22, scale, 14)}px {_px(5, scale, 3)}px {_px(8, scale, 5)}px; }}
QMenu::item:selected {{ background: #3f1015; }}
QToolTip {{ color: #f1e9dd; background: #0b0c0d; border: 1px solid #665137; padding: 5px 6px; }}
"""


# Compatibility sheet used by the base MainWindow before branded composition
# replaces it with the responsive scale-specific stylesheet.
BASE_STYLESHEET = build_brand_stylesheet(1.0)


def _apply_typography(window, scale: float) -> None:
    title = window.findChild(QLabel, "BrandTitle")
    if title is not None:
        # Photoshop reference: 120 pt with +350 tracking. Absolute Qt spacing
        # cannot map 1:1, but ~0.30 em at the design size reproduces the wide lockup.
        title.setFont(tracked_font(max(16.5, 23.5 * scale), max(4.2, 7.8 * scale)))
    subtitle = window.findChild(QLabel, "BrandSubtitle")
    if subtitle is not None:
        # Reference ratio: 50/120 title size, +300 tracking.
        subtitle.setFont(tracked_font(max(7.2, 9.8 * scale), max(1.8, 3.2 * scale)))
    for heading in window.findChildren(QLabel, "CardHeading"):
        # Reference card title is materially larger than ordinary body text and bold.
        heading.setFont(
            tracked_font(
                max(8.0, 11.3 * scale),
                max(0.7, 1.25 * scale),
                bold=True,
            )
        )


def apply_brand_skin(window) -> None:
    """Apply responsive concept-matched presentation without touching conversion logic."""
    window.resize(1260, 820)
    window.setMinimumSize(920, 640)
    apply_mockup_fidelity(window)

    def apply_scale(scale: float) -> None:
        window.setStyleSheet(build_brand_stylesheet(scale))
        registry = getattr(window, "_brand_scale_registry", None)
        if registry is not None:
            registry.apply(scale)
        _apply_typography(window, scale)
        for row in getattr(window, "_brand_queue_rows", lambda: [])():
            if hasattr(row, "apply_scale"):
                row.apply_scale(scale)
        button = getattr(window, "convert_btn", None)
        if button is not None and hasattr(button, "apply_scale"):
            button.apply_scale(scale)

    window.setProperty("polymorphSkin", "occult-gold-v5")
    window.setStyleSheet(build_brand_stylesheet(1.0))
    _apply_typography(window, 1.0)
    controller = ResponsiveBrandController(window, apply_scale)
    window._brand_responsive_controller = controller
    window.setProperty("brandScale", 1.0)
    apply_scale(1.0)
