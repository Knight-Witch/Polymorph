from __future__ import annotations

import math

from PySide6.QtGui import QColor

from .motion_effects import ELDER_FUTHARK, clamp, smoothstep


def _hash_u32(value: int) -> int:
    value &= 0xFFFFFFFF
    value ^= value >> 16
    value = (value * 0x7FEB352D) & 0xFFFFFFFF
    value ^= value >> 15
    value = (value * 0x846CA68B) & 0xFFFFFFFF
    value ^= value >> 16
    return value & 0xFFFFFFFF


def hash01(*values: int) -> float:
    seed = 0x9E3779B9
    for value in values:
        seed = _hash_u32(seed ^ _hash_u32(value + 0x9E3779B9))
    return seed / 0xFFFFFFFF


def mix_color(a: QColor, b: QColor, amount: float) -> QColor:
    amount = clamp(amount)
    return QColor(
        round(a.red() + (b.red() - a.red()) * amount),
        round(a.green() + (b.green() - a.green()) * amount),
        round(a.blue() + (b.blue() - a.blue()) * amount),
        round(a.alpha() + (b.alpha() - a.alpha()) * amount),
    )


def _rune_index(slot: int, cycle: int, seed: int = 0) -> int:
    # Deterministic random selection keeps previews reproducible while still avoiding
    # synchronized alphabet stepping.
    return int(hash01(slot + seed * 37, cycle * 101 + 17, seed + 911) * len(ELDER_FUTHARK)) % len(ELDER_FUTHARK)


def _transition_sample(state, slot: int, t: float, seed: int) -> tuple[int, float]:
    speed = max(0.001, float(state.rune_speed))
    fade_time = max(0.015, 0.60 / speed)
    bright_hold = max(0.0, float(state.rune_bright_hold))
    dark_hold = max(0.0, float(state.rune_dark_hold))
    randomness = clamp(float(state.rune_timing_randomness))

    if str(state.rune_transition_type).lower() == "snap":
        # Snap has no visible interpolation, but the speed control still controls
        # how quickly the bright/dark handoff can happen.
        snap_gap = max(0.005, fade_time * 0.08)
        total = max(0.02, bright_hold + dark_hold + snap_gap)
        phase_offset = hash01(slot, seed, 37) * total * randomness
        tempo = 1.0 + (hash01(slot, seed, 51) - 0.5) * 0.72 * randomness
        clock = max(0.0, t * tempo + phase_offset)
        cycle = math.floor(clock / total)
        local = clock - cycle * total
        current_index = _rune_index(slot, cycle, seed)
        next_index = _rune_index(slot, cycle + 1, seed)
        if local < bright_hold:
            return current_index, 1.0
        if local < bright_hold + dark_hold:
            return next_index, 0.0
        return next_index, 1.0

    total = max(0.02, bright_hold + fade_time + dark_hold + fade_time)
    phase_offset = hash01(slot, seed, 73) * total * randomness
    tempo = 1.0 + (hash01(slot, seed, 97) - 0.5) * 0.72 * randomness
    clock = max(0.0, t * tempo + phase_offset)
    cycle = math.floor(clock / total)
    local = clock - cycle * total
    current_index = _rune_index(slot, cycle, seed)
    next_index = _rune_index(slot, cycle + 1, seed)

    edge_1 = bright_hold
    edge_2 = edge_1 + fade_time
    edge_3 = edge_2 + dark_hold
    if local < edge_1:
        return current_index, 1.0
    if local < edge_2:
        amount = smoothstep(edge_1, edge_2, local)
        return current_index, 1.0 - amount
    if local < edge_3:
        return next_index, 0.0
    amount = smoothstep(edge_3, total, local)
    return next_index, amount


def _radial_glimmer(state, slot: int, count: int, t: float) -> float:
    speed = max(0.0, float(state.radial_speed))
    if speed <= 0.001:
        return 1.0
    direction = 1.0 if int(state.radial_direction) >= 0 else -1.0
    head = (t * speed * 0.18 * direction) % 1.0
    position = slot / max(1, count)
    signed = ((position - head + 0.5) % 1.0) - 0.5
    if direction < 0:
        signed = -signed
    length = max(0.015, clamp(float(state.radial_length), 0.01, 1.0))
    balance = clamp(float(state.radial_balance), -1.0, 1.0)
    before = length * (0.5 + 0.44 * max(0.0, -balance) + 0.18 * max(0.0, balance))
    after = length * (0.5 + 0.44 * max(0.0, balance) + 0.18 * max(0.0, -balance))
    if signed < 0:
        norm = abs(signed) / max(0.001, before)
    else:
        norm = signed / max(0.001, after)
    if norm >= 1.0:
        return 0.0
    fade = clamp(float(state.radial_fade_span), 0.02, 1.0)
    gamma = 0.45 + (1.0 - fade) * 4.2
    return max(0.0, 1.0 - norm) ** gamma


def _twinkle_glimmer(state, slot: int, count: int, t: float, seed: int) -> float:
    speed = max(0.0, float(state.twinkle_speed))
    if speed <= 0.001:
        return 1.0
    randomness = clamp(float(state.twinkle_randomness))
    related_phase = slot / max(1, count)
    random_phase = hash01(slot, seed, 131)
    phase = related_phase * (1.0 - randomness) + random_phase * randomness
    random_rate = 0.82 + 0.42 * hash01(slot, seed, 149)
    wave = 0.5 + 0.5 * math.sin(math.tau * (t * speed * 0.34 * random_rate + phase))
    # A small second harmonic stops neighboring runes from reading like identical bulbs.
    secondary = 0.5 + 0.5 * math.sin(math.tau * (t * speed * 0.19 + hash01(slot, seed, 163)))
    return clamp(wave * 0.82 + secondary * 0.18)


def _pulse_glimmer(state, t: float) -> float:
    speed = max(0.0, float(state.rune_pulse_speed))
    if speed <= 0.001:
        return 1.0
    phase = (t * speed * 0.24) % 1.0
    balance = clamp(float(state.rune_pulse_balance), -1.0, 1.0)
    center = 0.5 + balance * 0.22
    distance = abs(phase - center) / max(0.001, 0.5 + 0.18 * abs(balance))
    base = clamp(1.0 - distance)
    fade = clamp(float(state.rune_pulse_fade_span), 0.02, 1.0)
    gamma = 0.45 + (1.0 - fade) * 4.0
    return base ** gamma


def rune_sample(state, slot: int, count: int, t: float, *, base_index: int = 0, seed: int = 0) -> tuple[str, float, QColor]:
    if float(state.rune_speed) > 0.001:
        index, light = _transition_sample(state, slot + base_index, t, seed)
    else:
        index = (slot + base_index) % len(ELDER_FUTHARK)
        mode = str(state.glimmer_type).lower()
        if mode == "radial":
            light = _radial_glimmer(state, slot, count, t)
        elif mode == "pulse":
            light = _pulse_glimmer(state, t)
        elif mode == "twinkle":
            light = _twinkle_glimmer(state, slot, count, t, seed)
        else:
            light = 1.0

    min_b = max(0.0, float(state.rune_min_brightness))
    max_b = max(min_b, float(state.rune_max_brightness))
    brightness = min_b + (max_b - min_b) * clamp(light)
    dim = QColor(state.rune_dim_color)
    bright = QColor(state.rune_bright_color)
    color = mix_color(dim, bright, clamp(light))
    return ELDER_FUTHARK[index], brightness, color
