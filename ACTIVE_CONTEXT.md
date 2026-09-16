# Active Context — Polymorph `dev`

**Updated:** 2026-09-16  
**Current task:** Motion Lab scene-builder v7 validation and human tuning. v7 folds the post-v5 tuning requests into the standalone lab: mask opacity, selectable loader-ring behavior, tracer tail controls, transparent colors, rune render styles, context-aware control visibility, layer-first editing, undo/redo, geometry pulse order editing, and layer/group renaming. Production Polymorph remains on dev.27 and its conversion/framing/adaptive behavior remains closed/validated.

## Minimum continuation set

Read only:

1. `PROJECT_CONTRACT.md`
2. this file
3. `docs/MOTION_LAB.md`
4. `src/polymorph/motion_lab.py`
5. `src/polymorph/motion_editor.py`
6. `src/polymorph/motion_runes.py`
7. `src/polymorph/motion_loader.py`
8. `src/polymorph/motion_loader_base.py`
9. `src/polymorph/motion_effects.py`
10. `.github/workflows/motion-lab-build.yml` only when the standalone Windows artifact/build is implicated

Do not preload engine/history files unless the current task actually needs them.

## Production Dev candidate — protected

- Branch: `dev`.
- Runtime version: `0.1.0-dev.27`.
- Production implementation commit: `9b6954f30741437d2aabdf49fa4912d02fad99e6`.
- Motion Lab v5 implementation `d6d694e59358e9507bba540d43c44fb1fe32abc2` previously passed normal Windows Dev Build run #108 / run ID `35056008609`.
- Production app/conversion source remains untouched by the v7 Motion Lab work.
- No public release exists; `main` remains non-experimental.

## Motion Lab v7 candidate — FULL PASS / human visual tuning

- Standalone-only source candidate contains the following additional editor/runtime behavior:
  - undo/redo with standard `Ctrl+Z`, `Ctrl+Y`, and `Ctrl+Shift+Z` shortcuts plus UI buttons;
  - drag/drop geometry pulse-order editor, persisted in presets/workspaces;
  - layer rename, link-group rename, and expandable drag/drop group-hierarchy editing;
  - selected-layer opacity for opaque masks;
  - transparent/cleared colors for element, rune and sparkle colors;
  - loading-ring types `Static Ring`, `Progress Arc`, and `Gradient Tail`, with tail length/fade/balance controls;
  - tracer length/fade/front-back balance controls;
  - center completion flash removed and auto-loop avoids completion reveal/flash;
  - layer selection is the primary element-selection mechanism;
  - stronger section separation and context-aware rune/loader/tracer special-control visibility;
  - rune `Outline` / `Solid` rendering and `Thin` / `Regular` / `Bold` weight controls;
  - geometry-pulse master enable plus explicit editable pulse order;
  - per-layer visibility enable plus rune transition/glimmer toggles;
  - speed ceilings remain 2000% and existing/imported tuning values are not automatically raised.
- Existing v4/v5 preset values remain backward-compatible; newly introduced fields receive defaults.
- Six large outer runes remain frontmost by default.
- Accepted partial-window behavior and large-rune-circle masks remain preserved.
- Implementation commit `06750079ee2dfa837a56600011367f16cb87646b`.
- Dedicated Motion Lab run #9 / run ID `35060729400`: **FULL PASS** (source smoke, PyInstaller build, packaged smoke, artifact upload).
- Artifact `Polymorph-motion-lab`, ID `10431614039`, size 50,932,008 bytes, digest `sha256:41aed1fcdb226f028c76d962e97f5d36b7beaf9f8d2ad698a81e7cbf19b207f9`.
- Normal Windows Dev Build run #109 / run ID `35060729361`: **FULL PASS** across protected production gates.

## Protected PASS state — do not reopen without new evidence

- Preserve-motion GIF quality/smoothness, decimal-MB sizing, MP4, updater hardening and Windows no-console subprocess behavior.
- Favor-resolution exact source-frame decimation, measured-gain gating, loop closure repair, 8 FPS floor, 2048/native soft target and no-upscale behavior.
- Crop/Fit preview/export geometry is human-validated.
- Production dev.27 UI/runtime remains protected.

## Next gate

1. Amanda loads her current exported workspace into the validated v7 portable build and continues visual tuning.
2. Preserve imported/current values; new v7 fields use defaults until explicitly edited.
3. Treat runtime/packaging as validated but appearance as still under the human visual gate.
4. Do not integrate animation into production Polymorph, promote to `main`, or create a public release without a separate explicit decision.
