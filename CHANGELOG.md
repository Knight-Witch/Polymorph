# Changelog

Historical entries through dev.23 are preserved verbatim in [`HISTORY/PROJECT_LOGS/CHANGELOG_THROUGH_DEV23.md`](HISTORY/PROJECT_LOGS/CHANGELOG_THROUGH_DEV23.md). dev.24-dev.27 investigation/build history remains available in Git history; root tracking is intentionally rolling/compact.

## POLY-2026-09-15-066 — Motion Lab v5 scene-builder candidate

### Summary

- Promoted the standalone Motion Lab from fixed per-element tuning to a persistent scene-builder workflow while keeping production Polymorph dev.27 untouched.
- Added backward-compatible preset loading for v4 `polymorph-motion-spec` JSON plus v5 multi-study workspace export/load and in-memory progress checkpoints.
- Added numeric spinboxes/precision arrows and checkpoint reset controls to editable fields; wheel events no longer change sliders/spinboxes/combos while scrolling the control panel.
- Raised all exposed motion-speed ceilings to 2000% without altering saved/current values.
- Standardized every rune family on asynchronous deterministic rune transitions with Fade/Snap, timing randomization, bright/dark holds, dim/max brightness and dim/bright colors.
- Added zero-transition rune glimmer modes: radial, twinkle and whole-ring pulse, with mode-specific timing/fade/balance/direction controls.
- Added configurable background sparkle particles with spread/fade/density/speed/brightness and three cycling colors.
- Geometry pulse membership is now limited to linework/geometry; rune elements use their dedicated transition/glimmer system.
- Added drag/drop bottom→top layer order. Six large outer runes are the default frontmost loader layer, above both progress rings.
- Added element remove, plain duplicate, duplicate-with-linked-group, clear-selected-group and clear-all-groups workflows.
- Added `+ New Study` copy/rename workflow so multiple loader variants can be edited in one workspace.
- Accepted v4 opaque partial-window behavior and outer large-rune placement remain preserved.
- Candidate requires dedicated Windows Motion Lab CI and human visual/editor review before any production integration.

## POLY-2026-09-15-065 — Motion Lab v3 geometry/masking correction FULL PASS

- v3 implementation commit `5b265c7bd1e21f58753f5cfd13d7a0cf19f3bc30`.
- Dedicated Motion Lab run #4 / `34964398114`: FULL PASS.
- Artifact `10394437743`, digest `sha256:ee9528c126987c26744032d0c144c32ebba0274002aae1c263c577598a2cc4c1`.
- Normal Windows Dev Build run #104 / `34964398145`: FULL PASS.
