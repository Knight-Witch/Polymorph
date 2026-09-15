# Polymorph Pre-Flight Log

Historical entries through dev.23 are preserved verbatim in [`HISTORY/PROJECT_LOGS/PRE_FLIGHT_THROUGH_DEV23.md`](HISTORY/PROJECT_LOGS/PRE_FLIGHT_THROUGH_DEV23.md). dev.24-dev.26 technical/visual history remains available in Git history; root tracking is intentionally rolling/compact.

## PFC-2026-09-14-059 — Run #85 minimum-size failure diagnosed and corrected

- Run #85 / `34914748497` passed font preparation, 56 unit tests, FFmpeg 9.0.1/gifski 1.32.0 verification, adaptive integration, GIF reference comparison and frozen application build.
- Packaged smoke correctly failed at the protected minimum-size assertion: `POLYMORPH action is clipped at minimum size: button bottom 505, rail 467`.
- This is a presentation geometry regression only. No protected conversion/runtime behavior failed or was implicated.
- Root cause is confirmed in `visual_patch.py`: the normal-size 82px-class action treatment was forced at compact scale and the trailing rail spacer was removed irreversibly. That violated the explicit `<= 0.76` compaction boundary from the accepted responsive implementation.
- Corrective patch is responsive and reversible: at `<= 0.76`, the action returns to the proven `max(49, round(68 * scale))` minimum-height policy; above that threshold it keeps the new substantial `max(62, round(82 * scale))` treatment. Spacer removal is eliminated entirely.
- Full-width horizontal expansion, deep-crimson paint, and `CONVERT MEDIA` secondary copy remain intact.
- Python syntax compilation of the corrected module passes. Next gate is another complete Windows Dev Build; do not weaken or bypass the packaged 920×640 smoke assertion.
- Runtime remains `0.1.0-dev.26`. No engine, framing, adaptive, updater, no-console subprocess, pinned toolchain, font payload, `main`, or public release behavior changed.

## PFC-2026-09-14-058 — Human visual correction pass / dev.26 candidate

- Human review of run #84 accepted alignment but rejected remaining icon sharpness, palette, card gradient, action-button proportions, sizing-field parity, heading scale, and Ready-status hierarchy.
- dev.26 adds DPI-aware direct SVG rendering, smooth blue-black card gradients, cooler white-gold/champagne accents, equal sizing fields, slightly smaller section headings, a larger Ready ring/smaller helper line, and a substantial red primary action with `CONVERT MEDIA`.
- This is presentation-only. Protected conversion/framing/adaptive/updater/subprocess/toolchain behavior remains unchanged.

## PFC-2026-09-14-057 — Preserve self-contained Polymorph font boundary

- Polymorph Regular/Bold remain packaged application fonts loaded directly by Qt. No system-font installation or SVG text replacement is permitted for the branded display typography.
