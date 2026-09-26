# Active Context — Polymorph `dev`

**Updated:** 2026-09-24  
**Current task:** Third-pass visual tuning of the standalone `Polymorph Loader Preview` after Amanda's second review. The new candidate uses her Blender-vector emblem path as a dedicated clean alpha mask, restores a fully solid emblem fill, removes string-like materialization streaks, densifies/enlarges the rune band, replaces the static cyan-left/magenta-right split with an animated rotating spectrum, and rebuilds the inner geometry as cleaner nested angular frames. Production Polymorph remains on dev.27 and its conversion/framing/adaptive behavior remains closed/validated.

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

## Motion Lab current state — loader-preview FULL PASS / human visual gate

- v7 implementation commit `06750079ee2dfa837a56600011367f16cb87646b` previously passed dedicated Motion Lab run #9 / run ID `35060729400` and normal Windows Dev Build run #109.
- Readability implementation commit: `845b029df1027bf6f4fac2a3a346c5d04d32d134`.
- Dedicated Motion Lab run #10 / run ID `35064912753`: **FULL PASS** (source smoke, PyInstaller build, packaged smoke, artifact upload).
- Artifact `Polymorph-motion-lab`, ID `10433348032`, size 50,890,729 bytes, digest `sha256:59d479d9cba0a2bd1b830093c566b0dfa97d19d62a9aae7220a28c898c922af5`.
- Styling-only changes:
  - section headers are brighter crimson/red, heavier, and separated with a thin deep-red rule;
  - the grey/unfilled slider track is removed; unused slider area is transparent while the active red fill and ivory handle remain.
- No element values, presets, motion behavior, animation timing, loader geometry or production code were changed by the prior readability pass.
- First preview pass was rejected visually because it did not use the newly re-supplied exact emblem and diverged too far from the approved still mockup.
- Second-pass candidate uses the supplied `KW_EMBLEM_PATH.svg` path asset directly, keeps the emblem white, puts rotating runes inside a two-ring band, uses a third continuous outer progress ring, restores ornate angled mockup geometry and decorative nodes/dot trails, increases neon saturation/glow, and strengthens the top-to-bottom sparkle materialization front. Motion Lab run #12 caught a source-assembly syntax typo before packaging; that duplicate class stub is now removed.
- Existing scene-builder studies/presets remain separate.
- Third-pass implementation commit `aa6e91c9eb137b73923a70b1f7fb5fc76905bf38` uses the newly supplied Blender-vector emblem path as a dedicated clean mask, solid animated emblem fill, compact reveal particles, denser/larger rune band, moving full-sigil spectrum, and cleaner nested angular frames.
- Dedicated Motion Lab run #14 / run ID `36226971648`: **FULL PASS** for the third-pass loader candidate (source smoke, PyInstaller build, packaged smoke, artifact upload).
- Artifact `Polymorph-motion-lab`, ID `10900393943`, size 50,937,862 bytes, digest `sha256:b7bb6b363f8e5509b3fd3aefc38f197ebb420364477649820dcf7c3fbbbfceb8`.
- Normal Windows Dev Build run #113 / run ID `36226971451` passed all 56 unit tests and then failed only at the already-known pinned external FFmpeg 9.0.1 download 404 before production package stages; protected production run #109 remains the last full production PASS.
- Dedicated Motion Lab run #13 / run ID `36220819410`: **FULL PASS** for the prior second-pass loader candidate (source smoke, PyInstaller build, packaged smoke, artifact upload).
- Artifact `Polymorph-motion-lab`, ID `10898992118`, size 50,936,267 bytes, digest `sha256:5b42ade50295d5d4e6586bb5e57143e2645b9b13374ee8ca1a3cc3cabf6b1c8a`.
- Normal Windows Dev Build run #112 / run ID `36220819411` was again triggered by the `src/**` path filter and again failed only at the pinned external FFmpeg 9.0.1 download after all 56 unit tests passed. No production package stage ran; protected production run #109 remains the last full production PASS.

## Protected PASS state — do not reopen without new evidence

- Preserve-motion GIF quality/smoothness, decimal-MB sizing, MP4, updater hardening and Windows no-console subprocess behavior.
- Favor-resolution exact source-frame decimation, measured-gain gating, loop closure repair, 8 FPS floor, 2048/native soft target and no-upscale behavior.
- Crop/Fit preview/export geometry is human-validated.
- Production dev.27 UI/runtime remains protected.

## Next gate

1. Amanda reviews the packaged third-pass `Polymorph Loader Preview` from Motion Lab run #14 for solid emblem fill, particle behavior, denser rune band, animated color movement and cleaner inner geometry.
2. Preserve all existing scene-builder workspace values and controls during loader-preview tuning.
3. Treat the external FFmpeg 404 in normal Windows Dev Build run #110 as separate build-infrastructure evidence; do not broaden the loader-preview task into production toolchain repair unless explicitly requested.
4. Do not integrate the new loader into production Polymorph, promote to `main`, or create a public release without a separate explicit decision.
