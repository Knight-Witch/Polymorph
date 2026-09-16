# Active Context — Polymorph `dev`

**Updated:** 2026-09-15  
**Current task:** human tuning of Motion Lab v5 using the scene-builder/preset workflow. Amanda should load her existing v4 export, verify the old tuning resumes, then continue visually editing and export the selected v5 workspace. Production Polymorph remains on dev.27 and its conversion/framing/adaptive behavior remains closed/validated.

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
- Motion Lab v5 implementation commit `d6d694e59358e9507bba540d43c44fb1fe32abc2` triggered Windows Dev Build run #108 / run ID `35056008609`: **FULL PASS**.
- PASS on run #108: unit tests, pinned FFmpeg/gifski checks, adaptive integration, GIF reference comparison, production PyInstaller build, packaged production smoke, installer compilation, checksum and artifact uploads.
- Production app/conversion source remains unchanged by Motion Lab v5.
- No public release exists; `main` remains non-experimental.

## Motion Lab v5 candidate — FULL PASS

- Implementation commit: `d6d694e59358e9507bba540d43c44fb1fe32abc2`.
- Dedicated workflow: `Polymorph Motion Lab Build` run #8 / run ID `35056008606`: **FULL PASS**.
- PASS: Windows source smoke.
- PASS: PyInstaller portable build.
- PASS: packaged Windows smoke.
- PASS: portable artifact upload.
- Artifact: `Polymorph-motion-lab`, artifact ID `10430402445`, 50,889,797 bytes.
- Artifact digest: `sha256:4ae317285edc9a7fc821ea0374f2eb8ef1aacb4094e5e7a1abee9c2c08482ee4`.
- v4 `polymorph-motion-spec` JSON loads directly and preserves old saved values; missing v5-only fields receive v5 defaults.
- Six large outer runes are the default frontmost layer above both progress rings.
- Rune families share asynchronous Fade/Snap transitions with timing randomization, hold timing, dim/bright ranges and zero-transition radial/twinkle/pulse glimmer modes.
- Exposed speed controls reach 2000% without modifying imported/current values.
- Editor provides wheel-safe sliders/spinboxes/combos, numeric entry/precision arrows, checkpoint resets, drag/drop layers, duplicate/remove/group-copy/group-clear and multi-study copy/rename/workspace export.
- Background sparkles expose spread/fade/density/speed/brightness and three cycling colors.
- Geometry pulse membership is restricted to linework/geometry, not rune rings/glyphs.
- Accepted v4 opaque partial-window behavior and large outer rune size/placement remain preserved.

## Protected PASS state — do not reopen without new evidence

- Preserve-motion GIF quality/smoothness, decimal-MB sizing, MP4, updater hardening and Windows no-console subprocess behavior.
- Favor-resolution exact source-frame decimation, measured-gain gating, loop closure repair, 8 FPS floor, 2048/native soft target and no-upscale behavior.
- Crop/Fit preview/export geometry is human-validated.
- Production dev.27 UI/runtime remains protected.

## Next gate

1. Amanda opens the validated v5 portable Motion Lab.
2. Amanda loads her existing v4 exported JSON and verifies the old tuning resumes without unexpected value changes.
3. Amanda tunes rune timing/glimmer, sparkle field, layers, geometry and studies as desired, using checkpoints while iterating.
4. Amanda exports the selected v5 workspace and returns the JSON; treat it as authoritative for final loader implementation.
5. Review the animated POLYMORPH button separately; loader approval does not automatically approve button motion.
6. Do not integrate animation into production Polymorph, promote to `main`, or create a public release without a separate explicit decision.
