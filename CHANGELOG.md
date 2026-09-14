# Changelog

Historical entries through dev.23 are preserved verbatim in [`HISTORY/PROJECT_LOGS/CHANGELOG_THROUGH_DEV23.md`](HISTORY/PROJECT_LOGS/CHANGELOG_THROUGH_DEV23.md). Root tracking is intentionally rolling/compact; use archived detail only when a current task needs it.

## POLY-2026-09-14-054 — dev.25 visual-polish tester passes the complete Windows pipeline

### Summary

- Windows Dev Build run #79 / run ID `34821077711` from tested implementation commit `06ad854d3cab7c1f249b253673e99ce18196cee5` passed the complete canonical Windows pipeline.
- PASS includes bundled custom Polymorph font verification, all 56 unit tests, pinned FFmpeg 9.0.1/gifski 1.32.0 checks, protected conversion/adaptive/GIF-reference gates, frozen application build, complete packaged UI smoke, Inno Setup compilation, checksum generation, and both artifact uploads.
- Packaged smoke passed `mockup-v2`, applied Polymorph title/subtitle/card-heading typography, two-column composition, FILES grouping, 920×640 primary-action visibility, concept alignment/slider styling, preview decode, adaptive GIF controls, framing/crop zoom mapping, linked resolution, and footer metadata in the same frozen application.
- Installer artifact `Polymorph-dev-installer`: ID `10338840830`, digest `sha256:5f15f4246c1a6fa254b86b7977a0716ad2e385c6abb4135b7f66a8a0bb79cb7e`.
- Retrieved tester filename: `Polymorph-dev.25-visual-polish-installer.zip`.
- This candidate contains the human-requested smaller section headings, coherent/distinct thin-line SVG section icons, aligned radio/helper columns, smaller Browse/Add Files text, real SVG play/pause control, and primary POLYMORPH label centered against the full button bounds.
- Runtime remains `0.1.0-dev.25`. The next gate is human visual validation; CI proves technical/package correctness, not appearance.
- This tracking update is documentation-only. It does not change runtime, package contents, conversion behavior, UI behavior, version, or public-release state; the tested installer corresponds to commit `06ad854d3cab7c1f249b253673e99ce18196cee5`.

## POLY-2026-09-14-053 — Restore the proven packaged-smoke harness after run #77

### Summary

- Windows Dev Build run #77 / run ID `34820591656` again passed font assets, all 56 unit tests, protected FFmpeg/gifski/adaptive/GIF-reference gates, and the frozen application build.
- The `mockup-v2` assertion repair worked, but packaged smoke then failed earlier at font-state validation because the prior repair accidentally replaced more of `smoke_test.py` than intended. Proven run-#75 property names/checks (`polymorphFontsLoaded`, `polymorphDisplaySource`), offscreen window placement, converter readiness, and final Qt event processing had been altered or dropped.
- Restore `smoke_test.py` byte-for-byte from visual-polish commit `b9196d17c67393ba79f509b107e30c08b55915ef`, with exactly one intentional difference: the fidelity assertion expects `mockup-v2` instead of `mockup-v1`.
- Do not change the actual visual-polish implementation, font loader, font assets, responsive geometry, or protected runtime behavior in this repair.
- Runtime remains `0.1.0-dev.25`; run #77 produced no installer.

## POLY-2026-09-14-052 — Repair stale mockup-version smoke gate after run #75

### Summary

- Windows Dev Build run #75 / run ID `34820011338` passed font assets, all 56 unit tests, protected FFmpeg/gifski/adaptive/GIF-reference gates, and the frozen application build from visual-polish commit `b9196d17c67393ba79f509b107e30c08b55915ef`.
- Packaged smoke then stopped immediately after responsive geometry because its assertion still demanded `polymorphFidelity == "mockup-v1"`, while the intentional visual-polish pass now reports `mockup-v2`.
- This is a stale test-version tag, not evidence of a runtime or packaging regression. Update only that assertion to `mockup-v2`; retain all later Polymorph-font, content, 920×640 primary-action visibility, preview, framing, and footer gates unchanged.
- Runtime remains `0.1.0-dev.25`; run #75 produced no installer.
- No UI behavior, conversion/framing/adaptive logic, updater, subprocess, font assets, SVG assets, or package-toolchain behavior changed by this repair.

