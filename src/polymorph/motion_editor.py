from __future__ import annotations

from dataclasses import asdict, dataclass
import math
from typing import Any

from PySide6.QtGui import QColor

from .motion_effects import CRIMSON, GOLD, WHITE, clamp, smoothstep


@dataclass
class ElementState:
    label: str
    capabilities: tuple[str, ...]
    spread: float = 1.0
    scale: float = 1.0
    base_rotation: float = 0.0
    color: str = "#ffffff"
    brightness: float = 1.0
    glow_spread: float = 1.0
    spin: float = 0.0
    static: bool = True
    pulse: bool = False
    rune_speed: float = 0.0
    link_group: str = "None"
    nominal_radius: float = 0.0


class MotionEditorState:
    LINK_GROUPS = (
        "None",
        "Outer rings",
        "Outer runes",
        "Hexagons",
        "Triangle family",
        "Partial windows",
        "Inner rings",
        "Custom A",
        "Custom B",
        "Custom C",
    )

    def __init__(self) -> None:
        self.pulse_speed = 1.0
        self.pulse_trail = 0.46
        self.pulse_end_dark = 0.16
        self.elements = self._defaults()

    @staticmethod
    def _state(label: str, capabilities: tuple[str, ...], **kwargs: Any) -> ElementState:
        return ElementState(label=label, capabilities=capabilities, **kwargs)

    def _defaults(self) -> dict[str, ElementState]:
        generic = ("spread", "scale", "color", "brightness", "glow", "pulse", "link")
        visual = ("spread", "scale", "color", "brightness", "glow", "link")
        rotatable = generic + ("rotation", "spin", "static")
        rune = rotatable + ("rune_speed",)
        rune_static = generic + ("rotation", "rune_speed")
        return {
            "progress_outer": self._state(
                "Outer progress ring", generic,
                color=WHITE.name(), brightness=1.0, glow_spread=1.0,
                pulse=False, nominal_radius=1.055, link_group="Outer rings",
            ),
            "progress_inner": self._state(
                "Second progress ring", generic,
                color=WHITE.name(), brightness=1.0, glow_spread=1.0,
                pulse=False, nominal_radius=1.005, link_group="Outer rings",
            ),
            "outer_runes": self._state(
                "Outer rune ring", rune,
                color=GOLD.name(), brightness=0.90, glow_spread=0.78,
                spin=0.68, static=False, pulse=True, nominal_radius=0.832,
                link_group="Outer runes",
            ),
            "outer_large_runes": self._state(
                "6 large outer runes", rune,
                color=WHITE.name(), brightness=1.0, glow_spread=0.92,
                spin=0.68, static=False, pulse=True, nominal_radius=0.832,
                link_group="Outer runes",
            ),
            "ring_three": self._state(
                "Third ring", generic,
                color=CRIMSON.name(), brightness=0.78, glow_spread=0.82,
                pulse=True, nominal_radius=0.762,
            ),
            "hex_a": self._state(
                "6-point polygon A", rotatable,
                color=CRIMSON.name(), brightness=0.72, glow_spread=0.90,
                base_rotation=-90.0, spin=-0.46, static=False, pulse=True,
                nominal_radius=0.733, link_group="Hexagons",
            ),
            "hex_b": self._state(
                "6-point polygon B", rotatable,
                color=CRIMSON.name(), brightness=0.58, glow_spread=0.86,
                base_rotation=-60.0, spin=-0.46, static=False, pulse=True,
                nominal_radius=0.733, link_group="Hexagons",
            ),
            "ring_four": self._state(
                "Fourth ring", generic,
                color=CRIMSON.name(), brightness=0.82, glow_spread=0.82,
                pulse=True, nominal_radius=0.635,
            ),
            "partial_frames": self._state(
                "3 partial rune frames", generic + ("rotation",),
                color=CRIMSON.name(), brightness=0.88, glow_spread=0.76,
                pulse=True, nominal_radius=0.455, link_group="Partial windows",
            ),
            "partial_runes": self._state(
                "Runes inside partial frames", rune,
                color=GOLD.name(), brightness=0.94, glow_spread=0.60,
                spin=-0.62, static=False, pulse=True, nominal_radius=0.455,
                link_group="Partial windows",
            ),
            "triangle": self._state(
                "Triangle", rotatable,
                color=CRIMSON.name(), brightness=0.90, glow_spread=1.0,
                base_rotation=-90.0, spin=0.0, static=True, pulse=True,
                nominal_radius=0.733, link_group="Triangle family",
            ),
            "large_rune_circles": self._state(
                "3 large rune circles", rotatable,
                color=CRIMSON.name(), brightness=0.92, glow_spread=0.88,
                base_rotation=-30.0, spin=0.0, static=True, pulse=True, nominal_radius=0.3665,
                link_group="Triangle family",
            ),
            "large_rune_glyphs": self._state(
                "Runes inside large circles", rune_static,
                color=WHITE.name(), brightness=1.0, glow_spread=0.86,
                rune_speed=0.70, pulse=True, nominal_radius=0.3665,
                link_group="Triangle family",
            ),
            "middle_runes": self._state(
                "Middle glimmer rune ring", rune_static,
                color=GOLD.name(), brightness=0.92, glow_spread=0.56,
                rune_speed=0.72, pulse=True, nominal_radius=0.285,
                link_group="Inner rings",
            ),
            "ring_five": self._state(
                "Fifth ring", generic,
                color=CRIMSON.name(), brightness=0.80, glow_spread=0.76,
                pulse=True, nominal_radius=0.198, link_group="Inner rings",
            ),
            "inner_runes": self._state(
                "Innermost rune ring", rune,
                color=GOLD.name(), brightness=0.88, glow_spread=0.54,
                spin=-0.52, static=False, pulse=True, nominal_radius=0.160,
                link_group="Inner rings",
            ),
            "ring_seven": self._state(
                "Seventh / inner band ring", generic,
                color=CRIMSON.name(), brightness=0.80, glow_spread=0.76,
                pulse=True, nominal_radius=0.120, link_group="Inner rings",
            ),
            "tracers": self._state(
                "Tracer spokes", visual,
                color=CRIMSON.name(), brightness=0.98, glow_spread=1.08,
                pulse=False, nominal_radius=0.733, link_group="Hexagons",
            ),
        }

    def get(self, element_id: str) -> ElementState:
        return self.elements[element_id]

    def supports(self, element_id: str, capability: str) -> bool:
        return capability in self.elements[element_id].capabilities

    def color(self, element_id: str) -> QColor:
        return QColor(self.elements[element_id].color)

    def animated_angle(self, element_id: str, t: float, degrees_per_second: float = 18.0) -> float:
        state = self.get(element_id)
        if state.static or not self.supports(element_id, "spin"):
            return state.base_rotation
        return state.base_rotation + t * degrees_per_second * state.spin

    def set_value(self, element_id: str, field: str, value: Any) -> None:
        source = self.get(element_id)
        if field == "link_group":
            source.link_group = str(value)
            return
        targets = [element_id]
        if source.link_group != "None" and field in {"spread", "scale", "base_rotation", "brightness", "glow_spread"}:
            targets = [
                candidate_id
                for candidate_id, candidate in self.elements.items()
                if candidate.link_group == source.link_group
                and self._field_supported(candidate_id, field)
            ]
        for target_id in targets:
            if not self._field_supported(target_id, field):
                continue
            setattr(self.elements[target_id], field, value)

    def _field_supported(self, element_id: str, field: str) -> bool:
        capability = {
            "spread": "spread",
            "scale": "scale",
            "base_rotation": "rotation",
            "color": "color",
            "brightness": "brightness",
            "glow_spread": "glow",
            "spin": "spin",
            "static": "static",
            "pulse": "pulse",
            "rune_speed": "rune_speed",
            "link_group": "link",
        }.get(field)
        return capability is not None and self.supports(element_id, capability)

    def pulse_multiplier(self, element_id: str, t: float) -> float:
        state = self.get(element_id)
        if not state.pulse:
            return 1.0
        participating = [
            (candidate_id, candidate.nominal_radius * candidate.spread)
            for candidate_id, candidate in self.elements.items()
            if candidate.pulse
        ]
        participating.sort(key=lambda item: item[1], reverse=True)
        ids = [candidate_id for candidate_id, _ in participating]
        if element_id not in ids:
            return 1.0

        count = max(1, len(ids))
        index = ids.index(element_id)
        speed = max(0.05, self.pulse_speed)
        dark = clamp(self.pulse_end_dark, 0.0, 0.85)
        active_span = max(0.08, 1.0 - dark)
        trail = clamp(self.pulse_trail, 0.05, active_span)
        phase = (t * 0.16 * speed) % 1.0
        local = (phase - index / count) % 1.0
        rise_end = min(active_span * 0.30, max(0.04, trail * 0.34))
        hold_end = min(active_span, rise_end + trail * 0.46)
        if local < rise_end:
            return 0.16 + 0.84 * smoothstep(0.0, rise_end, local)
        if local < hold_end:
            return 1.0
        if local < active_span:
            return 1.0 - 0.84 * smoothstep(hold_end, active_span, local)
        return 0.12

    def rune_offset(self, element_id: str, t: float, rate: float = 4.0) -> int:
        state = self.get(element_id)
        if state.rune_speed <= 0.001:
            return 0
        return math.floor(t * rate * state.rune_speed)

    def export(self) -> dict[str, Any]:
        return {
            "format": "polymorph-motion-spec",
            "version": 1,
            "pulse": {
                "speed": self.pulse_speed,
                "trail": self.pulse_trail,
                "end_dark": self.pulse_end_dark,
            },
            "elements": {
                element_id: asdict(state)
                for element_id, state in self.elements.items()
            },
        }
