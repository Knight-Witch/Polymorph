# Polymorph Pre-Flight Log

Historical entries through dev.23 are preserved verbatim in [`HISTORY/PROJECT_LOGS/PRE_FLIGHT_THROUGH_DEV23.md`](HISTORY/PROJECT_LOGS/PRE_FLIGHT_THROUGH_DEV23.md). dev.24-dev.27 technical/visual history remains available in Git history; root tracking is intentionally rolling/compact.

## PFC-2026-09-14-062 — dev.27 narrow visual corrections staged

- Human review of dev.26 reports the overall app is much better; remaining scope is presentation-only.
- Staged: radio/selection labels larger than their helper subtitles; helper copy is reduced for clear hierarchy.
- Staged: FRAMING and ASPECT RATIO card stacks share top alignment so headings/dividers sit on the same horizontal level and framing options rise with the corrected stack.
- Staged: CROP ZOOM hourglass replaced by a telescope/spyglass SVG from the already licensed Lucide icon set.
- Version identity is bumped consistently to dev.27 for the next tester.
- No conversion, geometry semantics, adaptive, updater, subprocess, font, or toolchain changes are in scope.
- Next gate: full Windows Dev Build, including the unchanged 920×640 packaged smoke.

## PFC-2026-09-14-061 — dev.26 FULL PASS / tester artifact ready

- Run #93 / `34923465313` completed successfully and produced the verified dev.26 tester used for this human review.
- Technical gate remained closed; only presentation feedback continued.
