# Changelog

Historical entries through dev.23 are preserved verbatim in [`HISTORY/PROJECT_LOGS/CHANGELOG_THROUGH_DEV23.md`](HISTORY/PROJECT_LOGS/CHANGELOG_THROUGH_DEV23.md). dev.24-dev.26 investigation/build history remains available in Git history; root tracking is intentionally rolling/compact.

## POLY-2026-09-14-060 — Clamp compact action to actual height after run #86

### Summary

- Windows Dev Build run #86 / run ID `34915212307` again passed fonts, all 56 unit tests, pinned conversion toolchain, adaptive integration, GIF reference comparison and frozen app build, then failed only the protected 920×640 packaged UI gate.
- The first responsive correction reduced the overflow from 38 px to 9 px (`button bottom 476, rail 467`), confirming the action-height diagnosis but showing that Qt's fixed vertical size policy still honored a larger size hint when only the minimum height was lowered.
- The action now receives its actual fixed responsive height: proven compact `max(49, round(68 * scale))` at `<= 0.76`, and the new substantial `max(62, round(82 * scale))` treatment above that threshold.
- Deep-crimson styling, horizontal full-width behavior, and the `CONVERT MEDIA` secondary line remain unchanged. The packaged smoke assertion remains unchanged.
- Runtime stays `0.1.0-dev.26`; no conversion, framing, adaptive, updater, subprocess, font, toolchain, `main`, or public-release behavior changed.

## POLY-2026-09-14-059 — Restore minimum-size rail budget after run #85 smoke failure

- Run #85 / `34914748497` passed all non-UI runtime/build gates, then correctly failed packaged smoke because the first dev.26 action treatment clipped at 920×640 (`button bottom 505, rail 467`).
- Spacer removal was eliminated and compact-vs-normal button heights were separated at the protected `<= 0.76` boundary.

## POLY-2026-09-14-058 — Correct mockup palette, button weight, icon sharpness, and status scale

- dev.26 presentation pass adds final-device-pixel SVG rendering, smooth blue-black cards, cooler white-gold/champagne accents, equal sizing fields, smaller tool headings, larger Ready ring/smaller helper text, and a substantial deep-red `POLYMORPH` action with small `CONVERT MEDIA` beneath it.
- Protected conversion/runtime behavior remains unchanged.
