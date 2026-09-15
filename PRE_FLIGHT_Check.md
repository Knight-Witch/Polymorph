# Polymorph Pre-Flight Log

Historical entries through dev.23 are preserved verbatim in [`HISTORY/PROJECT_LOGS/PRE_FLIGHT_THROUGH_DEV23.md`](HISTORY/PROJECT_LOGS/PRE_FLIGHT_THROUGH_DEV23.md). dev.24-dev.26 technical/visual history remains available in Git history; root tracking is intentionally rolling/compact.

## PFC-2026-09-14-060 — Run #86 narrows compact overflow to 9 px; actual height clamp applied

- Run #86 / `34915212307` passed bundled fonts, all 56 unit tests, FFmpeg 9.0.1/gifski 1.32.0 checks, adaptive integration, GIF reference comparison and frozen application build.
- Packaged smoke remained the only failure: `POLYMORPH action is clipped at minimum size: button bottom 476, rail 467`.
- Improvement from run #85's 38 px overflow to 9 px confirms the responsive diagnosis. Remaining cause is Qt layout sizing: lowering only `minimumHeight` does not guarantee the button shrinks below its larger size hint while using a fixed vertical size policy.
- Corrective change now calls `setFixedHeight` with the same protected responsive split: compact `max(49, round(68 * scale))` at `<= 0.76`; normal/design `max(62, round(82 * scale))` above it.
- The smoke assertion is not changed. Full-width behavior, deep crimson action paint, and `CONVERT MEDIA` remain.
- Python syntax compilation passes. Next gate is another complete Windows Dev Build.
- No protected conversion/runtime/package semantics were changed; runtime remains `0.1.0-dev.26`.

## PFC-2026-09-14-059 — Run #85 minimum-size failure diagnosed and corrected

- Run #85 / `34914748497` passed all non-UI runtime/build gates and failed only the protected minimum-size action visibility check.
- Removed irreversible spacer deletion and restored compact-vs-normal action sizing at the existing `<= 0.76` responsive boundary.

## PFC-2026-09-14-058 — Human visual correction pass / dev.26 candidate

- dev.26 is presentation-only: DPI-aware SVG rendering, cooler white-gold palette, smooth dark gradients, matched sizing fields, smaller section headings, larger Ready ring/smaller helper copy, and a stronger red primary action with `CONVERT MEDIA`.
