# Active Context — Polymorph `dev`

**Updated:** 2026-09-14  
**Current task:** dev.26 branded-presentation correction after run #85 exposed one minimum-size geometry regression. Preserve the new crisp icons/cooler palette/clean gradients/equal sizing fields/larger Ready ring/red `POLYMORPH` + `CONVERT MEDIA` treatment, while restoring the protected 920×640 compact rail budget.  
**Runtime posture:** conversion/framing/adaptive behavior remains closed/validated for current v1 scope; branded presentation fidelity is the only active development area.

## Minimum continuation set

Read only:

1. `PROJECT_CONTRACT.md`
2. this file
3. `docs/UX_SPEC.md`
4. `src/polymorph/app.py`
5. `src/polymorph/ui/fonts.py`
6. `src/polymorph/ui/styles.py`
7. `src/polymorph/ui/branded_layout.py`
8. `src/polymorph/ui/brand_widgets.py`
9. `src/polymorph/ui/fidelity_pass.py`
10. `src/polymorph/ui/visual_patch.py`
11. `src/polymorph/smoke_test.py` only if a package assertion itself is implicated

Do not preload engine/history files unless the current task actually needs them.

## Current Dev candidate

- Branch: `dev`.
- Runtime version: `0.1.0-dev.26`.
- Protected technical baseline before dev.26: run #84 / `34890815616`, FULL PASS.
- Initial dev.26 implementation commit: `09b746d396748e82682ce6a484b2d31fae0667cc`.
- Windows Dev Build run #85 / `34914748497`: **FAILED only at packaged minimum-size UI smoke**.
- Run #85 passed bundled font preparation, all 56 unit tests, pinned FFmpeg/gifski checks, adaptive integration, GIF reference comparison, and frozen app build.
- Exact run #85 failure: `POLYMORPH action is clipped at minimum size: button bottom 505, rail 467`.
- Diagnosis: normal-size action height was forced at compact scale and the rail spacer was removed, violating the protected `<= 0.76` compact-layout boundary.
- Corrected dev.26 source restores the old compact action-height policy at `<= 0.76`, keeps the larger action above that threshold, and no longer removes the rail spacer.
- Presentation features to preserve through the correction:
  - SVG assets render directly at final device-pixel size before tinting for high-DPI sharpness;
  - card/status/preview surfaces use smooth black-to-very-dark blue-charcoal gradients with no warm radial glow or synthesized grain;
  - headings/icons/borders/hardware use cooler white-gold/champagne rather than yellow-gold;
  - right-rail CardHeading size is slightly smaller while preserving Polymorph Bold;
  - max-MB and resolution spin boxes use equal responsive widths and matching dark surfaces;
  - the primary action remains horizontally full-width, deep crimson, and includes small `CONVERT MEDIA` below `POLYMORPH`;
  - the Ready marker is a larger painted crimson ring and the status helper/detail line is smaller.
- No public release exists; `main` remains non-experimental.

## Typography — non-negotiable boundary

Amanda's supplied Polymorph Regular/Bold files remain the intended packaged display fonts. They are bundled/self-contained and registered directly with Qt; friends/users do not install them separately. Do not replace them with system fonts or outlined SVG text.

## Protected PASS state — do not reopen without new evidence

- Preserve-motion GIF quality/smoothness, decimal-MB sizing, MP4, updater hardening and Windows no-console subprocess behavior.
- Favor-resolution exact source-frame decimation, measured-gain gating, loop closure repair, 8 FPS floor, 2048/native soft target and no-upscale behavior.
- Crop/Fit preview/export geometry is human-validated.
- Preserve 1260×820 design geometry and the 920×640 supported minimum.
- Preserve minimum-only rail compaction at responsive scale `<= 0.76`; presentation geometry must not override it.
- Bundled Polymorph Regular/Bold and Inter application is confirmed.

## Next gate

1. Commit the responsive dev.26 action correction and run the complete Windows Dev Build again.
2. Require the packaged 920×640 primary-action visibility smoke to pass; do not weaken the assertion.
3. If CI passes, retrieve `Polymorph-dev-installer` directly and give Amanda the installer artifact for human visual review.
4. Human review should focus on icon sharpness, cooler white-gold color balance, smooth dark gradients, equal sizing fields, normal-size primary-action weight/full width and `CONVERT MEDIA`, smaller tool headings, larger Ready ring, smaller Ready helper copy, and normal/minimum-size balance.
5. If dev.26 is accepted visually, mark visual-fidelity HUMAN PASS and proceed to the deferred working/loading animation phase.
6. Do not promote to `main` or create a public release without explicit approval.
