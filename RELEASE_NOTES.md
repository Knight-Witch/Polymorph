# Polymorph 0.3.1 — Animated WebP improvements

**Fixed: Animated WebP conversion speed and excessive file sizes.**

Animated WebP processing now uses a faster encoder setting and a more practical lossy quality default. Compared with the previous high-quality setting, real screen-recording samples produced substantially smaller WebP animations without changing the selected resolution or frame timing. Animated WebP is not always smaller than MP4; video formats such as H.264 are generally more efficient for long recordings.

**NEW: Better animated WebP controls**

- **Quality presets:** Compact (65), Balanced (75, default), High (85), or Maximum (95). You can still choose Lossless WebP separately.
- **Limit MB with Set resolution:** The requested decimal-MB ceiling now applies to animated WebP even at a fixed resolution. Polymorph adjusts lossy quality, retaining your chosen pixel dimensions and source motion timing. If the cap cannot be met without exceeding the supported compression range, the conversion fails with an actionable explanation rather than saving an unexpectedly huge file.
- **More reliable progress:** Animated WebP displays live frame-encoding progress instead of appearing stalled while the encoder assembles the animation.
- **Cleaner cancellation:** Failed or cancelled WebP conversions remove incomplete outputs, and closing the app requests termination of active conversions.

**Unchanged:** Batch conversion with shared/individual settings and per-file logs, high-fidelity GIF conversion, MP4 output, static image conversions, framing options, local-only processing, and Knight Witch's support links and message. The What's New overlay announces these changes once per Stable installation, with a manual View What's New option.

## Updating and installing

Polymorph 0.3.1 checks [official public Releases](https://github.com/Knight-Witch/Polymorph/releases) for updates. When no verified exact-version incremental patch is available, the updater offers the full installer with a SHA-256 checksum. Close Polymorph before installing.

Download `Polymorph_Setup_v0.3.1.exe` and the accompanying `.sha256` from [v0.3.1](https://github.com/Knight-Witch/Polymorph/releases/tag/v0.3.1). Windows 10/11 x64. The installer is unsigned and may trigger Windows SmartScreen. Third-party licenses and source information remain in `THIRD_PARTY.md` and `THIRD_PARTY_SOURCE.md`.
