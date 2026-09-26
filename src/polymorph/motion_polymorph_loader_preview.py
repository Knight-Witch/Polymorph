from __future__ import annotations

import math

from PySide6.QtCore import QPointF, QRectF, Qt, QTimer, QSize
from PySide6.QtGui import QColor, QBrush, QImage, QLinearGradient, QPainter, QPainterPath, QPen
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
from .resources import asset_path


CYAN = QColor("#00dcff")
ELECTRIC_BLUE = QColor("#2f7dff")
VIOLET = QColor("#8155ff")
MAGENTA = QColor("#ef3dff")
DIM_RING = QColor("#151a2b")


def _mix(a: QColor, b: QColor, amount: float) -> QColor:
    amount = clamp(amount)
    return QColor(
        round(a.red() + (b.red() - a.red()) * amount),
        round(a.green() + (b.green() - a.green()) * amount),
        round(a.blue() + (b.blue() - a.blue()) * amount),
        round(a.alpha() + (b.alpha() - a.alpha()) * amount),
    )


def _side_color(degrees: float) -> QColor:
    # Screen-left stays cyan/blue and screen-right resolves violet/magenta.
    x = math.cos(math.radians(degrees))
    amount = (x + 1.0) * 0.5
    cool = _mix(CYAN, ELECTRIC_BLUE, 0.34)
    warm = _mix(VIOLET, MAGENTA, 0.48)
    return _mix(cool, warm, amount)


def _diamond(center: QPointF, radius: float) -> QPainterPath:
    # Cardinal vertices create a true 45-degree diamond instead of a checkbox/square.
    points = [polar(center, radius, i * 90.0) for i in range(4)]
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


def _ring(center: QPointF, radius: float) -> QPainterPath:
    path = QPainterPath()
    path.addEllipse(center, radius, radius)
    return path


def _gradient(center: QPointF, radius: float) -> QLinearGradient:
    gradient = QLinearGradient(center.x() - radius, center.y(), center.x() + radius, center.y())
    gradient.setColorAt(0.0, CYAN)
    gradient.setColorAt(0.30, ELECTRIC_BLUE)
    gradient.setColorAt(0.60, VIOLET)
    gradient.setColorAt(1.0, MAGENTA)
    return gradient


def _gradient_path(
    painter: QPainter,
    path: QPainterPath,
    center: QPointF,
    radius: float,
    *,
    intensity: float = 1.0,
    core_width: float = 1.25,
    spread: float = 1.0,
) -> None:
    if intensity <= 0.001:
        return
    painter.save()
    painter.setBrush(Qt.BrushStyle.NoBrush)
    brush = QBrush(_gradient(center, radius))
    passes = (
        (10.0 * spread, 0.055),
        (6.5 * spread, 0.095),
        (4.0 * spread, 0.17),
        (2.25 * spread, 0.34),
    )
    for width, opacity in passes:
        painter.setOpacity(opacity * intensity)
        painter.setPen(QPen(brush, max(core_width, width), Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap, Qt.PenJoinStyle.RoundJoin))
        painter.drawPath(path)
    painter.setOpacity(min(1.0, 0.94 * intensity))
    painter.setPen(QPen(brush, max(0.75, core_width), Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap, Qt.PenJoinStyle.RoundJoin))
    painter.drawPath(path)
    painter.restore()


def _polyline(points: list[QPointF]) -> QPainterPath:
    path = QPainterPath()
    path.moveTo(points[0])
    for point in points[1:]:
        path.lineTo(point)
    return path


class PolymorphLoaderPreview

