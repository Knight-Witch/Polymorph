from __future__ import annotations

from copy import deepcopy
from dataclasses import asdict, dataclass, field
import math
import re
from typing import Any

from PySide6.QtGui import QColor

from .motion_effects import CRIMSON, GOLD, WHITE, clamp, smoothstep


RUNE_CAPS = (
    "spread", "scale", "rotation", "color", "brightness", "glow", "spin", "static", "link",
    "rune_transition",
)
GEOMETRY_CAPS = (
    "spread", "scale", "rotation", "color", "brightness", "glow", "spin", "static", "pulse", "link",
)
RING_CAPS = ("spread", "scale", "color", "brightness", "glow", "pulse", "link")
VISUAL_CAPS = ("spread", "scale", "color", "brightness", "glow", "link")


@dataclass
class ElementState:
    label: str
    kind: str
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
    meta: dict[str, Any] = field(default_factory=dict)

    # Standard rune transition / glimmer behavior. rune_speed is retained as the
    # persisted field name for backwards compatibility with v4 exports.
    rune_timing_randomness: float = 0.72
    rune_transition_type: str = "Fade"
    rune_bright_hold: float = 0.70
    rune_dark_hold: float = 0.14
    rune_min_brightness: float = 0.0
    rune_max_brightness: float = 1.0
    rune_dim_color: str = "#9a5517"
    rune_bright_color: str = "#f0a72e"

    # Special glimmer mode is used when rune_speed == 0. It never changes glyphs.
    glimmer_type: str = "Twinkle"
    radial_speed: float = 1.0
    radial_length: float = 0.28
    radial_fade_span: float = 0.55
    radial_balance: float = 0.0
    radial_direction: int = 1
    twinkle_speed: float = 1.0
    twinkle_randomness: float = 0.80
    rune_pulse_speed: float = 1.0
    rune_pulse_fade_span: float = 0.55
    rune_pulse_balance: float = 0.0


@dataclass
class SparkleState:
    enabled: bool = True
    spread: float = 0.92
    fade: float = 0.62
    density: float = 0.34
    speed: float = 1.0
    max_brightness: float = 0.52
    color_1: str = "#ffffff"
    color_2: str = "#ffd36a"
    color_3: str = "#cf1733"


