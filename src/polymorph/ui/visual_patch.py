from __future__ import annotations

from PySide6.QtCore import QRectF, QSize, Qt
from PySide6.QtGui import QColor, QFont, QImage, QLinearGradient, QPainter, QPainterPath, QPen, QPixmap
from PySide6.QtSvg import QSvgRenderer
from PySide6.QtWidgets import QApplication, QLabel, QSizePolicy, QWidget

from ..resources import asset_path
from . import brand_widgets as _brand
from . import fidelity_pass as _fidelity


COOL_GOLD = QColor("#d7c7a4")
CRIMSON = QColor("#d51f2d")
_V4_MARKER = "/* POLYMORPH_MOCKUP_V4_OVERRIDES */"
_INSTALLED = False

_original_palette = _fidelity._apply_mockup_palette_and_body
_original_visual = _fidelity._apply_visual_polish


def _device_pixel_ratio() -> float:
    app = QApplication.instance()
    if app is None:
        return 1.0
    screen = app.primaryScreen()
    return max(1.0, float(screen.devicePixelRatio()) if screen is not None else 1.0)


def _crisp_tinted_icon_pixmap(name: str, size: int, color: QColor = COOL_GOLD) -> QPixmap:
    """Render vector assets at final device-pixel size before tinting."""
    requested = asset_path(f"ui/{name}")
    preferred = requested
    if requested.suffix.lower() != ".svg":
        vector = requested.with_suffix(".svg")
        if vector.is_file():
            preferred = vector

    dpr = _device_pixel_ratio()
    pixels = max(1, round(size * dpr))
    image = QImage(pixels, pixels, QImage.Format.Format_ARGB32_Premultiplied)
    image.fill(Qt.GlobalColor.transparent)

    if preferred.suffix.lower() == ".svg" and preferred.is_file():
        renderer = QSvgRenderer(str(preferred))
        if renderer.isValid():
            painter = QPainter(image)
            painter.setRenderHint(QPainter.RenderHint.Antialiasing, True)
            painter.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform, True)
            renderer.render(painter, QRectF(0, 0, pixels, pixels))
            painter.end()
    else:
        raster = QImage(str(preferred))
        if raster.isNull() and preferred != requested:
            raster = QImage(str(requested))
        if raster.isNull():
            return QPixmap()
        raster = raster.scaled(
            QSize(pixels, pixels),
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation,
        )
        x = (pixels - raster.width()) // 2
        y = (pixels - raster.height()) // 2
        painter = QPainter(image)
        painter.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform, True)
        painter.drawImage(x, y, raster)
        painter.end()

    painter = QPainter(image)
    painter.setCompositionMode(QPainter.CompositionMode.CompositionMode_SourceIn)
    painter.fillRect(image.rect(), color)
    painter.end()

    pixmap = QPixmap.fromImage(image)
    pixmap.setDevicePixelRatio(dpr)
    return pixmap


class RefinedTexturedFrame(_brand.TexturedFrame):
    """Smooth blue-black card gradient matching the approved mockup."""

    def paintEvent(self, _event) -> None:
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing, True)
        rect = QRectF(self.rect()).adjusted(0.5, 0.5, -0.5, -0.5)
        radius = 3.25

        path = QPainterPath()
        path.addRoundedRect(rect, radius, radius)

        selected = self.tone == "queue-selected" or bool(self.property("selected"))
        if selected:
            c0, mid, c1 = QColor("#22080d"), QColor("#12090c"), QColor("#08090b")
            border = QColor("#a92430")
        elif self.tone == "preview":
            c0, mid, c1 = QColor("#090c0f"), QColor("#06080a"), QColor("#030405")
            border = QColor("#4b4a45")
        elif self.tone == "status":
            c0, mid, c1 = QColor("#0d1115"), QColor("#080b0e"), QColor("#040506")
            border = QColor("#4b4a45")
        else:
            c0, mid, c1 = QColor("#101419"), QColor("#0a0d11"), QColor("#050607")
            border = QColor("#4b4a45")

        gradient = QLinearGradient(rect.topLeft(), rect.bottomRight())
        gradient.setColorAt(0.0, c0)
        gradient.setColorAt(0.52, mid)
        gradient.setColorAt(1.0, c1)

        painter.setClipPath(path)
        painter.fillPath(path, gradient)
        painter.setClipping(False)

        painter.setPen(QPen(border, 1.0))
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.drawRoundedRect(rect, radius, radius)

        inner = rect.adjusted(1.0, 1.0, -1.0, -1.0)
        painter.setPen(QPen(QColor(220, 205, 174, 14 if not selected else 18), 1.0))
        painter.drawRoundedRect(inner, max(1.5, radius - 1.0), max(1.5, radius - 1.0))


