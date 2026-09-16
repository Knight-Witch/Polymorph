from __future__ import annotations

import math

from PySide6.QtCore import QPointF, QRectF, Qt
from PySide6.QtGui import QColor, QBrush, QFont, QLinearGradient, QPainter, QPainterPath, QPen, QTransform

from . import motion_loader as base_loader
from .motion_effects import GOLD, GOLD_CORE, MASK_BG, WHITE, RunePainter, alpha, clamp, glow_ellipse, glow_path, polar, smoothstep
from .motion_loader import ArcaneLoader
from .motion_runes import hash01, rune_sample as base_rune_sample
from .motion_v7_state import ExtendedEditorState, RUNE_KINDS

class ExtendedRunePainter(RunePainter):
    def __init__(self, family: str) -> None:
        super().__init__(family)
        self.render_mode = "Outline"
        self.weight = "Regular"
        self._v7_cache: dict[tuple[str, int, str], QPainterPath] = {}

    def path(self, rune: str, size: float) -> QPainterPath:
        weight_name = str(self.weight or "Regular").title()
        key = (rune, max(6, round(size)), weight_name)
        cached = self._v7_cache.get(key)
        if cached is not None:
            return QPainterPath(cached)
        font = QFont(self.family)
        font.setPixelSize(key[1])
        font.setWeight({
            "Thin": QFont.Weight.Thin,
            "Regular": QFont.Weight.Normal,
            "Bold": QFont.Weight.Bold,
        }.get(weight_name, QFont.Weight.Normal))
        path = QPainterPath()
        path.addText(QPointF(0.0, 0.0), font, rune)
        bounds = path.boundingRect()
        transform = QTransform()
        transform.translate(-bounds.center().x(), -bounds.center().y())
        centered = transform.map(path)
        self._v7_cache[key] = centered
        return QPainterPath(centered)

    def draw(self, painter: QPainter, rune: str, position: QPointF, size: float, rotation: float, *, color: QColor = GOLD, core: QColor | None = None, intensity: float = 1.0, spread: float = 0.72) -> None:
        alpha_scale = color.alpha() / 255.0
        intensity *= alpha_scale
        if intensity <= 0.001:
            return
        painter.save()
        painter.translate(position)
        painter.rotate(rotation)
        path = self.path(rune, size)
        rune_core = core if core is not None else (GOLD_CORE if color == GOLD else WHITE)
        if str(self.render_mode).lower() == "solid":
            glow_path(
                painter,
                path,
                color,
                core=rune_core,
                intensity=intensity * 0.78,
                core_width=max(0.55, size * 0.035),
                spread=spread,
            )
            painter.setPen(Qt.PenStyle.NoPen)
            painter.setBrush(alpha(color, 205 * intensity))
            painter.drawPath(path)
            painter.setBrush(alpha(rune_core, 160 * intensity))
            painter.drawPath(path)
        else:
            glow_path(
                painter,
                path,
                color,
                core=rune_core,
                intensity=intensity,
                core_width=max(0.65, size * 0.055),
                spread=spread,
            )
        painter.restore()


def draw_comet_v7(painter: QPainter, tail: QPointF, head: QPointF, color: QColor, *, intensity: float, spread: float, fade_span: float, balance: float) -> None:
    alpha_scale = color.alpha() / 255.0
    intensity *= alpha_scale
    if intensity <= 0.001:
        return
    fade_span = clamp(fade_span, 0.02, 1.0)
    balance = clamp(balance, -1.0, 1.0)
    mid_a = clamp(0.28 + 0.22 * balance + 0.12 * (1.0 - fade_span), 0.08, 0.70)
    mid_b = clamp(0.70 + 0.18 * balance - 0.10 * (1.0 - fade_span), mid_a + 0.05, 0.94)
    gradient = QLinearGradient(tail, head)
    gradient.setColorAt(0.0, QColor(color.red(), color.green(), color.blue(), 0))
    gradient.setColorAt(mid_a, alpha(color, 30 * intensity))
    gradient.setColorAt(mid_b, alpha(color, 140 * intensity))
    gradient.setColorAt(1.0, alpha(WHITE, 255 * intensity))
    for width, opacity in (
        (14.0 * spread, 0.17),
        (9.0 * spread, 0.28),
        (5.2 * spread, 0.48),
        (2.6 * spread, 0.78),
        (1.1, 1.0),
    ):
        painter.setPen(QPen(QBrush(gradient), max(0.8, width * opacity), Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap))
        painter.drawLine(tail, head)
    for size, opacity in ((9.0 * spread, 15), (6.0 * spread, 25), (3.8 * spread, 55), (2.0 * spread, 125)):
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(alpha(color, opacity * intensity))
        painter.drawEllipse(head, size, size)
    painter.setBrush(alpha(WHITE, 245 * intensity))
    painter.drawEllipse(head, 1.35, 1.35)


