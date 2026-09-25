from __future__ import annotations

import math

from PySide6.QtCore import QPointF, QRectF, Qt, QTimer, QSize
from PySide6.QtGui import QColor, QImage, QPainter, QPainterPath, QPen
from PySide6.QtWidgets import (
    QCheckBox,
    QFrame,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QSlider,
    QVBoxLayout,
    QWidget,
)

from .motion_effects import ELDER_FUTHARK, WHITE, alpha, clamp, glow_path, polar, smoothstep
from .motion_loader_base import ArcaneLoaderBase


CYAN = QColor("#23d7ff")
BLUE = QColor("#5577ff")
VIOLET = QColor("#8b5cff")
MAGENTA = QColor("#dc4dff")
DIM_RING = QColor("#22283a")


def _mix(a: QColor, b: QColor, amount: float) -> QColor:
    amount = clamp(amount)
    return QColor(
        round(a.red() + (b.red() - a.red()) * amount),
        round(a.green() + (b.green() - a.green()) * amount),
        round(a.blue() + (b.blue() - a.blue()) * amount),
        round(a.alpha() + (b.alpha() - a.alpha()) * amount),
    )


def _side_color(degrees: float) -> QColor:
    # Left side resolves cyan/blue, right side violet/magenta.
    x = math.cos(math.radians(degrees))
    amount = (x + 1.0) * 0.5
    cool = _mix(CYAN, BLUE, 0.38)
    warm = _mix(VIOLET, MAGENTA, 0.52)
    return _mix(cool, warm, amount)


def _diamond(center: QPointF, radius: float, rotation: float = 0.0) -> QPainterPath:
    points = [polar(center, radius, rotation + 45.0 + i * 90.0) for i in range(4)]
    path = QPainterPath()
    path.moveTo(points[0])
    for point in points[1:]:
        path.lineTo(point)
    path.closeSubpath()
    return path


def _arc(center: QPointF, radius: float, start: float, span: float) -> QPainterPath:
    rect = QRectF(center.x() - radius, center.y() - radius, radius * 2.0, radius * 2.0)
    path = QPainterPath()
    path.arcMoveTo(rect, start)
    path.arcTo(rect, start, span)
    return path


