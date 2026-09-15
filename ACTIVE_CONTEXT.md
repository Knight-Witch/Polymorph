# Active Context — Polymorph `dev`

**Updated:** 2026-09-15  
**Current task:** human tuning of Motion Lab v4 using the new per-element editor/export workflow. `B — Dense Runes` remains the review baseline. Production Polymorph remains on dev.27 and its conversion/framing/adaptive behavior remains closed/validated.

## Minimum continuation set

Read only:

1. `PROJECT_CONTRACT.md`
2. this file
3. `docs/MOTION_LAB.md`
4. `src/polymorph/motion_lab.py`
5. `src/polymorph/motion_loader.py`
6. `src/polymorph/motion_editor.py`
7. `src/polymorph/motion_loader_base.py`
8. `src/polymorph/motion_effects.py`
9. `.github/workflows/motion-lab-build.yml` only when the standalone Windows artifact/build is implicated

Do not preload engine/history files unless the current task actually needs them.

## Production Dev candidate — protected

- Branch: `dev`.
- Runtime version: `0.1.0-dev.27`.
- Production implementation commit: `9b6954f30741437d2aabdf49fa4912d02fad99e6`.
- Last confirmed protected full production pass before v4: Windows Dev Build run #104 / `34964398145` on the v3 Motion Lab implementation.
- v4 implementation head `8f68d4003be672de93cb5ae576abb1c8fb642a39` triggered Windows Dev Build run #107 / `34972810969`; it was still in progress when this baton was updated.
- Production app/conversion source was not modified by Motion Lab v4.
- No public release exists; `main` remains non-experimental.

## Motion Lab v4 candidate — FULL PASS

- Implementation head: `8f68d4003be672de93cb5ae576abb1c8fb642a39` (includes new `motion_editor.py`, element-driven loader, and editor UI).
- Dedicated workflow: `Polymorph Motion Lab Build` run #7 / run ID `34972811122`: **FULL PASS**.
- PASS: Windows source offscreen smoke.
- PASS: PyInstaller portable build.
- PASS: packaged Windows offscreen launch smoke.
- PASS: portable artifact upload.
- Artifact: `Polymorph-motion-lab`, artifact ID `10398081397`, 50,856,993 bytes.
- Artifact digest: `sha256:4f49ffffcfbcf8b96d8a3ef418fb72e67e51641237f08203bb6b0d87b60651a0`.
- Triangle and three large rune circles are static by default.
- Per-element editor supports span, scale, base rotation, color, link group, brightness, glow spread, signed rotation speed, Static, pulse membership and rune-transition speed where applicable.
- Irrelevant controls are disabled per selected element.
- Linked elements propagate span/scale/base-rotation/brightness/glow edits where both elements support the field.
- Global pulse controls: speed, trail/hold and dark-end length. Pulse order derives from current outside-to-inside radius/spread.
- `Export motion spec…` writes exact UTF-8 JSON state for direct implementation handoff.
- v3 accepted masking/window behavior and outer large-rune placement/size remain preserved in the loader path.

## Protected PASS state — do not reopen without new evidence

- Preserve-motion GIF quality/smoothness, decimal-MB sizing, MP4, updater hardening and Windows no-console subprocess behavior.
- Favor-resolution exact source-frame decimation, measured-gain gating, loop closure repair, 8 FPS floor, 2048/native soft target and no-upscale behavior.
- Crop/Fit preview/export geometry is human-validated.
- Production dev.27 UI/runtime remains protected.

## Next gate

1. Amanda tunes the loader in Motion Lab v4 rather than requesting geometry changes by description.
2. When satisfied, Amanda presses `Export motion spec…` and sends the generated `polymorph-motion-spec.json` back into chat.
3. Treat that JSON as the authoritative visual/motion configuration for implementation.
4. Review the animated POLYMORPH button separately; loader approval does not automatically approve button motion.
5. Do not integrate animation into production Polymorph, promote to `main`, or create a public release without a separate explicit decision.
