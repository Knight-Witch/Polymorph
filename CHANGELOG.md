# Changelog

Historical entries through dev.23 are preserved verbatim in [`HISTORY/PROJECT_LOGS/CHANGELOG_THROUGH_DEV23.md`](HISTORY/PROJECT_LOGS/CHANGELOG_THROUGH_DEV23.md). dev.24-dev.27 investigation/build history remains available in Git history; root tracking is intentionally rolling/compact.

## POLY-2026-09-14-063 — Standalone Motion Lab prototype FULL PASS

### Summary

- Added a standalone PySide6 Motion Lab for the deferred loader/working animation and animated primary action; production Polymorph behavior and runtime remain dev.27 unchanged.
- Added four loader compositions with independent rune/counter rotation, energy traces, glow, real 0–100% progress, and a swappable SVG center-emblem layer.
- Added black, Polymorph blue-black, procedural textured, busy stress-test, and custom-image preview backgrounds so animation legibility can be judged over different surfaces.
- Added an animated POLYMORPH button prototype that behaves as a clipped window into an oversized arcane mechanism, wakes on hover, carries a moving text-light tracer, and produces a short cast burst on click.
- Added a debug reveal mode that expands the button preview canvas and shows the full mechanism outside the cyan button clipping boundary.
- Added runtime `Load emblem SVG…`; basic emblem rendering does not rely on SVG path direction. A future contour-following tracer, if selected, should use a normalized animation path instead of rewriting canonical emblem artwork.
- Added a dedicated Windows Motion Lab workflow with source smoke, PyInstaller package, packaged smoke, and portable artifact upload.
- Motion Lab Build run #1 / run ID `34931411518` is FULL PASS on implementation commit `0341ea270fb88495cde7f102e155e8ddd44680cc`.
- Portable artifact `Polymorph-motion-lab`, artifact ID `10381886805`, digest `sha256:b96ff563b952c411614417df483c1996de51d128895b39692f9bf933c12583b6`.
- No conversion, framing, adaptive, updater, production UI, runtime-version, installer, or public-release behavior changed.

## POLY-2026-09-14-062 — dev.27 final presentation polish from human review

### Summary

- Human review of dev.26 marked the overall presentation substantially improved and identified three narrow remaining visual issues only.
- Option labels now read larger than their helper subtitles; the helper copy beneath OUTPUT FORMAT and GIF PRIORITY is deliberately smaller and quieter.
- The FRAMING card stack is pinned to the same top alignment as ASPECT RATIO so both titles/dividers share one horizontal level and the framing radio row follows directly beneath.
- CROP ZOOM now uses a telescope/spyglass icon instead of the accidental hourglass.
- Runtime is `0.1.0-dev.27` only to identify this visual tester cleanly. Conversion, framing semantics, adaptive logic, updater, subprocess behavior, fonts, and toolchain are unchanged.
- Windows Dev Build run #100 / run ID `34926765260` is FULL PASS on implementation commit `9b6954f30741437d2aabdf49fa4912d02fad99e6`.
- All 56 unit tests, pinned toolchain checks, adaptive integration, GIF reference comparison, frozen application build, packaged application smoke, Inno Setup compilation, SHA-256 generation, and artifact uploads passed.
- The unchanged protected 920×640 packaged UI smoke also passed after these presentation changes.
- Verified tester artifact: `Polymorph-dev-installer`, artifact ID `10379458708`, ZIP SHA-256 `b15cf034c4d21b6d6eb76bdbe38ca768adf729b840fc1c89ac90c2742554fe9a`.
- Installer: `Polymorph_Setup_v0.1.0-dev.27.exe`, SHA-256 `738c8f2cb6f55f47e8013b99e8b07815acd1be656841756e5f49682315d0d03e`; companion checksum file matches.
- Next gate is Amanda's human visual confirmation of these three corrections.

## POLY-2026-09-14-061 — dev.26 packaged candidate reaches FULL PASS

- Windows Dev Build run #93 / `34923465313` is FULL PASS; verified dev.26 installer artifact was delivered for human review.
- The protected 920×640 primary-action visibility gate passed unchanged.

## POLY-2026-09-14-058 — Correct mockup palette, button weight, icon sharpness, and status scale

- dev.26 presentation pass added final-device-pixel SVG rendering, smooth blue-black cards, cooler white-gold/champagne accents, equal sizing fields, smaller tool headings, larger Ready ring/smaller helper text, and a substantial deep-red `POLYMORPH` action with small `CONVERT MEDIA` beneath it.
- Protected conversion/runtime behavior remains unchanged.
