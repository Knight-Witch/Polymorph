from __future__ import annotations

import base64
import math
import zlib

from PySide6.QtCore import QByteArray, QPointF, QRectF, Qt
from PySide6.QtGui import QColor, QImage, QLinearGradient, QPainter, QPainterPath, QPainterPathStroker, QPen, QRadialGradient
from PySide6.QtSvg import QSvgRenderer
from PySide6.QtWidgets import QWidget

from .motion_effects import (
    CRIMSON, ELDER_FUTHARK, GOLD, IVORY, MID_GOLD, DESIGNATED_RUNES, Clock, RunePainter,
    alpha, arc_path, clamp, comet, glow_ellipse, glow_path, lerp_point, polar, polygon_path, smoothstep,
)
from .resources import asset_path

class ArcaneLoaderBase(QWidget):
    VARIANTS = (
        "A — Transmutation",
        "B — Dense Runes",
        "C — Tracer Ritual",
        "D — Fractal Echo",
    )

    def __init__(self, rune_family: str, parent=None) -> None:
        super().__init__(parent)
        self.setFixedSize(500, 500)
        self.clock = Clock(self)
        self.runes = RunePainter(rune_family)
        self.variant = 0
        self.progress = 0.62
        self.glow = 1.0
        self.glow_spread = 1.0
        self.outer_rune_speed = 1.0
        self.inner_rune_speed = 1.0
        self.partial_speed = 1.0
        self.triangle_speed = 1.0
        self.hex_speed = 1.0
        self.trace_speed = 1.0
        self.flicker_speed = 1.0
        self.completion_start: float | None = None
        self.emblem: QSvgRenderer | None = None
        self.emblem_path = ""
        self.load_bundled_emblem()

    def load_bundled_emblem(self) -> bool:
        parts = [asset_path(f"kw_emblem.svg.zlib.b64.part{index:02d}") for index in range(1, 5)]
        if not all(part.is_file() for part in parts):
            return False
        try:
            packed_text = "".join(part.read_text(encoding="ascii") for part in parts)
            svg_bytes = zlib.decompress(base64.b64decode(packed_text))
        except (OSError, ValueError, zlib.error):
            return False
        renderer = QSvgRenderer(QByteArray(svg_bytes))
        if not renderer.isValid():
            return False
        self.emblem = renderer
        self.emblem_path = "bundled:kw_emblem.svg"
        self.update()
        return True

    def load_emblem(self, path: str) -> bool:
        renderer = QSvgRenderer(path)
        if not renderer.isValid():
            return False
        self.emblem = renderer
        self.emblem_path = path
        self.update()
        return True

    def set_progress(self, value: float) -> None:
        value = clamp(value)
        if value >= 0.999 and self.progress < 0.999:
            self.completion_start = self.clock.t
        elif value < 0.999:
            self.completion_start = None
        self.progress = value
        self.update()

    def completion_age(self) -> float | None:
        if self.completion_start is None or self.progress < 0.999:
            return None
        age = self.clock.t - self.completion_start
        if age < 0:
            age += 100000.0
        return age

    def grouped_flicker(self, group: int, *, offset: float = 0.0) -> float:
        t = self.clock.t * self.flicker_speed + offset
        wave = 0.5 + 0.5 * math.sin(t * (2.1 + group * 0.19) + group * 1.73)
        sharpened = wave**3
        return 0.36 + 0.64 * sharpened

    def cascade_level(self, index: int) -> float:
        period = 3.6 / max(0.2, self.flicker_speed)
        phase = self.clock.t % period
        delay = index * 0.24
        rise = smoothstep(delay, delay + 0.22, phase)
        fade_start = 2.05 + index * 0.20
        fall = 1.0 - smoothstep(fade_start, fade_start + 0.34, phase)
        return 0.18 + 0.82 * rise * fall

    def draw_arc_glow(self, painter: QPainter, center: QPointF, radius: float, start: float, span: float, color: QColor, intensity: float, width: float = 1.0) -> None:
        glow_path(painter, arc_path(center, radius, start, span), color, intensity=intensity, core_width=width, spread=self.glow_spread)

    def draw_partial_rune_band(self, painter: QPainter, satellite: QPointF, radius: float, rotation: float, window_center: float, *, span: float, offset: int, intensity: float) -> None:
        count = 24
        half = span / 2.0
        for i in range(count):
            degrees = rotation + i * 360.0 / count
            delta = (degrees - window_center + 180.0) % 360.0 - 180.0
            if abs(delta) > half:
                continue
            edge = 1.0 - smoothstep(half - 16.0, half, abs(delta))
            rune = ELDER_FUTHARK[(i + offset) % len(ELDER_FUTHARK)]
            self.runes.draw(painter, rune, polar(satellite, radius, degrees), 15.5, degrees + 90, color=GOLD, intensity=intensity * edge, spread=0.62 * self.glow_spread)

    def draw_glimmer_ring(self, painter: QPainter, center: QPointF, radius: float, t: float, intensity: float) -> None:
        count = 18
        for slot in range(count):
            duration = 1.55 + 0.17 * (slot % 5)
            clock = t + slot * 0.61
            cycle = math.floor(clock / duration)
            local = (clock / duration) - cycle
            opacity = math.sin(math.pi * local) ** 2
            if opacity < 0.025:
                continue
            rune_index = (slot * 7 + cycle * 5) % len(ELDER_FUTHARK)
            degrees = -90.0 + slot * 360.0 / count
            self.runes.draw(painter, ELDER_FUTHARK[rune_index], polar(center, radius, degrees), 12.0, degrees + 90, color=GOLD, intensity=intensity * opacity, spread=0.56 * self.glow_spread)

    def satellite_rune_indices(self, t: float) -> list[tuple[int, float]]:
        result: list[tuple[int, float]] = []
        used: set[int] = set()
        for index in range(3):
            duration = 1.65 + index * 0.21
            clock = t + index * 0.49
            cycle = math.floor(clock / duration)
            local = (clock / duration) - cycle
            rune_index = (cycle * 7 + index * 9 + 2) % len(ELDER_FUTHARK)
            while rune_index in used:
                rune_index = (rune_index + 1) % len(ELDER_FUTHARK)
            used.add(rune_index)
            opacity = 0.24 + 0.76 * (math.sin(math.pi * local) ** 0.62)
            result.append((rune_index, opacity))
        return result

    def tracer_clip(self, center: QPointF, radius: float, satellites: list[QPointF], partial_specs: list[tuple[QPointF, float, float, float]]) -> QPainterPath:
        clip = QPainterPath()
        clip.addEllipse(center, radius * 0.79, radius * 0.79)
        central = QPainterPath()
        central.addEllipse(center, radius * 0.31, radius * 0.31)
        clip = clip.subtracted(central)
        for satellite in satellites:
            block = QPainterPath()
            block.addEllipse(satellite, radius * 0.155, radius * 0.155)
            clip = clip.subtracted(block)
        stroker = QPainterPathStroker()
        stroker.setWidth(radius * 0.075)
        stroker.setCapStyle(Qt.PenCapStyle.RoundCap)
        for sat, arc_radius, start, span in partial_specs:
            clip = clip.subtracted(stroker.createStroke(arc_path(sat, arc_radius, start, span)))
        return clip

    def draw_spoke_tracers(self, painter: QPainter, center: QPointF, radius: float, angle: float, clip: QPainterPath, intensity: float) -> None:
        painter.save()
        painter.setClipPath(clip)
        phase = self.clock.t * 0.48 * self.trace_speed
        travel = 0.5 - 0.5 * math.cos(phase * math.tau)
        inward = math.sin(phase * math.tau) >= 0.0
        for i in range(6):
            outer = polar(center, radius * 0.74, angle + i * 60.0)
            head = lerp_point(outer, center, travel)
            tail_amount = max(0.0, travel - 0.20) if inward else min(1.0, travel + 0.20)
            tail = lerp_point(outer, center, tail_amount)
            comet(painter, tail, head, GOLD if i % 2 == 0 else CRIMSON, intensity=intensity, spread=self.glow_spread)
        painter.restore()

    def draw_progress_rings(self, painter: QPainter, center: QPointF, radius: float, completion: float) -> None:
        pulse = 1.0 + completion * (0.16 + 0.10 * math.sin(self.clock.t * 19.0))
        for ring_radius in (radius * 1.035, radius * 0.995):
            path = QPainterPath(); path.addEllipse(center, ring_radius, ring_radius)
            painter.setPen(QPen(alpha(MID_GOLD, 36 * self.glow), 1.0)); painter.setBrush(Qt.BrushStyle.NoBrush); painter.drawPath(path)
        span = 360.0 * self.progress
        outer_rect = QRectF(center.x() - radius * 1.035, center.y() - radius * 1.035, radius * 2.07, radius * 2.07)
        inner_rect = QRectF(center.x() - radius * 0.995, center.y() - radius * 0.995, radius * 1.99, radius * 1.99)
        for rect, span_sign, color in ((outer_rect, -span, GOLD), (inner_rect, span, CRIMSON)):
            arc = QPainterPath(); arc.arcMoveTo(rect, 90.0); arc.arcTo(rect, 90.0, span_sign)
            glow_path(painter, arc, color, intensity=self.glow * pulse, core_width=1.55, spread=1.15 * self.glow_spread)

    def draw_emblem(self, painter: QPainter, center: QPointF, radius: float, reveal: float) -> None:
        if reveal <= 0.001:
            return
        if self.emblem is None:
            glow_ellipse(painter, center, radius * 0.18 * reveal, GOLD, intensity=reveal * self.glow, spread=self.glow_spread)
            return
        width = max(24, round(radius * 0.34)); height = max(48, round(width * 2.0))
        image = QImage(width, height, QImage.Format.Format_ARGB32_Premultiplied); image.fill(Qt.GlobalColor.transparent)
        ip = QPainter(image); ip.setRenderHint(QPainter.RenderHint.Antialiasing, True); self.emblem.render(ip, QRectF(0, 0, width, height))
        ip.setCompositionMode(QPainter.CompositionMode.CompositionMode_SourceIn)
        tint = QLinearGradient(0, 0, 0, height); tint.setColorAt(0.0, IVORY); tint.setColorAt(0.48, GOLD); tint.setColorAt(1.0, IVORY); ip.fillRect(image.rect(), tint); ip.end()
        scale = 0.86 + 0.14 * smoothstep(0.0, 0.72, reveal); dw = width * scale; dh = height * scale
        dest = QRectF(center.x() - dw / 2, center.y() - dh / 2, dw, dh)
        clip_radius = math.hypot(dw, dh) * 0.58 * reveal
        clip = QPainterPath(); clip.addEllipse(center, clip_radius, clip_radius)
        painter.save(); painter.setClipPath(clip)
        for ox, oy in ((-3,0),(3,0),(0,-3),(0,3),(-2,-2),(2,2),(-2,2),(2,-2)):
            painter.setOpacity(0.055 * reveal * self.glow); painter.drawImage(dest.translated(ox, oy), image)
        painter.setOpacity(reveal); painter.drawImage(dest, image); painter.restore()

    def draw_fractal_echo(self, painter: QPainter, center: QPointF, radius: float, t: float, intensity: float) -> None:
        if self.variant != 3:
            return
        for level in range(5):
            scale = 0.74 - level * 0.105
            angle = t * (3.8 + level * 0.7) * (-1 if level % 2 else 1)
            path = polygon_path(center, radius * scale, 6, angle + level * 17)
            glow_path(painter, path, CRIMSON if level % 2 else GOLD, intensity=intensity * (0.24 - level * 0.025), core_width=0.7, spread=0.72 * self.glow_spread)
