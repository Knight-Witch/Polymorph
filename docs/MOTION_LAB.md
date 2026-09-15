# Polymorph Motion Lab

Standalone PySide6 design sandbox for Polymorph's deferred loading/working animation and animated primary action.

This remains isolated from the production Polymorph window and does not touch conversion, framing, updater, queue, or encoder behavior.

## Current review baseline

`B — Dense Runes` is the current visual baseline after Amanda's v2 review.

The loader uses real Elder Futhark through bundled Noto Sans Runic. The active geometry order is:

1. two white outer progress rings;
2. one clockwise gold outer rune ring with six larger white designated runes replacing six small-rune slots;
3. a red third ring;
4. two red counter-clockwise six-point polygons;
5. a red fourth ring tangent to the polygon flats;
6. three fixed opaque partial-rune windows ending at the fourth ring, with complete Elder Futhark circles rotating behind the windows;
7. one red clockwise triangle with the same circumradius as the polygons;
8. three opaque large-rune spheres anchored to triangle-edge midpoints, carrying independently cycling white Elder Futhark glyphs;
9. one stationary/glimmering gold rune ring intersecting the inner third of the large rune spheres;
10. an inner opaque annulus bounded by red fifth/seventh rings, containing the smallest counter-clockwise gold rune ring;
11. six red comet tracers that alone pass through the innermost open center and converge at the epicenter.

All ordinary rune glyphs are warmer yellow-orange gold. Large runes are white. All geometry is red except the two outer progress rings, which are white.

The tracer tails are approximately three times the v2 length. Partial frames and large rune spheres are opaque foreground masks, so underlying geometry/tracers do not bleed through them.

## Motion families

- Outer rune ring: clockwise.
- Innermost rune ring: counter-clockwise.
- Partial-window rune content: counter-clockwise; window frames stay fixed.
- Triangle + rune spheres: clockwise.
- Twin hexagons: counter-clockwise.
- Middle rune ring: stationary; glyphs asynchronously glimmer/change.
- Large rune spheres: independently cycle glyphs.
- Structural rings: outside-in cascade/flicker.
- Six radial tracers: outer ↔ epicenter, rotating with the hexagon family.
- At 100%: progress rings pulse, inner ritual fades, a radial flash fires, and the Knight Witch emblem materializes.

## Study variants

- `A — Transmutation`: balanced treatment.
- `B — Dense Runes`: current review baseline, with denser ring/window glyph spacing.
- `C — Tracer Ritual`: emphasizes tracer motion.
- `D — Fractal Echo`: experimental nested red polygon echoes.

## Acceptance boundary

This lab is exploratory visual tooling. None of its motion is part of the shipping Polymorph UI until Amanda explicitly approves a treatment and it is deliberately integrated behind a separate human visual gate.
