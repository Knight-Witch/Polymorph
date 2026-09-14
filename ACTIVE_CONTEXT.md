# Active Context — Polymorph `dev`

**Updated:** 2026-09-14  
**Current task:** human visual validation of the post-run-#79 mockup-fidelity correction from Windows Dev Build run #84. The implementation is technically PASS; do not continue visual changes until Amanda evaluates this installed tester.  
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
- Runtime version: `0.1.0-dev.25`.
- Tested implementation commit: `e76f88808f471c74ae100469ed4452a5095560b0` (`Match mockup alignment and icon rhythm`).
- Windows Dev Build run #84 / run ID `34890815616`: **FULL PASS**.
- The complete configured Windows pipeline passed: bundled Polymorph/Inter font preparation, unit tests, pinned FFmpeg 9.0.1/gifski 1.32.0 checks, adaptive integration, GIF reference comparison, frozen application build, packaged UI smoke, Inno Setup, checksum generation, and both artifact uploads.
- Packaged UI smoke passed the existing bundled-font/fidelity/two-column/FILES/920×640 primary-action/preview/adaptive/framing/linked-resolution/footer gates unchanged.
- Installer artifact: `Polymorph-dev-installer`, artifact ID `10366663850`, artifact digest `sha256:a3ccd6e2d1a131fe0ef66f70d3a3781605ea4b9be2e6e09362f29c366f3f4c38`.
- Installer inside artifact: `Polymorph_Setup_v0.1.0-dev.25.exe`, SHA-256 `5dc38ba315cb274fee8db9377db93d10f532c4ba39784187d16b69a891496c29`.
- Human-requested presentation changes in this candidate:
  - normal-size card/container rhythm and body/helper typography moved closer to the approved mockup;
  - right-rail section titles, controls and subtitles use one optical text axis instead of large inconsistent indents;
  - darker input surfaces, softer ivory body copy, muted helper copy, champagne-gold headings/dividers and restrained crimson selection remain the palette;
  - coherent larger Lucide thin-line SVG section icons;
  - `FRAMING` uses the Crop glyph;
  - `CROP ZOOM` uses the Hourglass glyph exactly as Amanda requested;
  - footer/social SVG icons render larger with wider icon-to-label spacing;
  - Lucide license notice is packaged/documented.
- The accidental temporary staging files created while assembling this pass are absent from the final candidate tree.
- No public release exists; `main` remains non-experimental.

## Intended typography

Amanda's supplied custom files register as one Polymorph family with Regular and Bold faces. They are bundled/self-contained; users do not install them separately.

- Brand title, subtitle/byline, primary action: Polymorph Regular.
- FILES and every right-rail CardHeading: Polymorph Bold.
- Body/control/footer text: bundled Inter.
- Run #84 changes optical size/rhythm only; it does not change font ownership or registration.

## Protected PASS state — do not reopen without new evidence

- Preserve-motion GIF quality/smoothness, decimal-MB sizing, MP4, updater hardening and Windows no-console subprocess behavior.
- Favor-resolution exact source-frame decimation, measured-gain gating, loop closure repair, 8 FPS floor, 2048/native soft target and no-upscale behavior.
- Crop/Fit preview/export geometry is human-validated.
- Preserve 1260×820 design geometry and 920×640 supported minimum; run #84 cleared the minimum-size packaged gate.
- Preserve current minimum-only rail compaction at responsive scale `<= 0.76`; presentation geometry overrides must not replace it.
- Bundled Polymorph Regular/Bold and Inter application is confirmed; do not reintroduce system-font dependencies.

## Next gate

1. Amanda installs/runs the run-#84 tester and compares it directly against the approved mockup.
2. Human review focuses on section title/content/helper horizontal alignment, card/container spacing, body/helper text scale, color balance, larger crisp icons, Framing=Crop, Crop Zoom=Hourglass, footer icon-label rhythm, and normal/minimum window balance.
3. If she finds visual issues, change only the implicated branded presentation/UI layer; do not reopen protected conversion/runtime areas.
4. If accepted, mark dev.25 visual-fidelity HUMAN PASS and proceed to the deferred working/loading animation phase.
5. Do not promote to `main` or create a public release without explicit approval.
