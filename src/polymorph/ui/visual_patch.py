from __future__ import annotations

from PySide6.QtCore import QByteArray, QRectF, QSize, Qt
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


def _polymorph_mark_pixmap(
    size: int,
    start_color: QColor,
    end_color: QColor,
    *,
    mid_color: QColor | None = None,
) -> QPixmap:
    """Render Amanda's canonical uploaded Polymorph SVG with placement-specific color."""
    source = asset_path("polymorph_mark.svg")
    renderer = QSvgRenderer(str(source))
    if not renderer.isValid():
        return QPixmap()

    dpr = _device_pixel_ratio()
    pixels = max(1, round(size * dpr))
    image = QImage(pixels, pixels, QImage.Format.Format_ARGB32_Premultiplied)
    image.fill(Qt.GlobalColor.transparent)

    intrinsic = renderer.defaultSize()
    source_w = max(1.0, float(intrinsic.width() or 4000))
    source_h = max(1.0, float(intrinsic.height() or 3869.3333))
    fit = min(pixels / source_w, pixels / source_h)
    width = source_w * fit
    height = source_h * fit
    target = QRectF((pixels - width) / 2.0, (pixels - height) / 2.0, width, height)

    painter = QPainter(image)
    painter.setRenderHint(QPainter.RenderHint.Antialiasing, True)
    painter.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform, True)
    renderer.render(painter, target)

    gradient = QLinearGradient(0, 0, pixels, pixels)
    gradient.setColorAt(0.0, start_color)
    if mid_color is not None:
        gradient.setColorAt(0.52, mid_color)
    gradient.setColorAt(1.0, end_color)
    painter.setCompositionMode(QPainter.CompositionMode.CompositionMode_SourceIn)
    painter.fillRect(image.rect(), gradient)
    painter.end()

    pixmap = QPixmap.fromImage(image)
    pixmap.setDevicePixelRatio(dpr)
    return pixmap


