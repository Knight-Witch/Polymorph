# Changelog

Historical entries through dev.23 are preserved verbatim in [`HISTORY/PROJECT_LOGS/CHANGELOG_THROUGH_DEV23.md`](HISTORY/PROJECT_LOGS/CHANGELOG_THROUGH_DEV23.md). Root tracking is intentionally rolling/compact; use archived detail only when a current task needs it.

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
- Keep the restored body/control QSS sizing model, but make each BrandTitle, BrandSubtitle and CardHeading own a direct widget stylesheet containing its registered Polymorph family/point size, then reapply its tracked QFont for absolute letter spacing and bold state.
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