class RefinedPolymorphButton(_brand.PolymorphButton):
    """Substantial crimson action with a secondary CONVERT MEDIA label."""

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setMinimumHeight(82)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

    def apply_scale(self, scale: float) -> None:
        self._scale = scale
        self.setMinimumHeight(max(62, round(82 * scale)))
        self.update()

    def paintEvent(self, _event) -> None:
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing, True)
        rect = QRectF(self.rect()).adjusted(0.5, 0.5, -0.5, -0.5)
        radius = max(3.0, 4.5 * self._scale)

        enabled = self.isEnabled()
        down = self.isDown()
        hover = self.underMouse()
        if not enabled:
            left, center, right = QColor("#13070a"), QColor("#2a0d12"), QColor("#13070a")
            border = QColor("#595147")
        elif down:
            left, center, right = QColor("#2b070c"), QColor("#881723"), QColor("#2b070c")
            border = QColor("#ead8ad")
        elif hover:
            left, center, right = QColor("#31080d"), QColor("#951a27"), QColor("#31080d")
            border = QColor("#e3cfa2")
        else:
            left, center, right = QColor("#25070b"), QColor("#76131d"), QColor("#25070b")
            border = QColor("#cfba8e")

        path = QPainterPath()
        path.addRoundedRect(rect, radius, radius)
        painter.setClipPath(path)

        gradient = QLinearGradient(rect.left(), rect.center().y(), rect.right(), rect.center().y())
        gradient.setColorAt(0.0, left)
        gradient.setColorAt(0.5, center)
        gradient.setColorAt(1.0, right)
        painter.fillPath(path, gradient)

        sheen = QLinearGradient(rect.left(), rect.top(), rect.left(), rect.bottom())
        sheen.setColorAt(0.0, QColor(255, 237, 205, 18 if enabled else 5))
        sheen.setColorAt(0.36, QColor(255, 255, 255, 0))
        sheen.setColorAt(1.0, QColor(0, 0, 0, 74))
        painter.fillPath(path, sheen)

        cy = rect.center().y()
        sigil_cx = rect.left() + max(48.0, 56.0 * self._scale)
        ring_color = QColor(226, 211, 180, 95 if enabled else 32)
        painter.setPen(QPen(ring_color, max(0.8, self._scale)))
        for radius_px in (14, 22):
            rr = radius_px * self._scale
            painter.drawEllipse(QRectF(sigil_cx - rr, cy - rr, rr * 2, rr * 2))
        tri = 10.0 * self._scale
        painter.drawLine(int(sigil_cx), int(cy - tri), int(sigil_cx - tri), int(cy + tri * 0.82))
        painter.drawLine(int(sigil_cx - tri), int(cy + tri * 0.82), int(sigil_cx + tri), int(cy + tri * 0.82))
        painter.drawLine(int(sigil_cx + tri), int(cy + tri * 0.82), int(sigil_cx), int(cy - tri))

        painter.setClipping(False)
        painter.setPen(QPen(border, 1.0))
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.drawRoundedRect(rect, radius, radius)
        inner = rect.adjusted(1.0, 1.0, -1.0, -1.0)
        painter.setPen(QPen(QColor(232, 215, 180, 30 if enabled else 10), 1.0))
        painter.drawRoundedRect(inner, max(2.0, radius - 1.0), max(2.0, radius - 1.0))

        title_rect = QRectF(rect).translated(0, -7 * self._scale)
        subtitle_rect = QRectF(rect).translated(0, 14 * self._scale)

        painter.setPen(QColor("#f0e9de") if enabled else QColor("#766f66"))
        painter.setFont(
            _brand.tracked_font(
                max(9.8, 13.1 * self._scale),
                max(2.2, 4.6 * self._scale),
                bold=False,
            )
        )
        painter.drawText(title_rect, Qt.AlignmentFlag.AlignCenter, "POLYMORPH")

        subtitle_font = QFont("Inter")
        subtitle_font.setPointSizeF(max(5.4, 6.3 * self._scale))
        subtitle_font.setWeight(QFont.Weight.Medium)
        subtitle_font.setLetterSpacing(
            QFont.SpacingType.AbsoluteSpacing,
            max(0.9, 1.55 * self._scale),
        )
        painter.setFont(subtitle_font)
        painter.setPen(QColor("#d8cbb9") if enabled else QColor("#675f57"))
        painter.drawText(subtitle_rect, Qt.AlignmentFlag.AlignCenter, "CONVERT MEDIA")


