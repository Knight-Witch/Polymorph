# Active Context — Polymorph `dev`

**Updated:** 2026-09-13  
**Current task:** dev.25 branded-display typography repair after dev.24 human visual rejection, with run #58 proving the font now applies but exposing a minimum-size responsive regression.  
**Runtime posture:** conversion/framing/adaptive behavior remains closed/validated for current v1 scope; UI fidelity is the active development phase.

## Minimum continuation set

Read only:

1. `PROJECT_CONTRACT.md`
2. this file
3. `docs/UX_SPEC.md`
4. `src/polymorph/ui/fonts.py`
5. `src/polymorph/ui/styles.py`
6. `src/polymorph/ui/branded_layout.py`
7. `src/polymorph/ui/brand_widgets.py`
8. `src/polymorph/smoke_test.py` only if a UI/package assertion is being changed

Read architecture/engine files only if the task actually touches conversion/framing/adaptive/updater/subprocess/toolchain behavior. Do not preload history archives.

## Current Dev candidate

- Branch: `dev`
- Runtime version: `0.1.0-dev.25`
- dev.25 first implementation commit: `0fee8bc7a3dc3b7fd3a264b02206ab8b050aff09` (`Fix branded display typography in dev.25`).
- Windows Dev Build run #58 / run ID `34806964426`: **FAILED at packaged smoke after proving the typography repair works.**
- Run #58 PASS before failure: bundled Polymorph font verification, 55 unit tests including the new global-QWidget typography regression test, FFmpeg/gifski toolchain, adaptive integration, GIF reference, frozen app build, and packaged smoke through `PASS applied Polymorph title/subtitle/card-heading typography`.
- Run #58 exact failure: at the existing 920×640 supported minimum, primary action bottom was 515 while right rail height was 489. Installer steps were therefore correctly skipped.
- Confirmed cause of that secondary regression: the first dev.25 fix moved body sizing from the previously accepted QSS model into the inherited window QFont, changing Qt size hints/layout metrics at minimum size.
- Immediate repair candidate restores the old body/control QSS sizing model under `QWidget#AppRoot QWidget` while explicitly overriding `BrandTitle`, `BrandSubtitle`, and `CardHeading` with registered Polymorph family + the established point sizes. `tracked_font(...)` remains responsible for absolute tracking. This keeps the font fix without reverting to dev.24's Inter override.
- Exact repair commit/run/artifact identity must be recorded here after the next full Windows workflow completes.
- dev.24 run #57 / artifact `10332274291` remains technical PASS but **human visual FAIL** and must not be promoted.
- No public release exists; `main` remains stable/non-experimental.

## Font assets / intended assignment

Amanda's supplied files identify as one `Polymorph` family with Regular and Bold faces. Shipped display subsets are generated from those exact TTFs and self-contained in the app; users do not install them separately. Inter remains body/UI; Cinzel is emergency fallback only.

- Original Regular SHA-256: `e3d1bf414bdd0b517989e89ea3350acafdd90b61322c6c6ec8c7390a9f6ea188`
- Original Bold SHA-256: `aea401e914959cd4638cec82c0a7328a5d84b8d79d942c850052b10a18cca511`
- Shipped Regular subset SHA-256: `5aeb68e5a95011f9a21c1c19d81514f04ad8ff23623f6e54ec20921d2ad2ef2c`
- Shipped Bold subset SHA-256: `d437ef4599771311a175d3e7832c041eb76058e26a7e826dc1ea09547a111e3a`

Intended UI assignment:
- Brand title, subtitle/byline, primary action: Polymorph Regular.
- FILES and every right-rail CardHeading: Polymorph Bold.
- Body/control/footer text: Inter.

Do not retune the established title/subtitle/card/button point sizes or tracking until Amanda sees a tester where the intended face is actually applied everywhere.

## Protected PASS state — do not reopen without new evidence

- Preserve-motion GIF quality/smoothness, decimal-MB sizing, MP4, updater hardening and Windows no-console subprocess behavior.
- Favor-resolution selection: exact source-frame decimation, measured-gain gating, loop closure repair, 8 FPS floor, 2048/native soft target, no upscale.
- Crop/Fit preview/export geometry is human-validated.
- Preserve 1260×820 design geometry and 920×640 supported minimum unless a later human decision explicitly changes it. Current repair is intended to restore 920×640, not raise it.
- dev.22 SVG icon wiring remains protected.

## Active UI specification

Approved mockup is specification, not inspiration. Two-column composition: compact queue + dominant preview left, settings/action rail right. Header `POLYMORPH`; subtitle `Media conversion magic — by Knight Witch™`; version in footer; primary action `POLYMORPH`. Palette remains near-black/charcoal, ivory, champagne gold and restrained crimson.

The working/loading animation remains deferred until typography/layout is visually accepted.

## Next gate

1. Commit the responsive-metrics repair on `dev` without changing dev.25 version.
2. Run the full Windows workflow.
3. Required packaged smoke PASS includes both `applied Polymorph title/subtitle/card-heading typography` and `responsive shrink keeps primary action visible`.
4. On PASS, record commit/run/artifact identity here, retrieve `Polymorph-dev-installer`, and give Amanda the installer directly.
5. Amanda visually confirms title, subtitle, FILES, all right-rail headings and primary action use the intended Polymorph faces.
6. Only then adjust optical size/tracking if requested; preserve protected runtime behavior.
7. After typography/layout acceptance, proceed to working/loading animation.

## Historical routing

- Engine architecture: `docs/ARCHITECTURE.md`
- UI spec: `docs/UX_SPEC.md`
- Detailed pre-dev.24 history: `HISTORY/PROJECT_LOGS/`
