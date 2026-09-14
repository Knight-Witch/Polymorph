# Active Context — Polymorph `dev`

**Updated:** 2026-09-13  
**Current task:** dev.25 branded-display typography is now confirmed inside the frozen EXE; run #60 leaves only a 920×640 right-rail vertical-budget failure to repair without disturbing full-size geometry.  
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

Do not preload engine/history files unless the current task actually needs them.

## Current Dev candidate

- Branch: `dev`
- Runtime version: `0.1.0-dev.25`
- First dev.25 implementation: `0fee8bc7a3dc3b7fd3a264b02206ab8b050aff09`.
- Responsive-QSS repair: `a59cd33670a124d4701a46686c6ae34f736a1538`.
- Direct-label typography repair: `b9aef66a703be4daf328614f015a54ce61013979`.
- Run #58 / ID `34806964426`: packaged typography assertion PASS, then minimum-size rail overflow FAIL.
- Run #59 / ID `34807445345`: app-level QSS repair still resolved normal QLabel fonts to Inter; no installer.
- Run #60 / ID `34807810638`: 56 unit tests, protected runtime/toolchain gates and frozen app build PASS. Packaged smoke then passed `applied Polymorph title/subtitle/card-heading typography`, title/byline fidelity and FILES grouping, proving the intended display face is now applied in the frozen EXE. Remaining failure is only `POLYMORPH action is clipped at minimum size: button bottom 508, rail 482`; no installer produced.
- Immediate repair keeps the confirmed font ownership and full-size geometry, but at responsive scale `<= 0.76` tightens only the top-level `ControlRailContent` gap and top/bottom padding of top-level `ControlCard` layouts. FILES, preview, footer and primary-action height remain unchanged.
- Exact repair commit/run/artifact identity must be recorded here after the next full Windows workflow completes.
- dev.24 run #57/artifact `10332274291` is technical PASS but **human visual FAIL** and must not be promoted.
- No public release exists; `main` remains non-experimental.

## Intended typography

Amanda's supplied custom files register as one Polymorph family with Regular and Bold faces. They are bundled/self-contained; users do not install them separately.

- Brand title, subtitle/byline, primary action: Polymorph Regular.
- FILES and every right-rail CardHeading: Polymorph Bold.
- Body/control/footer text: Inter.

Original font-source hashes and shipped subset hashes are unchanged from dev.24. Do not retune title/subtitle/card/button point sizes or tracking until Amanda receives a tester where the intended face is actually applied everywhere.

## Protected PASS state — do not reopen without new evidence

- Preserve-motion GIF quality/smoothness, decimal-MB sizing, MP4, updater hardening and Windows no-console subprocess behavior.
- Favor-resolution exact source-frame decimation, measured-gain gating, loop closure repair, 8 FPS floor, 2048/native soft target and no-upscale behavior.
- Crop/Fit preview/export geometry is human-validated.
- Preserve 1260×820 design geometry and 920×640 supported minimum; current repair must pass the existing minimum-size smoke gate.
- dev.22 SVG icon wiring remains protected.

## Next gate

1. Commit the compact-only rail repair on dev without changing dev.25 version.
2. Full Windows workflow must pass the real QLabel font test, protected runtime/toolchain gates, frozen app build, applied-typography packaged assertion, and 920×640 primary-action visibility in the same run.
3. On full Windows PASS, record commit/run/artifact identity here, retrieve `Polymorph-dev-installer`, and hand it to Amanda directly.
4. Amanda visually confirms title, subtitle, FILES, all right-rail headings and primary action.
5. Only after that visual PASS adjust optical size/tracking if requested; then move to loading-animation work.