# Active Context — Polymorph `dev`

**Updated:** 2026-09-14  
**Current task:** build and validate the post-run-#79 mockup-fidelity correction. Amanda's installed dev.25 tester is technically sound but human-visual FAIL for remaining container density, body/helper typography, right-rail alignment, palette nuance, footer icon/label rhythm, and icon quality/semantics.  
**Runtime posture:** conversion/framing/adaptive behavior remains closed/validated for current v1 scope; branded presentation fidelity is the active development phase.

## Minimum continuation set

Read only:

1. `PROJECT_CONTRACT.md`
2. this file
3. `docs/UX_SPEC.md`
4. `src/polymorph/ui/fonts.py`
5. `src/polymorph/ui/styles.py`
6. `src/polymorph/ui/branded_layout.py`
7. `src/polymorph/ui/brand_widgets.py`
8. `src/polymorph/ui/fidelity_pass.py`
9. `src/polymorph/smoke_test.py` only if a UI/package assertion is being changed
10. `THIRD_PARTY.md` only when icon/license packaging is relevant

Do not preload engine/history files unless the current task actually needs them.

## Current Dev candidate

- Branch: `dev`
- Runtime version: `0.1.0-dev.25` (unchanged for this presentation-only correction).
- Prior tested implementation: `06ad854d3cab7c1f249b253673e99ce18196cee5`; Windows Dev Build run #79 / ID `34821077711` was FULL TECHNICAL PASS but is now HUMAN VISUAL FAIL for the issues below.
- Current implementation candidate: the mockup-v3 optical/alignment/icon pass recorded by `POLY/PFC-2026-09-14-055`; exact commit/run/artifact identity must be recorded after the next full Windows pipeline completes.
- Presentation changes in the candidate:
  - tighter normal-size control/card density while preserving compact-minimum rail logic;
  - smaller Inter body/control/helper type and mockup-nearer ivory/gold/charcoal/crimson balance;
  - right-rail title/content/helper columns aligned to one optical text axis;
  - oversized legacy radio/helper indents removed;
  - coherent 18 px Lucide thin-line section SVGs;
  - `FRAMING` uses Crop; `CROP ZOOM` uses Hourglass exactly as Amanda requested;
  - Simple Icons footer/social SVGs are retained but displayed larger with wider icon-to-label spacing;
  - Lucide license notice is packaged/documented.
- No public release exists; `main` remains non-experimental.

## Intended typography

Amanda's supplied custom files register as one Polymorph family with Regular and Bold faces. They are bundled/self-contained; users do not install them separately.

- Brand title, subtitle/byline, primary action: Polymorph Regular.
- FILES and every right-rail CardHeading: Polymorph Bold.
- Body/control/footer text: bundled Inter.
- Current visual correction changes optical size/rhythm only; it does not change font ownership or registration.

## Protected PASS state — do not reopen without new evidence

- Preserve-motion GIF quality/smoothness, decimal-MB sizing, MP4, updater hardening and Windows no-console subprocess behavior.
- Favor-resolution exact source-frame decimation, measured-gain gating, loop closure repair, 8 FPS floor, 2048/native soft target and no-upscale behavior.
- Crop/Fit preview/export geometry is human-validated.
- Preserve 1260×820 design geometry and 920×640 supported minimum.
- Preserve current minimum-only rail compaction at responsive scale `<= 0.76`; presentation geometry overrides must not replace it.
- Bundled Polymorph Regular/Bold and Inter application is confirmed; do not reintroduce system-font dependencies.

## Next gate

1. Commit a clean candidate tree with no temporary staging files.
2. Run the complete canonical Windows pipeline unchanged.
3. If CI fails, diagnose the exact gate and repair surgically; do not weaken protected assertions without evidence.
4. If CI passes, retrieve the `Polymorph-dev-installer` artifact directly and record commit/run/artifact identity here.
5. Amanda installs/runs that tester and visually compares it directly with the approved mockup, focusing on section title/content/helper alignment, card/container spacing, body text scale, colors, crisp larger icons, Framing crop / Crop Zoom hourglass semantics, footer icon-label spacing, and normal/minimum window balance.
6. If accepted, mark the dev.25 visual-fidelity phase HUMAN PASS and proceed to the deferred working/loading animation phase. Do not promote to `main` or create a public release without explicit approval.
