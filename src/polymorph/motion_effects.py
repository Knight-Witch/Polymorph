from __future__ import annotations

import math

from PySide6.QtCore import QPointF, QRectF, Qt, QTimer
from PySide6.QtGui import QColor, QBrush, QFont, QFontDatabase, QLinearGradient, QPainter, QPainterPath, QPen, QTransform
from PySide6.QtWidgets import QWidget

from .resources import asset_path

IVORY = QColor("#fffaf2")
GOLD = QColor("#e7c985")
MID_GOLD = QColor("#bda46d")
CRIMSON = QColor("#d21f32")
DEEP_RED = QColor("#7e0d18")

ELDER_FUTHARK = tuple("ᚠᚢᚦᚨᚱᚲᚷᚹᚺᚾᛁᛃᛇᛈᛉᛋᛏᛒᛖᛗᛚᛜᛞᛟ")
DESIGNATED_RUNES = ("ᚠ", "ᚨ", "ᛉ", "ᛏ", "ᛞ", "ᛟ")


def alpha(color: QColor, value: float) -> QColor:
    out = QColor(color)
    out.setAlpha(max(0, min(255, round(value))))
    return out


def clamp(value: float, low: float = 0.0, high: float = 1.0) -> float:
    return max(low, min(high, value))


def smoothstep(edge0: float, edge1: float, value: float) -> float:
    if edge0 == edge1:
        return 1.0 if value >= edge1 else 0.0
    x = clamp((value - edge0) / (edge1 - edge0))
    return x * x * (3.0 - 2.0 * x)


def polar(center: QPointF, radius: float, degrees: float) -> QPointF:
    angle = math.radians(degrees)
    return QPointF(
        center.x() + math.cos(angle) * radius,
        center.y() + math.sin(angle) * radius,
    )


def lerp_point(a: QPointF, b: QPointF, amount: float) -> QPointF:
    return QPointF(a.x() + (b.x() - a.x()) * amount, a.y() + (b.y() - a.y()) * amount)


def polygon_path(center: QPointF, radius: float, sides: int, angle: float) -> QPainterPath:
    points = [polar(center, radius, angle + i * 360.0 / sides) for i in range(sides)]
    path = QPainterPath()
    path.moveTo(points[0])
    for point in points[1:]:
        path.lineTo(point)
    path.closeSubpath()
    return path


def arc_path(center: QPointF, radius: float, start: float, span: float) -> QPainterPath:
    rect = QRectF(center.x() - radius, center.y() - radius, radius * 2, radius * 2)
    path = QPainterPath()
    path.arcMoveTo(rect, start)
    path.arcTo(rect, start, span)
    return path


def glow_path(
    painter: QPainter,
    path: QPainterPath,
    color: QColor,
    *,
    core: QColor = IVORY,
    intensity: float = 1.0,
    core_width: float = 1.0,
    spread: float = 1.0,
) -> None:
    if intensity <= 0.001:
        return
    spread = max(0.25, spread)
    passes = (
        (13.5 * spread, 8),
        (9.5 * spread, 12),
        (6.5 * spread, 18),
        (4.2 * spread, 30),
        (2.7 * spread, 52),
        (1.65 * spread, 88),
    )
    painter.setBrush(Qt.BrushStyle.NoBrush)
    for width, opacity in passes:
        painter.setPen(
            QPen(
                alpha(color, opacity * intensity),
                max(core_width, width),
                Qt.PenStyle.SolidLine,
                Qt.PenCapStyle.RoundCap,
                Qt.PenJoinStyle.RoundJoin,
            )
        )
        painter.drawPath(path)
    painter.setPen(
        QPen(
            alpha(core, 235 * intensity),
            max(0.65, core_width),
            Qt.PenStyle.SolidLine,
            Qt.PenCapStyle.RoundCap,
            Qt.PenJoinStyle.RoundJoin,
        )
    )
    painter.drawPath(path)


def glow_ellipse(
    painter: QPainter,
    center: QPointF,
    radius: float,
    color: QColor,
    *,
    intensity: float = 1.0,
    core_width: float = 1.0,
    spread: float = 1.0,
) -> None:
    path = QPainterPath()
    path.addEllipse(center, radius, radius)
    glow_path(
        painter,
        path,
        color,
        intensity=intensity,
        core_width=core_width,
        spread=spread,
    )


