from __future__ import annotations

import base64
import math
import zlib

from PySide6.QtCore import QByteArray, QPointF, QRectF, Qt
from PySide6.QtGui import QImage, QLinearGradient, QPainter, QPainterPath, QRadialGradient
from PySide6.QtSvg import QSvgRenderer
from PySide6.QtWidgets import QWidget

from .motion_effects import (
    CRIMSON,
    ELDER_FUTHARK,
    GOLD,
    GOLD_CORE,
    IVORY,
    MASK_BG,
    RED_CORE,
    WHITE,
    Clock,
    RunePainter,
    alpha,
    clamp,
    comet,
    glow_ellipse,
    glow_path,
    lerp_point,
    polar,
    polygon_path,
    smoothstep,
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
        self.variant = 1
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

    def circle_path(self, center: QPointF, radius: float) -> QPainterPath:
        path = QPainterPath()
        path.addEllipse(center, radius, radius)
        return path

    def annulus_path(self, center: QPointF, outer_radius: float, inner_radius: float) -> QPainterPath:
        outer = self.circle_path(center, outer_radius)
        inner = self.circle_path(center, inner_radius)
        return outer.subtracted(inner)

    def fill_mask(self, painter: QPainter, path: QPainterPath) -> None:
        painter.save()
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(MASK_BG)
        painter.drawPath(path)
        painter.restore()

    def partial_window_path(
        self,
        center: QPointF,
        boundary_radius: float,
        satellite: QPointF,
        track_radius: float,
        band_width: float,
    ) -> QPainterPath:
        band = self.annulus_path(
            satellite,
            track_radius + band_width / 2.0,
            max(1.0, track_radius - band_width / 2.0),
        )
        boundary = self.circle_path(center, boundary_radius)
        return band.intersected(boundary)

    def draw_partial_rune_window(
        self,
        painter: QPainter,
        center: QPointF,
        boundary_radius: float,
        satellite: QPointF,
        track_radius: float,
        band_width: float,
        rotation: float,
        *,
        offset: int,
        intensity: float,
        count: int = 24,
    ) -> QPainterPath:
        window = self.partial_window_path(center, boundary_radius, satellite, track_radius, band_width)
        self.fill_mask(painter, window)

        painter.save()
        painter.setClipPath(window)
        for i in range(count):
            degrees = rotation + i * 360.0 / count
            rune = ELDER_FUTHARK[(i + offset) % len(ELDER_FUTHARK)]
            self.runes.draw(
                painter,
                rune,
                polar(satellite, track_radius, degrees),
                13.5,
                degrees + 90.0,
                color=GOLD,
                core=GOLD_CORE,
                intensity=intensity,
                spread=0.60 * self.glow_spread,
            )
        painter.restore()

        glow_path(
            painter,
            window,
            CRIMSON,
            core=RED_CORE,
            intensity=intensity * 0.88,
            core_width=0.9,
            spread=0.76 * self.glow_spread,
        )
        return window

    def draw_glimmer_ring(self, painter: QPainter, center: QPointF, radius: float, t: float, intensity: float) -> None:
        count = 18 if self.variant != 1 else 21
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
            self.runes.draw(
                painter,
                ELDER_FUTHARK[rune_index],
                polar(center, radius, degrees),
                10.5,
                degrees + 90.0,
                color=GOLD,
                core=GOLD_CORE,
                intensity=intensity * opacity,
                spread=0.54 * self.glow_spread,
            )

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

    def draw_spoke_tracers(
        self,
        painter: QPainter,
        center: QPointF,
        outer_radius: float,
        angle: float,
        intensity: float,
    ) -> None:
        phase = self.clock.t * 0.48 * self.trace_speed
        travel = 0.5 - 0.5 * math.cos(phase * math.tau)
        inward = math.sin(phase * math.tau) >= 0.0
        for i in range(6):
            outer = polar(center, outer_radius, angle + i * 60.0)
            head = lerp_point(outer, center, travel)
            tail_amount = max(0.0, travel - 0.60) if inward else min(1.0, travel + 0.60)
            tail = lerp_point(outer, center, tail_amount)
            comet(
                painter,
                tail,
                head,
                CRIMSON,
                intensity=intensity,
                spread=1.08 * self.glow_spread,
            )

    def draw_progress_rings(self, painter: QPainter, center: QPointF, radius: float, completion: float) -> None:
        pulse = 1.0 + completion * (0.16 + 0.10 * math.sin(self.clock.t * 19.0))
        outer_radius = radius * 1.055
        inner_radius = radius * 1.005
        for ring_radius in (outer_radius, inner_radius):
            glow_ellipse(
                painter,
                center,
                ring_radius,
                WHITE,
                core=WHITE,
                intensity=self.glow * 0.22,
                core_width=0.8,
                spread=0.75 * self.glow_spread,
            )
        span = 360.0 * self.progress
        outer_rect = QRectF(
            center.x() - outer_radius,
            center.y() - outer_radius,
            outer_radius * 2.0,
            outer_radius * 2.0,
        )
        inner_rect = QRectF(
            center.x() - inner_radius,
            center.y() - inner_radius,
            inner_radius * 2.0,
            inner_radius * 2.0,
        )
        for rect, span_sign in ((outer_rect, -span), (inner_rect, span)):
            arc = QPainterPath()
            arc.arcMoveTo(rect, 90.0)
            arc.arcTo(rect, 90.0, span_sign)
            glow_path(
                painter,
                arc,
                WHITE,
                core=WHITE,
                intensity=self.glow * pulse,
                core_width=1.55,
                spread=1.05 * self.glow_spread,
            )

    def draw_emblem(self, painter: QPainter, center: QPointF, radius: float, reveal: float) -> None:
        if reveal <= 0.001:
            return
        if self.emblem is None:
            glow_ellipse(
                painter,
                center,
                radius * 0.18 * reveal,
                GOLD,
                core=GOLD_CORE,
                intensity=reveal * self.glow,
                spread=self.glow_spread,
            )
            return
        width = max(24, round(radius * 0.34))
        height = max(48, round(width * 2.0))
        image = QImage(width, height, QImage.Format.Format_ARGB32_Premultiplied)
        image.fill(Qt.GlobalColor.transparent)
        ip = QPainter(image)
        ip.setRenderHint(QPainter.RenderHint.Antialiasing, True)
        self.emblem.render(ip, QRectF(0, 0, width, height))
        ip.setCompositionMode(QPainter.CompositionMode.CompositionMode_SourceIn)
        tint = QLinearGradient(0, 0, 0, height)
        tint.setColorAt(0.0, WHITE)
        tint.setColorAt(0.48, GOLD_CORE)
        tint.setColorAt(1.0, WHITE)
        ip.fillRect(image.rect(), tint)
        ip.end()
        scale = 0.86 + 0.14 * smoothstep(0.0, 0.72, reveal)
        dw = width * scale
        dh = height * scale
        dest = QRectF(center.x() - dw / 2, center.y() - dh / 2, dw, dh)
        clip_radius = math.hypot(dw, dh) * 0.58 * reveal
        clip = QPainterPath()
        clip.addEllipse(center, clip_radius, clip_radius)
        painter.save()
        painter.setClipPath(clip)
        for ox, oy in ((-3,0),(3,0),(0,-3),(0,3),(-2,-2),(2,2),(-2,2),(2,-2)):
            painter.setOpacity(0.055 * reveal * self.glow)
            painter.drawImage(dest.translated(ox, oy), image)
        painter.setOpacity(reveal)
        painter.drawImage(dest, image)
        painter.restore()

    def draw_fractal_echo(self, painter: QPainter, center: QPointF, radius: float, t: float, intensity: float) -> None:
        if self.variant != 3:
            return
        for level in range(5):
            scale = 0.70 - level * 0.09
            angle = t * (3.8 + level * 0.7) * (-1 if level % 2 else 1)
            path = polygon_path(center, radius * scale, 6, angle + level * 17)
            glow_path(
                painter,
                path,
                CRIMSON,
                core=RED_CORE,
                intensity=intensity * (0.22 - level * 0.025),
                core_width=0.7,
                spread=0.72 * self.glow_spread,
            )