class PolymorphLoaderPreview(ArcaneLoaderBase):
    """Standalone visual prototype for the deferred Polymorph working animation."""

    def __init__(self, rune_family: str, parent=None) -> None:
        super().__init__(rune_family, parent)
        self.setMinimumSize(520, 520)
        self.setMaximumSize(16777215, 16777215)
        self.progress = 0.68
        self.motion_speed = 1.0
        self.motion_paused = False
        self._load_exact_emblem()

    def _load_exact_emblem(self) -> bool:
        exact_path = asset_path("KW_EMBLEM_PATH.svg")
        if not exact_path.is_file():
            return False
        return self.load_emblem(str(exact_path))

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
        center = QPointF(self.width() / 2.0, self.height() / 2.0 - side * 0.010)
        outer = side * 0.405
        t = self._time()

        self._draw_outer_progress(painter, center, outer)
        self._draw_rune_band(painter, center, outer, t)
        self._draw_cardinal_ornaments(painter, center, outer, t)
        self._draw_ornate_geometry(painter, center, outer, t)
        self._draw_emblem_materialize(painter, center, outer, t)
        painter.end()

    def _draw_outer_progress(self, painter: QPainter, center: QPointF, radius: float) -> None:
        track = _ring(center, radius)
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.setPen(QPen(DIM_RING, max(1.7, radius * 0.012), Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap))
        painter.drawPath(track)

        span = -360.0 * self.progress
        active = _arc(center, radius, 90.0, span)
        _gradient_path(
            painter,
            active,
            center,
            radius,
            intensity=1.28,
            core_width=max(1.7, radius * 0.010),
            spread=1.15,
        )

        if 0.01 < self.progress < 0.995:
            head_degrees = -90.0 + 360.0 * self.progress
            head = polar(center, radius, head_degrees)
            color = _side_color(head_degrees)
            for dot_radius, opacity in ((8.0, 24), (5.2, 50), (2.7, 130)):
                painter.setPen(Qt.PenStyle.NoPen)
                painter.setBrush(alpha(color, opacity))
                painter.drawEllipse(head, dot_radius, dot_radius)
            painter.setBrush(WHITE)
            painter.drawEllipse(head, 1.55, 1.55)

    def _draw_rune_band(self, painter: QPainter, center: QPointF, outer: float, t: float) -> None:
        band_outer = outer * 0.865
        band_inner = outer * 0.705
        for radius, width, intensity in ((band_outer, 1.35, 0.94), (band_inner, 1.15, 0.82)):
            _gradient_path(
                painter,
                _ring(center, radius),
                center,
                outer,
                intensity=intensity,
                core_width=width,
                spread=0.76,
            )

        count = 22
        rune_radius = (band_outer + band_inner) * 0.5
        angle = -90.0 + t * 5.4
        for slot in range(count):
            degrees = angle + slot * 360.0 / count
            color = _side_color(degrees)
            pulse = 0.90 + 0.16 * math.sin(t * 1.65 + slot * 0.72)
            rune = ELDER_FUTHARK[(slot * 5 + 2) % len(ELDER_FUTHARK)]
            self.runes.draw(
                painter,
                rune,
                polar(center, rune_radius, degrees),
                max(12.0, outer * 0.062),
                degrees + 90.0,
                color=color,
                core=_mix(color, WHITE, 0.58),
                intensity=pulse,
                spread=0.58,
            )

    def _draw_cardinal_ornaments(self, painter: QPainter, center: QPointF, outer: float, t: float) -> None:
        node_radius = outer * 0.865
        marker_size = max(13.0, outer * 0.070)
        breathe = 0.92 + 0.08 * (0.5 + 0.5 * math.sin(t * 1.45))

        for degrees in (-90.0, 0.0, 90.0, 180.0):
            position = polar(center, node_radius, degrees)
            color = _side_color(degrees)
            glow_path(
                painter,
                _diamond(position, marker_size),
                color,
                core=_mix(color, WHITE, 0.72),
                intensity=1.12 * breathe,
                core_width=1.25,
                spread=0.76,
            )

            inner = polar(center, node_radius + marker_size * 0.95, degrees)
            outer_point = polar(center, outer * 0.975, degrees)
            path = QPainterPath(inner)
            path.lineTo(outer_point)
            glow_path(
                painter,
                path,
                color,
                core=_mix(color, WHITE, 0.50),
                intensity=0.70,
                core_width=0.92,
                spread=0.52,
            )

        # Cascading luminous dot trails at the top and bottom, matching the approved mockup language.
        for degrees in (-90.0, 90.0):
            color = _side_color(degrees)
            start = node_radius + marker_size * 1.55
            for index in range(6):
                distance = start + index * outer * 0.038
                point = polar(center, distance, degrees)
                size = max(1.15, outer * (0.016 - index * 0.0018))
                opacity = max(42, 235 - index * 31)
                painter.setPen(Qt.PenStyle.NoPen)
                painter.setBrush(alpha(color, opacity))
                painter.drawEllipse(point, size, size)
                if index < 3:
                    painter.setBrush(alpha(WHITE, opacity * 0.62))
                    painter.drawEllipse(point, max(0.72, size * 0.38), max(0.72, size * 0.38))

        # Side line extensions make the cardinal diamonds read as tech nodes rather than floating ornaments.
        for degrees in (0.0, 180.0):
            color = _side_color(degrees)
            a = polar(center, node_radius + marker_size * 1.15, degrees)
            b = polar(center, outer * 1.075, degrees)
            glow_path(
                painter,
                _polyline([a, b]),
                color,
                core=_mix(color, WHITE, 0.48),
                intensity=0.62,
                core_width=0.85,
                spread=0.46,
            )

    def _draw_ornate_geometry(self, painter: QPainter, center: QPointF, outer: float, t: float) -> None:
        pulse = 0.88 + 0.12 * (0.5 + 0.5 * math.sin(t * 1.22))

        def half_frame(side: int, scale: float, inset: float) -> QPainterPath:
            sx = float(side)
            rx = outer * 0.54 * scale
            ry = outer * 0.67 * scale
            points = [
                QPointF(center.x(), center.y() - ry),
                QPointF(center.x() + sx * rx * 0.58, center.y() - ry * 0.72),
                QPointF(center.x() + sx * rx * 0.58, center.y() - ry * 0.36),
                QPointF(center.x() + sx * rx * (0.94 - inset), center.y()),
                QPointF(center.x() + sx * rx * 0.58, center.y() + ry * 0.36),
                QPointF(center.x() + sx * rx * 0.58, center.y() + ry * 0.72),
                QPointF(center.x(), center.y() + ry),
            ]
            return _polyline(points)

        for side, color in ((-1, _mix(CYAN, ELECTRIC_BLUE, 0.34)), (1, _mix(VIOLET, MAGENTA, 0.50))):
            glow_path(
                painter,
                half_frame(side, 1.0, 0.0),
                color,
                core=_mix(color, WHITE, 0.50),
                intensity=0.88 * pulse,
                core_width=1.10,
                spread=0.64,
            )
            glow_path(
                painter,
                half_frame(side, 0.90, 0.055),
                color,
                core=_mix(color, WHITE, 0.44),
                intensity=0.55 * pulse,
                core_width=0.82,
                spread=0.48,
            )

            # Small paired diamonds beside the emblem, present in the visual mockup but intentionally restrained.
            x = center.x() + side * outer * 0.555
            for y_offset, size in ((-outer * 0.060, outer * 0.024), (outer * 0.018, outer * 0.019)):
                glow_path(
                    painter,
                    _diamond(QPointF(x, center.y() + y_offset), size),
                    color,
                    core=_mix(color, WHITE, 0.58),
                    intensity=0.78,
                    core_width=0.82,
                    spread=0.46,
                )

            # Extra straight diagonal rails echo the mockup's ornate, technical linework without adding noisy curves.
            upper_a = QPointF(center.x() + side * outer * 0.31, center.y() - outer * 0.50)
            upper_b = QPointF(center.x() + side * outer * 0.50, center.y() - outer * 0.37)
            lower_a = QPointF(center.x() + side * outer * 0.31, center.y() + outer * 0.50)
            lower_b = QPointF(center.x() + side * outer * 0.50, center.y() + outer * 0.37)
            for a, b in ((upper_a, upper_b), (lower_a, lower_b)):
                glow_path(
                    painter,
                    _polyline([a, b]),
                    color,
                    core=_mix(color, WHITE, 0.46),
                    intensity=0.54,
                    core_width=0.76,
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

    def _draw_emblem_materialize(self, painter: QPainter, center: QPointF, outer: float, t: float) -> None:
        rendered = self._emblem_image(outer * 1.40)
        if rendered is None:
            return
        image, width, height = rendered
        dest = QRectF(center.x() - width / 2.0, center.y() - height / 2.0, width, height)
        reveal = smoothstep(0.01, 0.97, self.progress)
        reveal_y = dest.top() + dest.height() * reveal

        if reveal > 0.001:
            painter.save()
            painter.setClipRect(
                QRectF(
                    dest.left() - 14.0,
                    dest.top() - 14.0,
                    dest.width() + 28.0,
                    max(1.0, reveal_y - dest.top() + 14.0),
                )
            )
            # Keep the exact SVG crisp; only the bloom copies move around it.
            for ox, oy in ((-3.0, 0.0), (3.0, 0.0), (0.0, -3.0), (0.0, 3.0), (-2.0, -2.0), (2.0, 2.0)):
                painter.setOpacity(0.050 + 0.050 * reveal)
                painter.drawImage(dest.translated(ox, oy), image)
            painter.setOpacity(1.0)
            painter.drawImage(dest, image)
            painter.restore()

        if 0.01 < reveal < 0.998:
            self._draw_materialize_front(painter, dest, image, reveal_y, t)

    def _active_columns(self, image: QImage, image_y: int) -> list[int]:
        columns: list[int] = []
        step = max(2, image.width() // 70)
        band = max(2, image.height() // 90)
        for px in range(0, image.width(), step):
            active = False
            for py in range(max(0, image_y - band), min(image.height(), image_y + band + 1), max(1, band // 2)):
                if image.pixelColor(px, py).alpha() >= 28:
                    active = True
                    break
            if active:
                columns.append(px)
        return columns

    def _draw_materialize_front(self, painter: QPainter, dest: QRectF, image: QImage, reveal_y: float, t: float) -> None:
        local_y = clamp((reveal_y - dest.top()) / max(1.0, dest.height()))
        image_y = max(0, min(image.height() - 1, round(local_y * (image.height() - 1))))
        columns = self._active_columns(image, image_y)
        if not columns:
            return

        trail = max(46.0, dest.height() * 0.25)
        painter.save()
        painter.setPen(Qt.PenStyle.NoPen)

        # A few vertical data-light streaks extend below the moving materialization edge.
        streak_count = min(14, max(5, len(columns) // 3))
        for index in range(streak_count):
            px = columns[(index * 7 + 3) % len(columns)]
            x_frac = px / max(1, image.width() - 1)
            x = dest.left() + x_frac * dest.width()
            phase = (index * 0.173 + t * 0.17) % 1.0
            length = trail * (0.22 + 0.62 * phase)
            color = _mix(CYAN, MAGENTA, x_frac)
            path = QPainterPath(QPointF(x, reveal_y + 1.0))
            path.lineTo(QPointF(x, reveal_y + length))
            glow_path(
                painter,
                path,
                color,
                core=_mix(color, WHITE, 0.48),
                intensity=0.28 * (1.0 - phase * 0.45),
                core_width=0.62 + (index % 3) * 0.18,
                spread=0.48,
            )

        # Sparkles and tiny data pixels form directly around the moving reveal edge.
        for index in range(86):
            px = columns[(index * 11 + index // 5) % len(columns)]
            x_frac = px / max(1, image.width() - 1)
            phase = (index * 0.61803398875 + t * (0.13 + (index % 7) * 0.006)) % 1.0
            jitter = math.sin(index * 2.73 + t * 2.0) * dest.width() * 0.012
            x = dest.left() + x_frac * dest.width() + jitter
            y = reveal_y + (phase - 0.14) * trail
            fade = max(0.0, 1.0 - phase) ** 1.30
            color = _mix(CYAN, MAGENTA, x_frac)
            size = 0.9 + (index % 5) * 0.52
            opacity = 80 + 175 * fade
            painter.setBrush(alpha(color, opacity))

            if index % 6 == 0:
                spark = QPainterPath()
                spark.moveTo(x, y - size * 3.2)
                spark.lineTo(x + size * 0.58, y - size * 0.58)
                spark.lineTo(x + size * 3.2, y)
                spark.lineTo(x + size * 0.58, y + size * 0.58)
                spark.lineTo(x, y + size * 3.2)
                spark.lineTo(x - size * 0.58, y + size * 0.58)
                spark.lineTo(x - size * 3.2, y)
                spark.lineTo(x - size * 0.58, y - size * 0.58)
                spark.closeSubpath()
                painter.drawPath(spark)
                painter.setBrush(alpha(WHITE, min(255, opacity * 1.12)))
                painter.drawEllipse(QPointF(x, y), max(0.60, size * 0.34), max(0.60, size * 0.34))
            elif index % 4 == 0:
                painter.drawEllipse(QPointF(x, y), size, size)
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
            "Isolated loader study using the exact supplied Knight Witch SVG. "
            "The outer ring and logo reveal follow progress; rune/geometry motion loops independently."
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