def comet(
    painter: QPainter,
    tail: QPointF,
    head: QPointF,
    color: QColor,
    *,
    intensity: float,
    spread: float,
) -> None:
    if intensity <= 0.001:
        return
    gradient = QLinearGradient(tail, head)
    gradient.setColorAt(0.0, QColor(color.red(), color.green(), color.blue(), 0))
    gradient.setColorAt(0.45, alpha(color, 38 * intensity))
    gradient.setColorAt(0.78, alpha(color, 135 * intensity))
    gradient.setColorAt(1.0, alpha(IVORY, 255 * intensity))
    for width, opacity in (
        (14.0 * spread, 0.17),
        (9.0 * spread, 0.28),
        (5.2 * spread, 0.48),
        (2.6 * spread, 0.78),
        (1.1, 1.0),
    ):
        brush = QBrush(gradient)
        pen = QPen(brush, max(0.8, width * opacity), Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap)
        painter.setPen(pen)
        painter.drawLine(tail, head)

    for radius, opacity in (
        (9.0 * spread, 15),
        (6.0 * spread, 25),
        (3.8 * spread, 55),
        (2.0 * spread, 125),
    ):
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(alpha(color, opacity * intensity))
        painter.drawEllipse(head, radius, radius)
    painter.setBrush(alpha(IVORY, 245 * intensity))
    painter.drawEllipse(head, 1.35, 1.35)


class Clock:
    def __init__(self, owner: QWidget) -> None:
        self.t = 0.0
        self.owner = owner
        self.timer = QTimer(owner)
        self.timer.setInterval(16)
        self.timer.setTimerType(Qt.TimerType.PreciseTimer)
        self.timer.timeout.connect(self.tick)
        self.timer.start()

    def tick(self) -> None:
        self.t = (self.t + 0.016) % 100000.0
        self.owner.update()


def load_runic_font() -> str:
    path = asset_path("fonts/NotoSansRunic-Regular.ttf")
    if path.is_file():
        font_id = QFontDatabase.addApplicationFont(str(path))
        if font_id >= 0:
            families = QFontDatabase.applicationFontFamilies(font_id)
            if families:
                return families[0]
    return "Segoe UI Historic"


class RunePainter:
    def __init__(self, family: str) -> None:
        self.family = family
        self._cache: dict[tuple[str, int], QPainterPath] = {}

    def path(self, rune: str, size: float) -> QPainterPath:
        key = (rune, max(6, round(size)))
        cached = self._cache.get(key)
        if cached is not None:
            return QPainterPath(cached)
        font = QFont(self.family)
        font.setPixelSize(key[1])
        font.setWeight(QFont.Weight.Normal)
        path = QPainterPath()
        path.addText(QPointF(0.0, 0.0), font, rune)
        bounds = path.boundingRect()
        transform = QTransform()
        transform.translate(-bounds.center().x(), -bounds.center().y())
        centered = transform.map(path)
        self._cache[key] = centered
        return QPainterPath(centered)

    def draw(
        self,
        painter: QPainter,
        rune: str,
        position: QPointF,
        size: float,
        rotation: float,
        *,
        color: QColor = GOLD,
        intensity: float = 1.0,
        spread: float = 0.72,
    ) -> None:
        painter.save()
        painter.translate(position)
        painter.rotate(rotation)
        path = self.path(rune, size)
        glow_path(
            painter,
            path,
            color,
            intensity=intensity,
            core_width=max(0.65, size * 0.055),
            spread=spread,
        )
        painter.restore()

    def ring(
        self,
        painter: QPainter,
        center: QPointF,
        radius: float,
        angle: float,
        *,
        count: int,
        size: float,
        intensity: float,
        color: QColor,
        offset: int = 0,
    ) -> None:
        for i in range(count):
            degrees = angle + i * 360.0 / count
            rune = ELDER_FUTHARK[(i + offset) % len(ELDER_FUTHARK)]
            self.draw(
                painter,
                rune,
                polar(center, radius, degrees),
                size,
                degrees + 90,
                color=color,
                intensity=intensity,
            )
