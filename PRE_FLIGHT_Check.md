# Polymorph Pre-Flight Log

Historical entries through dev.23 are preserved verbatim in [`HISTORY/PROJECT_LOGS/PRE_FLIGHT_THROUGH_DEV23.md`](HISTORY/PROJECT_LOGS/PRE_FLIGHT_THROUGH_DEV23.md). dev.24-dev.26 technical/visual history remains available in Git history; root tracking is intentionally rolling/compact.

## PFC-2026-09-14-061 — dev.26 FULL PASS / tester artifact ready

- Windows Dev Build run #93 / `34923465313` completed successfully on implementation commit `1927f88264786ea2b568bb98a87653571ab7168d`.
- PASS: bundled Polymorph fonts, all 56 unit tests, FFmpeg 9.0.1/gifski 1.32.0 checks, adaptive converter integration, GIF reference comparison, PyInstaller build, packaged application smoke, Inno Setup, checksum generation, unpacked app upload, and installer upload.
- PASS: unchanged 920×640 primary-action visibility gate. Root cause was timing/path placement: the compact height must be applied in the button's synchronous responsive `apply_scale` path, not only in deferred visual polish.
- PASS: normal-size Ready ring remains enlarged; compact scale restores its proven 24 px footprint.
- Run #92 / `34923070361` already proved the geometry correction technically. Packaging audit then found the installer script still hardcoded to dev.25; `installer/Polymorph.iss` now matches runtime dev.26 and run #93 revalidated the whole build.
- Artifact `Polymorph-dev-installer` ID `10378963848`; ZIP SHA-256 `465caa8821f642a5e3139ffc4a0d803e8803cd70beb2a7809d1ce05257bef2b5`.
- `Polymorph_Setup_v0.1.0-dev.26.exe` SHA-256 `203013ebc65c1dc99321c25b9c6143db98f8a6aaed1ce99b053a1bc751e8c6fe`; companion `.sha256` file matches.
- Technical gate is closed. Next gate is human visual review only. Do not reopen conversion/framing/adaptive behavior without new evidence.
- No `main` promotion or public release is authorized.

## PFC-2026-09-14-060 — Run #86 isolated remaining minimum-size defect

- Run #86 / `34915212307` passed all non-UI runtime/build gates and reduced the protected minimum-size overflow to 9 px.
- Subsequent work remained presentation-only and preserved the smoke assertion rather than relaxing it.

## PFC-2026-09-14-058 — Human visual correction pass / dev.26 candidate

- dev.26 is presentation-only: DPI-aware SVG rendering, cooler white-gold palette, smooth dark gradients, matched sizing fields, smaller section headings, larger Ready ring/smaller helper copy, and a stronger red primary action with `CONVERT MEDIA`.
