from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

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
    """Tint a supplied monochrome-alpha PNG without changing its silhouette."""
    path = asset_path(f"ui/{name}")
    pixmap = QPixmap(str(path))
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
    """Dark gradient panel with deterministic, very low-opacity synthesized grain."""

    def __init__(self, tone: str = "control", parent=None) -> None:
        super().__init__(parent)
        self.tone = tone
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, False)

    def paintEvent(self, _event) -> None:
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing, True)
        rect = QRectF(self.rect()).adjusted(0.5, 0.5, -0.5, -0.5)
        radius = 5.0

        path = QPainterPath()
        path.addRoundedRect(rect, radius, radius)
        painter.setClipPath(path)

        if self.tone == "preview":
            c0, c1 = QColor("#090a0b"), QColor("#070809")
        elif self.tone == "status":
            c0, c1 = QColor("#0b0c0d"), QColor("#070809")
        elif self.tone == "queue-selected" or bool(self.property("selected")):
            c0, c1 = QColor("#1d090c"), QColor("#0e0d0d")
        else:
            c0, c1 = QColor("#101112"), QColor("#090a0b")

        gradient = QLinearGradient(rect.topLeft(), rect.bottomRight())
        gradient.setColorAt(0.0, c0)
        gradient.setColorAt(0.48, QColor("#0c0d0e"))
        gradient.setColorAt(1.0, c1)
        painter.fillPath(path, gradient)

        # Stable low-density grain. It adds surface depth without becoming visible noise.
        width = max(1, self.width())
        height = max(1, self.height())
        samples = min(260, max(40, (width * height) // 8500))
        state = 0x5EED1234
        for index in range(samples):
            state = (1664525 * state + 1013904223 + index) & 0xFFFFFFFF
            x = state % width
            state = (1664525 * state + 1013904223) & 0xFFFFFFFF
            y = state % height
            alpha = 5 + ((state >> 24) & 0x03)
            painter.setPen(QColor(255, 244, 226, alpha))
            painter.drawPoint(int(x), int(y))

        painter.setClipping(False)
        if bool(self.property("selected")):
            border = QColor("#a3262e")
        elif self.tone == "preview":
            border = QColor("#54422c")
        else:
            border = QColor("#403326")
        painter.setPen(QPen(border, 1.0))
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.drawRoundedRect(rect, radius, radius)


class PolymorphButton(QPushButton):
    """Centered branded action button with static alchemic decoration."""

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setObjectName("Primary")
        self.setText("POLYMORPH")
        self.setAccessibleName("Polymorph")
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setMinimumHeight(62)
        self._scale = 1.0

    def apply_scale(self, scale: float) -> None:
        self._scale = scale
        self.setMinimumHeight(max(48, round(66 * scale)))
        self.update()

    def paintEvent(self, _event) -> None:
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing, True)
        rect = QRectF(self.rect()).adjusted(0.5, 0.5, -0.5, -0.5)
        radius = max(4.0, 7.0 * self._scale)

        enabled = self.isEnabled()
        down = self.isDown()
        hover = self.underMouse()
        if not enabled:
            left, mid, right = QColor("#180f10"), QColor("#241315"), QColor("#180f10")
            border = QColor("#4e4030")
        elif down:
            left, mid, right = QColor("#26080c"), QColor("#681119"), QColor("#26080c")
            border = QColor("#f0ce8a")
        elif hover:
            left, mid, right = QColor("#28090d"), QColor("#8b1d26"), QColor("#28090d")
            border = QColor("#e2bd76")
        else:
            left, mid, right = QColor("#1b0709"), QColor("#68131a"), QColor("#1b0709")
            border = QColor("#b98d49")

        path = QPainterPath()
        path.addRoundedRect(rect, radius, radius)
        painter.setClipPath(path)
        gradient = QLinearGradient(rect.left(), rect.center().y(), rect.right(), rect.center().y())
        gradient.setColorAt(0.0, left)
        gradient.setColorAt(0.48, mid)
        gradient.setColorAt(0.52, mid)
        gradient.setColorAt(1.0, right)
        painter.fillPath(path, gradient)

        # Quiet static rings/triangle behind the label; this is not the loader animation.
        cx, cy = rect.center().x(), rect.center().y()
        ring_color = QColor(214, 177, 108, 32 if enabled else 14)
        painter.setPen(QPen(ring_color, 1.0))
        for radius_px in (22, 30, 39):
            rr = radius_px * self._scale
            painter.drawEllipse(QRectF(cx - rr, cy - rr, rr * 2, rr * 2))
        tri = 15 * self._scale
        painter.drawLine(int(cx), int(cy - tri), int(cx - tri), int(cy + tri * 0.8))
        painter.drawLine(int(cx - tri), int(cy + tri * 0.8), int(cx + tri), int(cy + tri * 0.8))
        painter.drawLine(int(cx + tri), int(cy + tri * 0.8), int(cx), int(cy - tri))

        line_y = cy
        gap = 120 * self._scale
        line_len = 44 * self._scale
        painter.setPen(QPen(QColor(191, 148, 80, 135 if enabled else 55), 1.0))
        painter.drawLine(int(cx - gap - line_len), int(line_y), int(cx - gap), int(line_y))
        painter.drawLine(int(cx + gap), int(line_y), int(cx + gap + line_len), int(line_y))

        painter.setClipping(False)
        painter.setPen(QPen(border, 1.0))
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.drawRoundedRect(rect, radius, radius)

        text_color = QColor("#f0d9af") if enabled else QColor("#776a5b")
        painter.setPen(text_color)
        painter.setFont(
            tracked_font(
                max(10.0, 14.0 * self._scale),
                max(1.2, 3.1 * self._scale),
                bold=False,
            )
        )
        painter.drawText(self.rect(), Qt.AlignmentFlag.AlignCenter, "POLYMORPH")


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
        for layout, margins, spacing in self.layout_specs:
            l, t, r, b = margins
            layout.setContentsMargins(
                round(l * scale), round(t * scale), round(r * scale), round(b * scale)
            )
            layout.setSpacing(max(0, round(spacing * scale)))
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
