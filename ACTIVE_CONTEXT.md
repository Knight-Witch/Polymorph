# Active Context — Polymorph `dev`

**Updated:** 2026-09-16  
**Current task:** Motion Lab human tuning after the control-panel readability pass. The standalone lab now uses brighter crimson section headers and transparent unused slider tracks so the right-side editor is easier to scan. Production Polymorph remains on dev.27 and its conversion/framing/adaptive behavior remains closed/validated.

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
10. `run_motion_lab.py` when the standalone scene-builder shell/theme is implicated
11. `.github/workflows/motion-lab-build.yml` only when the standalone Windows artifact/build is implicated

Do not preload engine/history files unless the current task actually needs them.

## Production Dev candidate — protected

- Branch: `dev`.
- Runtime version: `0.1.0-dev.27`.
- Production implementation commit: `9b6954f30741437d2aabdf49fa4912d02fad99e6`.
- Normal Windows Dev Build run #109 / run ID `35060729361`: **FULL PASS** across protected production gates.
- The panel-readability commit changed only `run_motion_lab.py` plus tracking docs, so the normal Windows Dev Build path filter did not trigger; no production `src/**`, build, installer, pyproject or `run_polymorph.py` path changed.
- Production app/conversion source remains untouched by Motion Lab visual-tuning work.
- No public release exists; `main` remains non-experimental.

## Motion Lab current state — FULL PASS / human visual gate

- v7 implementation commit `06750079ee2dfa837a56600011367f16cb87646b` previously passed dedicated Motion Lab run #9 / run ID `35060729400` and normal Windows Dev Build run #109.
- Readability implementation commit: `845b029df1027bf6f4fac2a3a346c5d04d32d134`.
- Dedicated Motion Lab run #10 / run ID `35064912753`: **FULL PASS** (source smoke, PyInstaller build, packaged smoke, artifact upload).
- Artifact `Polymorph-motion-lab`, ID `10433348032`, size 50,890,729 bytes, digest `sha256:59d479d9cba0a2bd1b830093c566b0dfa97d19d62a9aae7220a28c898c922af5`.
- Styling-only changes:
  - section headers are brighter crimson/red, heavier, and separated with a thin deep-red rule;
  - the grey/unfilled slider track is removed; unused slider area is transparent while the active red fill and ivory handle remain.
- No element values, presets, motion behavior, animation timing, loader geometry or production code are intentionally changed by this pass.

## Protected PASS state — do not reopen without new evidence

- Preserve-motion GIF quality/smoothness, decimal-MB sizing, MP4, updater hardening and Windows no-console subprocess behavior.
- Favor-resolution exact source-frame decimation, measured-gain gating, loop closure repair, 8 FPS floor, 2048/native soft target and no-upscale behavior.
- Crop/Fit preview/export geometry is human-validated.
- Production dev.27 UI/runtime remains protected.

## Next gate

1. Amanda visually reviews the right-panel section headers and slider treatment in the packaged Motion Lab artifact from run #10.
2. Preserve all imported/current workspace values during further visual tuning.
3. Treat runtime/packaging as validated but appearance as still under the human visual gate.
4. Do not integrate animation into production Polymorph, promote to `main`, or create a public release without a separate explicit decision.
