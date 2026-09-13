from __future__ import annotations

from PySide6.QtWidgets import QLabel

from .brand_widgets import ResponsiveBrandController, tracked_font


def _px(value: float, scale: float, minimum: int = 1) -> int:
    return max(minimum, round(value * scale))


def build_brand_stylesheet(scale: float = 1.0) -> str:
    body = max(7.8, 9.8 * scale)
    small = max(7.0, 8.2 * scale)
    tiny = max(6.5, 7.5 * scale)
    control_pad_v = _px(4, scale, 2)
    control_pad_h = _px(7, scale, 4)
    radius = _px(5, scale, 3)
    radio = _px(12, scale, 9)
    radio_radius = max(5, radio // 2 + 1)
    slider_handle = _px(12, scale, 9)
    slider_margin = -_px(5, scale, 3)

    return f"""
QMainWindow {{
    background: #050607;
    color: #f2ece2;
}}
QWidget {{
    color: #f2ece2;
    font-family: "Inter", "Segoe UI", sans-serif;
    font-size: {body:.2f}pt;
}}
QWidget#AppRoot,
QWidget#Workspace,
QWidget#ControlRailContent {{
    background: #050607;
}}

/* Brand header */
QLabel#BrandTitle {{ color: #f3ede3; background: transparent; }}
QLabel#BrandSubtitle {{ color: #c8a667; background: transparent; }}

/* Card/header text */
QLabel#CardHeading {{ color: #d1ad69; background: transparent; }}
QLabel#FileCount {{ color: #7f7a72; font-size: {small:.2f}pt; background: transparent; }}
QLabel#SecondaryText {{ color: #807b74; font-size: {small:.2f}pt; background: transparent; }}
QLabel#PreviewMeta {{
    color: #948e85;
    font-size: {small:.2f}pt;
    background: transparent;
    padding-top: {_px(2, scale, 1)}px;
}}
QLabel#StatusLabel {{
    color: #eee6db;
    font-size: {max(8.0, 9.4*scale):.2f}pt;
    font-weight: 650;
    background: transparent;
}}
QLabel#StatusDetail {{ color: #807a72; font-size: {small:.2f}pt; background: transparent; }}
QLabel#FooterMeta {{ color: #6f6960; font-size: {tiny:.2f}pt; background: transparent; }}
QLabel#UnitLabel,
QLabel#TimesLabel,
QLabel#ZoomValue,
QLabel#PlaybackTime {{
    color: #938a7d;
    font-size: {small:.2f}pt;
    background: transparent;
}}
QLabel#PathText {{
    color: #d0c8bc;
    background: #070809;
    border: 1px solid #352e26;
    border-radius: {radius}px;
    padding: {_px(5, scale, 3)}px {_px(7, scale, 4)}px;
    font-size: {max(7.4, 8.6*scale):.2f}pt;
}}
QFrame#CardSeparator,
QFrame#PreviewMetaSeparator,
QFrame#FooterSeparator {{
    color: #3a3125;
    background: #3a3125;
    border: none;
    max-height: 1px;
}}
QFrame#VerticalSeparator {{
    color: #3b342b;
    background: #3b342b;
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
    border: 1px solid #463a2b;
    border-radius: {_px(2, scale, 1)}px;
}}
QLabel#QueueFileName {{
    color: #eee6da;
    font-size: {max(7.8, 9.0*scale):.2f}pt;
    font-weight: 600;
    background: transparent;
}}
QLabel#QueueMeta {{ color: #79736b; font-size: {tiny:.2f}pt; background: transparent; }}
QToolButton#QueueMenuButton {{
    color: #aaa39a;
    background: transparent;
    border: none;
    font-size: {max(14.0, 19.0*scale):.2f}pt;
    padding: 0px;
}}
QToolButton#QueueMenuButton:hover {{ color: #f0d297; background: #1a1511; }}

/* Radios */
QRadioButton {{
    min-height: {_px(18, scale, 14)}px;
    spacing: {_px(6, scale, 4)}px;
    background: transparent;
    font-size: {max(7.6, 8.9*scale):.2f}pt;
}}
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
    background: #0a0b0c;
    border: 1px solid #3b3329;
    border-radius: {radius}px;
    padding: {control_pad_v}px {control_pad_h}px;
}}
QPushButton,
QToolButton {{ min-height: {_px(19, scale, 16)}px; }}
QComboBox,
QSpinBox,
QDoubleSpinBox {{ min-height: {_px(20, scale, 17)}px; }}
QPushButton:hover,
QToolButton:hover,
QComboBox:hover,
QSpinBox:hover,
QDoubleSpinBox:hover {{
    color: #fff5e7;
    background: #171411;
    border-color: #806542;
}}
QPushButton:focus,
QToolButton:focus,
QComboBox:focus,
QSpinBox:focus,
QDoubleSpinBox:focus {{ border-color: #b89459; }}
QPushButton:pressed,
QToolButton:pressed {{ background: #240d10; border-color: #a82b33; }}
QPushButton:disabled,
QToolButton:disabled,
QComboBox:disabled,
QSpinBox:disabled,
QDoubleSpinBox:disabled {{
    color: #595650;
    background: #101112;
    border-color: #262521;
}}
QAbstractSpinBox::up-button,
QAbstractSpinBox::down-button,
QAbstractSpinBox::up-arrow,
QAbstractSpinBox::down-arrow {{ width: 0px; height: 0px; border: none; }}

QPushButton#HeaderAction {{
    color: #ecd6ac;
    background: #11100e;
    border-color: #886c43;
    font-weight: 600;
    padding-left: {_px(11, scale, 7)}px;
    padding-right: {_px(11, scale, 7)}px;
}}
QPushButton#HeaderAction:hover {{ color: #fff2dc; border-color: #d2aa68; }}
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
    background: #050607;
    border: 1px solid #28241f;
    border-radius: 2px;
}}
QSlider::sub-page:horizontal {{
    background: qlineargradient(
        x1: 0, y1: 0, x2: 1, y2: 0,
        stop: 0 #9b1820,
        stop: 0.72 #c72630,
        stop: 1 #c9a563
    );
    border-radius: 2px;
}}
QSlider::handle:horizontal {{
    width: {slider_handle}px;
    margin: {slider_margin}px 0;
    background: #c9a663;
    border: 1px solid #ebca87;
    border-radius: {max(5, slider_handle//2)}px;
}}
QSlider::handle:horizontal:hover {{ background: #e1c17d; border-color: #ffe2a4; }}
QSlider::groove:horizontal:disabled,
QSlider::sub-page:horizontal:disabled {{ background: #1c1d1e; border-color: #25241f; }}
QSlider::handle:horizontal:disabled {{ background: #4f4b45; border-color: #5d564d; }}
QSlider#CropZoomSlider::groove:horizontal {{
    height: {_px(5, scale, 3)}px;
    background: #050607;
    border: 1px solid #332b21;
}}
QSlider#CropZoomSlider::handle:horizontal {{
    width: {_px(14, scale, 10)}px;
    margin: {-_px(5, scale, 3)}px 0;
    background: #c39b58;
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
    padding: {_px(2, scale, 1)}px {_px(6, scale, 3)}px;
    font-size: {small:.2f}pt;
}}
QToolButton#FooterLink:hover {{ color: #e8dccb; background: transparent; }}

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
        title.setFont(tracked_font(max(17.5, 24.5 * scale), max(2.4, 4.2 * scale)))
    subtitle = window.findChild(QLabel, "BrandSubtitle")
    if subtitle is not None:
        subtitle.setFont(tracked_font(max(7.3, 9.4 * scale), max(1.35, 2.2 * scale)))
    for heading in window.findChildren(QLabel, "CardHeading"):
        heading.setFont(
            tracked_font(
                max(7.1, 9.0 * scale),
                max(0.6, 1.05 * scale),
                bold=True,
            )
        )


def apply_brand_skin(window) -> None:
    """Apply responsive concept-matched presentation without touching conversion logic."""
    window.resize(1260, 820)
    window.setMinimumSize(920, 640)

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

    window.setProperty("polymorphSkin", "occult-gold-v4")
    window.setStyleSheet(build_brand_stylesheet(1.0))
    _apply_typography(window, 1.0)
    controller = ResponsiveBrandController(window, apply_scale)
    window._brand_responsive_controller = controller
    window.setProperty("brandScale", 1.0)
    apply_scale(1.0)
