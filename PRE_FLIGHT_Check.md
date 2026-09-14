# Polymorph Pre-Flight Log

Historical entries through dev.23 are preserved verbatim in [`HISTORY/PROJECT_LOGS/PRE_FLIGHT_THROUGH_DEV23.md`](HISTORY/PROJECT_LOGS/PRE_FLIGHT_THROUGH_DEV23.md). Root tracking is intentionally rolling/compact; older detail is not mandatory startup reading.

## PFC-2026-09-13-046 — Keep Polymorph display typography while restoring responsive QSS metrics

- Run #58 / run ID `34806964426` is useful failed evidence, not a candidate to hand to Amanda.
- PASS before failure: custom font assets, 55 unit tests including the new stylesheet regression test, conversion toolchain, adaptive integration, GIF reference, frozen app build, and the strengthened packaged assertion `PASS applied Polymorph title/subtitle/card-heading typography`.
- Exact failure: minimum-size responsive assertion only — `POLYMORPH action is clipped at minimum size: button bottom 515, rail 489`.
- Diagnosis: moving body sizing from QSS into the inherited window QFont changed Qt size-hint/layout behavior. This is separate from the font-assignment bug; do not revert the applied Polymorph typography or weaken its regression check.
- Restore the prior responsive body/control QSS sizing under the branded app-root descendant selector, while adding explicit more-specific Polymorph family/size rules for BrandTitle, BrandSubtitle and CardHeading. Keep tracked QFont assignments for absolute letter spacing.
- Preserve 1260×820 default and 920×640 minimum geometry. Preserve all conversion/framing/adaptive/updater/subprocess behavior.
- Runtime remains dev.25 because run #58 produced no installer.
- Re-run the complete Windows pipeline. Only hand over an installer if both the applied typography gate and minimum-size action-visibility gate pass.

## PFC-2026-09-13-045 — Repair stylesheet precedence after dev.24 visual rejection

- Human visual gate rejected dev.24: custom Polymorph appeared only on the custom-painted primary action; title/subtitle/FILES/right-rail headings remained Inter/fallback.
- Confirmed root cause was generic QWidget QSS overriding explicit QLabel QFonts.
- dev.25 adds a real applied-font packaged assertion and fast regression test; do not treat font registration alone as proof of visual application again.

## PFC-2026-09-13-044 — dev.24 technical PASS, later human visual FAIL

- Windows run #57 / run ID `34805017987` passed the canonical technical/package pipeline.
- Installer artifact ID `10332274291`, digest `sha256:6e18bc546f065b29bf7b193e8bd84a6972c434f6a3c672bdf7a8572dd1bcbf26`.
- dev.24 is not visually accepted and must not be promoted.
