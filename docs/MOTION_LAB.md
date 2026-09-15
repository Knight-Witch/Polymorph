# Polymorph Motion Lab

Standalone PySide6 design sandbox for Polymorph's deferred loading/working animation and animated primary action.

This is intentionally isolated from the production Polymorph window. It does not touch conversion, framing, updater, queue, or encoder behavior.

## Run from source

```powershell
python run_motion_lab.py
```

or, with the package installed/editable:

```powershell
python -m polymorph.motion_lab
```

## Current transmutation study

The current loader direction is based on Amanda's annotated transmutation-circle study and uses real Elder Futhark glyphs through bundled Noto Sans Runic in the standalone Windows build.

- Two outer progress rings travel in opposite directions and are the actual 0-100% loading indicators.
- The outer Elder Futhark ring rotates clockwise and carries six larger designated Elder Futhark glyphs with it.
- The inner Elder Futhark ring rotates counter-clockwise.
- Three partial Elder Futhark rings rotate counter-clockwise behind fixed visibility windows, so glyphs disappear outside each exposed arc.
- A stationary middle rune band glimmers: individual glyphs fade in/out and change only while dim, avoiding hard random pops.
- Three large rune spheres rotate with the crimson triangle and independently cycle Elder Futhark glyphs without matching each other on the same frame.
- The crimson triangle rotates clockwise while two offset hexagonal structures rotate counter-clockwise.
- Four structural circles perform a timed outside-in cascade pulse; other structural groups flicker asynchronously rather than in lockstep.
- Six radial comet tracers move from the outer points to the center and back, rotating with the hexagon system. The tracers are clipped behind the marked rune spheres, central circle, and partial-ring no-go zones.
- Glow rendering uses a tight bright core plus multiple wider low-opacity passes for a softer falloff. Tracers use a bright head and fading comet tail.
- At 100%, the progress rings pulse, the inner ritual fades, a brief radial flash fires, and the Knight Witch emblem materializes with a radial reveal.

## Study variants

The same transmutation architecture can be compared with four emphasis treatments:

- `A — Transmutation`: balanced reference treatment.
- `B — Dense Runes`: increases outer/inner rune density.
- `C — Tracer Ritual`: strengthens radial tracers and adds opposed circular tracer accents.
- `D — Fractal Echo`: layers low-intensity nested polygon echoes behind the main geometry as an experimental trippy direction.

## Controls

The ambiguous prototype controls were replaced with explicit motion-family controls:

- Master glow and glow spread.
- Outer rune ring clockwise speed.
- Inner rune ring counter-clockwise speed.
- Partial rune-arc counter-clockwise speed.
- Triangle + rune-sphere clockwise speed.
- Twin-hexagon counter-clockwise speed.
- Comet tracer speed.
- Cascade/flicker pace.
- Button glow and button rune-ring speed.

Preview backgrounds remain switchable between black, Polymorph blue-black, procedural dark textures, a deliberately busy stress-test surface, or a custom image.

## Emblem handling

`src/polymorph/assets/kw_emblem.svg` is the bundled center asset for this study, derived from Amanda's supplied SVG with path-coordinate simplification only; raster comparison was visually equivalent at review scale.

The emblem is rendered as normal SVG artwork rather than relying on CSS `stroke-dasharray` traversal, so source subpath direction is not required for the reveal. `Load alternate emblem SVG…` remains as an optional development override, but the lab no longer depends on that chooser to show the correct Knight Witch mark.

## Acceptance boundary

This lab is exploratory visual tooling. None of its motion is part of the shipping Polymorph UI until Amanda selects/approves a treatment and it is deliberately integrated behind a separate human visual gate.
