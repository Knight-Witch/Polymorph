# Active Context — Polymorph `dev`

**Updated:** 2026-09-15  
**Current task:** Motion Lab v5 scene-builder candidate: restore Amanda's v4 exported state, provide high-range motion/rune controls, layer ordering, study/version management, duplication/grouping, checkpoint/reset and workspace export. Production Polymorph remains on dev.27 and its conversion/framing/adaptive behavior remains closed/validated.

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
- Last confirmed protected full production pass before v5: Windows Dev Build run #104 / `34964398145` on the v3 Motion Lab implementation.
- Motion Lab source remains isolated from production app/conversion code.
- No public release exists; `main` remains non-experimental.

## Motion Lab v5 candidate

- v4 FULL PASS baseline artifact: run #7 / `34972811122`, artifact `10398081397`.
- v5 preserves accepted opaque partial-window behavior and outer large-rune placement.
- Six large outer runes are now the default frontmost layer above both progress rings.
- All rune families use the same asynchronous transition engine with Fade/Snap, timing randomization, bright/dark holds, brightness/color range, and zero-transition radial/twinkle/pulse glimmer modes.
- Exposed speed controls extend to 2000% without modifying imported/current values.
- v4 `polymorph-motion-spec` JSON can be loaded directly; v5 exports multi-study workspaces.
- Editor adds drag/drop layers, duplicate/remove/group-copy/group-clear, study copy/rename, checkpoint/reset, numeric spinboxes and wheel-safe scrolling.
- Background sparkle particles expose spread/fade/density/speed/brightness and three cycling colors.
- Geometry pulse membership is restricted to linework/geometry, not rune rings/glyphs.
- Dedicated Windows Motion Lab CI: pending at candidate creation.
- Normal Windows Dev Build isolation check: pending at candidate creation.

## Protected PASS state — do not reopen without new evidence

- Preserve-motion GIF quality/smoothness, decimal-MB sizing, MP4, updater hardening and Windows no-console subprocess behavior.
- Favor-resolution exact source-frame decimation, measured-gain gating, loop closure repair, 8 FPS floor, 2048/native soft target and no-upscale behavior.
- Crop/Fit preview/export geometry is human-validated.
- Production dev.27 UI/runtime remains protected.

## Next gate

1. Complete v5 dedicated Motion Lab Windows CI and protected normal Windows Dev Build isolation check.
2. Give Amanda the validated v5 portable artifact directly.
3. Amanda loads her existing v4 exported JSON and confirms the old tuning resumes without value changes.
4. Amanda tunes/reorders/duplicates as desired, saves checkpoints, and exports the selected v5 workspace.
5. Treat the returned workspace JSON as authoritative for final loader implementation.
6. Do not integrate animation into production Polymorph, promote to `main`, or create a public release without a separate explicit decision.
