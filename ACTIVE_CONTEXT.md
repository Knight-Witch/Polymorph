# Active Context — Polymorph `dev`

**Updated:** 2026-09-13  
**Current task:** dev.25 is technical PASS on run #62 with the custom Polymorph face confirmed in the frozen app and the 920×640 compact rail gate cleared; Amanda's human visual validation is now the active gate.  
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
- Technical-PASS code commit: `112f2e2efb128ef806cb6f44ed650b9753a5471e` (`Finish compact minimum-size rail budget`).
- Windows Dev Build run #62 / run ID `34809405250`: **PASS**.
- Installer artifact: `Polymorph-dev-installer`, artifact ID `10334421612`, digest `sha256:c77908691be09782951a52d8537e7c629681a3f6638e5a48e09b7880966b9384`.
- Run #62 PASS includes custom Polymorph font asset verification, all 56 unit tests, protected FFmpeg/gifski toolchain, adaptive integration, GIF reference, frozen app build, packaged smoke, installer compilation/checksum, and artifact uploads.
- The packaged smoke passed both `applied Polymorph title/subtitle/card-heading typography` and the existing 920×640 primary-action visibility gate in the same frozen application.
- First dev.25 implementation: `0fee8bc7a3dc3b7fd3a264b02206ab8b050aff09`.
- Responsive-QSS repair: `a59cd33670a124d4701a46686c6ae34f736a1538`.
- Direct-label typography repair: `b9aef66a703be4daf328614f015a54ce61013979`.
- First compact-only rail repair: `c0f0ad67d88494db899ab0eb45321f21c2a43088`.
- Run #60 proved the frozen packaged typography; run #61 measured the remaining rail deficit; run #62 is the first build to clear typography and compact geometry together.
- dev.24 run #57/artifact `10332274291` remains technical PASS but **human visual FAIL** and must not be promoted.
- No public release exists; `main` remains non-experimental.

## Intended typography

Amanda's supplied custom files register as one Polymorph family with Regular and Bold faces. They are bundled/self-contained; users do not install them separately.

- Brand title, subtitle/byline, primary action: Polymorph Regular.
- FILES and every right-rail CardHeading: Polymorph Bold.
- Body/control/footer text: Inter.

Original font-source hashes and shipped subset hashes are unchanged from dev.24. Do not retune title/subtitle/card/button point sizes or tracking until Amanda visually evaluates this run #62 tester.

## Protected PASS state — do not reopen without new evidence

- Preserve-motion GIF quality/smoothness, decimal-MB sizing, MP4, updater hardening and Windows no-console subprocess behavior.
- Favor-resolution exact source-frame decimation, measured-gain gating, loop closure repair, 8 FPS floor, 2048/native soft target and no-upscale behavior.
- Crop/Fit preview/export geometry is human-validated.
- Preserve 1260×820 design geometry and 920×640 supported minimum; run #62 cleared the minimum-size packaged gate.
- dev.22 SVG icon wiring remains protected.

## Next gate

1. Hand Amanda the run #62 dev.25 installer directly.
2. Amanda visually confirms the installed title, subtitle/byline, FILES heading, all right-rail headings, and primary action use the intended Polymorph faces; also check card density/alignment and compact/full-size balance against the approved mockup.
3. If visual issues remain, change only branded UI/presentation unless new evidence points elsewhere; do not reopen protected runtime areas.
4. Only after visual PASS adjust optical size/tracking if requested, then proceed to the deferred working/loading animation phase.

This successful-run record is documentation-only: it does not change runtime, version, package contents, UI behavior, conversion behavior, or public-release state.