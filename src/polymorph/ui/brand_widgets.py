from __future__ import annotations

from dataclasses import dataclass, field

from PySide6.QtCore import QEvent, QObject, QRectF, QSize, Qt, QTimer
from PySide6.QtGui import (
    QColor,
    QFont,
    QImage,
    QLinearGradient,
    QPainter,
    QPainterPath,
    QPen,
    QPixmap,
    QRadialGradient,
)
from PySide6.QtWidgets import QFrame, QLabel, QPushButton

from ..resources import asset_path

GOLD = QColor("#d0ad6d")
IVORY = QColor("#f2ece2")
CRIMSON = QColor("#c9252e")


def display_family() -> str:
    """Return the runtime display face selected by fonts.py."""
    from PySide6.QtWidgets import QApplication

    app = QApplication.instance()
    if app is not None:
        family = str(app.property("polymorphDisplayFont") or "").strip()
        if family:
            return family
    return "Cinzel"


def tracked_font(
    point_size: float,
    spacing: float,
    *,
    bold: bool = False,
    family: str | None = None,
) -> QFont:
    font = QFont(family or display_family())
    font.setPointSizeF(point_size)
    font.setWeight(QFont.Weight.Bold if bold else QFont.Weight.Normal)
    font.setLetterSpacing(QFont.SpacingType.AbsoluteSpacing, spacing)
    return font


def tinted_icon_pixmap(name: str, size: int, color: QColor = GOLD) -> QPixmap:
    """Tint a UI icon, preferring a sharp sibling SVG while keeping PNG fallback."""
    requested = asset_path(f"ui/{name}")
    preferred = requested
    if requested.suffix.lower() != ".svg":
        vector = requested.with_suffix(".svg")
        if vector.is_file():
            preferred = vector

    pixmap = QPixmap(str(preferred))
    if pixmap.isNull() and preferred != requested:
        pixmap = QPixmap(str(requested))
    if pixmap.isNull():
        return QPixmap()
    target = pixmap.scaled(
        QSize(size, size),
        Qt.AspectRatioMode.KeepAspectRatio,
        Qt.TransformationMode.SmoothTransformation,
    )
    image = target.toImage().convertToFormat(QImage.Format.Format_ARGB32_Premultiplied)
    painter = QPainter(image)
    painter.setCompositionMode(QPainter.CompositionMode.CompositionMode_SourceIn)
    painter.fillRect(image.rect(), color)
    painter.end()
    return QPixmap.fromImage(image)


class TintIconLabel(QLabel):
    def __init__(self, name: str, size: int = 15, parent=None) -> None:
        super().__init__(parent)
        self._asset = name
        self._icon_size = size
        self.setFixedSize(size, size)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.refresh()

    def refresh(self, scale: float = 1.0) -> None:
        size = max(10, round(self._icon_size * scale))
        self.setFixedSize(size, size)
        self.setPixmap(tinted_icon_pixmap(self._asset, size))


