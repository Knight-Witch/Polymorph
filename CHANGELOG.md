# Changelog

Historical entries through dev.23 are preserved verbatim in [`HISTORY/PROJECT_LOGS/CHANGELOG_THROUGH_DEV23.md`](HISTORY/PROJECT_LOGS/CHANGELOG_THROUGH_DEV23.md). dev.24-dev.27 investigation/build history remains available in Git history; root tracking is intentionally rolling/compact.

## POLY-2026-09-16-068 — Motion Lab panel readability pass

### Summary

- Kept the standalone Motion Lab behavior unchanged and adjusted only the scene-builder control-panel styling.
- Section headers are now brighter crimson/red with stronger weight and a thin deep-red divider, making major sections easier to scan while scrolling.
- Removed the grey/unfilled slider-track background; the unused portion of sliders is transparent while the active red fill and existing ivory handle remain visible.
- Change remains isolated to the Motion Lab entrypoint/theme layer; production Polymorph dev.27 conversion/framing/adaptive behavior is untouched.
- Human visual review remains required for appearance acceptance.

## POLY-2026-09-16-067 — Motion Lab v7 scene-builder controls — FULL PASS

### Summary

- Continued the standalone Motion Lab editor without touching production Polymorph dev.27 conversion/framing/adaptive code.
- Added undo/redo with UI controls plus `Ctrl+Z`, `Ctrl+Y`, and `Ctrl+Shift+Z`, including coalescing for continuous slider edits.
- Added a drag/drop geometry-pulse-order editor and persisted explicit pulse order in workspaces/presets.
- Added layer renaming and link-group renaming, plus an expandable drag/drop group-hierarchy editor for moving layers between groups or ungrouping them.
- Added per-layer enabled/visible state and a geometry-pulse master enable.
- Added opacity control for opaque mask-capable elements.
- Added explicit clear-to-transparent behavior for element, rune and sparkle colors.
- Removed the periodic center completion flash and changed automatic preview looping so it does not enter the completion reveal/flash path.
- Added loading-ring types `Static Ring`, `Progress Arc`, and `Gradient Tail`, with tail length/fade/balance controls.
- Added tracer length, fade/softness and front/back gradient-balance controls.
- Added rune `Outline` / `Solid` render styles and `Thin` / `Regular` / `Bold` weight controls.
- Added rune transition/glimmer enable controls and context-aware visibility/enablement for incompatible mode-specific controls.
- Made layer selection the primary editor-selection workflow; retained the internal combo only for compatibility/synchronization.
- Strengthened panel section separation and added hover help for non-obvious controls.
- Preserved v4/v5 workspace compatibility; existing values are retained and new fields receive defaults.
- Implementation commit `06750079ee2dfa837a56600011367f16cb87646b`.
- Dedicated `Polymorph Motion Lab Build` run #9 / run ID `35060729400`: **FULL PASS**.
- Portable artifact `Polymorph-motion-lab`, artifact ID `10431614039`, size 50,932,008 bytes, digest `sha256:41aed1fcdb226f028c76d962e97f5d36b7beaf9f8d2ad698a81e7cbf19b207f9`.
- Normal Windows Dev Build run #109 / run ID `35060729361`: **FULL PASS** across unit/toolchain/adaptive/GIF-reference/frozen-app/installer/checksum/artifact gates.
- Production Polymorph remains dev.27 unchanged; v7 remains standalone exploratory tooling pending human visual approval.

## POLY-2026-09-15-066 — Motion Lab v5 scene builder FULL PASS

- Implementation commit `d6d694e59358e9507bba540d43c44fb1fe32abc2`.
- Dedicated Motion Lab run #8 / `35056008606`: FULL PASS.
- Artifact `10430402445`, digest `sha256:4ae317285edc9a7fc821ea0374f2eb8ef1aacb4094e5e7a1abee9c2c08482ee4`.
- Normal Windows Dev Build run #108 / `35056008609`: FULL PASS.
- Production Polymorph remains dev.27 unchanged.
