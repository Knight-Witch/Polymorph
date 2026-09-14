# Changelog

Historical entries through dev.23 are preserved verbatim in [`HISTORY/PROJECT_LOGS/CHANGELOG_THROUGH_DEV23.md`](HISTORY/PROJECT_LOGS/CHANGELOG_THROUGH_DEV23.md). Root tracking is intentionally rolling/compact; use archived detail only when a current task needs it.

## POLY-2026-09-13-046 — Preserve accepted responsive metrics while keeping Polymorph display overrides

### Summary

- Windows Dev Build run #58 / run ID `34806964426` proved the dev.25 font-assignment repair itself works: packaged smoke passed `applied Polymorph title/subtitle/card-heading typography` before stopping later at the minimum-size responsive gate.
- Run #58 failed only at 920×640 because the first dev.25 implementation moved body sizing from QSS into the inherited window QFont; that changed Qt size-hint/layout behavior and pushed the POLYMORPH action 26 px below the right rail (`button bottom 515`, `rail 489`).
- Restore the previously accepted body/control sizing mechanism through QSS, but scope it to the branded app root/descendants rather than the bare generic `QWidget` rule.
- Add more-specific QSS rules for `BrandTitle`, `BrandSubtitle`, and `CardHeading` using the registered Polymorph family and the existing dev.23/dev.24 point sizes. The explicit branded rules outrank the Inter body rule while preserving the original responsive control metrics.
- Keep the existing `tracked_font(...)` assignments so absolute tracking remains controlled in QFont.
- Do not alter font assets, display point sizes/tracking, conversion/framing/adaptive behavior, updater/subprocess behavior, accepted 1260×820 / 920×640 window geometry, or primary-action rendering.
- Runtime remains `0.1.0-dev.25`; run #58 did not produce an installer, so this is a repair to the same dev.25 candidate.

### Validation notes

- The strengthened typography regression gate remains intact; it is not being weakened to make CI pass.
- Next gate is a fresh full Windows build. It must pass both the applied-Polymorph typography assertion and the minimum-size primary-action visibility assertion before an installer is handed to Amanda.

## POLY-2026-09-13-045 — Fix display-font stylesheet override in dev.25

- Amanda's installed dev.24 visual check rejected the typography pass: the custom Polymorph face appeared on the custom-painted primary action, but the app title, subtitle/byline, `FILES`, and right-rail card headings still rendered in Inter/fallback styling.
- Confirmed root cause: the generic `QWidget` stylesheet rule forced Inter and body size over the explicit `tracked_font(...)` QFonts on QLabel-based branded display text. The custom-painted primary button bypassed that QSS path, matching the screenshot exactly.
- dev.25 removes that override path, adds applied-font regression coverage, and advances runtime/package/installer metadata to `0.1.0-dev.25`.
- Font bytes and protected conversion/framing/adaptive behavior remain unchanged.

## POLY-2026-09-13-044 — Record successful dev.24 technical tester

- Windows run #57 / run ID `34805017987` passed all technical/package gates from commit `c4f9e1962716a56650366964acff806f61ae38b0`.
- Installer artifact ID `10332274291`, digest `sha256:6e18bc546f065b29bf7b193e8bd84a6972c434f6a3c672bdf7a8572dd1bcbf26`.
- dev.24 was subsequently **human-visually rejected** because registered Polymorph fonts were not actually applied to normal QLabel display text. It must not be promoted.