class MotionEditorState:
    BASE_LINK_GROUPS = (
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
        self.sparkles = SparkleState()
        self.elements = self._defaults()
        self.layer_order = self._default_layer_order()

    @staticmethod
    def _state(label: str, kind: str, capabilities: tuple[str, ...], **kwargs: Any) -> ElementState:
        return ElementState(label=label, kind=kind, capabilities=capabilities, **kwargs)

    def _defaults(self) -> dict[str, ElementState]:
        return {
            "progress_outer": self._state(
                "Outer progress ring", "progress_ring", RING_CAPS,
                color=WHITE.name(), brightness=1.0, glow_spread=1.0,
                pulse=False, nominal_radius=1.055, link_group="Outer rings",
                meta={"direction": -1.0},
            ),
            "progress_inner": self._state(
                "Second progress ring", "progress_ring", RING_CAPS,
                color=WHITE.name(), brightness=1.0, glow_spread=1.0,
                pulse=False, nominal_radius=1.005, link_group="Outer rings",
                meta={"direction": 1.0},
            ),
            "outer_runes": self._state(
                "Outer rune ring", "rune_ring", RUNE_CAPS,
                color=GOLD.name(), brightness=0.90, glow_spread=0.78,
                spin=0.68, static=False, pulse=False, nominal_radius=0.832,
                link_group="Outer runes", rune_speed=0.0,
                rune_timing_randomness=0.72,
                rune_dim_color="#9a5517", rune_bright_color=GOLD.name(),
                glimmer_type="Twinkle", twinkle_speed=0.72, twinkle_randomness=0.76,
                meta={"count_dense": 30, "count_default": 24, "size": 13.2, "offset": 0, "skip_designated": True},
            ),
            "outer_large_runes": self._state(
                "6 large outer runes", "designated_outer_runes", RUNE_CAPS,
                color=WHITE.name(), brightness=1.0, glow_spread=0.92,
                spin=0.68, static=False, pulse=False, nominal_radius=0.832,
                link_group="Outer runes", rune_speed=0.0,
                rune_timing_randomness=0.72,
                rune_dim_color="#7f7f7f", rune_bright_color=WHITE.name(),
                glimmer_type="Twinkle", twinkle_speed=0.72, twinkle_randomness=0.60,
                meta={"count": 6, "size": 24.0},
            ),
            "ring_three": self._state(
                "Third ring", "ring", RING_CAPS,
                color=CRIMSON.name(), brightness=0.78, glow_spread=0.82,
                pulse=True, nominal_radius=0.762,
            ),
            "hex_a": self._state(
                "6-point polygon A", "polygon6", GEOMETRY_CAPS,
                color=CRIMSON.name(), brightness=0.72, glow_spread=0.90,
                base_rotation=-90.0, spin=-0.46, static=False, pulse=True,
                nominal_radius=0.733, link_group="Hexagons",
            ),
            "hex_b": self._state(
                "6-point polygon B", "polygon6", GEOMETRY_CAPS,
                color=CRIMSON.name(), brightness=0.58, glow_spread=0.86,
                base_rotation=-60.0, spin=-0.46, static=False, pulse=True,
                nominal_radius=0.733, link_group="Hexagons",
            ),
            "ring_four": self._state(
                "Fourth ring", "ring", RING_CAPS,
                color=CRIMSON.name(), brightness=0.82, glow_spread=0.82,
                pulse=True, nominal_radius=0.635,
            ),
            "partial_frames": self._state(
                "3 partial rune frames", "partial_frames",
                ("spread", "scale", "rotation", "color", "brightness", "glow", "pulse", "link"),
                color=CRIMSON.name(), brightness=0.88, glow_spread=0.76,
                pulse=True, nominal_radius=0.455, link_group="Partial windows",
                meta={"band_width": 0.088},
            ),
            "partial_runes": self._state(
                "Runes inside partial frames", "partial_runes", RUNE_CAPS,
                color=GOLD.name(), brightness=0.94, glow_spread=0.60,
                spin=-0.62, static=False, pulse=False, nominal_radius=0.455,
                link_group="Partial windows", rune_speed=0.0,
                rune_timing_randomness=0.82,
                rune_dim_color="#9a5517", rune_bright_color=GOLD.name(),
                glimmer_type="Twinkle", twinkle_speed=0.76, twinkle_randomness=0.84,
                meta={"count_dense": 30, "count_default": 24, "size": 13.5},
            ),
            "triangle": self._state(
                "Triangle", "triangle", GEOMETRY_CAPS,
                color=CRIMSON.name(), brightness=0.90, glow_spread=1.0,
                base_rotation=-90.0, spin=0.0, static=True, pulse=True,
                nominal_radius=0.733, link_group="Triangle family",
            ),
            "large_rune_circles": self._state(
                "3 large rune circles", "large_rune_circles", GEOMETRY_CAPS,
                color=CRIMSON.name(), brightness=0.92, glow_spread=0.88,
                base_rotation=-30.0, spin=0.0, static=True, pulse=True, nominal_radius=0.3665,
                link_group="Triangle family", meta={"circle_radius": 0.130},
            ),
            "large_rune_glyphs": self._state(
                "Runes inside large circles", "large_rune_glyphs", RUNE_CAPS,
                color=WHITE.name(), brightness=1.0, glow_spread=0.86,
                base_rotation=0.0, spin=0.0, static=True, rune_speed=0.70,
                pulse=False, nominal_radius=0.3665, link_group="Triangle family",
                rune_timing_randomness=0.88,
                rune_dim_color="#737373", rune_bright_color=WHITE.name(),
                glimmer_type="Twinkle", twinkle_speed=0.82, twinkle_randomness=0.90,
                meta={"count": 3, "size": 18.6},
            ),
            "middle_runes": self._state(
                "Middle glimmer rune ring", "rune_ring", RUNE_CAPS,
                color=GOLD.name(), brightness=0.92, glow_spread=0.56,
                base_rotation=-90.0, spin=0.0, static=True, rune_speed=0.72,
                pulse=False, nominal_radius=0.285, link_group="Inner rings",
                rune_timing_randomness=0.95,
                rune_dim_color="#8b4c16", rune_bright_color=GOLD.name(),
                glimmer_type="Twinkle", twinkle_speed=0.92, twinkle_randomness=0.92,
                meta={"count_dense": 21, "count_default": 18, "size": 10.5, "offset": 0},
            ),
            "ring_five": self._state(
                "Fifth ring", "ring", RING_CAPS,
                color=CRIMSON.name(), brightness=0.80, glow_spread=0.76,
                pulse=True, nominal_radius=0.198, link_group="Inner rings",
            ),
            "inner_runes": self._state(
                "Innermost rune ring", "rune_ring", RUNE_CAPS,
                color=GOLD.name(), brightness=0.88, glow_spread=0.54,
                spin=-0.52, static=False, pulse=False, nominal_radius=0.160,
                link_group="Inner rings", rune_speed=0.0,
                rune_timing_randomness=0.72,
                rune_dim_color="#9a5517", rune_bright_color=GOLD.name(),
                glimmer_type="Twinkle", twinkle_speed=0.66, twinkle_randomness=0.72,
                meta={"count_dense": 20, "count_default": 18, "size": 8.8, "offset": 5, "opaque_annulus": True},
            ),
            "ring_seven": self._state(
                "Seventh / inner band ring", "ring", RING_CAPS,
                color=CRIMSON.name(), brightness=0.80, glow_spread=0.76,
                pulse=True, nominal_radius=0.120, link_group="Inner rings",
            ),
            "tracers": self._state(
                "Tracer spokes", "tracers", VISUAL_CAPS,
                color=CRIMSON.name(), brightness=0.98, glow_spread=1.08,
                pulse=False, nominal_radius=0.733, link_group="Hexagons",
            ),
        }

    def _default_layer_order(self) -> list[str]:
        # Bottom -> top. Large outer runes intentionally sit above both progress rings.
        return [
            "tracers",
            "ring_three",
            "hex_a",
            "hex_b",
            "triangle",
            "middle_runes",
            "ring_five",
            "inner_runes",
            "ring_seven",
            "partial_runes",
            "partial_frames",
            "ring_four",
            "large_rune_circles",
            "large_rune_glyphs",
            "outer_runes",
            "progress_outer",
            "progress_inner",
            "outer_large_runes",
        ]

    def get(self, element_id: str) -> ElementState:
        return self.elements[element_id]

    def supports(self, element_id: str, capability: str) -> bool:
        return capability in self.elements[element_id].capabilities

    def color(self, element_id: str) -> QColor:
        return QColor(self.elements[element_id].color)

    def link_groups(self) -> list[str]:
        groups = list(self.BASE_LINK_GROUPS)
        for state in self.elements.values():
            if state.link_group not in groups:
                groups.append(state.link_group)
        return groups

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
        if source.link_group != "None":
            targets = [
                candidate_id
                for candidate_id, candidate in self.elements.items()
                if candidate.link_group == source.link_group and self._field_supported(candidate_id, field)
            ]
        for target_id in targets:
            if self._field_supported(target_id, field):
                setattr(self.elements[target_id], field, value)
                if field == "color" and self.supports(target_id, "rune_transition"):
                    self.elements[target_id].rune_bright_color = str(value)

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
            "link_group": "link",
            "rune_speed": "rune_transition",
            "rune_timing_randomness": "rune_transition",
            "rune_transition_type": "rune_transition",
            "rune_bright_hold": "rune_transition",
            "rune_dark_hold": "rune_transition",
            "rune_min_brightness": "rune_transition",
            "rune_max_brightness": "rune_transition",
            "rune_dim_color": "rune_transition",
            "rune_bright_color": "rune_transition",
            "glimmer_type": "rune_transition",
            "radial_speed": "rune_transition",
            "radial_length": "rune_transition",
            "radial_fade_span": "rune_transition",
            "radial_balance": "rune_transition",
            "radial_direction": "rune_transition",
            "twinkle_speed": "rune_transition",
            "twinkle_randomness": "rune_transition",
            "rune_pulse_speed": "rune_transition",
            "rune_pulse_fade_span": "rune_transition",
            "rune_pulse_balance": "rune_transition",
        }.get(field)
        return capability is not None and self.supports(element_id, capability)

    def pulse_multiplier(self, element_id: str, t: float) -> float:
        state = self.get(element_id)
        if not state.pulse or not self.supports(element_id, "pulse"):
            return 1.0
        participating = [
            (candidate_id, candidate.nominal_radius * candidate.spread)
            for candidate_id, candidate in self.elements.items()
            if candidate.pulse and "pulse" in candidate.capabilities
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

    def snapshot(self) -> dict[str, Any]:
        return self.export()

    def export(self) -> dict[str, Any]:
        return {
            "format": "polymorph-motion-spec",
            "version": 2,
            "pulse": {
                "speed": self.pulse_speed,
                "trail": self.pulse_trail,
                "end_dark": self.pulse_end_dark,
            },
            "sparkles": asdict(self.sparkles),
            "layer_order": list(self.layer_order),
            "elements": {element_id: asdict(state) for element_id, state in self.elements.items()},
        }

    def load(self, payload: dict[str, Any]) -> None:
        if payload.get("format") not in (None, "polymorph-motion-spec"):
            raise ValueError("Not a Polymorph motion spec")
        version = int(payload.get("version", 1) or 1)
        defaults = self._defaults()
        incoming_elements = payload.get("elements", {})
        loaded: dict[str, ElementState] = {}
        for element_id, raw in incoming_elements.items():
            base = deepcopy(defaults.get(element_id))
            if base is None:
                kind = str(raw.get("kind", "ring"))
                caps = tuple(raw.get("capabilities", RING_CAPS))
                base = ElementState(label=str(raw.get("label", element_id)), kind=kind, capabilities=caps)
            for key, value in raw.items():
                if hasattr(base, key):
                    if key == "capabilities":
                        if version < 2 and element_id in defaults:
                            continue
                        value = tuple(value)
                    if key == "kind" and version < 2 and element_id in defaults:
                        continue
                    setattr(base, key, value)
            # v4 exports had only one rune color. Preserve that user choice as the
            # new bright-rune color instead of silently reverting to the v5 default.
            if "rune_bright_color" not in raw and "rune_transition" in base.capabilities:
                base.rune_bright_color = str(raw.get("color", base.rune_bright_color))
            # v4 exports had no kind; keep canonical kind from defaults.
            loaded[element_id] = base
        # If a legacy preset omitted elements, preserve only the ones it actually exported if any;
        # otherwise use a complete fresh scene.
        self.elements = loaded if loaded else defaults
        pulse = payload.get("pulse", {})
        self.pulse_speed = float(pulse.get("speed", self.pulse_speed))
        self.pulse_trail = float(pulse.get("trail", self.pulse_trail))
        self.pulse_end_dark = float(pulse.get("end_dark", self.pulse_end_dark))
        sparkle = payload.get("sparkles")
        if isinstance(sparkle, dict):
            for key, value in sparkle.items():
                if hasattr(self.sparkles, key):
                    setattr(self.sparkles, key, value)
        requested_order = [str(value) for value in payload.get("layer_order", [])]
        order = [element_id for element_id in requested_order if element_id in self.elements]
        for element_id in self.elements:
            if element_id not in order:
                order.append(element_id)
        # Legacy v4 presets had no layer order. In that case use the new canonical order so the
        # six large outer runes are above the progress rings without altering any saved values.
        if not requested_order:
            order = [element_id for element_id in self._default_layer_order() if element_id in self.elements]
            order.extend(element_id for element_id in self.elements if element_id not in order)
        self.layer_order = order

    def remove_element(self, element_id: str) -> None:
        self.elements.pop(element_id, None)
        self.layer_order = [value for value in self.layer_order if value != element_id]

    def _unique_id(self, source_id: str) -> str:
        stem = re.sub(r"_copy\d+$", "", source_id)
        index = 1
        while f"{stem}_copy{index}" in self.elements:
            index += 1
        return f"{stem}_copy{index}"

    def _unique_group(self, source_group: str) -> str:
        stem = source_group if source_group != "None" else "Group"
        existing = set(self.link_groups())
        index = 1
        while f"{stem} copy {index}" in existing:
            index += 1
        return f"{stem} copy {index}"

    def duplicate_element(self, element_id: str) -> str:
        new_id = self._unique_id(element_id)
        clone = deepcopy(self.get(element_id))
        clone.label = f"{clone.label} copy"
        clone.link_group = "None"
        self.elements[new_id] = clone
        position = self.layer_order.index(element_id) + 1 if element_id in self.layer_order else len(self.layer_order)
        self.layer_order.insert(position, new_id)
        return new_id

    def duplicate_element_with_group(self, element_id: str) -> str:
        source = self.get(element_id)
        if source.link_group == "None":
            return self.duplicate_element(element_id)
        members = [candidate_id for candidate_id, state in self.elements.items() if state.link_group == source.link_group]
        new_group = self._unique_group(source.link_group)
        selected_clone = ""
        insert_after = max((self.layer_order.index(mid) for mid in members if mid in self.layer_order), default=len(self.layer_order) - 1)
        new_ids: list[str] = []
        for member_id in members:
            clone_id = self._unique_id(member_id)
            clone = deepcopy(self.get(member_id))
            clone.label = f"{clone.label} copy"
            clone.link_group = new_group
            self.elements[clone_id] = clone
            new_ids.append(clone_id)
            if member_id == element_id:
                selected_clone = clone_id
        for offset, clone_id in enumerate(new_ids, 1):
            self.layer_order.insert(insert_after + offset, clone_id)
        return selected_clone or new_ids[0]

    def clear_all_groups(self) -> None:
        for state in self.elements.values():
            state.link_group = "None"

    def clear_group(self, group_name: str) -> None:
        if group_name == "None":
            return
        for state in self.elements.values():
            if state.link_group == group_name:
                state.link_group = "None"
