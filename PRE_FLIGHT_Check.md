# Polymorph Pre-Flight Log

Historical entries through dev.23 are preserved verbatim in [`HISTORY/PROJECT_LOGS/PRE_FLIGHT_THROUGH_DEV23.md`](HISTORY/PROJECT_LOGS/PRE_FLIGHT_THROUGH_DEV23.md). dev.24-dev.27 technical/visual history remains available in Git history; root tracking is intentionally rolling/compact.

## PFC-2026-09-15-064 — Elder Futhark transmutation Motion Lab FULL PASS

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
- PASS CI: dedicated `Polymorph Motion Lab Build` run #3 / run ID `34944466899` completed successfully on implementation commit `be7939fabedc6c719b5500dd7578ab4b2d8534fd`.
- PASS CI: Windows source offscreen smoke, PyInstaller portable build, packaged Windows offscreen launch smoke and portable artifact upload.
- Artifact `Polymorph-motion-lab`, artifact ID `10386399042`, size 50,819,549 bytes, digest `sha256:ca12e0e0bcf2f239c8e2acd75046443e4016bdefb7df11bb040625390bc6b767`.
- PASS isolation check: normal Windows Dev Build run #103 / run ID `34944466940` also completed successfully on the same implementation commit, including unit tests, pinned toolchain verification, adaptive integration, GIF reference comparison, production PyInstaller build, packaged production smoke, installer compilation and artifact upload.
- No production conversion, geometry semantics, adaptive, updater, subprocess, app-window, installer, runtime-version or release behavior changed.
- Next gate: Amanda's human visual review of the v2 portable Motion Lab, especially rune readability, glow spread/core, tracer tails/occlusion, partial-rune clipping, cascade timing, dual progress behavior and completion/emblem reveal.

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

## Documentation note

- This follow-up records completed CI/artifact identities only. It changes no runtime, package, production UI, conversion, installer, or public-release behavior.