def _cool_heading_typography(window, scale: float) -> None:
    app = QApplication.instance()
    family = "Polymorph"
    if app is not None:
        family = str(app.property("polymorphDisplayBoldFont") or family).strip() or family
    point_size = max(6.25, 7.65 * scale)
    spacing = max(0.38, 0.66 * scale)
    escaped = family.replace("\\", "\\\\").replace('"', '\\"')
    for heading in window.findChildren(QLabel, "CardHeading"):
        heading.setStyleSheet(
            f'font-family: "{escaped}"; '
            f"font-size: {point_size:.2f}pt; font-weight: 700; "
            "color: #d8c9a7; background: transparent;"
        )
        heading.setFont(
            _brand.tracked_font(
                point_size,
                spacing,
                bold=True,
                family=family,
            )
        )


def _cool_palette(window, scale: float) -> None:
    _original_palette(window, scale)
    sheet = window.styleSheet()
    if _V4_MARKER in sheet:
        sheet = sheet.split(_V4_MARKER, 1)[0].rstrip()

    status_detail_size = max(5.7, 6.30 * scale)
    override = f"""
{_V4_MARKER}
QWidget#AppRoot QRadioButton {{
    color: #e2dfda;
}}
QLabel#SecondaryText {{
    color: #85898d;
}}
QLabel#StatusDetail {{
    font-size: {status_detail_size:.2f}pt;
    color: #74797e;
}}
QLabel#UnitLabel,
QLabel#TimesLabel,
QLabel#ZoomValue,
QLabel#PlaybackTime {{
    color: #9da0a2;
}}
QLabel#PathText {{
    color: #d7d4cf;
    background: #080a0c;
    border-color: #383b3d;
}}
QPushButton#HeaderAction,
QPushButton#BrowseButton {{
    color: #ddd2bb;
    background: #090b0d;
    border-color: #5a554b;
}}
QToolButton#FooterLink {{
    color: #b7b5b0;
}}
QToolButton#FooterLink:hover {{
    color: #f0ece5;
}}
QFrame#CardSeparator,
QFrame#PreviewMetaSeparator,
QFrame#FooterSeparator {{
    color: #34383b;
    background: #34383b;
}}
QFrame#VerticalSeparator {{
    color: #34383b;
    background: #34383b;
}}
QRadioButton::indicator {{
    border-color: #686c70;
    background: #050607;
}}
QRadioButton::indicator:hover {{
    border-color: #b8aa8c;
}}
QRadioButton::indicator:checked {{
    border-color: #d6c49d;
    background: qradialgradient(
        cx: 0.5, cy: 0.5, radius: 0.5,
        fx: 0.5, fy: 0.5,
        stop: 0 #e12836,
        stop: 0.35 #e12836,
        stop: 0.36 #050607,
        stop: 1 #050607
    );
}}
QComboBox,
QSpinBox,
QDoubleSpinBox {{
    color: #e4e2de;
    background: #080a0c;
    border-color: #383b3e;
}}
QComboBox:hover,
QSpinBox:hover,
QDoubleSpinBox:hover {{
    background: #0d1013;
    border-color: #777064;
}}
QComboBox:disabled,
QSpinBox:disabled,
QDoubleSpinBox:disabled {{
    color: #6f7478;
    background: #080a0c;
    border-color: #303438;
}}
QSlider::handle:horizontal {{
    background: qradialgradient(
        cx:0.42,cy:0.38,radius:0.72,
        stop:0 #f0e5cf,
        stop:0.55 #d3c29f,
        stop:1 #7b705e
    );
    border-color: #e0cfaa;
}}
"""
    window.setStyleSheet(sheet + "\n" + override)


