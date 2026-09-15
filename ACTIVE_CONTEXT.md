# Active Context — Polymorph `dev`

**Updated:** 2026-09-14  
**Current task:** dev.27 HUMAN VISUAL REVIEW. Amanda's dev.26 review said the app was much better and requested exactly three remaining presentation corrections: option/helper text hierarchy, FRAMING/ASPECT top alignment, and a spyglass icon for CROP ZOOM. dev.27 implements those corrections and Windows Dev Build run #100 is FULL PASS.  
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
- Implementation commit: `9b6954f30741437d2aabdf49fa4912d02fad99e6`.
- Windows Dev Build run #100 / run ID `34926765260`: **FULL PASS**.
- Tester artifact: `Polymorph-dev-installer`, artifact ID `10379458708`.
- Artifact ZIP SHA-256: `b15cf034c4d21b6d6eb76bdbe38ca768adf729b840fc1c89ac90c2742554fe9a`.
- Installer: `Polymorph_Setup_v0.1.0-dev.27.exe`.
- Installer SHA-256: `738c8f2cb6f55f47e8013b99e8b07815acd1be656841756e5f49682315d0d03e`.
- Companion `.sha256` was checked and matches.
- dev.27 changes are presentation-only:
  - selection/radio labels are explicitly larger than SecondaryText helper subtitles;
  - FRAMING and ASPECT RATIO card contents are pinned to the top of their equal-height pair so the title/divider baselines match;
  - CROP ZOOM uses a telescope/spyglass SVG instead of the accidental hourglass.
- dev.26 features remain preserved: cool white-gold palette, smooth blue-black panels, crisp high-DPI SVG rendering, matched sizing fields, smaller tool headings, full-width deep-crimson action with `CONVERT MEDIA`, larger Ready ring/smaller helper copy, supplied Polymorph fonts, and protected responsive compaction.
- No public release exists; `main` remains non-experimental.

## Protected PASS state — do not reopen without new evidence

- Preserve-motion GIF quality/smoothness, decimal-MB sizing, MP4, updater hardening, and Windows no-console subprocess behavior.
- Favor-resolution exact source-frame decimation, measured-gain gating, loop closure repair, 8 FPS floor, 2048/native soft target, and no-upscale behavior.
- Crop/Fit preview/export geometry is human-validated.
- Preserve 1260×820 design geometry and the 920×640 supported minimum.
- Preserve minimum-only rail compaction at responsive scale `<= 0.76`.
- Bundled Polymorph Regular/Bold and Inter application is confirmed.
- Packaged application smoke passes unchanged after dev.27.

## Next gate

1. Give Amanda the run #100 dev.27 installer for human visual review.
2. Review only the three requested corrections: option-label/helper hierarchy, FRAMING/ASPECT alignment, and spyglass icon.
3. If accepted, record visual-fidelity **HUMAN PASS** and proceed to the deferred working/loading animation phase.
4. If one remains off, change only that implicated presentation element.
5. Do not promote to `main` or create a public release without explicit approval.
