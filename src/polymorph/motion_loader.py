from __future__ import annotations

import math

from PySide6.QtCore import QPointF, QRectF, Qt
from PySide6.QtGui import QColor, QPainter, QPainterPath, QRadialGradient
from PySide6.QtSvg import QSvgRenderer

from .motion_editor import MotionEditorState
from .motion_effects import (
    CRIMSON,
    DESIGNATED_RUNES,
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
from .motion_runes import hash01, rune_sample
from .resources import asset_path


class ArcaneLoader(ArcaneLoaderBase):
    def __init__(self, rune_family: str, parent=None) -> None:
        super().__init__(rune_family, parent)
        self.editor = MotionEditorState()
        self.trace_speed = 1.0

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

    def _core_for_color(self, color: QColor) -> QColor:
        if color.lightness() > 220:
            return WHITE
        if color.red() > color.green() * 1.45 and color.red() > color.blue() * 1.25:
            return RED_CORE
        return GOLD_CORE

    def _core(self, element_id: str) -> QColor:
        return self._core_for_color(self._color(element_id))

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

    def _partner(self, element_id: str, kind: str):
        source = self._state(element_id)
        candidates = [
            candidate_id
            for candidate_id, state in self.editor.elements.items()
            if candidate_id != element_id and state.kind == kind and state.link_group == source.link_group
        ]
        if candidates:
            return candidates[0]
        return next((candidate_id for candidate_id, state in self.editor.elements.items() if state.kind == kind), None)

    def _draw_sparkles(self, painter: QPainter, center: QPointF, radius: float) -> None:
        state = self.editor.sparkles
        if not state.enabled or state.density <= 0.001 or state.max_brightness <= 0.001:
            return
        count = max(0, min(420, round(12 + state.density * 300)))
        max_radius = radius * (0.20 + 1.05 * max(0.0, state.spread))
        colors = [QColor(state.color_1), QColor(state.color_2), QColor(state.color_3)]
        for index in range(count):
            rr = math.sqrt(hash01(index, 11)) * max_radius
            degrees = hash01(index, 17) * 360.0
            point = polar(center, rr, degrees)
            rate = 0.55 + 1.2 * hash01(index, 23)
            phase = hash01(index, 29) * math.tau
            wave = 0.5 + 0.5 * math.sin(self.clock.t * state.speed * rate * 2.4 + phase)
            wave = wave * wave
            brightness = state.max_brightness * wave
            if brightness < 0.025:
                continue
            cycle = int(self.clock.t * max(0.05, state.speed) * 0.5 + hash01(index, 31) * 9)
            color = colors[(index + cycle) % len(colors)]
            fade = max(0.05, min(1.0, state.fade))
            halo = 0.75 + fade * 2.8
            painter.setPen(Qt.PenStyle.NoPen)
            painter.setBrush(alpha(color, 38 * brightness))
            painter.drawEllipse(point, halo, halo)
            painter.setBrush(alpha(color, 115 * brightness))
            painter.drawEllipse(point, 1.15, 1.15)
            painter.setBrush(alpha(WHITE, 235 * brightness))
            painter.drawEllipse(point, 0.55, 0.55)

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

    def _draw_progress_ring(self, painter: QPainter, center: QPointF, radius: float, element_id: str, completion: float) -> None:
        state = self._state(element_id)
        ring_radius = self._radius(element_id, radius)
        pulse = 1.0 + completion * (0.16 + 0.10 * math.sin(self.clock.t * 19.0))
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
        direction = float(state.meta.get("direction", 1.0))
        arc.arcTo(rect, 90.0, direction * 360.0 * self.progress)
        glow_path(
            painter,
            arc,
            self._color(element_id),
            core=self._core(element_id),
            intensity=self._intensity(element_id) * pulse,
            core_width=max(0.7, 1.55 * state.scale),
            spread=1.05 * self._spread(element_id),
        )

    def _draw_polygon(self, painter: QPainter, center: QPointF, radius: float, element_id: str, inner_alpha: float) -> None:
        state = self._state(element_id)
        path = polygon_path(center, self._radius(element_id, radius), 6, self._angle(element_id, self.clock.t, 5.4))
        glow_path(
            painter,
            path,
            self._color(element_id),
            core=self._core(element_id),
            intensity=self._intensity(element_id, inner_alpha),
            core_width=max(0.55, 0.9 * state.scale),
            spread=self._spread(element_id),
        )

    def _draw_triangle(self, painter: QPainter, center: QPointF, radius: float, element_id: str, inner_alpha: float) -> None:
        state = self._state(element_id)
        angle = self._angle(element_id, self.clock.t, 8.4)
        triangle_radius = self._radius(element_id, radius)
        vertices = [polar(center, triangle_radius, angle + i * 120.0) for i in range(3)]
        path = QPainterPath()
        path.moveTo(vertices[0])
        path.lineTo(vertices[1])
        path.lineTo(vertices[2])
        path.closeSubpath()
        glow_path(
            painter,
            path,
            self._color(element_id),
            core=self._core(element_id),
            intensity=self._intensity(element_id, inner_alpha),
            core_width=max(0.55, 1.15 * state.scale),
            spread=self._spread(element_id),
        )

    def _draw_rune_ring(self, painter: QPainter, center: QPointF, radius: float, element_id: str, inner_alpha: float) -> None:
        state = self._state(element_id)
        count = int(state.meta.get("count_dense" if self.variant == 1 else "count_default", state.meta.get("count", 18)))
        count = max(1, count)
        ring_radius = self._radius(element_id, radius)
        angle = self._angle(element_id, self.clock.t, 18.0)
        size = float(state.meta.get("size", 11.0)) * state.scale
        offset = int(state.meta.get("offset", 0))
        skip: set[int] = set()
        if bool(state.meta.get("skip_designated", False)) and count >= 6:
            skip = {round(index * count / 6.0) % count for index in range(6)}

        if bool(state.meta.get("opaque_annulus", False)):
            ring_ids = [candidate_id for candidate_id, candidate in self.editor.elements.items() if candidate.kind == "ring" and candidate.link_group == state.link_group]
            if len(ring_ids) >= 2:
                ordered = sorted((self._radius(candidate_id, radius) for candidate_id in ring_ids), reverse=True)
                annulus = self.annulus_path(center, ordered[0], ordered[-1])
                self.fill_mask(painter, annulus)
                painter.save()
                painter.setClipPath(annulus)
            else:
                painter.save()
        else:
            painter.save()

        seed = sum((index + 1) * ord(char) for index, char in enumerate(element_id)) % 10000
        for slot in range(count):
            if slot in skip:
                continue
            degrees = angle + slot * 360.0 / count
            rune, rune_brightness, rune_color = rune_sample(state, slot, count, self.clock.t, base_index=offset, seed=seed)
            if rune_brightness <= 0.001:
                continue
            self.runes.draw(
                painter,
                rune,
                polar(center, ring_radius, degrees),
                size,
                degrees + 90.0,
                color=rune_color,
                core=self._core_for_color(rune_color),
                intensity=self._intensity(element_id, inner_alpha) * rune_brightness,
                spread=0.60 * self._spread(element_id),
            )
        painter.restore()

    def _draw_designated_outer_runes(self, painter: QPainter, center: QPointF, radius: float, element_id: str, inner_alpha: float) -> None:
        state = self._state(element_id)
        count = int(state.meta.get("count", 6))
        ring_radius = self._radius(element_id, radius)
        angle = self._angle(element_id, self.clock.t, 18.0)
        size = float(state.meta.get("size", 24.0)) * state.scale
        designated_indices = [ELDER_FUTHARK.index(rune) for rune in DESIGNATED_RUNES]
        for slot in range(count):
            degrees = angle + slot * 360.0 / count
            rune, rune_brightness, rune_color = rune_sample(
                state,
                slot,
                count,
                self.clock.t,
                base_index=designated_indices[slot % len(designated_indices)] - slot,
                seed=991,
            )
            if state.rune_speed <= 0.001:
                rune = DESIGNATED_RUNES[slot % len(DESIGNATED_RUNES)]
            if rune_brightness <= 0.001:
                continue
            self.runes.draw(
                painter,
                rune,
                polar(center, ring_radius, degrees),
                size,
                degrees + 90.0,
                color=rune_color,
                core=self._core_for_color(rune_color),
                intensity=self._intensity(element_id, inner_alpha) * rune_brightness,
                spread=0.82 * self._spread(element_id),
            )

    def _partial_geometry(self, element_id: str, center: QPointF, radius: float):
        state = self._state(element_id)
        frame_id = element_id if state.kind == "partial_frames" else self._partner(element_id, "partial_frames")
        frame_state = self._state(frame_id) if frame_id else state
        boundary_ids = [candidate_id for candidate_id, candidate in self.editor.elements.items() if candidate.kind == "ring"]
        ring_four = next((candidate_id for candidate_id in boundary_ids if "Fourth" in self._state(candidate_id).label), None)
        boundary_radius = self._radius(ring_four, radius) if ring_four else radius * 0.635
        triangle_id = self._partner(element_id, "triangle") or next((cid for cid, candidate in self.editor.elements.items() if candidate.kind == "triangle"), None)
        triangle_radius = self._radius(triangle_id, radius) if triangle_id else radius * 0.733
        center_angle = frame_state.base_rotation - 90.0
        centers = [polar(center, triangle_radius, center_angle + i * 120.0) for i in range(3)]
        track_radius = radius * frame_state.nominal_radius * frame_state.spread
        band_width = radius * float(frame_state.meta.get("band_width", 0.088)) * frame_state.scale
        return boundary_radius, centers, track_radius, band_width

    def _draw_partial_runes(self, painter: QPainter, center: QPointF, radius: float, element_id: str, inner_alpha: float) -> None:
        state = self._state(element_id)
        boundary_radius, centers, track_radius, band_width = self._partial_geometry(element_id, center, radius)
        count = int(state.meta.get("count_dense" if self.variant == 1 else "count_default", 24))
        size = float(state.meta.get("size", 13.5)) * state.scale
        angle = self._angle(element_id, self.clock.t, 12.0)
        for window_index, satellite in enumerate(centers):
            window = self.partial_window_path(center, boundary_radius, satellite, track_radius, band_width)
            self.fill_mask(painter, window)
            painter.save()
            painter.setClipPath(window)
            for slot in range(count):
                degrees = angle + window_index * 31.0 + slot * 360.0 / count
                rune, rune_brightness, rune_color = rune_sample(
                    state,
                    slot + window_index * count,
                    count * 3,
                    self.clock.t,
                    base_index=window_index * 8,
                    seed=211 + window_index,
                )
                if rune_brightness <= 0.001:
                    continue
                self.runes.draw(
                    painter,
                    rune,
                    polar(satellite, track_radius, degrees),
                    size,
                    degrees + 90.0,
                    color=rune_color,
                    core=self._core_for_color(rune_color),
                    intensity=self._intensity(element_id, inner_alpha) * rune_brightness,
                    spread=0.60 * self._spread(element_id),
                )
            painter.restore()

    def _draw_partial_frames(self, painter: QPainter, center: QPointF, radius: float, element_id: str, inner_alpha: float) -> None:
        state = self._state(element_id)
        boundary_radius, centers, track_radius, band_width = self._partial_geometry(element_id, center, radius)
        for satellite in centers:
            window = self.partial_window_path(center, boundary_radius, satellite, track_radius, band_width)
            glow_path(
                painter,
                window,
                self._color(element_id),
                core=self._core(element_id),
                intensity=self._intensity(element_id, inner_alpha),
                core_width=max(0.55, 0.9 * state.scale),
                spread=0.76 * self._spread(element_id),
            )

    def _large_circle_centers(self, element_id: str, center: QPointF, radius: float):
        state = self._state(element_id)
        centers_radius = self._radius(element_id, radius)
        angle = self._angle(element_id, self.clock.t, 8.4)
        return [polar(center, centers_radius, angle + i * 120.0) for i in range(3)]

    def _draw_large_circles(self, painter: QPainter, center: QPointF, radius: float, element_id: str, inner_alpha: float) -> None:
        state = self._state(element_id)
        sphere_radius = radius * float(state.meta.get("circle_radius", 0.130)) * state.scale
        for satellite in self._large_circle_centers(element_id, center, radius):
            self.fill_mask(painter, self.circle_path(satellite, sphere_radius))
            glow_ellipse(
                painter,
                satellite,
                sphere_radius,
                self._color(element_id),
                core=self._core(element_id),
                intensity=self._intensity(element_id, inner_alpha),
                core_width=max(0.55, 1.05 * state.scale),
                spread=self._spread(element_id),
            )

    def _draw_large_glyphs(self, painter: QPainter, center: QPointF, radius: float, element_id: str, inner_alpha: float) -> None:
        state = self._state(element_id)
        circle_id = self._partner(element_id, "large_rune_circles")
        if circle_id:
            centers = self._large_circle_centers(circle_id, center, radius)
        else:
            centers = [polar(center, self._radius(element_id, radius), state.base_rotation + i * 120.0) for i in range(3)]
        size = float(state.meta.get("size", 18.6)) * state.scale
        seen: set[str] = set()
        for slot, satellite in enumerate(centers):
            rune, rune_brightness, rune_color = rune_sample(state, slot, 3, self.clock.t, base_index=slot * 7 + 2, seed=503)
            if rune in seen:
                index = (ELDER_FUTHARK.index(rune) + 1) % len(ELDER_FUTHARK)
                while ELDER_FUTHARK[index] in seen:
                    index = (index + 1) % len(ELDER_FUTHARK)
                rune = ELDER_FUTHARK[index]
            seen.add(rune)
            if rune_brightness <= 0.001:
                continue
            self.runes.draw(
                painter,
                rune,
                satellite,
                size,
                state.base_rotation,
                color=rune_color,
                core=self._core_for_color(rune_color),
                intensity=self._intensity(element_id, inner_alpha) * rune_brightness,
                spread=0.78 * self._spread(element_id),
            )

    def _draw_tracers(self, painter: QPainter, center: QPointF, radius: float, element_id: str, inner_alpha: float) -> None:
        state = self._state(element_id)
        partner = self._partner(element_id, "polygon6")
        angle = self._angle(partner, self.clock.t, 5.4) if partner else state.base_rotation
        outer_radius = self._radius(element_id, radius)
        phase = self.clock.t * 0.48 * self.trace_speed
        travel = 0.5 - 0.5 * math.cos(phase * math.tau)
        inward = math.sin(phase * math.tau) >= 0.0
        for index in range(6):
            outer = polar(center, outer_radius, angle + index * 60.0)
            head = QPointF(outer.x() + (center.x() - outer.x()) * travel, outer.y() + (center.y() - outer.y()) * travel)
            tail_amount = max(0.0, travel - 0.60) if inward else min(1.0, travel + 0.60)
            tail = QPointF(outer.x() + (center.x() - outer.x()) * tail_amount, outer.y() + (center.y() - outer.y()) * tail_amount)
            comet(
                painter,
                tail,
                head,
                self._color(element_id),
                intensity=self._intensity(element_id, inner_alpha),
                spread=self._spread(element_id) * state.scale,
            )

    def _draw_element(self, painter: QPainter, center: QPointF, radius: float, element_id: str, inner_alpha: float, completion: float) -> None:
        if element_id not in self.editor.elements:
            return
        kind = self._state(element_id).kind
        if kind == "ring":
            self._draw_ring(painter, center, radius, element_id, inner_alpha)
        elif kind == "progress_ring":
            self._draw_progress_ring(painter, center, radius, element_id, completion)
        elif kind == "polygon6":
            self._draw_polygon(painter, center, radius, element_id, inner_alpha)
        elif kind == "triangle":
            self._draw_triangle(painter, center, radius, element_id, inner_alpha)
        elif kind == "rune_ring":
            self._draw_rune_ring(painter, center, radius, element_id, inner_alpha)
        elif kind == "designated_outer_runes":
            self._draw_designated_outer_runes(painter, center, radius, element_id, inner_alpha)
        elif kind == "partial_runes":
            self._draw_partial_runes(painter, center, radius, element_id, inner_alpha)
        elif kind == "partial_frames":
            self._draw_partial_frames(painter, center, radius, element_id, inner_alpha)
        elif kind == "large_rune_circles":
            self._draw_large_circles(painter, center, radius, element_id, inner_alpha)
        elif kind == "large_rune_glyphs":
            self._draw_large_glyphs(painter, center, radius, element_id, inner_alpha)
        elif kind == "tracers":
            self._draw_tracers(painter, center, radius, element_id, inner_alpha)

    def paintEvent(self, _event) -> None:
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing, True)
        painter.setRenderHint(QPainter.RenderHint.TextAntialiasing, True)

        center = QPointF(self.width() / 2.0, self.height() / 2.0)
        radius = 202.0
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
        haze.setColorAt(0.0, QColor(240, 167, 46, round(12 * self.glow * inner_alpha)))
        haze.setColorAt(0.46, QColor(207, 23, 51, round(9 * self.glow * inner_alpha)))
        haze.setColorAt(1.0, QColor(0, 0, 0, 0))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(haze)
        painter.drawEllipse(center, radius * 1.18, radius * 1.18)

        self._draw_sparkles(painter, center, radius)

        for element_id in list(self.editor.layer_order):
            self._draw_element(painter, center, radius, element_id, inner_alpha, completion)

        if self.variant == 3:
            self.draw_fractal_echo(painter, center, radius, self.clock.t, self.glow * inner_alpha)

        if flash > 0.002:
            flare = QRadialGradient(center, radius * 0.72)
            flare.setColorAt(0.0, QColor(255, 255, 255, round(170 * flash * self.glow)))
            flare.setColorAt(0.28, QColor(255, 211, 106, round(72 * flash * self.glow)))
            flare.setColorAt(1.0, QColor(0, 0, 0, 0))
            painter.setPen(Qt.PenStyle.NoPen)
            painter.setBrush(flare)
            painter.drawEllipse(center, radius * 0.72, radius * 0.72)

        self.draw_emblem(painter, center, radius, emblem_reveal)