class PolymorphLoaderPreview(ArcaneLoaderBase):
    """Standalone visual prototype for the deferred Polymorph working animation."""

    def __init__(self, rune_family: str, parent=None) -> None:
        super().__init__(rune_family, parent)
        self.setMinimumSize(520, 520)
        self.setMaximumSize(16777215, 16777215)
        self.progress = 0.68
        self.motion_speed = 1.0
        self.motion_paused = False

    def sizeHint(self) -> QSize:  # noqa: N802
        return QSize(660, 660)

    def set_motion_speed(self, value: float) -> None:
        self.motion_speed = max(0.05, float(value))
        self.update()

    def set_motion_paused(self, paused: bool) -> None:
        self.motion_paused = bool(paused)
        self.update()

    def _time(self) -> float:
        return 0.0 if self.motion_paused else self.clock.t * self.motion_speed

    def paintEvent(self, event) -> None:  # noqa: N802
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing, True)
        painter.fillRect(self.rect(), QColor("#000000"))

        side = min(self.width(), self.height())
        center = QPointF(self.width() / 2.0, self.height() / 2.0 - side * 0.012)
        outer = side * 0.405
        t = self._time()

        self._draw_outer_progress(painter, center, outer)
        self._draw_cardinal_nodes(painter, center, outer * 0.925)
        self._draw_rune_ring(painter, center, outer * 0.78, t)
        self._draw_segmented_ring(painter, center, outer * 0.64, t)
        self._draw_tech_diamond(painter, center, outer * 0.585, t)
        self._draw_emblem_materialize(painter, center, outer * 0.57, t)
        painter.end()

    def _draw_outer_progress(self, painter: QPainter, center: QPointF, radius: float) -> None:
        track = _arc(center, radius, 90.0, -360.0)
        painter.setPen(QPen(DIM_RING, max(1.5, radius * 0.010), Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap))
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.drawPath(track)

        segments = 108
        active = max(0, min(segments, round(self.progress * segments)))
        step = 360.0 / segments
        gap = 0.62
        for index in range(active):
            start = 90.0 - index * step
            mid = start - step * 0.5
            color = _side_color(mid)
            path = _arc(center, radius, start, -(step - gap))
            glow_path(
                painter,
                path,
                color,
                core=_mix(color, WHITE, 0.48),
                intensity=0.88,
                core_width=max(1.15, radius * 0.006),
                spread=0.72,
            )

    def _draw_cardinal_nodes(self, painter: QPainter, center: QPointF, radius: float) -> None:
        for degrees in (-90.0, 0.0, 90.0, 180.0):
            position = polar(center, radius, degrees)
            color = _side_color(degrees)
            marker = _diamond(position, max(7.0, radius * 0.040), 0.0)
            glow_path(
                painter,
                marker,
                color,
                core=_mix(color, WHITE, 0.56),
                intensity=0.68,
                core_width=1.0,
                spread=0.56,
            )

    def _draw_rune_ring(self, painter: QPainter, center: QPointF, radius: float, t: float) -> None:
        count = 20
        angle = -90.0 + t * 7.5
        for slot in range(count):
            degrees = angle + slot * 360.0 / count
            color = _side_color(degrees)
            pulse = 0.78 + 0.18 * math.sin(t * 1.7 + slot * 0.83)
            rune = ELDER_FUTHARK[(slot * 5 + 2) % len(ELDER_FUTHARK)]
            self.runes.draw(
                painter,
                rune,
                polar(center, radius, degrees),
                max(11.0, radius * 0.077),
                degrees + 90.0,
                color=color,
                core=_mix(color, WHITE, 0.50),
                intensity=pulse,
                spread=0.44,
            )

    def _draw_segmented_ring(self, painter: QPainter, center: QPointF, radius: float, t: float) -> None:
        rotation = -t * 10.0
        for index in range(8):
            start = rotation + index * 45.0 + 8.0
            color = _side_color(start + 14.0)
            path = _arc(center, radius, start, 28.0)
            glow_path(
                painter,
                path,
                color,
                core=_mix(color, WHITE, 0.42),
                intensity=0.48,
                core_width=0.95,
                spread=0.46,
            )

    def _draw_tech_diamond(self, painter: QPainter, center: QPointF, radius: float, t: float) -> None:
        breathe = 0.90 + 0.10 * (0.5 + 0.5 * math.sin(t * 1.35))
        points = [polar(center, radius, -90.0 + i * 90.0) for i in range(4)]
        for index in range(4):
            a = points[index]
            b = points[(index + 1) % 4]
            dx = b.x() - a.x()
            dy = b.y() - a.y()
            start = QPointF(a.x() + dx * 0.10, a.y() + dy * 0.10)
            end = QPointF(a.x() + dx * 0.90, a.y() + dy * 0.90)
            path = QPainterPath(start)
            path.lineTo(end)
            color = _side_color(-90.0 + index * 90.0 + 45.0)
            glow_path(
                painter,
                path,
                color,
                core=_mix(color, WHITE, 0.50),
                intensity=0.38 * breathe,
                core_width=0.82,
                spread=0.44,
            )

        # A few straight circuit rails preserve the cyber-witch line language without clutter.
        rail_radius = radius * 0.95
        for degrees in (0.0, 90.0, 180.0, 270.0):
            color = _side_color(degrees)
            inner = polar(center, rail_radius * 0.87, degrees)
            outer = polar(center, rail_radius * 1.04, degrees)
            path = QPainterPath(inner)
            path.lineTo(outer)
            glow_path(
                painter,
                path,
                color,
                core=_mix(color, WHITE, 0.45),
                intensity=0.42,
                core_width=0.85,
                spread=0.42,
            )

    def _emblem_image(self, target_height: float) -> tuple[QImage, float, float] | None:
        if self.emblem is None:
            return None
        view = self.emblem.viewBoxF()
        if view.height() <= 0.0 or view.width() <= 0.0:
            return None
        ratio = view.width() / view.height()
        height = max(80.0, target_height)
        width = height * ratio
        scale = 2.0
        image = QImage(
            max(1, round(width * scale)),
            max(1, round(height * scale)),
            QImage.Format.Format_ARGB32_Premultiplied,
        )
        image.fill(Qt.GlobalColor.transparent)
        ip = QPainter(image)
        ip.setRenderHint(QPainter.RenderHint.Antialiasing, True)
        self.emblem.render(ip, QRectF(0.0, 0.0, image.width(), image.height()))
        ip.setCompositionMode(QPainter.CompositionMode.CompositionMode_SourceIn)
        ip.fillRect(image.rect(), WHITE)
        ip.end()
        return image, width, height

    def _draw_emblem_materialize(self, painter: QPainter, center: QPointF, radius: float, t: float) -> None:
        rendered = self._emblem_image(radius * 1.52)
        if rendered is None:
            return
        image, width, height = rendered
        dest = QRectF(center.x() - width / 2.0, center.y() - height / 2.0, width, height)
        reveal = smoothstep(0.015, 0.96, self.progress)
        reveal_y = dest.top() + dest.height() * reveal

        if reveal > 0.001:
            painter.save()
            painter.setClipRect(QRectF(dest.left() - 8.0, dest.top() - 8.0, dest.width() + 16.0, max(1.0, reveal_y - dest.top() + 8.0)))
            for ox, oy in ((-2.0, 0.0), (2.0, 0.0), (0.0, -2.0), (0.0, 2.0)):
                painter.setOpacity(0.035 + 0.07 * reveal)
                painter.drawImage(dest.translated(ox, oy), image)
            painter.setOpacity(1.0)
            painter.drawImage(dest, image)
            painter.restore()

        if 0.015 < reveal < 0.995:
            self._draw_materialize_sparks(painter, dest, image, reveal_y, t)

    def _draw_materialize_sparks(self, painter: QPainter, dest: QRectF, image: QImage, reveal_y: float, t: float) -> None:
        local_y = clamp((reveal_y - dest.top()) / max(1.0, dest.height()))
        image_y = round(local_y * (image.height() - 1))
        trail = max(28.0, dest.height() * 0.20)

        painter.save()
        painter.setPen(Qt.PenStyle.NoPen)
        for index in range(44):
            phase = (index * 0.61803398875 + t * (0.10 + (index % 5) * 0.007)) % 1.0
            x_frac = (index * 0.754877666 + 0.17) % 1.0
            px = max(0, min(image.width() - 1, round(x_frac * (image.width() - 1))))
            probe_y = max(0, min(image.height() - 1, image_y + round((phase - 0.32) * image.height() * 0.035)))
            if image.pixelColor(px, probe_y).alpha() < 32:
                continue
            x = dest.left() + x_frac * dest.width()
            y = reveal_y + phase * trail
            fade = (1.0 - phase) ** 1.45
            color = _mix(CYAN, MAGENTA, x_frac)
            size = 1.0 + (index % 4) * 0.55
            painter.setBrush(alpha(color, 190 * fade))
            if index % 5 == 0:
                spark = QPainterPath()
                spark.moveTo(x, y - size * 2.4)
                spark.lineTo(x + size * 0.62, y - size * 0.62)
                spark.lineTo(x + size * 2.4, y)
                spark.lineTo(x + size * 0.62, y + size * 0.62)
                spark.lineTo(x, y + size * 2.4)
                spark.lineTo(x - size * 0.62, y + size * 0.62)
                spark.lineTo(x - size * 2.4, y)
                spark.lineTo(x - size * 0.62, y - size * 0.62)
                spark.closeSubpath()
                painter.drawPath(spark)
            else:
                painter.drawRect(QRectF(x - size / 2.0, y - size / 2.0, size, size))
        painter.restore()


