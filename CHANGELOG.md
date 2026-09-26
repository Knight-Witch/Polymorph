# Changelog

## POLY-2026-09-25-070 — Polymorph loader visual-fidelity second pass — FULL PASS / human visual gate

### Summary

- Reworked the standalone loader preview after the first packaged visual review.
- Added Amanda's newly supplied exact `KW_EMBLEM_PATH.svg` as a packaged Motion Lab asset; the renderer uses that SVG directly and tints it white rather than approximating the mark.
- Replaced the broken/segmented progress treatment with one continuous outer progress ring that becomes a complete ring at 100%.
- Moved the runes into a dedicated band bounded by two luminous rings.
- Increased cyan/blue/violet/magenta saturation and glow strength.
- Rebuilt the center framing as a more ornate angular cyber-arcane structure closer to the approved still mockup, including larger true-diamond cardinal nodes, side tech stubs, paired mini-diamonds and cascading top/bottom dot trails.
- Strengthened the top-to-bottom emblem reveal with denser sparkles plus restrained vertical data-light streaks at the materialization front.
- Existing Motion Lab scene-builder studies and production Polymorph remain isolated and untouched.
- Fixed the second-pass source assembly typo found by Motion Lab run #12 source smoke before packaging; no visual design intent changed.
- Dedicated `Polymorph Motion Lab Build` run #13 / run ID `36220819410`: **FULL PASS** across source smoke, PyInstaller portable build, packaged Windows smoke and artifact upload.
- Portable artifact `Polymorph-motion-lab`, artifact ID `10898992118`, size 50,936,267 bytes, digest `sha256:5b42ade50295d5d4e6586bb5e57143e2645b9b13374ee8ca1a3cc3cabf6b1c8a`.
- Normal Windows Dev Build run #112 again passed all 56 unit tests and then stopped at the already-known upstream FFmpeg 9.0.1 404; no production package stage ran and no loader-preview regression is indicated.
- Human visual review of the packaged second-pass loader is now the active gate.

## POLY-2026-09-24-069 — Standalone Polymorph loader preview tab — FULL PASS / human visual gate

### Summary

- Added a separate `Polymorph Loader Preview` tab to the standalone Motion Lab so the newer loading/working concept can be reviewed without integrating it into production Polymorph.
- Added a purpose-built Qt animation using the bundled canonical emblem renderer rather than generated animation frames.
- Preview concept includes an outer progress ring, rotating Elder Futhark rune ring, counter-rotating segmented ring, restrained angular cyber-arcane geometry, and progress-driven emblem materialization with a sparkle/pixel reveal front.
- Added review-only controls for auto-loop progress, manual progress scrubbing, animation speed, motion freeze and replay.
- Existing Motion Lab scene-builder studies, presets, layers, groups and values remain separate and untouched by the new preview page.
- Production Polymorph dev.27 conversion/framing/adaptive/updater/encoder behavior remains untouched.
- Dedicated `Polymorph Motion Lab Build` run #11 / run ID `36098491868`: **FULL PASS** across source smoke, PyInstaller portable build, packaged Windows smoke and artifact upload.
- Portable artifact `Polymorph-motion-lab`, artifact ID `10848177893`, size 50,903,007 bytes, digest `sha256:df052b79f4dfa6fb3c5a586455bf0a0bfa2ea0de9def00291621cac1b975b2d1`.
- Normal Windows Dev Build run #110 / run ID `36098491841` also triggered because the new module lives under `src/**`; its 56 unit tests passed, then the run stopped at the pinned FFmpeg download because the upstream `gyan.dev` URL returned 404. No production package stage ran, so this is recorded as unrelated external build-infrastructure evidence rather than a loader-preview regression.
- Human visual review of the packaged loader preview is now the active gate.

Historical entries through dev.23 are preserved verbatim in [`HISTORY/PROJECT_LOGS/CHANGELOG_THROUGH_DEV23.md`](HISTORY/PROJECT_LOGS/CHANGELOG_THROUGH_DEV23.md). dev.24-dev.27 investigation/build history remains available in Git history; root tracking is intentionally rolling/compact.

## POLY-2026-09-16-068 — Motion Lab panel readability pass — FULL PASS

### Summary

- Kept the standalone Motion Lab behavior unchanged and adjusted only the scene-builder control-panel styling.
- Section headers are now brighter crimson/red with stronger weight and a thin deep-red divider, making major sections easier to scan while scrolling.
- Removed the grey/unfilled slider-track background; the unused portion of sliders is transparent while the active red fill and existing ivory handle remain visible.
- Readability implementation commit `845b029df1027bf6f4fac2a3a346c5d04d32d134`.
- Dedicated `Polymorph Motion Lab Build` run #10 / run ID `35064912753`: **FULL PASS**.
- PASS: source smoke, PyInstaller portable build, packaged Windows smoke and portable artifact upload.
- Portable artifact `Polymorph-motion-lab`, artifact ID `10433348032`, size 50,890,729 bytes, digest `sha256:59d479d9cba0a2bd1b830093c566b0dfa97d19d62a9aae7220a28c898c922af5`.
- The normal Windows Dev Build did not trigger because this styling pass changed only `run_motion_lab.py` plus tracking docs, which are outside that workflow's production path filters; protected production run #109 remains FULL PASS and no production source changed.
- Production Polymorph remains dev.27 unchanged; human visual review is still required for appearance acceptance.

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
