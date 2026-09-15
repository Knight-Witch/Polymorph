# Changelog

Historical entries through dev.23 are preserved verbatim in [`HISTORY/PROJECT_LOGS/CHANGELOG_THROUGH_DEV23.md`](HISTORY/PROJECT_LOGS/CHANGELOG_THROUGH_DEV23.md). dev.24-dev.27 investigation/build history remains available in Git history; root tracking is intentionally rolling/compact.

## POLY-2026-09-15-066 — Motion Lab v4 element editor FULL PASS

### Summary

- Converted the standalone Motion Lab from fixed tuning sliders into a per-element editor so Amanda can directly establish the exact loader composition instead of iterating layout by guesswork.
- Triangle and the three large rune circles are static by default. Their motion can be explicitly re-enabled from the signed rotation-speed control.
- Added per-element span/radius control independent of element/glyph/stroke scale.
- Added per-element scale, manual base rotation, color picker, brightness, glow spread, signed CW/CCW rotation speed, Static toggle, pulse-array toggle, rune-transition speed, and editable link groups.
- Irrelevant controls are disabled for the selected element; tracers do not expose spin/pulse/rune-transition controls, for example.
- Linked elements can share span, scale, base-rotation, brightness and glow edits; defaults include outer-ring, outer-rune, hexagon, triangle, partial-window and inner-ring families plus custom groups.
- Added global pulse speed, pulse trail/hold and pulse dark-end controls. Pulse ordering derives from current outside-to-inside element position.
- Rune-bearing elements can cycle Elder Futhark at user-selected rates; transition speed zero preserves glyph identity.
- Added `Export motion spec…`, writing UTF-8 JSON with every element setting plus pulse timing, active study, master brightness/glow and tracer travel speed for direct implementation handoff.
- Preserved v3 accepted behavior: fixed opaque partial-rune windows, outer designated-rune placement/size, foreground masking, palette defaults and long comet trails.
- Dedicated `Polymorph Motion Lab Build` run #7 / run ID `34972811122` is FULL PASS on implementation head `8f68d4003be672de93cb5ae576abb1c8fb642a39`.
- PASS: Windows source offscreen smoke, PyInstaller portable build, packaged Windows launch smoke and artifact upload.
- Portable artifact `Polymorph-motion-lab`, artifact ID `10398081397`, size 50,856,993 bytes, digest `sha256:4f49ffffcfbcf8b96d8a3ef418fb72e67e51641237f08203bb6b0d87b60651a0`.
- Normal Windows Dev Build run #107 / run ID `34972810969` was triggered by the same implementation head and remained in progress when this log entry was recorded; production runtime code was not modified by the Motion Lab editor work.

## POLY-2026-09-15-065 — Motion Lab v3 geometry/masking correction FULL PASS

- v3 implementation commit `5b265c7bd1e21f58753f5cfd13d7a0cf19f3bc30`.
- Dedicated Motion Lab run #4 / `34964398114`: FULL PASS.
- Portable artifact `10394437743`, digest `sha256:ee9528c126987c26744032d0c144c32ebba0274002aae1c263c577598a2cc4c1`.
- Normal Windows Dev Build run #104 / `34964398145` passed all protected production gates.

## POLY-2026-09-15-064 — Motion Lab Elder Futhark transmutation rebuild FULL PASS

- v2 implementation commit `be7939fabedc6c719b5500dd7578ab4b2d8534fd`.
- Dedicated Motion Lab run #3 / `34944466899`: FULL PASS.
- Portable artifact `10386399042`, digest `sha256:ca12e0e0bcf2f239c8e2acd75046443e4016bdefb7df11bb040625390bc6b767`.
