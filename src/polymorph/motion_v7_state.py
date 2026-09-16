from __future__ import annotations

from copy import deepcopy
from typing import Any

from .motion_editor import MotionEditorState
from .motion_effects import clamp, smoothstep

EXTRA_FIELDS: dict[str, Any] = {
    "enabled": True,
    "opaque_fill_alpha": 1.0,
    "loader_ring_type": "Progress Arc",
    "loader_tail_length": 0.28,
    "loader_tail_fade_span": 0.60,
    "loader_tail_balance": 0.0,
    "tracer_length": 0.60,
    "tracer_fade_span": 0.60,
    "tracer_balance": 0.0,
    "rune_render_mode": "Outline",
    "rune_weight": "Regular",
    "rune_transition_enabled": True,
    "rune_glimmer_enabled": True,
}

RUNE_KINDS = {"rune_ring", "designated_outer_runes", "partial_runes", "large_rune_glyphs"}
OPAQUE_KINDS = {"partial_frames", "partial_runes", "large_rune_circles"}


class ExtendedEditorState(MotionEditorState):
    """Backward-compatible v7 editor state layered on top of the validated v5 scene model."""

    def __init__(self) -> None:
        super().__init__()
        self.geometry_pulse_enabled = True
        self.pulse_order = self._default_pulse_order()
        self._ensure_extras()

    def _ensure_extras(self) -> None:
        for state in self.elements.values():
            for field, default in EXTRA_FIELDS.items():
                if not hasattr(state, field):
                    setattr(state, field, deepcopy(default))
        inner = self.elements.get("inner_runes")
        if inner is not None and bool(inner.meta.get("opaque_annulus", False)):
            setattr(inner, "opaque_fill_alpha", getattr(inner, "opaque_fill_alpha", 1.0))

    def _default_pulse_order(self) -> list[str]:
        ordered: list[str] = []
        for element_id in self.layer_order:
            state = self.elements.get(element_id)
            if state is not None and "pulse" in state.capabilities:
                ordered.append(element_id)
        for element_id, state in self.elements.items():
            if "pulse" in state.capabilities and element_id not in ordered:
                ordered.append(element_id)
        return ordered

    def supports(self, element_id: str, capability: str) -> bool:
        if element_id not in self.elements:
            return False
        if capability == "enabled":
            return True
        state = self.elements[element_id]
        if capability == "opaque":
            return state.kind in OPAQUE_KINDS or bool(state.meta.get("opaque_annulus", False))
        if capability == "loader_effect":
            return state.kind == "progress_ring"
        if capability == "tracer_effect":
            return state.kind == "tracers"
        if capability == "rune_style":
            return state.kind in RUNE_KINDS
        return super().supports(element_id, capability)

    def _field_supported(self, element_id: str, field: str) -> bool:
        if field == "enabled":
            return self.supports(element_id, "enabled")
        if field == "opaque_fill_alpha":
            return self.supports(element_id, "opaque")
        if field in {"loader_ring_type", "loader_tail_length", "loader_tail_fade_span", "loader_tail_balance"}:
            return self.supports(element_id, "loader_effect")
        if field in {"tracer_length", "tracer_fade_span", "tracer_balance"}:
            return self.supports(element_id, "tracer_effect")
        if field in {"rune_render_mode", "rune_weight"}:
            return self.supports(element_id, "rune_style")
        if field in {"rune_transition_enabled", "rune_glimmer_enabled"}:
            return self.supports(element_id, "rune_transition")
        return super()._field_supported(element_id, field)

    def pulse_multiplier(self, element_id: str, t: float) -> float:
        state = self.get(element_id)
        if not self.geometry_pulse_enabled or not state.pulse or not self.supports(element_id, "pulse"):
            return 1.0
        ids = [
            candidate_id
            for candidate_id in self.pulse_order
            if candidate_id in self.elements
            and self.elements[candidate_id].pulse
            and "pulse" in self.elements[candidate_id].capabilities
        ]
        for candidate_id, candidate in self.elements.items():
            if candidate.pulse and "pulse" in candidate.capabilities and candidate_id not in ids:
                ids.append(candidate_id)
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

    def export(self) -> dict[str, Any]:
        payload = super().export()
        payload["version"] = 3
        pulse = payload.setdefault("pulse", {})
        pulse["enabled"] = self.geometry_pulse_enabled
        pulse["order"] = list(self.pulse_order)
        for element_id, state in self.elements.items():
            raw = payload["elements"].setdefault(element_id, {})
            for field, default in EXTRA_FIELDS.items():
                raw[field] = deepcopy(getattr(state, field, default))
        return payload

    def load(self, payload: dict[str, Any]) -> None:
        super().load(payload)
        self._ensure_extras()
        incoming = payload.get("elements", {})
        for element_id, raw in incoming.items():
            state = self.elements.get(element_id)
            if state is None or not isinstance(raw, dict):
                continue
            for field, default in EXTRA_FIELDS.items():
                if field in raw:
                    setattr(state, field, deepcopy(raw[field]))
                elif not hasattr(state, field):
                    setattr(state, field, deepcopy(default))
        pulse = payload.get("pulse", {}) if isinstance(payload.get("pulse", {}), dict) else {}
        self.geometry_pulse_enabled = bool(pulse.get("enabled", True))
        requested = [str(value) for value in pulse.get("order", [])]
        order = [
            element_id for element_id in requested
            if element_id in self.elements and "pulse" in self.elements[element_id].capabilities
        ]
        for element_id in self._default_pulse_order():
            if element_id not in order:
                order.append(element_id)
        self.pulse_order = order

    def remove_element(self, element_id: str) -> None:
        super().remove_element(element_id)
        self.pulse_order = [value for value in self.pulse_order if value != element_id]

    def duplicate_element(self, element_id: str) -> str:
        new_id = super().duplicate_element(element_id)
        state = self.elements[new_id]
        if "pulse" in state.capabilities:
            position = self.pulse_order.index(element_id) + 1 if element_id in self.pulse_order else len(self.pulse_order)
            self.pulse_order.insert(position, new_id)
        return new_id

    def duplicate_element_with_group(self, element_id: str) -> str:
        before = set(self.elements)
        selected = super().duplicate_element_with_group(element_id)
        for new_id in [value for value in self.elements if value not in before]:
            state = self.elements[new_id]
            if "pulse" in state.capabilities and new_id not in self.pulse_order:
                self.pulse_order.append(new_id)
        return selected

    def rename_element(self, element_id: str, new_label: str) -> None:
        if element_id not in self.elements:
            return
        label = str(new_label).strip()
        if label:
            self.elements[element_id].label = label

    def rename_group(self, old_name: str, new_name: str) -> None:
        old_name = str(old_name).strip()
        new_name = str(new_name).strip()
        if not old_name or old_name == "None" or not new_name or old_name == new_name:
            return
        for state in self.elements.values():
            if state.link_group == old_name:
                state.link_group = new_name