def rune_sample_v7(state, slot: int, count: int, t: float, *, base_index: int = 0, seed: int = 0):
    transition_enabled = bool(getattr(state, "rune_transition_enabled", True))
    glimmer_enabled = bool(getattr(state, "rune_glimmer_enabled", True))
    old_speed = state.rune_speed
    old_mode = state.glimmer_type
    try:
        if not transition_enabled:
            state.rune_speed = 0.0
        if not glimmer_enabled:
            state.glimmer_type = "None"
        return base_rune_sample(state, slot, count, t, base_index=base_index, seed=seed)
    finally:
        state.rune_speed = old_speed
        state.glimmer_type = old_mode


class ExtendedArcaneLoader(ArcaneLoader):
    def __init__(self, rune_family: str, parent=None) -> None:
        super().__init__(rune_family, parent)
        self.editor = ExtendedEditorState()
        self.runes = ExtendedRunePainter(rune_family)
        base_loader.rune_sample = rune_sample_v7
        self._active_element_id: str | None = None

    def _optional_color(self, value: str) -> QColor:
        if not value:
            return QColor(0, 0, 0, 0)
        color = QColor(value)
        return color if color.isValid() else QColor(0, 0, 0, 0)

    def _color(self, element_id: str) -> QColor:
        return self._optional_color(str(self._state(element_id).color))

    def _intensity(self, element_id: str, inner_alpha: float = 1.0) -> float:
        state = self._state(element_id)
        color_alpha = self._color(element_id).alpha() / 255.0
        return self.glow * state.brightness * self.editor.pulse_multiplier(element_id, self.clock.t) * inner_alpha * color_alpha

    def fill_mask(self, painter: QPainter, path: QPainterPath) -> None:
        opacity = 1.0
        if self._active_element_id in self.editor.elements:
            opacity = clamp(float(getattr(self._state(self._active_element_id), "opaque_fill_alpha", 1.0)))
        if opacity <= 0.001:
            return
        painter.save()
        painter.setPen(Qt.PenStyle.NoPen)
        mask = QColor(MASK_BG)
        mask.setAlpha(round(255 * opacity))
        painter.setBrush(mask)
        painter.drawPath(path)
        painter.restore()

    def _draw_sparkles(self, painter: QPainter, center: QPointF, radius: float) -> None:
        state = self.editor.sparkles
        if not state.enabled or state.density <= 0.001 or state.max_brightness <= 0.001:
            return
        count = max(0, min(420, round(12 + state.density * 300)))
        max_radius = radius * (0.20 + 1.05 * max(0.0, state.spread))
        colors = [self._optional_color(state.color_1), self._optional_color(state.color_2), self._optional_color(state.color_3)]
        for index in range(count):
            rr = math.sqrt(hash01(index, 11)) * max_radius
            degrees = hash01(index, 17) * 360.0
            point = polar(center, rr, degrees)
            rate = 0.55 + 1.2 * hash01(index, 23)
            phase = hash01(index, 29) * math.tau
            wave = (0.5 + 0.5 * math.sin(self.clock.t * state.speed * rate * 2.4 + phase)) ** 2
            normalized_radius = rr / max(0.001, max_radius)
            fade_span = max(0.001, min(0.98, state.fade))
            fade_start = 1.0 - fade_span
            edge_fade = 1.0 if normalized_radius <= fade_start else 1.0 - smoothstep(fade_start, 1.0, normalized_radius)
            brightness = state.max_brightness * wave * edge_fade
            if brightness < 0.025:
                continue
            cycle = int(self.clock.t * max(0.05, state.speed) * 0.5 + hash01(index, 31) * 9)
            color = colors[(index + cycle) % len(colors)]
            alpha_scale = color.alpha() / 255.0
            if alpha_scale <= 0.001:
                continue
            painter.setPen(Qt.PenStyle.NoPen)
            painter.setBrush(alpha(color, 42 * brightness * alpha_scale))
            painter.drawEllipse(point, 1.85, 1.85)
            painter.setBrush(alpha(color, 125 * brightness * alpha_scale))
            painter.drawEllipse(point, 1.05, 1.05)
            painter.setBrush(alpha(WHITE, 235 * brightness * alpha_scale))
            painter.drawEllipse(point, 0.48, 0.48)

    def _draw_progress_ring(self, painter: QPainter, center: QPointF, radius: float, element_id: str, completion: float) -> None:
        state = self._state(element_id)
        ring_radius = self._radius(element_id, radius)
        ring_type = str(getattr(state, "loader_ring_type", "Progress Arc"))
        rect = QRectF(center.x() - ring_radius, center.y() - ring_radius, ring_radius * 2.0, ring_radius * 2.0)
        direction = float(state.meta.get("direction", 1.0))
        if ring_type == "Static Ring":
            glow_ellipse(
                painter,
                center,
                ring_radius,
                self._color(element_id),
                core=self._core(element_id),
                intensity=self._intensity(element_id),
                core_width=max(0.7, 1.25 * state.scale),
                spread=self._spread(element_id),
            )
            return

        glow_ellipse(
            painter,
            center,
            ring_radius,
            self._color(element_id),
            core=self._core(element_id),
            intensity=self._intensity(element_id) * 0.18,
            core_width=max(0.55, 0.8 * state.scale),
            spread=0.70 * self._spread(element_id),
        )
        sweep_total = direction * 360.0 * self.progress
        if ring_type == "Gradient Tail":
            tail_fraction = clamp(float(getattr(state, "loader_tail_length", 0.28)), 0.01, 1.0)
            tail_degrees = max(6.0, 360.0 * tail_fraction)
            fade = clamp(float(getattr(state, "loader_tail_fade_span", 0.60)), 0.02, 1.0)
            balance = clamp(float(getattr(state, "loader_tail_balance", 0.0)), -1.0, 1.0)
            segments = 24
            gamma = 0.35 + (1.0 - fade) * 4.2
            for index in range(segments):
                frac0 = index / segments
                frac1 = (index + 1) / segments
                strength = max(0.0, 1.0 - frac0) ** gamma
                if balance > 0.0:
                    strength = strength ** (0.55 + 0.40 * balance)
                elif balance < 0.0:
                    strength = strength ** (1.0 + 1.8 * (-balance))
                start_angle = 90.0 + sweep_total - direction * tail_degrees * frac1
                arc = QPainterPath()
                arc.arcMoveTo(rect, start_angle)
                arc.arcTo(rect, start_angle, direction * tail_degrees / segments)
                glow_path(
                    painter,
                    arc,
                    self._color(element_id),
                    core=self._core(element_id),
                    intensity=self._intensity(element_id) * strength,
                    core_width=max(0.7, 1.55 * state.scale),
                    spread=(0.72 + 0.55 * fade) * self._spread(element_id),
                )
            return

        arc = QPainterPath()
        arc.arcMoveTo(rect, 90.0)
        arc.arcTo(rect, 90.0, sweep_total)
        glow_path(
            painter,
            arc,
            self._color(element_id),
            core=self._core(element_id),
            intensity=self._intensity(element_id),
            core_width=max(0.7, 1.55 * state.scale),
            spread=1.05 * self._spread(element_id),
        )

    def _draw_tracers(self, painter: QPainter, center: QPointF, radius: float, element_id: str, inner_alpha: float) -> None:
        state = self._state(element_id)
        partner = self._partner(element_id, "polygon6")
        angle = self._angle(partner, self.clock.t, 5.4) if partner else state.base_rotation
        outer_radius = self._radius(element_id, radius)
        phase = self.clock.t * 0.48 * self.trace_speed
        travel = 0.5 - 0.5 * math.cos(phase * math.tau)
        inward = math.sin(phase * math.tau) >= 0.0
        tracer_len = clamp(float(getattr(state, "tracer_length", 0.60)), 0.02, 1.4)
        fade_span = clamp(float(getattr(state, "tracer_fade_span", 0.60)), 0.02, 1.0)
        balance = clamp(float(getattr(state, "tracer_balance", 0.0)), -1.0, 1.0)
        toward_head = tracer_len * (0.50 + 0.34 * max(0.0, balance) + 0.15 * max(0.0, -balance))
        toward_tail = tracer_len * (0.50 + 0.34 * max(0.0, -balance) + 0.15 * max(0.0, balance))
        for index in range(6):
            outer = polar(center, outer_radius, angle + index * 60.0)
            head = QPointF(outer.x() + (center.x() - outer.x()) * travel, outer.y() + (center.y() - outer.y()) * travel)
            tail_amount = max(0.0, travel - toward_tail) if inward else min(1.0, travel + toward_head)
            tail = QPointF(outer.x() + (center.x() - outer.x()) * tail_amount, outer.y() + (center.y() - outer.y()) * tail_amount)
            draw_comet_v7(
                painter,
                tail,
                head,
                self._color(element_id),
                intensity=self._intensity(element_id, inner_alpha),
                spread=self._spread(element_id) * state.scale,
                fade_span=fade_span,
                balance=balance,
            )

    def _draw_element(self, painter: QPainter, center: QPointF, radius: float, element_id: str, inner_alpha: float, completion: float) -> None:
        if element_id not in self.editor.elements:
            return
        state = self._state(element_id)
        if not bool(getattr(state, "enabled", True)):
            return
        previous_active = self._active_element_id
        previous_mode = self.runes.render_mode
        previous_weight = self.runes.weight
        self._active_element_id = element_id
        if state.kind in RUNE_KINDS:
            self.runes.render_mode = str(getattr(state, "rune_render_mode", "Outline"))
            self.runes.weight = str(getattr(state, "rune_weight", "Regular"))
        try:
            super()._draw_element(painter, center, radius, element_id, inner_alpha, completion)
        finally:
            self._active_element_id = previous_active
            self.runes.render_mode = previous_mode
            self.runes.weight = previous_weight

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
        else:
            completion = smoothstep(0.0, 0.55, age)
            inner_alpha = 1.0 - smoothstep(0.24, 1.30, age)
            emblem_reveal = smoothstep(0.42, 1.42, age)

        from PySide6.QtGui import QRadialGradient
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
        self.draw_emblem(painter, center, radius, emblem_reveal)