class RefinedBrandSigil(_brand.BrandSigil):
    """Header treatment of the canonical Polymorph SVG."""

    def apply_scale(self, scale: float) -> None:
        self._scale = scale
        # Keep the requested 64px design-size mark while restoring the protected
        # minimum-height budget with a smooth, stronger compact scale-down.
        compact = max(0.0, min(1.0, (scale - 0.73) / 0.27))
        size = round(32 + (self._base_size - 32) * compact)
        self.setFixedSize(max(32, size), max(32, size))
        self.update()

    def paintEvent(self, _event) -> None:
        mark = _polymorph_mark_pixmap(
            max(1, min(self.width(), self.height()) - 1),
            QColor("#f8f3ea"),
            QColor("#b58a55"),
            mid_color=QColor("#d9c9a7"),
        )
        if mark.isNull():
            return
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing, True)
        logical = mark.width() / mark.devicePixelRatio()
        painter.setOpacity(0.98)
        painter.drawPixmap(
            round((self.width() - logical) / 2.0),
            round((self.height() - logical) / 2.0),
            mark,
        )


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
        # Recolor the vector source itself, then render once at final device-pixel size.
        # This avoids the old raster-mask tint pass that softened thin 18px strokes.
        svg_text = preferred.read_text(encoding="utf-8")
        tint = color.name(QColor.NameFormat.HexRgb)
        svg_text = svg_text.replace('stroke="#000000"', f'stroke="{tint}"')
        svg_text = svg_text.replace('stroke="#000"', f'stroke="{tint}"')
        svg_text = svg_text.replace('fill="#000000"', f'fill="{tint}"')
        svg_text = svg_text.replace('fill="#000"', f'fill="{tint}"')
        renderer = QSvgRenderer(QByteArray(svg_text.encode("utf-8")))
        if renderer.isValid():
            painter = QPainter(image)
            painter.setRenderHint(QPainter.RenderHint.Antialiasing, True)
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

    if preferred.suffix.lower() != ".svg" or not preferred.is_file():
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

        painter.setPen(QPen(border, 1.35))
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
        height = max(45, round(62 * scale)) if scale <= 0.76 else max(62, round(82 * scale))
        self.setFixedHeight(height)
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
            left, center, right = QColor("#30080d"), QColor("#911925"), QColor("#30080d")
            border = QColor("#f4cf86")
        elif hover:
            left, center, right = QColor("#35090f"), QColor("#9e1d2a"), QColor("#35090f")
            border = QColor("#e9bf72")
        else:
            left, center, right = QColor("#2b090d"), QColor("#821821"), QColor("#2b090d")
            border = QColor("#d6a45c")

        path = QPainterPath()
        path.addRoundedRect(rect, radius, radius)
        painter.setClipPath(path)

        gradient = QLinearGradient(rect.left(), rect.center().y(), rect.right(), rect.center().y())
        gradient.setColorAt(0.0, left)
        gradient.setColorAt(0.5, center)
        gradient.setColorAt(1.0, right)
        painter.fillPath(path, gradient)

        sheen = QLinearGradient(rect.left(), rect.top(), rect.left(), rect.bottom())
        sheen.setColorAt(0.0, QColor(235, 190, 108, 34 if enabled else 6))
        sheen.setColorAt(0.34, QColor(211, 151, 75, 10 if enabled else 0))
        sheen.setColorAt(0.58, QColor(255, 255, 255, 0))
        sheen.setColorAt(1.0, QColor(0, 0, 0, 72))
        painter.fillPath(path, sheen)

        # Large ghost mark first: same canonical SVG, center-right and deliberately faint.
        ghost_size = max(138, round(self.height() * 2.46))
        ghost = _polymorph_mark_pixmap(
            ghost_size,
            QColor("#deb36d"),
            QColor("#5f1722"),
            mid_color=QColor("#985143"),
        )
        if not ghost.isNull():
            logical = ghost.width() / ghost.devicePixelRatio()
            center_x = rect.left() + rect.width() * 0.70
            painter.save()
            painter.setOpacity(
                0.040 if not enabled else
                0.185 if hover else
                0.155 if down else
                0.130
            )
            painter.drawPixmap(
                round(center_x - logical / 2.0),
                round(rect.center().y() - logical / 2.0),
                ghost,
            )
            painter.restore()

        # Foreground mark: keep the accepted left-side placement, but make it visibly present.
        mark_size = max(62, round(self.height() * 1.42))
        mark = _polymorph_mark_pixmap(
            mark_size,
            QColor("#f0cf88"),
            QColor("#8a2e3d"),
            mid_color=QColor("#c47b58"),
        )
        if not mark.isNull():
            logical = mark.width() / mark.devicePixelRatio()
            mark_x = rect.left() + max(8.0, 12.0 * self._scale)
            mark_y = rect.center().y() - logical / 2.0
            painter.save()
            painter.setOpacity(
                0.090 if not enabled else
                0.430 if hover else
                0.385 if down else
                0.340
            )
            painter.drawPixmap(round(mark_x), round(mark_y), mark)
            painter.restore()

        painter.setClipping(False)
        painter.setPen(QPen(border, 1.0))
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.drawRoundedRect(rect, radius, radius)
        inner = rect.adjusted(1.0, 1.0, -1.0, -1.0)
        painter.setPen(QPen(QColor(235, 187, 96, 108 if enabled else 16), 1.0))
        painter.drawRoundedRect(inner, max(2.0, radius - 1.0), max(2.0, radius - 1.0))

        title_rect = QRectF(rect).translated(0, -7 * self._scale)
        subtitle_rect = QRectF(rect).translated(0, 14 * self._scale)

        painter.setPen(QColor("#e8bf6e") if enabled else QColor("#776a58"))
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
        painter.setPen(QColor("#c99652") if enabled else QColor("#675848"))
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
    height = max(45, round(62 * scale)) if scale <= 0.76 else max(62, round(82 * scale))
    button.setFixedHeight(height)

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
    _brand.BrandSigil = RefinedBrandSigil
    _brand.TexturedFrame = RefinedTexturedFrame
    _brand.PolymorphButton = RefinedPolymorphButton

    _fidelity.tinted_icon_pixmap = _crisp_tinted_icon_pixmap
    _fidelity._apply_heading_typography = _cool_heading_typography
    _fidelity._apply_mockup_palette_and_body = _cool_palette
    _fidelity._apply_visual_polish = _refined_visual
