# Active Context — Polymorph `dev`

**Updated:** 2026-09-14  
**Current task:** run-#84/dev.25 human visual review identified specific remaining presentation defects. A dev.26 presentation-only correction is being built: sharpen high-DPI icons, make the primary action substantial/full-width with `CONVERT MEDIA`, normalize sizing-field geometry/surface color, shift the palette from yellow-gold to cooler white-gold, replace warm/grainy card fills with smooth black-to-blue-black gradients, reduce tool-heading size, enlarge the Ready ring, and reduce Ready helper text.  
**Runtime posture:** conversion/framing/adaptive behavior remains closed/validated for current v1 scope; branded presentation fidelity is still the active phase.

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
11. `src/polymorph/smoke_test.py` only if a UI/package assertion is being changed
12. `THIRD_PARTY.md` only when icon/license packaging is relevant

Do not preload engine/history files unless the current task actually needs them.

## Current Dev candidate

- Branch: `dev`.
- Runtime version: `0.1.0-dev.26`.
- Previous protected technical baseline: implementation commit `e76f88808f471c74ae100469ed4452a5095560b0`, Windows Dev Build run #84 / run ID `34890815616`, **FULL PASS**.
- Current dev.26 source is the presentation-correction commit containing `POLY-2026-09-14-058`; Windows CI is the immediate gate and exact run/artifact identity should be recorded here after it completes.
- dev.26 changes are intentionally presentation-only:
  - SVG assets render directly at final device-pixel size before tinting to remove the observed blur/upscale softness;
  - card/status/preview surfaces use smooth black-to-very-dark blue-charcoal gradients with no warm radial glow or synthesized grain;
  - headings/icons/borders/control hardware move from yellow-gold toward the approved mockup's cooler white-gold/champagne range;
  - right-rail CardHeading size is reduced slightly while preserving Polymorph Bold;
  - max-MB and resolution spin boxes use equal responsive widths and the same dark surface color, including disabled state;
  - the primary action is taller/substantial, remains full rail width, uses a stronger deep-crimson surface, and renders small `CONVERT MEDIA` below `POLYMORPH`;
  - the trailing spacer below the primary action is removed so it no longer looks stranded in a narrow strip;
  - the Ready marker is a larger painted crimson ring and its helper/detail line is smaller.
- No public release exists; `main` remains non-experimental.

## Typography — explicit non-negotiable boundary

Amanda's supplied custom display files are the intended packaged font. Her provenance clarification is authoritative for the current project unless she asks for independent verification: they came from a free/open-license font provider, are a version derived from/visually based on Trajan, and are not Adobe's font distribution.

- Exact packaged assets currently present on `dev`: `src/polymorph/assets/fonts/Polymorph-Regular.ttf.xz` and `src/polymorph/assets/fonts/Polymorph-Bold.ttf.xz`.
- `src/polymorph/ui/fonts.py` losslessly decompresses those assets in memory and registers the exact font bytes with Qt before the UI is built. Users/friends do **not** install them separately.
- Brand title, subtitle/byline and primary action: Polymorph Regular.
- FILES and every right-rail `CardHeading`: Polymorph Bold.
- Body/control/footer text: bundled Inter.
- Cinzel is only an emergency fallback if a packaged Polymorph face fails to load; it is not the intended normal tester appearance.
- Do not reintroduce a system-font dependency. Do not reinterpret the font as Adobe based only on Trajan resemblance/naming. Do not replace live UI text with pre-outlined SVG text as a workaround.

## Protected PASS state — do not reopen without new evidence

- Preserve-motion GIF quality/smoothness, decimal-MB sizing, MP4, updater hardening and Windows no-console subprocess behavior.
- Favor-resolution exact source-frame decimation, measured-gain gating, loop closure repair, 8 FPS floor, 2048/native soft target and no-upscale behavior.
- Crop/Fit preview/export geometry is human-validated.
- Preserve 1260×820 design geometry and 920×640 supported minimum; run #84 cleared the minimum-size packaged gate. dev.26 must clear it again before human review.
- Preserve current minimum-only rail compaction at responsive scale `<= 0.76`; presentation geometry overrides must not replace it.
- Bundled Polymorph Regular/Bold and Inter application is confirmed; do not re-open or weaken self-contained typography without concrete runtime evidence.

## Next gate

1. Run the canonical Windows Dev Build pipeline for dev.26 and require all existing unit/toolchain/adaptive/reference/frozen-smoke/installer/checksum/artifact gates to pass.
2. In particular, confirm the packaged 920×640 smoke still keeps the primary action visible after the larger button treatment.
3. If CI passes, retrieve the installer artifact directly and give Amanda the tester for human visual review.
4. Human review should focus on icon sharpness, cooler white-gold color balance, smooth dark gradients, equal sizing fields, primary-action height/full-width balance and `CONVERT MEDIA`, smaller tool headings, larger Ready ring, smaller Ready helper copy, and normal/minimum-size balance.
5. If dev.26 is accepted visually, mark visual-fidelity HUMAN PASS and proceed to the deferred working/loading animation phase.
6. Do not promote to `main` or create a public release without explicit approval.

## Handoff note

Run #84/dev.25 remains the protected technical baseline. dev.26 is a narrow branded-presentation correction only; conversion/runtime behavior must remain untouched unless new evidence directly implicates it.