## POLY-2026-09-14-051 — Visual polish from dev.25 human review

### Summary

- Amanda's installed run #62 tester confirmed the custom Polymorph face is finally applied correctly, but the human visual gate identified presentation issues that CI cannot judge: card headings are optically too large, the mixed section-icon set reads poorly, Output Format/Sizing radio bubbles do not align with GIF Priority, GIF-priority helper copy is over-indented, the playback glyph is effectively missing, Browse/Add Files typography is too large, and the primary POLYMORPH label is visibly right-shifted inside its button.
- Keep the proven bundled Polymorph font assignment, accepted 1260×820 / 920×640 responsive geometry, compact-rail fix, and all protected conversion/framing/adaptive/updater/subprocess behavior.
- Add an optical presentation controller that reapplies human-requested polish after responsive scaling: smaller Polymorph Bold card headings, unified radio-column indentation, helper-copy alignment with radio label text, and smaller Browse/Add Files text.
- Replace the current section-icon presentation with a coherent thin-line SVG set. Framing and Crop Zoom now use distinct symbols; Output Format, Sizing, GIF Priority, Aspect Ratio, Files and Output Folder each receive purpose-specific vectors.
- Replace the tiny text-based playback affordance with real play/pause SVG icons that follow preview playback state.
- Center the primary `POLYMORPH` title against the full action-button bounds rather than an offset text rectangle; the left decorative sigil remains separate decoration.
- Runtime remains `0.1.0-dev.25`; this is a visual-fidelity revision of the same development line and requires a new installed human check before acceptance.
- No GIF/MP4 encoding, adaptive selection, Crop/Fit geometry, file-size logic, updater, subprocess, or toolchain behavior changed.

## POLY-2026-09-13-050 — Record successful dev.25 technical tester

### Summary

- Windows Dev Build run #62 / run ID `34809405250` passed the complete technical pipeline from code commit `112f2e2efb128ef806cb6f44ed650b9753a5471e`.
- PASS includes bundled custom Polymorph font verification, all 56 unit tests, protected FFmpeg/gifski conversion gates, adaptive integration, GIF reference comparison, frozen application build, packaged smoke, Inno Setup compilation, checksum generation, and both artifact uploads.
- Crucially, the same frozen packaged smoke passed both `applied Polymorph title/subtitle/card-heading typography` and the existing 920×640 primary-action visibility gate. This is the first dev.25 build to clear both requirements together.
- Installer artifact: `Polymorph-dev-installer`, artifact ID `10334421612`, digest `sha256:c77908691be09782951a52d8537e7c629681a3f6638e5a48e09b7880966b9384`.
- dev.25 remains behind the human visual gate. Amanda must confirm the installed title, subtitle/byline, FILES heading, right-rail headings, and primary action before any promotion or optical typography retuning.
- This entry is documentation-only: no runtime, version, package contents, conversion behavior, UI behavior, or public-release state changed.

## POLY-2026-09-13-049 — Finish measured compact-rail budget after run #61

### Summary

