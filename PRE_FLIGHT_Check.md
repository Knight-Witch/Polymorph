# Polymorph Pre-Flight Log

Historical entries through dev.23 are preserved verbatim in [`HISTORY/PROJECT_LOGS/PRE_FLIGHT_THROUGH_DEV23.md`](HISTORY/PROJECT_LOGS/PRE_FLIGHT_THROUGH_DEV23.md). dev.24-dev.27 technical/visual history remains available in Git history; root tracking is intentionally rolling/compact.

## PFC-2026-09-14-063 — Motion Lab FULL PASS

- PASS static: standalone Motion Lab source parses/compiles without syntax errors.
- PASS architecture: Motion Lab is isolated from production `PolymorphWindow`, conversion, framing, updater and encoder code; runtime version remains dev.27.
- PASS: loader exposes four compositions, 0–100% progress, auto-loop, independent motion/glow controls and runtime SVG emblem loading.
- PASS: preview surfaces cover black, current blue-black, procedural texture, busy contrast and arbitrary custom images.
- PASS: primary-action prototype uses an oversized arcane mechanism clipped by the visual button, plus hover wake, text tracer, click burst and expanded clipping-debug view.
- PASS: SVG direction risk is contained; canonical SVG is rendered normally and no CSS-style `stroke-dasharray` dependency exists for the basic emblem layer.
- PASS: Motion Lab Build run #1 / run ID `34931411518` completed successfully on implementation commit `0341ea270fb88495cde7f102e155e8ddd44680cc`.
- PASS: Windows source offscreen smoke, PyInstaller portable build, packaged Windows offscreen launch smoke, and artifact upload.
- Artifact `Polymorph-motion-lab`, artifact ID `10381886805`, size 50,767,525 bytes, digest `sha256:b96ff563b952c411614417df483c1996de51d128895b39692f9bf933c12583b6`.
- No production conversion, geometry semantics, adaptive, updater, subprocess, app-window, installer, runtime-version, or release behavior changed.
- Next gate: Amanda's human visual review of the portable Motion Lab only.

## PFC-2026-09-14-062 — dev.27 narrow visual corrections FULL PASS

- Human review of dev.26 reported the overall app much better; remaining scope was presentation-only.
- PASS: radio/selection labels are larger than their helper subtitles; helper copy is reduced for clear hierarchy.
- PASS candidate implementation: FRAMING and ASPECT RATIO card stacks share top alignment so headings/dividers sit on the same horizontal level and framing options rise with the corrected stack.
- PASS candidate implementation: CROP ZOOM hourglass replaced by a telescope/spyglass SVG from the already licensed Lucide icon set.
- Version identity is consistently dev.27.
- Windows Dev Build run #100 / `34926765260` completed successfully on `9b6954f30741437d2aabdf49fa4912d02fad99e6`.
- PASS: bundled fonts, all 56 unit tests, FFmpeg/gifski checks, adaptive integration, GIF reference comparison, PyInstaller build, packaged application smoke, Inno Setup, checksum generation, unpacked app upload, and installer upload.
- PASS: unchanged protected 920×640 packaged UI smoke.
- Artifact `Polymorph-dev-installer` ID `10379458708`; ZIP SHA-256 `b15cf034c4d21b6d6eb76bdbe38ca768adf729b840fc1c89ac90c2742554fe9a`.
- `Polymorph_Setup_v0.1.0-dev.27.exe` SHA-256 `738c8f2cb6f55f47e8013b99e8b07815acd1be656841756e5f49682315d0d03e`; companion `.sha256` matches.
- No conversion, geometry semantics, adaptive, updater, subprocess, font, or toolchain behavior changed.
- Next gate: human visual confirmation only.

## PFC-2026-09-14-061 — dev.26 FULL PASS / tester artifact ready

- Run #93 / `34923465313` completed successfully and produced the verified dev.26 tester used for this human review.
- Technical gate remained closed; only presentation feedback continued.
