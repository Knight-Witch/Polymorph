# Polymorph Pre-Flight Log

Historical entries through dev.23 are preserved verbatim in [`HISTORY/PROJECT_LOGS/PRE_FLIGHT_THROUGH_DEV23.md`](HISTORY/PROJECT_LOGS/PRE_FLIGHT_THROUGH_DEV23.md). dev.24-dev.27 technical/visual history remains available in Git history; root tracking is intentionally rolling/compact.

## PFC-2026-09-15-064 — Elder Futhark transmutation Motion Lab candidate

- PASS static: rewritten standalone Motion Lab source parses/compiles without syntax errors.
- PASS architecture: changes remain isolated from production `PolymorphWindow`, conversion, framing, updater and encoder behavior; runtime remains dev.27.
- PASS source design: real Elder Futhark glyph content is wired through Noto Sans Runic for the standalone build rather than fake rune-like marks.
- PASS source design: outer CW/inner CCW rune rings, six designated outer glyphs, three clipped partial rune bands, stationary glimmer rune ring and three independently cycling large rune spheres are implemented.
- PASS source design: clockwise triangle family, twin CCW hexagons, grouped structural flicker and a four-stage outside-in cascade are implemented.
- PASS source design: six radial comet tracers perform synchronized outer↔center travel with bright heads, gradient tails and explicit no-go clipping under foreground rune structures.
- PASS source design: glow renderer uses a narrow bright core plus multiple wide low-alpha passes instead of the previous short three-pass glow.
- PASS source design: dual opposite-direction outer progress arcs drive completion; 100% initiates pulse/flash, inner fade and emblem materialization.
- PASS emblem: bundled `kw_emblem.svg` is derived from Amanda's supplied SVG with path-coordinate simplification only; raster comparison was visually equivalent at review scale and path direction is not used by the reveal.
- PASS source design: controls now name the exact motion family they change, removing the ambiguous original Rune/Counter mapping.
- PENDING: dedicated Windows Motion Lab source smoke, PyInstaller build, packaged smoke and portable artifact upload for this candidate.
- No production conversion, geometry semantics, adaptive, updater, subprocess, app-window, installer, runtime-version or release behavior changed.

## PFC-2026-09-14-063 — Motion Lab FULL PASS

- PASS static: standalone Motion Lab source parses/compiles without syntax errors.
- PASS architecture: Motion Lab is isolated from production `PolymorphWindow`, conversion, framing, updater and encoder code; runtime version remains dev.27.
- PASS: loader exposes four compositions, 0–100% progress, auto-loop, independent motion/glow controls and runtime SVG emblem loading.
- PASS: preview surfaces cover black, current blue-black, procedural texture, busy contrast and arbitrary custom images.
- PASS: primary-action prototype uses an oversized arcane mechanism clipped by the visual button, plus hover wake, text tracer, click burst and expanded clipping-debug view.
- PASS: SVG direction risk is contained; canonical SVG is rendered normally and no CSS-style `stroke-dasharray` dependency exists for the basic emblem layer.
- PASS: Motion Lab Build run #1 / run ID `34931411518` completed successfully on implementation commit `0341ea270fb88495cde7f102e155e8ddd44680cc`.
- PASS: Windows source offscreen smoke, PyInstaller portable build, packaged Windows offscreen launch smoke, and artifact upload.
- Artifact `Polymorph-motion-lab`, artifact ID `10381886805`, size 50,767,525 bytes, digest `sha256:b96ff563b952c411614417df483c1996de51d128895b39692f9bf933c12583b6`.
- No production conversion, geometry semantics, adaptive, updater, subprocess, app-window, installer, runtime-version, or release behavior changed.
