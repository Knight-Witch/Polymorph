# Polymorph Pre-Flight Log

Historical entries through dev.23 are preserved verbatim in [`HISTORY/PROJECT_LOGS/PRE_FLIGHT_THROUGH_DEV23.md`](HISTORY/PROJECT_LOGS/PRE_FLIGHT_THROUGH_DEV23.md). Root tracking is intentionally rolling/compact; older detail is not mandatory startup reading.

## PFC-2026-09-13-047 — Direct widget-owned Polymorph typography after run #59

- Run #59 / run ID `34807445345` failed packaged smoke with `Brand title is not using Polymorph Regular: 'Inter' != 'Polymorph'`; installer steps were correctly skipped.
- Do not weaken the smoke. App-level specific QSS still leaves the resolved QLabel font as Inter under the body stylesheet.
- Keep the restored QSS body/control sizing model from the responsive repair.
- Apply the branded face directly on each BrandTitle, BrandSubtitle and CardHeading widget with a local stylesheet, then set the tracked QFont for absolute letter spacing/bold state.
- Add an offscreen Qt unit test using the packaged font loader and real QLabel objects under the Inter body QSS; require resolved Polymorph family before the slow build proceeds.
- Runtime remains dev.25; no installer from run #59.
- Preserve font bytes, existing point sizes/tracking, 1260×820 / 920×640 geometry, and all protected conversion/framing/adaptive/updater/subprocess behavior.

## PFC-2026-09-13-046 — Restore responsive QSS metrics after run #58

- Run #58 proved applied Polymorph typography but failed the minimum-size primary-action visibility gate after body sizing moved into inherited QFont.
- Restore the accepted body/control QSS sizing mechanism without reverting the font-assignment repair.

## PFC-2026-09-13-045 — dev.24 visual rejection / root-cause repair

- dev.24 was technical PASS but human visual FAIL: only the custom-painted primary action visibly used Polymorph.
- Root cause was global Inter QWidget QSS overriding QLabel display fonts. dev.25 adds real applied-font gates.