def _status_ring_pixmap(size: int) -> QPixmap:
    dpr = _device_pixel_ratio()
    pixels = max(1, round(size * dpr))
    image = QImage(pixels, pixels, QImage.Format.Format_ARGB32_Premultiplied)
    image.fill(Qt.GlobalColor.transparent)
    painter = QPainter(image)
    painter.setRenderHint(QPainter.RenderHint.Antialiasing, True)

    margin = max(3, round(pixels * 0.10))
    rect = QRectF(margin, margin, pixels - margin * 2, pixels - margin * 2)
    width = max(3.0, pixels * 0.11)

    painter.setPen(QPen(QColor("#271215"), width, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap))
    painter.drawEllipse(rect)
    painter.setPen(QPen(CRIMSON, width, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap))
    painter.drawArc(rect, 42 * 16, 286 * 16)
    painter.end()

    pixmap = QPixmap.fromImage(image)
    pixmap.setDevicePixelRatio(dpr)
    return pixmap


def _refine_runtime_geometry(window, scale: float) -> None:
    target = max(58, round(78 * scale))
    for spin in (window.max_mb, window.width_spin, window.height_spin):
        spin.setFixedWidth(target)

    button = window.convert_btn
    button.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
    button.setMinimumHeight(max(62, round(82 * scale)))

    rail = window.findChild(QWidget, "ControlRailContent")
    if rail is not None and rail.layout() is not None:
        layout = rail.layout()
        button_index = layout.indexOf(button)
        if button_index >= 0:
            for index in range(layout.count() - 1, button_index, -1):
                item = layout.itemAt(index)
                if item is not None and item.spacerItem() is not None:
                    layout.takeAt(index)

    status = window.findChild(QWidget, "StatusCard")
    if status is not None:
        for label in status.findChildren(QLabel):
            if label.text() == "◯" or bool(label.property("polymorphStatusRing")):
                label.setProperty("polymorphStatusRing", True)
                ring_size = max(34, round(45 * scale))
                label.setText("")
                label.setFixedSize(ring_size, ring_size)
                label.setPixmap(_status_ring_pixmap(ring_size))
                label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                break


def _refined_visual(window) -> None:
    _original_visual(window)
    scale = float(window.property("brandScale") or 1.0)
    _refine_runtime_geometry(window, scale)


def install_visual_patch() -> None:
    """Install the approved mockup-fidelity refinements before branded layout imports."""
    global _INSTALLED
    if _INSTALLED:
        return
    _INSTALLED = True

    _brand.tinted_icon_pixmap = _crisp_tinted_icon_pixmap
    _brand.TexturedFrame = RefinedTexturedFrame
    _brand.PolymorphButton = RefinedPolymorphButton

    _fidelity.tinted_icon_pixmap = _crisp_tinted_icon_pixmap
    _fidelity._apply_heading_typography = _cool_heading_typography
    _fidelity._apply_mockup_palette_and_body = _cool_palette
    _fidelity._apply_visual_polish = _refined_visual
