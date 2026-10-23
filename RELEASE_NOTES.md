# Polymorph 0.2.0 — Static Images, Animated WebP and Efficient Updates

Polymorph remains a Windows utility for high-quality, platform-ready local media conversion. This update adds static-image conversion, animated WebP output and a verified incremental-update system.

## New features

- **PNG → WebP:** Convert Hero Forge captures and other images, with alpha/ICC handling, optional pixel-preserving Lossless WebP and high-quality lossy compression.
- **WebP → PNG:** Export compatible PNG images where WebP is unsupported.
- **PNG → PNG:** Downsize resolution to meet a chosen file-size ceiling (for example, 16 MB → 10 MB), without reducing colors or silently dropping transparency.
- **GIF or video → animated WebP:** Preserve frame sequence, GIF frame delays, transparency and looping. Choose compact high-quality encoding or lossless output.
- **Static-image defaults:** Original resolution, 1:1 aspect-ratio selector and Lossless WebP enabled; Original framing does not crop unexpectedly.
- **Conversion status:** Real animated activity indicator with clear success and failure states.
- **First-launch What's New:** Feature overview and optional Ko-fi/PayPal support links, shown once.
- **Incremental updates for future releases:** Changed-file patch packages keep unchanged FFmpeg/gifski/runtime components. Updates verify hashes and restore original files if an application step fails. An exact matching published patch is required; otherwise use the full installer.

## Existing features retained

- High-fidelity animated WebP/MP4 → GIF, preserving source frames and timing by default using pinned FFmpeg and gifski.
- Optional Favor Resolution GIF mode, H.264 MP4 output, source-aware colors, Original/Crop/Fit framing, live preview, batch queue and measured decimal-MB targeting.
- Processing remains entirely local; there is no media upload or telemetry.

## Upgrade from 0.1.0

Existing users will be notified by the built-in launch-time update checker after this version is published. **The first upgrade uses the full installer** because v0.1.0 predates the incremental updater. Future releases may ship small version-specific patches.

## Installer and verification

Download `Polymorph_Setup_v0.2.0.exe` and `Polymorph_Setup_v0.2.0.exe.sha256` from the official [v0.2.0 release](https://github.com/Knight-Witch/Polymorph/releases/tag/v0.2.0). The unsigned executable may display Windows SmartScreen **Unknown Publisher**; use the SHA-256 file to verify the download.

Official Windows target: 64-bit Windows 10 and Windows 11. The bundle includes FFmpeg 9.0.1, gifski 1.32.0, PySide6 6.11.2 and Pillow 12.3.0. Their licenses are separate from the Knight Witch Community Source License; see `THIRD_PARTY.md` and `THIRD_PARTY_SOURCE.md`.
