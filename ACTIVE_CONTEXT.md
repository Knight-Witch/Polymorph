# Active Context — Polymorph `dev`

**Updated:** 2026-09-14  
**Current task:** dev.27 narrow branded-presentation polish from Amanda's dev.26 human review. Overall dev.26 presentation was accepted as much improved; only option/helper hierarchy, FRAMING/ASPECT vertical alignment, and the CROP ZOOM icon remain in scope.  
**Runtime posture:** conversion/framing/adaptive behavior remains closed/validated for current v1 scope; do not reopen it without new evidence.

## Minimum continuation set

Read only:

1. `PROJECT_CONTRACT.md`
2. this file
3. `docs/UX_SPEC.md`
4. `src/polymorph/app.py`
5. `src/polymorph/ui/styles.py`
6. `src/polymorph/ui/branded_layout.py`
7. `src/polymorph/ui/fidelity_pass.py`
8. `src/polymorph/ui/visual_patch.py`
9. `src/polymorph/ui/compact_status_patch.py`
10. `src/polymorph/ui/final_polish_patch.py`
11. `src/polymorph/smoke_test.py` only if a package assertion itself is implicated

Do not preload engine/history files unless the current task actually needs them.

## Current Dev candidate

- Branch: `dev`.
- Runtime version: `0.1.0-dev.27`.
- dev.26 technical baseline: run #93 / `34923465313`, FULL PASS.
- Human review: dev.26 is substantially improved; preserve its palette, gradients, icon sharpness, matched sizing fields, primary action, Ready treatment, typography assets, and responsive behavior.
- dev.27 changes are presentation-only:
  - selection/radio labels are explicitly larger than SecondaryText helper subtitles;
  - FRAMING and ASPECT RATIO card contents are pinned to the top of their equal-height pair so the title/divider baselines match;
  - CROP ZOOM uses a telescope/spyglass SVG instead of the accidental hourglass.
- No public release exists; `main` remains non-experimental.

## Protected PASS state — do not reopen without new evidence

- Preserve-motion GIF quality/smoothness, decimal-MB sizing, MP4, updater hardening, and Windows no-console subprocess behavior.
- Favor-resolution exact source-frame decimation, measured-gain gating, loop closure repair, 8 FPS floor, 2048/native soft target, and no-upscale behavior.
- Crop/Fit preview/export geometry is human-validated.
- Preserve 1260×820 design geometry and the 920×640 supported minimum.
- Preserve minimum-only rail compaction at responsive scale `<= 0.76`.
- Bundled Polymorph Regular/Bold and Inter application is confirmed.

## Next gate

1. Complete the dev.27 implementation as one narrow presentation candidate.
2. Run the full Windows Dev Build and require the unchanged packaged 920×640 smoke to pass.
3. Retrieve the correctly labeled dev.27 installer and give Amanda the tester for human visual confirmation.
4. If these three corrections are accepted, record visual-fidelity HUMAN PASS and proceed to the deferred working/loading animation phase.
5. Do not promote to `main` or create a public release without explicit approval.
