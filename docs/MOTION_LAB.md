# Polymorph Motion Lab

Standalone PySide6 design sandbox for Polymorph's deferred loading/working animation and animated primary action.

This remains isolated from the production Polymorph window and does not touch conversion, framing, updater, queue, or encoder behavior.

## Current review baseline

`B — Dense Runes` remains the visual baseline, but v4 turns the loader into a live element editor so Amanda can tune the composition directly instead of iterating geometry by guesswork.

The existing v3 wins are preserved: real Elder Futhark through bundled Noto Sans Runic; fixed opaque partial-rune windows; six large white replacement runes in the outer rune ring; red geometry / gold normal runes / white large runes; opaque large-rune circles; opaque inner annulus; and long comet tracer tails.

The triangle and the three large rune circles are static by default in v4.

## Element editor

Choose an element from the dropdown. Controls are enabled only when they apply to that element.

Available per-element controls:

- `Expand / contract span`: changes the radius/circumference/orbit spread without changing glyph or stroke size.
- `Element scale`: changes glyph size, circle size, or stroke/tracer thickness without changing the element's overall span.
- `Base rotation`: sets the manual starting/orientation angle independently of animation.
- `Colour`: Qt colour picker for that element.
- `Link group`: elements assigned to one link group receive shared span, scale, base-rotation, brightness, and glow-spread edits when those controls are applicable to both elements.
- `Element brightness`: per-element intensity multiplier.
- `Element glow spread`: per-element glow falloff multiplier.
- `Rotation direction / speed`: signed slider; center is static, left is counter-clockwise, right is clockwise, magnitude controls speed.
- `Static`: disables rotational animation while preserving the stored motion speed for later re-enable.
- `Include in pulse array`: adds the element to the global outside-to-inside timed pulse order using current element radius/spread.
- `Rune transition speed`: rune-bearing elements can cycle Elder Futhark; zero means glyph identity stays fixed.

Controls that are not meaningful for the selected element are disabled. Tracers, for example, do not expose spin or pulse-array controls.

## Global pulse controls

- Pulse speed.
- Pulse trail / hold length.
- Pulse dark-end length.

Master brightness, master glow spread, progress, tracer travel speed, study variant, background switching, emblem override, and the separate Polymorph-button preview remain available.

## Export

`Export motion spec…` writes a UTF-8 JSON file containing:

- every element's span, scale, base rotation, color, brightness, glow spread, spin direction/speed, static state, pulse membership, rune transition speed, and link group;
- global pulse timing;
- selected study variant;
- master brightness / master glow spread;
- tracer travel speed.

That JSON is the exact implementation handoff for the selected loader setup.

## Acceptance boundary

This lab is exploratory visual tooling. None of its motion is part of the shipping Polymorph UI until Amanda explicitly approves a treatment and it is deliberately integrated behind a separate human visual gate.