class TexturedFrame(QFrame):
    """Dark restrained gradient panel with deterministic synthesized grain."""

    def __init__(self, tone: str = "control", parent=None) -> None:
        super().__init__(parent)
        self.tone = tone
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, False)

    def paintEvent(self, _event) -> None:
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing, True)
        rect = QRectF(self.rect()).adjusted(0.5, 0.5, -0.5, -0.5)
        radius = 3.25

        path = QPainterPath()
        path.addRoundedRect(rect, radius, radius)
        painter.setClipPath(path)

        selected = self.tone == "queue-selected" or bool(self.property("selected"))
        if self.tone == "preview":
            c0, mid, c1 = QColor("#0b0c0d"), QColor("#08090a"), QColor("#060708")
        elif self.tone == "status":
            c0, mid, c1 = QColor("#0d0e0f"), QColor("#090a0b"), QColor("#060708")
        elif selected:
            c0, mid, c1 = QColor("#23090d"), QColor("#16090b"), QColor("#0b0b0c")
        else:
            c0, mid, c1 = QColor("#141311"), QColor("#0d0e0f"), QColor("#08090a")

        base = QLinearGradient(rect.topLeft(), rect.bottomRight())
        base.setColorAt(0.0, c0)
        base.setColorAt(0.46, mid)
        base.setColorAt(1.0, c1)
        painter.fillPath(path, base)

        # Slight warm center illumination keeps the panels from reading as flat
        # gray boxes while staying substantially darker than the content.
        glow = QRadialGradient(rect.center(), max(rect.width(), rect.height()) * 0.82)
        glow.setColorAt(0.0, QColor(198, 153, 86, 8 if not selected else 5))
        glow.setColorAt(0.52, QColor(111, 74, 37, 3))
        glow.setColorAt(1.0, QColor(0, 0, 0, 0))
        painter.fillPath(path, glow)

        # Stable low-density grain. It adds surface depth without visible speckling.
        width = max(1, self.width())
        height = max(1, self.height())
        samples = min(320, max(48, (width * height) // 7200))
        state = 0x5EED1234
        for index in range(samples):
            state = (1664525 * state + 1013904223 + index) & 0xFFFFFFFF
            x = state % width
            state = (1664525 * state + 1013904223) & 0xFFFFFFFF
            y = state % height
            alpha = 4 + ((state >> 24) & 0x03)
            painter.setPen(QColor(255, 244, 226, alpha))
            painter.drawPoint(int(x), int(y))

        painter.setClipping(False)
        if selected:
            border = QColor("#a92a32")
        elif self.tone == "preview":
            border = QColor("#55422d")
        else:
            border = QColor("#493827")
        painter.setPen(QPen(border, 1.0))
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.drawRoundedRect(rect, radius, radius)

        # Hairline inner highlight gives the mockup's etched/shadowed card edge.
        inner = rect.adjusted(1.0, 1.0, -1.0, -1.0)
        painter.setPen(QPen(QColor(224, 186, 113, 13 if not selected else 18), 1.0))
        painter.drawRoundedRect(inner, max(1.5, radius - 1.0), max(1.5, radius - 1.0))


class PolymorphButton(QPushButton):
    """Branded action surface matching the approved concept; animation comes later."""

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setObjectName("Primary")
        self.setText("POLYMORPH")
        self.setAccessibleName("Polymorph")
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setMinimumHeight(66)
        self._scale = 1.0

    def apply_scale(self, scale: float) -> None:
        self._scale = scale
        self.setMinimumHeight(max(49, round(68 * scale)))
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
            left, center, right = QColor("#140b0c"), QColor("#241014"), QColor("#140b0c")
            border = QColor("#50402e")
        elif down:
            left, center, right = QColor("#240609"), QColor("#7a151e"), QColor("#240609")
            border = QColor("#f0ce8a")
        elif hover:
            left, center, right = QColor("#25070a"), QColor("#8e1b25"), QColor("#25070a")
            border = QColor("#e2bd76")
        else:
            left, center, right = QColor("#160608"), QColor("#671018"), QColor("#160608")
            border = QColor("#bd914b")

        path = QPainterPath()
        path.addRoundedRect(rect, radius, radius)
        painter.setClipPath(path)
        gradient = QLinearGradient(rect.left(), rect.center().y(), rect.right(), rect.center().y())
        gradient.setColorAt(0.0, left)
        gradient.setColorAt(0.18, QColor("#26080c") if enabled else left)
        gradient.setColorAt(0.50, center)
        gradient.setColorAt(0.82, QColor("#26080c") if enabled else right)
        gradient.setColorAt(1.0, right)
        painter.fillPath(path, gradient)

        # Subtle top/bottom light shaping makes the action look inset rather than flat.
        sheen = QLinearGradient(rect.left(), rect.top(), rect.left(), rect.bottom())
        sheen.setColorAt(0.0, QColor(255, 220, 158, 18 if enabled else 6))
        sheen.setColorAt(0.32, QColor(255, 255, 255, 0))
        sheen.setColorAt(1.0, QColor(0, 0, 0, 70))
        painter.fillPath(path, sheen)

        # Mockup-inspired left sigil. It stays static until the dedicated loader pass.
        sigil_cx = rect.left() + 58 * self._scale
        cy = rect.center().y()
        ring_color = QColor(222, 184, 113, 95 if enabled else 35)
        painter.setPen(QPen(ring_color, max(0.8, 1.0 * self._scale)))
        for radius_px in (15, 23):
            rr = radius_px * self._scale
            painter.drawEllipse(QRectF(sigil_cx - rr, cy - rr, rr * 2, rr * 2))
        tri = 10.5 * self._scale
        painter.drawLine(int(sigil_cx), int(cy - tri), int(sigil_cx - tri), int(cy + tri * 0.82))
        painter.drawLine(int(sigil_cx - tri), int(cy + tri * 0.82), int(sigil_cx + tri), int(cy + tri * 0.82))
        painter.drawLine(int(sigil_cx + tri), int(cy + tri * 0.82), int(sigil_cx), int(cy - tri))

        # Thin architectural separators, like the concept art, without crowding the title.
        painter.setPen(QPen(QColor(201, 160, 91, 120 if enabled else 45), 1.0))
        line_y = cy
        painter.drawLine(
            int(rect.left() + 13 * self._scale),
            int(line_y),
            int(rect.left() + 27 * self._scale),
            int(line_y),
        )
        painter.drawLine(
            int(rect.right() - 27 * self._scale),
            int(line_y),
            int(rect.right() - 13 * self._scale),
            int(line_y),
        )

        painter.setClipping(False)
        painter.setPen(QPen(border, 1.0))
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.drawRoundedRect(rect, radius, radius)
        inner = rect.adjusted(1.0, 1.0, -1.0, -1.0)
        painter.setPen(QPen(QColor(244, 203, 128, 35 if enabled else 12), 1.0))
        painter.drawRoundedRect(inner, max(2.0, radius - 1.0), max(2.0, radius - 1.0))

        text_color = QColor("#f1ddb7") if enabled else QColor("#776a5b")
        painter.setPen(text_color)
        painter.setFont(
            tracked_font(
                max(9.6, 13.2 * self._scale),
                max(2.6, 5.5 * self._scale),
                bold=False,
            )
        )
        text_rect = QRectF(
            rect.left() + 92 * self._scale,
            rect.top(),
            max(1.0, rect.width() - 116 * self._scale),
            rect.height(),
        )
        painter.drawText(text_rect, Qt.AlignmentFlag.AlignCenter, "POLYMORPH")


@dataclass
class ScaleRegistry:
    layout_specs: list[tuple[object, tuple[int, int, int, int], int]] = field(default_factory=list)
    fixed_widths: list[tuple[object, int]] = field(default_factory=list)
    fixed_heights: list[tuple[object, int]] = field(default_factory=list)
    fixed_sizes: list[tuple[object, QSize]] = field(default_factory=list)
    min_heights: list[tuple[object, int]] = field(default_factory=list)
    callbacks: list[object] = field(default_factory=list)

    def layout(self, layout, margins: tuple[int, int, int, int], spacing: int) -> None:
        self.layout_specs.append((layout, margins, spacing))

    def width(self, widget, value: int) -> None:
        self.fixed_widths.append((widget, value))

    def height(self, widget, value: int) -> None:
        self.fixed_heights.append((widget, value))

    def size(self, widget, width: int, height: int) -> None:
        self.fixed_sizes.append((widget, QSize(width, height)))

    def min_height(self, widget, value: int) -> None:
        self.min_heights.append((widget, value))

    def callback(self, fn) -> None:
        self.callbacks.append(fn)

    def apply(self, scale: float) -> None:
        compact_rail = scale <= 0.76
        for layout, margins, spacing in self.layout_specs:
            l, t, r, b = margins
            scaled_l = round(l * scale)
            scaled_t = round(t * scale)
            scaled_r = round(r * scale)
            scaled_b = round(b * scale)
            scaled_spacing = max(0, round(spacing * scale))

            if compact_rail:
                parent = layout.parentWidget()
                if parent is not None and parent.layout() is layout:
                    if parent.objectName() == "ControlRailContent":
                        scaled_spacing = min(scaled_spacing, 2)
                    elif parent.objectName() == "ControlCard":
                        scaled_t = max(0, scaled_t - 1)
                        scaled_b = max(0, scaled_b - 2)

            layout.setContentsMargins(scaled_l, scaled_t, scaled_r, scaled_b)
            layout.setSpacing(scaled_spacing)
        for widget, value in self.fixed_widths:
            widget.setFixedWidth(max(1, round(value * scale)))
        for widget, value in self.fixed_heights:
            widget.setFixedHeight(max(1, round(value * scale)))
        for widget, size in self.fixed_sizes:
            widget.setFixedSize(
                max(1, round(size.width() * scale)),
                max(1, round(size.height() * scale)),
            )
        for widget, value in self.min_heights:
            widget.setMinimumHeight(max(1, round(value * scale)))
        for fn in self.callbacks:
            fn(scale)


class ResponsiveBrandController(QObject):
    DESIGN_WIDTH = 1260
    DESIGN_HEIGHT = 820
    MIN_SCALE = 0.73

    def __init__(self, window, apply_callback) -> None:
        super().__init__(window)
        self.window = window
        self.apply_callback = apply_callback
        self._last_scale = -1.0
        self._pending = False
        window.installEventFilter(self)

    def eventFilter(self, watched, event) -> bool:
        if watched is self.window and event.type() == QEvent.Type.Resize:
            if not self._pending:
                self._pending = True
                QTimer.singleShot(0, self._apply)
        return super().eventFilter(watched, event)

    def _apply(self) -> None:
        self._pending = False
        width = max(1, self.window.width())
        height = max(1, self.window.height())
        scale = min(1.0, width / self.DESIGN_WIDTH, height / self.DESIGN_HEIGHT)
        scale = max(self.MIN_SCALE, scale)
        if abs(scale - self._last_scale) < 0.012:
            return
        self._last_scale = scale
        self.window.setProperty("brandScale", scale)
        self.apply_callback(scale)


class BrandSigil(QFrame):
    """Small static Polymorph mark used in the header; not the working loader."""

    def __init__(self, base_size: int = 38, parent=None) -> None:
        super().__init__(parent)
        self._base_size = base_size
        self._scale = 1.0
        self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents, True)
        self.apply_scale(1.0)

    def apply_scale(self, scale: float) -> None:
        self._scale = scale
        size = max(24, round(self._base_size * scale))
        self.setFixedSize(size, size)
        self.update()

    def paintEvent(self, _event) -> None:
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing, True)
        rect = QRectF(self.rect()).adjusted(2.5, 2.5, -2.5, -2.5)
        painter.setPen(QPen(QColor("#b99454"), max(1.0, 1.15 * self._scale)))
        painter.drawEllipse(rect)
        inner = rect.adjusted(5 * self._scale, 5 * self._scale, -5 * self._scale, -5 * self._scale)
        painter.setPen(QPen(QColor("#d5b775"), max(1.0, 1.05 * self._scale)))
        painter.drawEllipse(inner)
        cx = inner.center().x()
        top = inner.top() + 1
        left = inner.left() + 2
        right = inner.right() - 2
        bottom = inner.bottom() - 2
        painter.drawLine(int(cx), int(top), int(left), int(bottom))
        painter.drawLine(int(left), int(bottom), int(right), int(bottom))
        painter.drawLine(int(right), int(bottom), int(cx), int(top))