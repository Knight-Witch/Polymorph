from __future__ import annotations

import math

from PySide6.QtCore import QPointF, Qt
from PySide6.QtGui import QColor, QPainter, QPainterPath, QRadialGradient
from PySide6.QtSvg import QSvgRenderer

from .motion_effects import CRIMSON, ELDER_FUTHARK, GOLD, IVORY, DESIGNATED_RUNES, alpha, comet, glow_ellipse, glow_path, polar, polygon_path, smoothstep
from .motion_loader_base import ArcaneLoaderBase
from .resources import asset_path


class ArcaneLoader(ArcaneLoaderBase):
    def load_bundled_emblem(self) -> bool:
        path = asset_path("kw_emblem.svg")
        if not path.is_file():
            return False
        renderer = QSvgRenderer(str(path))
        if not renderer.isValid():
            return False
        self.emblem = renderer
        self.emblem_path = str(path)
        self.update()
        return True

    def paintEvent(self, _event) -> None:
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing, True)
        painter.setRenderHint(QPainter.RenderHint.TextAntialiasing, True)
        center = QPointF(self.width() / 2.0, self.height() / 2.0)
        radius = 202.0
        t = self.clock.t
        age = self.completion_age()
        if age is None:
            inner_alpha = 1.0; emblem_reveal = 0.0; completion = 0.0; flash = 0.0
        else:
            completion = smoothstep(0.0, 0.55, age)
            inner_alpha = 1.0 - smoothstep(0.24, 1.30, age)
            emblem_reveal = smoothstep(0.42, 1.42, age)
            flash = math.exp(-((age - 0.20) / 0.115) ** 2)
        haze = QRadialGradient(center, radius * 1.18)
        haze.setColorAt(0.0, alpha(GOLD, 18 * self.glow * inner_alpha))
        haze.setColorAt(0.48, alpha(CRIMSON, 9 * self.glow * inner_alpha))
        haze.setColorAt(1.0, QColor(0, 0, 0, 0))
        painter.setPen(Qt.PenStyle.NoPen); painter.setBrush(haze); painter.drawEllipse(center, radius * 1.18, radius * 1.18)
        outer_angle = t * 15.0 * self.outer_rune_speed
        inner_angle = -t * 20.0 * self.inner_rune_speed
        partial_angle = -t * 12.0 * self.partial_speed
        triangle_angle = -90.0 + t * 8.4 * self.triangle_speed
        hex_angle = -90.0 - t * 5.4 * self.hex_speed
        base_intensity = self.glow * inner_alpha
        satellites = [polar(center, radius * 0.48, triangle_angle + i * 120.0) for i in range(3)]
        for index, ring_radius in enumerate((0.93, 0.80, 0.55, 0.325)):
            glow_ellipse(painter, center, radius * ring_radius, GOLD if index % 2 == 0 else CRIMSON, intensity=base_intensity * self.cascade_level(index), core_width=0.85, spread=0.82 * self.glow_spread)
        hex_a = polygon_path(center, radius * 0.74, 6, hex_angle)
        hex_b = polygon_path(center, radius * 0.74, 6, hex_angle + 30.0)
        glow_path(painter, hex_a, GOLD, intensity=base_intensity * 0.72, core_width=0.9, spread=self.glow_spread)
        glow_path(painter, hex_b, CRIMSON, intensity=base_intensity * 0.48, core_width=0.8, spread=0.92 * self.glow_spread)
        self.draw_fractal_echo(painter, center, radius, t, base_intensity)
        triangle = QPainterPath(); triangle.moveTo(satellites[0]); triangle.lineTo(satellites[1]); triangle.lineTo(satellites[2]); triangle.closeSubpath()
        triangle_pulse = 0.74 + 0.26 * (0.5 + 0.5 * math.sin(t * 3.0))
        glow_path(painter, triangle, CRIMSON, intensity=base_intensity * triangle_pulse, core_width=1.15, spread=1.08 * self.glow_spread)
        partial_specs: list[tuple[QPointF, float, float, float]] = []
        for satellite in satellites:
            dx = center.x() - satellite.x(); dy = center.y() - satellite.y()
            inward_angle = math.degrees(math.atan2(-dy, dx))
            arc_radius = radius * 0.39; start = inward_angle - 57.0; span = 114.0
            partial_specs.append((satellite, arc_radius, start, span))
        tracer_clip = self.tracer_clip(center, radius, satellites, partial_specs)
        tracer_intensity = base_intensity * (1.15 if self.variant == 2 else 0.92)
        self.draw_spoke_tracers(painter, center, radius, hex_angle, tracer_clip, tracer_intensity)
        partial_flicker = self.grouped_flicker(1)
        sphere_flicker = self.grouped_flicker(2, offset=0.4)
        for index, (satellite, arc_radius, start, span) in enumerate(partial_specs):
            self.draw_arc_glow(painter, satellite, arc_radius, start, span, GOLD, base_intensity * partial_flicker, width=0.95)
            inward = start + span / 2.0
            self.draw_partial_rune_band(painter, satellite, arc_radius, partial_angle + index * 37.0, inward, span=span, offset=index * 8, intensity=base_intensity * 0.92)
        glow_ellipse(painter, center, radius * 0.325, GOLD, intensity=base_intensity * self.grouped_flicker(3), core_width=0.9, spread=0.74 * self.glow_spread)
        self.draw_glimmer_ring(painter, center, radius * 0.285, t, base_intensity * 0.9)
        sphere_states = self.satellite_rune_indices(t)
        for index, satellite in enumerate(satellites):
            glow_ellipse(painter, satellite, radius * 0.135, GOLD if index != 1 else CRIMSON, intensity=base_intensity * sphere_flicker, core_width=1.05, spread=0.9 * self.glow_spread)
            rune_index, rune_opacity = sphere_states[index]
            self.runes.draw(painter, ELDER_FUTHARK[rune_index], satellite, radius * 0.105, triangle_angle + index * 120.0 + 90.0, color=GOLD if index != 1 else CRIMSON, intensity=base_intensity * rune_opacity, spread=0.92 * self.glow_spread)
        outer_count = 30 if self.variant == 1 else 24
        inner_count = 28 if self.variant == 1 else 24
        self.runes.ring(painter, center, radius * 0.875, outer_angle, count=outer_count, size=13.5, intensity=base_intensity * 0.86, color=GOLD, offset=0)
        for i, rune in enumerate(DESIGNATED_RUNES):
            degrees = outer_angle + i * 60.0
            self.runes.draw(painter, rune, polar(center, radius * 0.94, degrees), 24.0, degrees + 90.0, color=CRIMSON if i % 2 else GOLD, intensity=base_intensity, spread=1.0 * self.glow_spread)
        self.runes.ring(painter, center, radius * 0.655, inner_angle, count=inner_count, size=11.5, intensity=base_intensity * 0.74, color=GOLD, offset=5)
        if self.variant == 2:
            for j, ring_radius in enumerate((0.655, 0.875)):
                degrees = (t * (78 if j == 0 else -61) * self.trace_speed + j * 130.0) % 360.0
                head = polar(center, radius * ring_radius, degrees); tail = polar(center, radius * ring_radius, degrees - (22 if j == 0 else -22))
                comet(painter, tail, head, CRIMSON if j else GOLD, intensity=base_intensity, spread=self.glow_spread)
        self.draw_progress_rings(painter, center, radius, completion)
        if flash > 0.002:
            flare = QRadialGradient(center, radius * 0.72)
            flare.setColorAt(0.0, alpha(IVORY, 160 * flash * self.glow)); flare.setColorAt(0.28, alpha(GOLD, 80 * flash * self.glow)); flare.setColorAt(1.0, QColor(0,0,0,0))
            painter.setPen(Qt.PenStyle.NoPen); painter.setBrush(flare); painter.drawEllipse(center, radius * 0.72, radius * 0.72)
        self.draw_emblem(painter, center, radius, emblem_reveal)
