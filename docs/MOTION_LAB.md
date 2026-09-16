# Polymorph Motion Lab

Standalone PySide6 design sandbox for Polymorph's deferred loading/working animation and animated primary action. It remains isolated from the production Polymorph window and does not touch conversion, framing, updater, queue, or encoder behavior.

## Current review baseline

`B — Dense Runes` remains the visual baseline, but v5 turns the lab into a reusable scene builder rather than a fixed one-off editor.

The six large outer runes are the default frontmost loader layer, above both white progress rings. The accepted opaque partial-window behavior and opaque large-rune-circle masks are preserved.

## Scene builder

Every visual element has an editable state and a drag/drop layer position. Relevant controls include span, element scale, base rotation, color, brightness, glow spread, signed rotation speed, Static, geometry-pulse membership, and link group. Speed ceilings are 2000% for rotational motion, tracer motion, geometry pulse, rune transition/glimmer motion, and sparkle motion without changing existing saved values.

Elements can be duplicated, removed, or duplicated together with their linked group. Link groups can be cleared individually or globally. Plain duplication intentionally disconnects the new element; `Duplicate + group` clones the full linked family into a new linked group.

Study workspaces can be copied with `+ New Study`, renamed, checkpointed in-memory, exported, and loaded again. v5 reads v4 `polymorph-motion-spec` JSON and preserves the values that existed in the older format. New exports use a workspace format so multiple study variants can travel together.

Each numeric field has a slider plus editable spinbox and precision arrows. Mouse-wheel input is ignored by sliders/spinboxes/combos so the right-side panel scrolls instead of accidentally changing values. Each editable field has a reset control that returns to the last saved checkpoint.

## Rune transitions and glimmer

All rune families now use the same deterministic asynchronous transition engine rather than synchronized whole-ring alphabet snaps.

- Transition speed controls fade-out/fade-in duration; 0 disables glyph changes.
- Transition timing randomizer ranges from synchronized timing to independent per-rune timing.
- Transition type can be `Fade` or `Snap`.
- Bright-hold and dark-hold durations are independently editable.
- Dim/max brightness and dim/bright colors define the rune's visual range.
- When transition speed is 0, glyphs stay fixed and can use `Radial`, `Twinkle`, `Pulse`, or no special glimmer.
- Radial glimmer exposes speed, length, fade span, head/tail balance, and direction.
- Twinkle exposes speed and neighbor/random independence.
- Rune pulse exposes speed, fade span, and balance.

Rune rings are not members of the geometry pulse array; geometry pulse remains limited to linework/geometry.

## Sparkle particles

A deterministic background sparkle field can be enabled independently of loader geometry. Controls cover spread, outer fade softness, density, speed, max brightness, and three independently cycling particle colors.

## Layering

The layer list is ordered bottom → top and supports drag/drop. Because large outer runes are last in the default order, they render in front of both progress rings. Duplicated elements participate in the same renderer and can be reordered like built-in elements.

## Acceptance boundary

This lab is exploratory visual tooling. None of its motion is part of the shipping Polymorph UI until Amanda explicitly approves a treatment and it is deliberately integrated behind a separate human visual gate.
