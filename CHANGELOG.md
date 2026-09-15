# Changelog

Historical entries through dev.23 are preserved verbatim in [`HISTORY/PROJECT_LOGS/CHANGELOG_THROUGH_DEV23.md`](HISTORY/PROJECT_LOGS/CHANGELOG_THROUGH_DEV23.md). dev.24-dev.27 investigation/build history remains available in Git history; root tracking is intentionally rolling/compact.

## POLY-2026-09-14-062 — dev.27 final presentation polish from human review

### Summary

- Human review of dev.26 marked the overall presentation substantially improved and identified three narrow remaining visual issues only.
- Option labels now read larger than their helper subtitles; the helper copy beneath OUTPUT FORMAT and GIF PRIORITY is deliberately smaller and quieter.
- The FRAMING card stack is pinned to the same top alignment as ASPECT RATIO so both titles/dividers share one horizontal level and the framing radio row follows directly beneath.
- CROP ZOOM now uses a telescope/spyglass icon instead of the accidental hourglass.
- Runtime is bumped to `0.1.0-dev.27` only to identify this visual tester cleanly. Conversion, framing semantics, adaptive logic, updater, subprocess behavior, fonts, and toolchain are unchanged.
- Next gate: complete Windows Dev Build and human visual confirmation.

## POLY-2026-09-14-061 — dev.26 packaged candidate reaches FULL PASS

- Windows Dev Build run #93 / `34923465313` is FULL PASS; verified dev.26 installer artifact was delivered for human review.
- The protected 920×640 primary-action visibility gate passed unchanged.

## POLY-2026-09-14-058 — Correct mockup palette, button weight, icon sharpness, and status scale

- dev.26 presentation pass added final-device-pixel SVG rendering, smooth blue-black cards, cooler white-gold/champagne accents, equal sizing fields, smaller tool headings, larger Ready ring/smaller helper text, and a substantial deep-red `POLYMORPH` action with small `CONVERT MEDIA` beneath it.
- Protected conversion/runtime behavior remains unchanged.
