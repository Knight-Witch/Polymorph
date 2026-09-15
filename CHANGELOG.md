# Changelog

Historical entries through dev.23 are preserved verbatim in [`HISTORY/PROJECT_LOGS/CHANGELOG_THROUGH_DEV23.md`](HISTORY/PROJECT_LOGS/CHANGELOG_THROUGH_DEV23.md). dev.24-dev.26 investigation/build history remains available in Git history; root tracking is intentionally rolling/compact.

## POLY-2026-09-14-061 — dev.26 packaged candidate reaches FULL PASS

### Summary

- Windows Dev Build run #93 / run ID `34923465313` is FULL PASS on implementation head `1927f88264786ea2b568bb98a87653571ab7168d`.
- All 56 unit tests, pinned FFmpeg 9.0.1/gifski 1.32.0 toolchain checks, adaptive integration, GIF reference comparison, frozen application build, packaged application smoke, Inno Setup compilation, SHA-256 generation, and both artifact uploads passed.
- The protected 920×640 primary-action visibility gate now passes without weakening the assertion. The final correction applies compact action height synchronously through `RefinedPolymorphButton.apply_scale` at `<= 0.76`, while normal/design sizing remains visually substantial.
- The enlarged Ready ring remains at normal sizes and returns to its proven compact footprint at the minimum responsive breakpoint.
- Run #92 / `34923070361` first proved the responsive geometry fix with a full technical PASS. A packaging audit then caught that `installer/Polymorph.iss` still labeled the installer dev.25; run #93 corrects that identity mismatch and re-passes the complete pipeline.
- Verified tester artifact: `Polymorph-dev-installer`, artifact ID `10378963848`, artifact ZIP SHA-256 `465caa8821f642a5e3139ffc4a0d803e8803cd70beb2a7809d1ce05257bef2b5`.
- Installer inside artifact: `Polymorph_Setup_v0.1.0-dev.26.exe`, SHA-256 `203013ebc65c1dc99321c25b9c6143db98f8a6aaed1ce99b053a1bc751e8c6fe`.
- Runtime remains `0.1.0-dev.26`; conversion, framing, adaptive, updater, subprocess, font, and toolchain behavior remain protected and unchanged.
- No public release or `main` promotion has occurred. Next gate is Amanda's human visual review of dev.26.

## POLY-2026-09-14-060 — Clamp compact action to actual height after run #86

- Run #86 / `34915212307` passed all non-UI gates and narrowed the protected minimum-size overflow to 9 px (`button bottom 476, rail 467`).
- This established that the remaining defect was responsive action geometry, not conversion/runtime behavior.

## POLY-2026-09-14-058 — Correct mockup palette, button weight, icon sharpness, and status scale

- dev.26 presentation pass adds final-device-pixel SVG rendering, smooth blue-black cards, cooler white-gold/champagne accents, equal sizing fields, smaller tool headings, larger Ready ring/smaller helper text, and a substantial deep-red `POLYMORPH` action with small `CONVERT MEDIA` beneath it.
- Protected conversion/runtime behavior remains unchanged.
