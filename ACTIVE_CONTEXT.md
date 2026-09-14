# Active Context — Polymorph `dev`

**Updated:** 2026-09-14  
**Current task:** direct continuation handoff at chat limit. Resume from the technically passing run-#84 dev.25 mockup-fidelity candidate, with one explicit typography correction from Amanda: the supplied Polymorph Regular/Bold files are a free/open-license Trajan-derived version from a free font provider, are **not Adobe**, and must remain bundled/self-contained inside Polymorph. Do not make friends install a system font, do not remove these assets, and do not substitute SVG/vector-outline text for the actual bundled font.  
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

- Branch: `dev`.
- Runtime version: `0.1.0-dev.25`.
- Tested implementation commit: `e76f88808f471c74ae100469ed4452a5095560b0` (`Match mockup alignment and icon rhythm`).
- Current documentation head before this handoff: `ee585aa058b82a5fe3ab5cb38b0c9645168cf168` (`docs: record run #84 technical PASS [skip ci]`).
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
- The closing chat briefly proposed refusing to bundle the font and converting display text to vector outlines. That proposal was wrong, was rejected by Amanda, and was **not implemented**. Ignore it in the next chat.

## Protected PASS state — do not reopen without new evidence

- Preserve-motion GIF quality/smoothness, decimal-MB sizing, MP4, updater hardening and Windows no-console subprocess behavior.
- Favor-resolution exact source-frame decimation, measured-gain gating, loop closure repair, 8 FPS floor, 2048/native soft target and no-upscale behavior.
- Crop/Fit preview/export geometry is human-validated.
- Preserve 1260×820 design geometry and 920×640 supported minimum; run #84 cleared the minimum-size packaged gate.
- Preserve current minimum-only rail compaction at responsive scale `<= 0.76`; presentation geometry overrides must not replace it.
- Bundled Polymorph Regular/Bold and Inter application is confirmed; do not re-open or weaken self-contained typography without concrete runtime evidence.

## Next gate

1. Start the next chat by reading `PROJECT_CONTRACT.md` and this file only, then the UI files routed above as needed.
2. Do not restart font-license speculation. Preserve the actual bundled Polymorph Regular/Bold implementation and treat Amanda's free/open-provider provenance clarification as the current project source of truth.
3. Resume the run-#84 human visual review against the approved mockup. Focus on section title/content/helper alignment, card/container spacing, body/helper text scale, color balance, larger crisp icons, Framing=Crop, Crop Zoom=Hourglass, footer icon-label rhythm, and normal/minimum window balance.
4. If Amanda identifies visual issues, change only the implicated branded presentation/UI layer; do not reopen protected conversion/runtime areas.
5. If dev.25 is accepted visually, mark visual-fidelity HUMAN PASS and proceed to the deferred working/loading animation phase.
6. Do not promote to `main` or create a public release without explicit approval.

## Handoff note

This handoff is documentation-only. No runtime code, font assets, version metadata, package behavior, tested installer identity, or protected behavior changed after run #84. The next chat should continue from this baton rather than reconstructing the project from earlier conversation history.
