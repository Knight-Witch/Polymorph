# Active Context — Polymorph `dev`

**Updated:** 2026-09-24  
**Current task:** Human visual review of a new standalone Polymorph loader prototype inside Motion Lab. A separate `Polymorph Loader Preview` tab is being added so the newer rune-ring / progress-ring / sparkle-materialization concept can be reviewed in motion without integrating it into production Polymorph or altering the existing scene-builder workspace. Production Polymorph remains on dev.27 and its conversion/framing/adaptive behavior remains closed/validated.

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
10. `src/polymorph/motion_polymorph_loader_preview.py`
11. `run_motion_lab.py` when the standalone scene-builder shell/theme is implicated
12. `.github/workflows/motion-lab-build.yml` only when the standalone Windows artifact/build is implicated

Do not preload engine/history files unless the current task actually needs them.

## Production Dev candidate — protected

- Branch: `dev`.
- Runtime version: `0.1.0-dev.27`.
- Production implementation commit: `9b6954f30741437d2aabdf49fa4912d02fad99e6`.
- Normal Windows Dev Build run #109 / run ID `35060729361`: **FULL PASS** across protected production gates.
- The panel-readability commit changed only `run_motion_lab.py` plus tracking docs, so the normal Windows Dev Build path filter did not trigger; no production `src/**`, build, installer, pyproject or `run_polymorph.py` path changed.
- Production app/conversion source remains untouched by Motion Lab visual-tuning work.
- No public release exists; `main` remains non-experimental.

## Motion Lab current state — loader-preview candidate / human visual gate

- v7 implementation commit `06750079ee2dfa837a56600011367f16cb87646b` previously passed dedicated Motion Lab run #9 / run ID `35060729400` and normal Windows Dev Build run #109.
- Readability implementation commit: `845b029df1027bf6f4fac2a3a346c5d04d32d134`.
- Dedicated Motion Lab run #10 / run ID `35064912753`: **FULL PASS** (source smoke, PyInstaller build, packaged smoke, artifact upload).
- Artifact `Polymorph-motion-lab`, ID `10433348032`, size 50,890,729 bytes, digest `sha256:59d479d9cba0a2bd1b830093c566b0dfa97d19d62a9aae7220a28c898c922af5`.
- Styling-only changes:
  - section headers are brighter crimson/red, heavier, and separated with a thin deep-red rule;
  - the grey/unfilled slider track is removed; unused slider area is transparent while the active red fill and ivory handle remain.
- No element values, presets, motion behavior, animation timing, loader geometry or production code were changed by the prior readability pass.
- New candidate: a separate `Polymorph Loader Preview` tab adds an isolated Qt-rendered review concept with rotating runes/inner segments, progress ring, angular neon geometry, and progress-driven sparkle materialization of the bundled exact emblem. Existing scene-builder studies/presets remain separate.
- Dedicated Motion Lab run #11 / run ID `36098491868`: **FULL PASS** (source smoke, PyInstaller build, packaged smoke, artifact upload).
- Artifact `Polymorph-motion-lab`, ID `10848177893`, size 50,903,007 bytes, digest `sha256:df052b79f4dfa6fb3c5a586455bf0a0bfa2ea0de9def00291621cac1b975b2d1`.
- Normal Windows Dev Build run #110 / run ID `36098491841` was triggered by the `src/**` path filter and failed only while fetching the pinned external FFmpeg 9.0.1 archive because the upstream `gyan.dev` URL returned 404. All 56 unit tests passed before that external-download failure; no production package stage ran. This is not evidence of a loader-preview regression, and protected production run #109 remains the last full production PASS.

## Protected PASS state — do not reopen without new evidence

- Preserve-motion GIF quality/smoothness, decimal-MB sizing, MP4, updater hardening and Windows no-console subprocess behavior.
- Favor-resolution exact source-frame decimation, measured-gain gating, loop closure repair, 8 FPS floor, 2048/native soft target and no-upscale behavior.
- Crop/Fit preview/export geometry is human-validated.
- Production dev.27 UI/runtime remains protected.

## Next gate

1. Amanda reviews the packaged `Polymorph Loader Preview` tab from Motion Lab run #11 and gives visual feedback on rune speed, ring motion, sparkle/materialization behavior, progress treatment, spacing and glow.
2. Preserve all existing scene-builder workspace values and controls during loader-preview tuning.
3. Treat the external FFmpeg 404 in normal Windows Dev Build run #110 as separate build-infrastructure evidence; do not broaden the loader-preview task into production toolchain repair unless explicitly requested.
4. Do not integrate the new loader into production Polymorph, promote to `main`, or create a public release without a separate explicit decision.