- Windows Dev Build run #61 / run ID `34808985545` again passed the custom-font assets, all 56 unit tests, protected conversion/adaptive/GIF gates, frozen app build, and the packaged Polymorph typography assertions.
- The first compact-only rail pass worked as intended but was not quite sufficient: minimum-size action bottom improved from 508 to 494 while the rail remained 482, leaving 12 px of overflow.
- Preserve the confirmed font fix, primary-action height, full-size 1260×820 geometry, FILES/preview/footer geometry, and all protected runtime behavior.
- At compact scale only, reduce the top-level settings-rail gap from 2 px to 1 px and trim one additional pixel from the bottom padding of each top-level `ControlCard`. This is a measured continuation of the same minimum-only repair and does not alter normal-size metrics.
- Runtime remains `0.1.0-dev.25`; run #61 produced no installer.
- No GIF/MP4 conversion, adaptive GIF selection, framing/export geometry, updater, subprocess, or toolchain behavior changed.

## POLY-2026-09-13-048 — Compact only the minimum-size settings rail after run #60

### Summary

- Windows Dev Build run #60 / run ID `34807810638` proved the direct-label repair in the frozen EXE: packaged smoke passed `applied Polymorph title/subtitle/card-heading typography`, title/byline fidelity, and FILES grouping.
- Exact remaining failure is now isolated to responsive vertical budget only: at 920×640, `POLYMORPH action is clipped at minimum size: button bottom 508, rail 482`.
- Preserve the now-confirmed Polymorph font application. Do not change title/subtitle/card/button point sizes, tracking, font assets, primary-action height, or the accepted 1260×820 design geometry.
- At compact responsive scale only (`<= 0.76`), the scale registry now tightens only the top-level `ControlRailContent` gap and the top/bottom padding of top-level `ControlCard` layouts. The FILES card, left workspace, preview, footer, and full-size rail metrics are untouched.
- Runtime remains `0.1.0-dev.25`; run #60 produced no installer.
- No GIF/MP4 conversion, adaptive GIF selection, framing/export geometry, updater, subprocess, or toolchain behavior changed.

## POLY-2026-09-13-047 — Make branded font ownership local to the labels

### Summary

- Windows Dev Build run #59 / run ID `34807445345` again cleared font assets, 55 unit tests, protected conversion/adaptive/GIF gates and the frozen application build, then failed packaged smoke before installer creation.
- Exact run #59 smoke failure: `Brand title is not using Polymorph Regular: 'Inter' != 'Polymorph'`.
- Diagnosis: app-level selector specificity is still not a sufficient guarantee for Qt's resolved `QLabel.font()` state under the inherited Inter body stylesheet. Do not weaken the applied-font smoke assertion.
- Keep the restored body/control QSS sizing model, but make each BrandTitle, BrandSubtitle and CardHeading own a direct widget stylesheet containing its registered Polymorph family/point size, then reapply its tracked QFont for absolute letter spacing/bold state.
- Add a real offscreen Qt unit test that registers the packaged fonts, creates branded labels under the Inter app-root body QSS, applies typography, and asserts their resolved font families/tracking/bold state.
- Runtime remains `0.1.0-dev.25`; run #59 produced no installer.
- No font bytes, optical typography values, conversion/framing/adaptive logic, updater/subprocess behavior or window geometry changed.

## POLY-2026-09-13-046 — Preserve accepted responsive metrics while keeping Polymorph display overrides

- Run #58 proved the first dev.25 font fix worked but exposed a 920×640 right-rail overflow after moving body sizing into inherited QFont.
- Restore body/control sizing through QSS and keep explicit Polymorph display rules; runtime remains dev.25.

## POLY-2026-09-13-045 — Fix display-font stylesheet override in dev.25

- dev.24 human visual check showed only the custom-painted primary action used Polymorph. Root cause was generic QWidget QSS forcing Inter over normal QLabel display text.
- dev.25 introduced applied-font regression checks and versioned the rejected dev.24 tester separately.

## POLY-2026-09-13-044 — dev.24 technical PASS, human visual FAIL

- Run #57 / run ID `34805017987` technically passed; installer artifact ID `10332274291`, digest `sha256:6e18bc546f065b29bf7b193e8bd84a6972c434f6a3c672bdf7a8572dd1bcbf26`.
- dev.24 must not be promoted because the human visual gate rejected its font application.
