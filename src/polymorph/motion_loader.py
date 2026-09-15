from __future__ import annotations

import math

from PySide6.QtCore import QPointF, Qt
from PySide6.QtGui import QColor, QPainter, QPainterPath, QRadialGradient
from PySide6.QtSvg import QSvgRenderer

from .motion_effects import (
    CRIMSON,
    DESIGNATED_RUNES,
    ELDER_FUTHARK,
    GOLD,
    GOLD_CORE,
    RED_CORE,
    WHITE,
    alpha,
    comet,
    glow_ellipse,
    glow_path,
    polar,
    polygon_path,
    smoothstep,
)
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

    def _midpoint(self, a: QPointF, b: QPointF) -> QPointF:
        return QPointF((a.x() + b.x()) / 2.0, (a.y() + b.y()) / 2.0)

    def _draw_red_ring(
        self,
        painter: QPainter,
        center: QPointF,
        ring_radius: float,
        intensity: float,
        *,
        width: float = 0.9,
        spread: float = 0.82,
    ) -> None:
        glow_ellipse(
            painter,
            center,
            ring_radius,
            CRIMSON,
            core=RED_CORE,
            intensity=intensity,
            core_width=width,
            spread=spread * self.glow_spread,
        )

    def paintEvent(self, _event) -> None:
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing, True)
        painter.setRenderHint(QPainter.RenderHint.TextAntialiasing, True)

        center = QPointF(self.width() / 2.0, self.height() / 2.0)
        radius = 202.0
        t = self.clock.t
        age = self.completion_age()

        if age is None:
            inner_alpha = 1.0
            emblem_reveal = 0.0
            completion = 0.0
            flash = 0.0
        else:
            completion = smoothstep(0.0, 0.55, age)
            inner_alpha = 1.0 - smoothstep(0.24, 1.30, age)
            emblem_reveal = smoothstep(0.42, 1.42, age)
            flash = math.exp(-((age - 0.20) / 0.115) ** 2)

        base_intensity = self.glow * inner_alpha

        haze = QRadialGradient(center, radius * 1.18)
        haze.setColorAt(0.0, alpha(GOLD, 14 * base_intensity))
        haze.setColorAt(0.46, alpha(CRIMSON, 10 * base_intensity))
        haze.setColorAt(1.0, QColor(0, 0, 0, 0))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(haze)
        painter.drawEllipse(center, radius * 1.18, radius * 1.18)

        outer_angle = t * 15.0 * self.outer_rune_speed
        inner_angle = -t * 20.0 * self.inner_rune_speed
        partial_angle = -t * 12.0 * self.partial_speed
        triangle_angle = -90.0 + t * 8.4 * self.triangle_speed
        hex_angle = -90.0 - t * 5.4 * self.hex_speed

        outer_rune_radius = radius * 0.832
        third_ring_radius = radius * 0.762
        polygon_radius = radius * 0.733
        fourth_ring_radius = polygon_radius * math.cos(math.radians(30.0))
        partial_track_radius = radius * 0.455
        partial_band_width = radius * 0.088
        sphere_radius = radius * 0.130
        middle_glimmer_radius = radius * 0.285
        fifth_ring_radius = radius * 0.198
        inner_rune_radius = radius * 0.160
        seventh_ring_radius = radius * 0.120

        partial_centers = [
            polar(center, polygon_radius, -90.0 + i * 120.0)
            for i in range(3)
        ]

        hex_a = polygon_path(center, polygon_radius, 6, hex_angle)
        hex_b = polygon_path(center, polygon_radius, 6, hex_angle + 30.0)

        triangle_vertices = [
            polar(center, polygon_radius, triangle_angle + i * 120.0)
            for i in range(3)
        ]
        triangle = QPainterPath()
        triangle.moveTo(triangle_vertices[0])
        triangle.lineTo(triangle_vertices[1])
        triangle.lineTo(triangle_vertices[2])
        triangle.closeSubpath()

        satellites = [
            self._midpoint(triangle_vertices[i], triangle_vertices[(i + 1) % 3])
            for i in range(3)
        ]

        self._draw_red_ring(
            painter,
            center,
            third_ring_radius,
            base_intensity * self.cascade_level(0),
            width=0.9,
        )

        glow_path(
            painter,
            hex_a,
            CRIMSON,
            core=RED_CORE,
            intensity=base_intensity * 0.72,
            core_width=0.9,
            spread=self.glow_spread,
        )
        glow_path(
            painter,
            hex_b,
            CRIMSON,
            core=RED_CORE,
            intensity=base_intensity * 0.56,
            core_width=0.8,
            spread=0.92 * self.glow_spread,
        )

        self.draw_fractal_echo(painter, center, radius, t, base_intensity)

        triangle_pulse = 0.74 + 0.26 * (0.5 + 0.5 * math.sin(t * 3.0))
        glow_path(
            painter,
            triangle,
            CRIMSON,
            core=RED_CORE,
            intensity=base_intensity * triangle_pulse,
            core_width=1.15,
            spread=1.05 * self.glow_spread,
        )

        tracer_intensity = base_intensity * (1.18 if self.variant == 2 else 0.94)
        self.draw_spoke_tracers(
            painter,
            center,
            polygon_radius,
            hex_angle,
            tracer_intensity,
        )

        self.draw_glimmer_ring(
            painter,
            center,
            middle_glimmer_radius,
            t,
            base_intensity * 0.92,
        )

        partial_flicker = self.grouped_flicker(1)
        partial_count = 30 if self.variant == 1 else 24
        for index, partial_center in enumerate(partial_centers):
            self.draw_partial_rune_window(
                painter,
                center,
                fourth_ring_radius,
                partial_center,
                partial_track_radius,
                partial_band_width,
                partial_angle + index * 31.0,
                offset=index * 8,
                intensity=base_intensity * partial_flicker,
                count=partial_count,
            )

        self._draw_red_ring(
            painter,
            center,
            fourth_ring_radius,
            base_intensity * self.cascade_level(1),
            width=0.95,
        )

        sphere_flicker = self.grouped_flicker(2, offset=0.4)
        sphere_states = self.satellite_rune_indices(t)
        for index, satellite in enumerate(satellites):
            sphere_mask = self.circle_path(satellite, sphere_radius)
            self.fill_mask(painter, sphere_mask)
            glow_ellipse(
                painter,
                satellite,
                sphere_radius,
                CRIMSON,
                core=RED_CORE,
                intensity=base_intensity * sphere_flicker,
                core_width=1.05,
                spread=0.88 * self.glow_spread,
            )
            rune_index, rune_opacity = sphere_states[index]
            self.runes.draw(
                painter,
                ELDER_FUTHARK[rune_index],
                satellite,
                radius * 0.092,
                triangle_angle + index * 120.0 + 30.0,
                color=WHITE,
                core=WHITE,
                intensity=base_intensity * rune_opacity,
                spread=0.88 * self.glow_spread,
            )

        inner_annulus = self.annulus_path(center, fifth_ring_radius, seventh_ring_radius)
        self.fill_mask(painter, inner_annulus)

        self._draw_red_ring(
            painter,
            center,
            fifth_ring_radius,
            base_intensity * self.cascade_level(2),
            width=0.9,
            spread=0.76,
        )
        self._draw_red_ring(
            painter,
            center,
            seventh_ring_radius,
            base_intensity * self.cascade_level(3),
            width=0.9,
            spread=0.76,
        )

        inner_count = 20 if self.variant == 1 else 18
        painter.save()
        painter.setClipPath(inner_annulus)
        self.runes.ring(
            painter,
            center,
            inner_rune_radius,
            inner_angle,
            count=inner_count,
            size=8.8,
            intensity=base_intensity * 0.88,
            color=GOLD,
            offset=5,
        )
        painter.restore()

        outer_count = 30 if self.variant == 1 else 24
        slot_step = outer_count // 6
        designated_slots = {i * slot_step for i in range(6)}
        self.runes.ring(
            painter,
            center,
            outer_rune_radius,
            outer_angle,
            count=outer_count,
            size=13.2,
            intensity=base_intensity * 0.90,
            color=GOLD,
            offset=0,
            skip_indices=designated_slots,
        )
        for designated_index, rune in enumerate(DESIGNATED_RUNES):
            slot = designated_index * slot_step
            degrees = outer_angle + slot * 360.0 / outer_count
            self.runes.draw(
                painter,
                rune,
                polar(center, outer_rune_radius, degrees),
                24.0,
                degrees + 90.0,
                color=WHITE,
                core=WHITE,
                intensity=base_intensity,
                spread=0.98 * self.glow_spread,
            )

        if self.variant == 2:
            for j, ring_radius in enumerate((middle_glimmer_radius, outer_rune_radius)):
                degrees = (t * (78 if j == 0 else -61) * self.trace_speed + j * 130.0) % 360.0
                head = polar(center, ring_radius, degrees)
                tail = polar(center, ring_radius, degrees - (58 if j == 0 else -58))
                comet(
                    painter,
                    tail,
                    head,
                    CRIMSON,
                    intensity=base_intensity,
                    spread=1.02 * self.glow_spread,
                )

        self.draw_progress_rings(painter, center, radius, completion)

        if flash > 0.002:
            flare = QRadialGradient(center, radius * 0.72)
            flare.setColorAt(0.0, alpha(WHITE, 170 * flash * self.glow))
            flare.setColorAt(0.28, alpha(GOLD_CORE, 72 * flash * self.glow))
            flare.setColorAt(1.0, QColor(0, 0, 0, 0))
            painter.setPen(Qt.PenStyle.NoPen)
            painter.setBrush(flare)
            painter.drawEllipse(center, radius * 0.72, radius * 0.72)

        self.draw_emblem(painter, center, radius, emblem_reveal)