class PolymorphLoaderPage(QWidget):
    """Self-contained review page; no production Polymorph runtime is touched."""

    def __init__(self, rune_family: str, parent=None) -> None:
        super().__init__(parent)
        self._hold_ticks = 0

        root = QHBoxLayout(self)
        root.setContentsMargins(18, 18, 18, 18)
        root.setSpacing(18)

        stage = QFrame()
        stage.setObjectName("PolymorphPreviewStage")
        stage_layout = QVBoxLayout(stage)
        stage_layout.setContentsMargins(28, 22, 28, 22)
        title = QLabel("POLYMORPH LOADER PREVIEW")
        title.setObjectName("LabTitle")
        title.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        stage_layout.addWidget(title)
        subtitle = QLabel("ARCANE MATERIALIZATION / REVIEW ONLY")
        subtitle.setObjectName("LabSubtitle")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        stage_layout.addWidget(subtitle)

        self.preview = PolymorphLoaderPreview(rune_family)
        row = QHBoxLayout()
        row.addStretch()
        row.addWidget(self.preview, 1)
        row.addStretch()
        stage_layout.addLayout(row, 1)

        self.readout = QLabel("68%")
        self.readout.setObjectName("PreviewReadout")
        self.readout.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        stage_layout.addWidget(self.readout)
        self.status = QLabel("POLYMORPHING…")
        self.status.setObjectName("PreviewStatus")
        self.status.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        stage_layout.addWidget(self.status)
        root.addWidget(stage, 1)

        panel = QFrame()
        panel.setObjectName("Panel")
        panel.setFixedWidth(330)
        controls = QVBoxLayout(panel)
        controls.setContentsMargins(18, 18, 18, 18)
        controls.setSpacing(10)

        heading = QLabel("PREVIEW CONTROLS")
        heading.setObjectName("Section")
        controls.addWidget(heading)

        note = QLabel(
            "This page is isolated from the existing Motion Lab scene builder. "
            "Rune motion and inner geometry loop continuously; logo materialization and the outer ring follow progress."
        )
        note.setObjectName("Note")
        note.setWordWrap(True)
        controls.addWidget(note)

        self.auto = QCheckBox("Auto-loop progress")
        self.auto.setChecked(True)
        controls.addWidget(self.auto)

        self.freeze = QCheckBox("Freeze ring / rune motion")
        self.freeze.toggled.connect(self.preview.set_motion_paused)
        controls.addWidget(self.freeze)

        controls.addWidget(QLabel("Progress"))
        self.progress = QSlider(Qt.Orientation.Horizontal)
        self.progress.setRange(0, 100)
        self.progress.setValue(68)
        self.progress.valueChanged.connect(self._progress_changed)
        controls.addWidget(self.progress)

        controls.addWidget(QLabel("Motion speed"))
        self.speed = QSlider(Qt.Orientation.Horizontal)
        self.speed.setRange(25, 200)
        self.speed.setValue(100)
        self.speed.valueChanged.connect(lambda value: self.preview.set_motion_speed(value / 100.0))
        controls.addWidget(self.speed)
        self.speed_label = QLabel("100%")
        self.speed_label.setObjectName("Note")
        self.speed.valueChanged.connect(lambda value: self.speed_label.setText(f"{value}%"))
        controls.addWidget(self.speed_label)

        replay = QPushButton("Replay materialization")
        replay.clicked.connect(self.replay)
        controls.addWidget(replay)
        controls.addStretch()
        root.addWidget(panel)

        self.timer = QTimer(self)
        self.timer.setInterval(34)
        self.timer.timeout.connect(self._tick)
        self.timer.start()

        self.setStyleSheet(
            "QFrame#PolymorphPreviewStage{background:#000000;border:1px solid #24283a;border-radius:6px} "
            "QLabel#PreviewReadout{font-size:17pt;font-weight:700;letter-spacing:1px;color:#f4f6ff;background:transparent} "
            "QLabel#PreviewStatus{font-size:8.5pt;font-weight:700;letter-spacing:2.4px;color:#8f96b7;background:transparent}"
        )
        self._progress_changed(self.progress.value())

    def _progress_changed(self, value: int) -> None:
        self.preview.set_progress(value / 100.0)
        self.readout.setText(f"{value}%")
        if value >= 100:
            self.status.setText("MATERIALIZED")
        elif value <= 0:
            self.status.setText("INITIALIZING…")
        else:
            self.status.setText("POLYMORPHING…")

    def replay(self) -> None:
        self._hold_ticks = 0
        self.progress.setValue(0)
        self.auto.setChecked(True)

    def _tick(self) -> None:
        if not self.auto.isChecked():
            return
        value = self.progress.value()
        if value >= 100:
            self._hold_ticks += 1
            if self._hold_ticks >= 35:
                self._hold_ticks = 0
                self.progress.setValue(0)
            return
        self._hold_ticks = 0
        step = max(1, round(self.speed.value() / 100.0))
        self.progress.setValue(min(100, value + step))
