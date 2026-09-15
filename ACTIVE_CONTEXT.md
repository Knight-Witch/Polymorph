# Active Context — Polymorph `dev`

**Updated:** 2026-09-14  
**Current task:** dev.26 branded-presentation correction. Runs #85 and #86 isolated the only failing gate to compact primary-action geometry; run #86 reduced minimum-size overflow from 38 px to 9 px. Current source now clamps the action's actual fixed height at the protected compact scale instead of only lowering minimum height.  
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
- Initial dev.26 presentation commit: `09b746d396748e82682ce6a484b2d31fae0667cc`.
- Run #85 / `34914748497`: all non-UI gates passed; packaged minimum-size smoke failed with action bottom 505 vs rail 467.
- First compact correction commit: `4f6a27d4b3224a3dd346e8e76dca344b3f422860`.
- Run #86 / `34915212307`: all non-UI gates passed; packaged minimum-size smoke improved to action bottom 476 vs rail 467, leaving 9 px overflow.
- Current correction: both the button's responsive `apply_scale` and final visual-geometry pass now use `setFixedHeight`, not only `setMinimumHeight`, so Qt cannot retain the larger normal-size hint at the compact gate.
- Responsive action height policy: at scale `<= 0.76`, `max(49, round(68 * scale))`; above it, `max(62, round(82 * scale))`.
- Preserve these dev.26 presentation features:
  - direct final-device-pixel SVG rendering for high-DPI sharpness;
  - smooth black-to-blue-black card gradients without warm glow/grain;
  - cooler white-gold/champagne headings/icons/borders/hardware;
  - slightly smaller Polymorph Bold tool headings;
  - equal max-MB / resolution-field widths and matching dark surfaces;
  - horizontally full-width deep-crimson primary action with small `CONVERT MEDIA` below `POLYMORPH`;
  - larger Ready ring and smaller Ready helper/detail text.
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

1. Commit the fixed-height compact correction and run the complete Windows Dev Build again.
2. Require the unchanged packaged 920×640 primary-action visibility smoke to pass.
3. If CI passes, retrieve `Polymorph-dev-installer` directly and give Amanda the artifact for human visual review.
4. Human review should focus on icon sharpness, cooler white-gold color balance, smooth dark gradients, equal sizing fields, normal-size primary-action weight/full width and `CONVERT MEDIA`, smaller tool headings, larger Ready ring, smaller Ready helper copy, and normal/minimum-size balance.
5. If dev.26 is accepted visually, mark visual-fidelity HUMAN PASS and proceed to the deferred working/loading animation phase.
6. Do not promote to `main` or create a public release without explicit approval.
