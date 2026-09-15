from __future__ import annotations

import math

from PySide6.QtCore import QPointF, QRectF, Qt
from PySide6.QtGui import QColor, QPainter, QPainterPath, QRadialGradient
from PySide6.QtSvg import QSvgRenderer

from .motion_editor import MotionEditorState
from .motion_effects import (
    CRIMSON,
    ELDER_FUTHARK,
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
    def __init__(self, rune_family: str, parent=None) -> None:
        super().__init__(rune_family, parent)
        self.editor = MotionEditorState()
        self.outer_rune_speed = 1.0
        self.inner_rune_speed = 1.0
        self.partial_speed = 1.0
        self.triangle_speed = 1.0
        self.hex_speed = 1.0
        self.trace_speed = 1.0
        self.flicker_speed = 1.0

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

    def _state(self, element_id: str):
        return self.editor.get(element_id)

    def _color(self, element_id: str) -> QColor:
        return self.editor.color(element_id)

    def _core(self, element_id: str) -> QColor:
        color = self._color(element_id)
        if color.lightness() > 220:
            return WHITE
        if color.red() > color.green() * 1.45 and color.red() > color.blue() * 1.25:
            return RED_CORE
        return GOLD_CORE

    def _intensity(self, element_id: str, inner_alpha: float = 1.0) -> float:
        state = self._state(element_id)
        return self.glow * state.brightness * self.editor.pulse_multiplier(element_id, self.clock.t) * inner_alpha

    def _spread(self, element_id: str) -> float:
        return self.glow_spread * self._state(element_id).glow_spread

    def _radius(self, element_id: str, radius: float) -> float:
        state = self._state(element_id)
        return radius * state.nominal_radius * state.spread

    def _angle(self, element_id: str, t: float, rate: float) -> float:
        return self.editor.animated_angle(element_id, t, rate)

    def _draw_ring(self, painter: QPainter, center: QPointF, radius: float, element_id: str, inner_alpha: float) -> None:
        state = self._state(element_id)
        glow_ellipse(
            painter,
            center,
            self._radius(element_id, radius),
            self._color(element_id),
            core=self._core(element_id),
            intensity=self._intensity(element_id, inner_alpha),
            core_width=max(0.55, 0.92 * state.scale),
            spread=self._spread(element_id),
        )

    def _draw_partial_window(
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
        count: int,
    ) -> None:
        frame = self._state("partial_frames")
        rune_state = self._state("partial_runes")
        window = self.partial_window_path(center, boundary_radius, satellite, track_radius, band_width * frame.scale)
        self.fill_mask(painter, window)
        painter.save()
        painter.setClipPath(window)
        rune_shift = self.editor.rune_offset("partial_runes", self.clock.t)
        for i in range(count):
            degrees = rotation + i * 360.0 / count
            rune = ELDER_FUTHARK[(i + offset + rune_shift) % len(ELDER_FUTHARK)]
            self.runes.draw(
                painter,
                rune,
                polar(satellite, track_radius, degrees),
                13.5 * rune_state.scale,
                degrees + 90.0,
                color=self._color("partial_runes"),
                core=self._core("partial_runes"),
                intensity=intensity,
                spread=0.60 * self._spread("partial_runes"),
            )
        painter.restore()
        glow_path(
            painter,
            window,
            self._color("partial_frames"),
            core=self._core("partial_frames"),
            intensity=self._intensity("partial_frames"),
            core_width=max(0.55, 0.9 * frame.scale),
            spread=0.76 * self._spread("partial_frames"),
        )

    def _draw_glimmer_ring(self, painter: QPainter, center: QPointF, radius: float, t: float, inner_alpha: float) -> None:
        element_id = "middle_runes"
        state = self._state(element_id)
        count = 21 if self.variant == 1 else 18
        transition = max(0.0, state.rune_speed)
        for slot in range(count):
            duration = 1.55 + 0.17 * (slot % 5)
            clock = t + slot * 0.61
            cycle = math.floor(clock / duration)
            local = (clock / duration) - cycle
            opacity = math.sin(math.pi * local) ** 2
            if opacity < 0.025:
                continue
            transition_step = 0 if transition <= 0.001 else math.floor(cycle * transition * 3.0)
            rune_index = (slot * 7 + transition_step) % len(ELDER_FUTHARK)
            degrees = state.base_rotation + slot * 360.0 / count
            self.runes.draw(
                painter,
                ELDER_FUTHARK[rune_index],
                polar(center, radius, degrees),
                10.5 * state.scale,
                degrees + 90.0,
                color=self._color(element_id),
                core=self._core(element_id),
                intensity=self._intensity(element_id, inner_alpha) * opacity,
                spread=0.54 * self._spread(element_id),
            )

    def _large_rune_states(self, t: float) -> list[tuple[int, float]]:
        state = self._state("large_rune_glyphs")
        result: list[tuple[int, float]] = []
        used: set[int] = set()
        for index in range(3):
            duration = 1.65 + index * 0.21
            clock = t + index * 0.49
            raw_cycle = math.floor(clock / duration)
            local = (clock / duration) - raw_cycle
            cycle = 0 if state.rune_speed <= 0.001 else math.floor(raw_cycle * state.rune_speed * 2.5)
            rune_index = (cycle * 7 + index * 9 + 2) % len(ELDER_FUTHARK)
            while rune_index in used:
                rune_index = (rune_index + 1) % len(ELDER_FUTHARK)
            used.add(rune_index)
            opacity = 1.0 if state.rune_speed <= 0.001 else 0.24 + 0.76 * (math.sin(math.pi * local) ** 0.62)
            result.append((rune_index, opacity))
        return result

    def _draw_tracers(self, painter: QPainter, center: QPointF, outer_radius: float, angle: float, inner_alpha: float) -> None:
        state = self._state("tracers")
        phase = self.clock.t * 0.48 * self.trace_speed
        travel = 0.5 - 0.5 * math.cos(phase * math.tau)
        inward = math.sin(phase * math.tau) >= 0.0
        for i in range(6):
            outer = polar(center, outer_radius, angle + i * 60.0)
            head = QPointF(outer.x() + (center.x() - outer.x()) * travel, outer.y() + (center.y() - outer.y()) * travel)
            tail_amount = max(0.0, travel - 0.60) if inward else min(1.0, travel + 0.60)
            tail = QPointF(outer.x() + (center.x() - outer.x()) * tail_amount, outer.y() + (center.y() - outer.y()) * tail_amount)
            comet(
                painter,
                tail,
                head,
                self._color("tracers"),
                intensity=self._intensity("tracers", inner_alpha),
                spread=self._spread("tracers") * state.scale,
            )

    def _draw_progress(self, painter: QPainter, center: QPointF, radius: float, completion: float) -> None:
        span = 360.0 * self.progress
        pulse = 1.0 + completion * (0.16 + 0.10 * math.sin(self.clock.t * 19.0))
        for element_id, sign in (("progress_outer", -1.0), ("progress_inner", 1.0)):
            state = self._state(element_id)
            ring_radius = self._radius(element_id, radius)
            glow_ellipse(
                painter,
                center,
                ring_radius,
                self._color(element_id),
                core=self._core(element_id),
                intensity=self._intensity(element_id) * 0.22,
                core_width=max(0.55, 0.8 * state.scale),
                spread=0.75 * self._spread(element_id),
            )
            rect = QRectF(center.x() - ring_radius, center.y() - ring_radius, ring_radius * 2.0, ring_radius * 2.0)
            arc = QPainterPath()
            arc.arcMoveTo(rect, 90.0)
            arc.arcTo(rect, 90.0, sign * span)
            glow_path(
                painter,
                arc,
                self._color(element_id),
                core=self._core(element_id),
                intensity=self._intensity(element_id) * pulse,
                core_width=max(0.7, 1.55 * state.scale),
                spread=1.05 * self._spread(element_id),
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

        haze = QRadialGradient(center, radius * 1.18)
        haze.setColorAt(0.0, alpha(self._color("middle_runes"), 12 * self.glow * inner_alpha))
        haze.setColorAt(0.46, alpha(self._color("triangle"), 9 * self.glow * inner_alpha))
        haze.setColorAt(1.0, QColor(0, 0, 0, 0))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(haze)
        painter.drawEllipse(center, radius * 1.18, radius * 1.18)

        triangle_angle = self._angle("triangle", t, 8.4)
        triangle_radius = self._radius("triangle", radius)
        triangle_vertices = [polar(center, triangle_radius, triangle_angle + i * 120.0) for i in range(3)]
        triangle = QPainterPath()
        triangle.moveTo(triangle_vertices[0])
        triangle.lineTo(triangle_vertices[1])
        triangle.lineTo(triangle_vertices[2])
        triangle.closeSubpath()

        circle_state = self._state("large_rune_circles")
        circle_orbit_angle = self._angle("large_rune_circles", t, 8.4)
        circle_center_radius = radius * circle_state.nominal_radius * circle_state.spread
        satellites = [polar(center, circle_center_radius, circle_orbit_angle + i * 120.0) for i in range(3)]
        sphere_radius = radius * 0.130 * circle_state.scale

        polygon_radius_a = self._radius("hex_a", radius)
        polygon_radius_b = self._radius("hex_b", radius)
        hex_angle_a = self._angle("hex_a", t, 5.4)
        hex_angle_b = self._angle("hex_b", t, 5.4)
        hex_a = polygon_path(center, polygon_radius_a, 6, hex_angle_a)
        hex_b = polygon_path(center, polygon_radius_b, 6, hex_angle_b)

        self._draw_ring(painter, center, radius, "ring_three", inner_alpha)
        for element_id, path in (("hex_a", hex_a), ("hex_b", hex_b)):
            state = self._state(element_id)
            glow_path(
                painter,
                path,
                self._color(element_id),
                core=self._core(element_id),
                intensity=self._intensity(element_id, inner_alpha),
                core_width=max(0.55, 0.9 * state.scale),
                spread=self._spread(element_id),
            )

        tri_state = self._state("triangle")
        glow_path(
            painter,
            triangle,
            self._color("triangle"),
            core=self._core("triangle"),
            intensity=self._intensity("triangle", inner_alpha),
            core_width=max(0.55, 1.15 * tri_state.scale),
            spread=self._spread("triangle"),
        )

        self.draw_fractal_echo(painter, center, radius, t, self.glow * inner_alpha)
        self._draw_tracers(painter, center, self._radius("tracers", radius), hex_angle_a, inner_alpha * (1.18 if self.variant == 2 else 0.94))
        self._draw_glimmer_ring(painter, center, self._radius("middle_runes", radius), t, inner_alpha)

        fourth_ring_radius = self._radius("ring_four", radius)
        partial_frame_state = self._state("partial_frames")
        partial_track_radius = radius * partial_frame_state.nominal_radius * partial_frame_state.spread
        partial_band_width = radius * 0.088
        partial_centers = [polar(center, triangle_radius, partial_frame_state.base_rotation - 90.0 + i * 120.0) for i in range(3)]
        partial_angle = self._angle("partial_runes", t, 12.0)
        partial_count = 30 if self.variant == 1 else 24
        for index, partial_center in enumerate(partial_centers):
            self._draw_partial_window(
                painter,
                center,
                fourth_ring_radius,
                partial_center,
                partial_track_radius,
                partial_band_width,
                partial_angle + index * 31.0,
                offset=index * 8,
                intensity=self._intensity("partial_runes", inner_alpha),
                count=partial_count,
            )

        self._draw_ring(painter, center, radius, "ring_four", inner_alpha)

        sphere_states = self._large_rune_states(t)
        for index, satellite in enumerate(satellites):
            sphere_mask = self.circle_path(satellite, sphere_radius)
            self.fill_mask(painter, sphere_mask)
            glow_ellipse(
                painter,
                satellite,
                sphere_radius,
                self._color("large_rune_circles"),
                core=self._core("large_rune_circles"),
                intensity=self._intensity("large_rune_circles", inner_alpha),
                core_width=max(0.55, 1.05 * circle_state.scale),
                spread=self._spread("large_rune_circles"),
            )
            rune_index, rune_opacity = sphere_states[index]
            glyph_state = self._state("large_rune_glyphs")
            self.runes.draw(
                painter,
                ELDER_FUTHARK[rune_index],
                satellite,
                radius * 0.092 * glyph_state.scale,
                glyph_state.base_rotation,
                color=self._color("large_rune_glyphs"),
                core=self._core("large_rune_glyphs"),
                intensity=self._intensity("large_rune_glyphs", inner_alpha) * rune_opacity,
                spread=self._spread("large_rune_glyphs"),
            )

        ring_five_radius = self._radius("ring_five", radius)
        ring_seven_radius = self._radius("ring_seven", radius)
        inner_annulus = self.annulus_path(center, ring_five_radius, ring_seven_radius)
        self.fill_mask(painter, inner_annulus)
        self._draw_ring(painter, center, radius, "ring_five", inner_alpha)
        self._draw_ring(painter, center, radius, "ring_seven", inner_alpha)

        inner_state = self._state("inner_runes")
        inner_count = 20 if self.variant == 1 else 18
        inner_angle = self._angle("inner_runes", t, 20.0)
        inner_shift = self.editor.rune_offset("inner_runes", t)
        painter.save()
        painter.setClipPath(inner_annulus)
        for i in range(inner_count):
            degrees = inner_angle + i * 360.0 / inner_count
            rune = ELDER_FUTHARK[(i + 5 + inner_shift) % len(ELDER_FUTHARK)]
            self.runes.draw(
                painter,
                rune,
                polar(center, self._radius("inner_runes", radius), degrees),
                8.8 * inner_state.scale,
                degrees + 90.0,
                color=self._color("inner_runes"),
                core=self._core("inner_runes"),
                intensity=self._intensity("inner_runes", inner_alpha),
                spread=self._spread("inner_runes"),
            )
        painter.restore()

        outer_state = self._state("outer_runes")
        outer_large_state = self._state("outer_large_runes")
        outer_count = 30 if self.variant == 1 else 24
        slot_step = outer_count // 6
        designated_slots = {i * slot_step for i in range(6)}
        outer_angle = self._angle("outer_runes", t, 15.0)
        outer_large_angle = self._angle("outer_large_runes", t, 15.0)
        outer_shift = self.editor.rune_offset("outer_runes", t)
        for i in range(outer_count):
            if i in designated_slots:
                continue
            degrees = outer_angle + i * 360.0 / outer_count
            rune = ELDER_FUTHARK[(i + outer_shift) % len(ELDER_FUTHARK)]
            self.runes.draw(
                painter,
                rune,
                polar(center, self._radius("outer_runes", radius), degrees),
                13.2 * outer_state.scale,
                degrees + 90.0,
                color=self._color("outer_runes"),
                core=self._core("outer_runes"),
                intensity=self._intensity("outer_runes", inner_alpha),
                spread=self._spread("outer_runes"),
            )
        large_shift = self.editor.rune_offset("outer_large_runes", t)
        designated = ("ᚠ", "ᚨ", "ᛉ", "ᛏ", "ᛞ", "ᛟ")
        for designated_index in range(6):
            slot = designated_index * slot_step
            degrees = outer_large_angle + slot * 360.0 / outer_count
            if outer_large_state.rune_speed <= 0.001:
                rune = designated[designated_index]
            else:
                rune = ELDER_FUTHARK[(designated_index * 4 + large_shift) % len(ELDER_FUTHARK)]
            self.runes.draw(
                painter,
                rune,
                polar(center, self._radius("outer_large_runes", radius), degrees),
                24.0 * outer_large_state.scale,
                degrees + 90.0,
                color=self._color("outer_large_runes"),
                core=self._core("outer_large_runes"),
                intensity=self._intensity("outer_large_runes", inner_alpha),
                spread=self._spread("outer_large_runes"),
            )

        self._draw_progress(painter, center, radius, completion)

        if flash > 0.002:
            flare = QRadialGradient(center, radius * 0.72)
            flare.setColorAt(0.0, alpha(WHITE, 170 * flash * self.glow))
            flare.setColorAt(0.28, alpha(GOLD_CORE, 72 * flash * self.glow))
            flare.setColorAt(1.0, QColor(0, 0, 0, 0))
            painter.setPen(Qt.PenStyle.NoPen)
            painter.setBrush(flare)
            painter.drawEllipse(center, radius * 0.72, radius * 0.72)

        self.draw_emblem(painter, center, radius, emblem_reveal)
