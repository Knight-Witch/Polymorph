# Polymorph Motion Lab

Standalone PySide6 design sandbox for Polymorph's deferred loading/working animation and animated primary action. It remains isolated from the production Polymorph window and does not touch conversion, framing, updater, queue, or encoder behavior.

## Current review baseline

`B — Dense Runes` remains the visual baseline for the existing scene builder, while the lab now functions as a reusable scene builder rather than a fixed one-off editor.

The six large outer runes remain the default frontmost loader layer, above both white loading rings. Accepted partial-rune-window behavior and the opaque large-rune-circle treatment remain preserved.

## Polymorph loader preview

Motion Lab now has a separate `Polymorph Loader Preview` tab for the newer working/loading concept. It is intentionally isolated from the scene-builder workspace and from production Polymorph.

The preview is a purpose-built animation rather than an AI frame sequence. It uses the bundled canonical Knight Witch SVG renderer at runtime and layers deterministic Qt drawing around it:

- the exact user-supplied `KW_EMBLEM_PATH.svg` asset, preserved as path geometry and tinted white at render time;
- one continuous outer progress ring that fills from 0–100% and becomes a complete solid ring at completion;
- a slowly rotating Elder Futhark rune band contained between two luminous rings;
- a brighter cyan/blue-to-violet/magenta ornate angular tech frame modeled more closely on the approved still mockup;
- four larger true-diamond cardinal nodes, horizontal tech stubs, paired side diamonds and cascading top/bottom dot trails;
- progress-driven emblem materialization from top to bottom;
- a denser sparkle/data-light front below the reveal edge so the emblem visibly forms out of light rather than simply appearing.

The review page exposes auto-loop progress, manual progress scrubbing, motion speed, motion freeze, and replay. Those controls affect only this preview tab and do not mutate Motion Lab scene-builder studies, presets, layers, groups, or production application state.

## Scene builder

The layer list is the primary element selector and is ordered bottom -> top. Click a layer to edit it, drag it to change z-order, and double-click it to rename it. Link groups can also be renamed, cleared individually, or cleared globally. `Group hierarchy…` opens an expandable drag/drop group view so layers can be moved between groups or into `Ungrouped` without using the flat group dropdown.

Every element persists editable span, element scale, base rotation, color, brightness, glow spread, rotation speed/static state, link group and layer visibility. Opaque-mask layers additionally expose mask opacity. Existing v4/v5 workspace values remain loadable; fields introduced later receive defaults rather than rewriting saved values.

Undo/redo is workspace-aware and available from buttons plus standard hotkeys: `Ctrl+Z` for Undo, and `Ctrl+Y` or `Ctrl+Shift+Z` for Redo. Continuous slider edits are coalesced so a drag behaves like one editing action rather than dozens of tiny history steps.

## Geometry pulse

Geometry pulse is restricted to linework/geometry. A global enable toggle can suspend the pulse without deleting membership or timing. `Geometry pulse order...` opens a drag/drop list of currently pulse-enabled geometry so the firing sequence can be authored explicitly rather than inferred from radius.

Pulse speed, trail/hold, and dark-end length remain independently adjustable.

## Rune transitions and rendering

Rune families share the deterministic asynchronous transition engine. Relevant controls include transition enable, transition speed, timing randomization, Fade/Snap type, bright/dark holds, dim/max brightness, dim/bright colors, and special glimmer.

When transition behavior permits it, special glimmer supports Radial, Twinkle, Pulse, or None, with only the controls relevant to the selected mode shown. Runes can render as `Outline` or `Solid`, with `Thin`, `Regular`, or `Bold` glyph weight.

Rune colors can be cleared completely; a cleared color is treated as transparent rather than silently replaced.

## Loading rings

Loading-ring layers expose a ring type:

- `Static Ring` — ordinary full circle, independent of progress;
- `Progress Arc` — progress-driven arc;
- `Gradient Tail` — progress-driven traveling head/tail treatment suited to seamless looping.

Gradient tails expose tail length, fade span and head/tail balance. Auto-loop avoids the old completion flash/reveal restart path, and the old center flash has been removed.

## Tracers

Tracer layers expose travel speed plus tracer length, gradient/fade softness, and front/back balance so the head/tail emphasis can be tuned directly.

## Opaque masks and transparency

Partial-window masks, large rune circles, and other mask-capable layers expose opacity from 0% to 100%. Color controls include an explicit clear action; cleared colors are fully transparent.

## Background sparkles

Background sparkle particles remain independently switchable and expose spread, outer fade softness, density, speed, max brightness, and three independently cycling colors. Each color can also be cleared to transparent.

## Editing ergonomics

Numeric fields combine a wheel-safe slider, editable numerical spinbox and precision arrows. Mouse-wheel scrolling no longer changes slider/spinbox/combo values. Fields retain checkpoint reset behavior, and effect-specific controls are shown/hidden according to the selected layer and selected effect type. Section headers use stronger visual separation, and hover tooltips explain the less obvious controls.

## Acceptance boundary

This lab is exploratory visual tooling. None of its motion is part of the shipping Polymorph UI until Amanda explicitly approves a treatment and it is deliberately integrated behind a separate human visual gate.
