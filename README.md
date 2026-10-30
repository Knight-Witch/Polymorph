# Polymorph

## [[Click Here to Download & Install]](https://github.com/Knight-Witch/Polymorph/releases/download/v0.2.1/Polymorph_Setup_v0.2.1.exe)

**Polymorph 0.2.1** expands the original media converter of Knight Witch's Windows media-conversion utility for animated WebP workflows. This project was created with the primary intent to serve the _Heroforge_ community and provide users with a tool to convert high res WebP captures into near-lossless GIF and MP4 conversions. While Heroforge was the initial spark to making this, the app can be used for anything you like. 
- **Reddit** treats animated WebP as static images once you hit the submit button on a post. As a result, only GIF or MP4 options are available for sharing spinny captures, and only GIFs come with the autoplay / looping function in Reddit's native post embed/previewer.
- **Discord** converts animated WebP into GIFs upon upload and the end-result is something that looks like it was converted into potato salad.

Online converters do not have the capability to produce true high-quality GIFs with minimal colour fidelity and resolution scale/clarity loss. Results are often highly blotchy.
Likewise, offline converts also seem to lack GIF output achieving a suitable / near-losseless quality, so I wanted to fix that.
- This application is designed for minimal user effort, maximum results.
  - No editing experience or technical know-how required.
  - Simply drop in your WebP, tell it what you want the end-result to be, and receive exactly that.

Everything runs locally on your PC. Polymorph does not upload your media to a cloud service and does not include telemetry.

## Highlights

- **NEW:** PNG, JPEG, BMP, TIFF and static WebP conversion to PNG or WebP; 4K/8K sources supported.
- **NEW:** PNG → lossless WebP, WebP → PNG, and PNG → PNG resolution-downscaling for user-specified MB ceilings.
- **NEW:** Animated GIF and video → looping animated WebP, with frame timing and transparency checks.
- **NEW:** Fast, verified incremental updates for future versions when an exact compatible update is published; otherwise a full installer is offered.
- **FIXED:** Some failed MP4 → GIF and MP4 → animated WebP conversions when encoders consolidate repeated stored frames.
- **What's New:** Updated notice with the existing optional Ko-fi and PayPal support buttons.

- Animated WebP, animated GIF, MP4 and common still-image input.
- High-quality GIF output with preserved source timing by default.
- MP4 output for platforms that support video.
- File-size targeting using spatial-resolution adjustment rather than silently lowering quality.
- Optional **Favor Resolution** GIF mode that may retain fewer original source frames only when measured results show a worthwhile resolution gain.
- Original, Crop, and Fit framing with shared preview/export geometry.
- Aspect-ratio presets and Crop zoom/repositioning.
- Live animated preview and queue-based batch processing.
- Local-only media processing with no telemetry or cloud upload service.
- Self-contained Windows installer.

## Platform

Polymorph 0.2.1 is intended for 64-bit Windows 10 and Windows 11.

## Install

Official Windows builds are published under this repository's **Releases** section.

For the first release, download:

- `Polymorph_Setup_v0.2.1.exe`
- `Polymorph_Setup_v0.2.1.exe.sha256`

Polymorph 0.2.1 is currently unsigned, so Windows SmartScreen may show an **Unknown Publisher** warning. The accompanying SHA-256 file lets you verify that the installer is the exact file published by Knight Witch.

## Basic use

1. Add one or more GIF/animated WebP/MP4 files, or a batch of static images.
2. Choose GIF, MP4, animated WebP, static WebP, or PNG as appropriate for the source.
3. Choose a sizing mode:
   - **Fit under file size** — Polymorph adjusts spatial resolution to stay under the requested limit.
   - **Set resolution** — choose exact output dimensions without upscaling beyond the source.
4. For GIF file-size mode, choose **Preserve Motion** or **Favor Resolution**.
5. Choose Original, Crop, or Fit framing and an aspect ratio if needed.
6. Choose an output folder.
7. Press **POLYMORPH**.

## Privacy

Polymorph performs media conversion locally. There is no media-upload service, account requirement, telemetry service, or background daemon.

Update checks query only this repository's official public GitHub Releases endpoint. Starting in v0.2.0, compatible later releases may offer verified changed-file packages; otherwise the updater offers a checksum-verified full installer. Upgrading from v0.1.0 also requires a full installer.

## Source and license

Polymorph's own source is distributed under the **Knight Witch Community Source License v1.0** in [`LICENSE`](LICENSE).

This is a **source-available license, not an open-source license**. It permits personal, educational, hobby, and professional creative use—including commercial work created with Polymorph—while restricting redistribution, resale, repackaging, hosted-service use, and commercialization of Polymorph itself.

Third-party components retain their own licenses. See `THIRD_PARTY.md` and `THIRD_PARTY_SOURCE.md` for the release component inventory, notices, and corresponding source information.

## Official links

- GitHub: https://github.com/Knight-Witch/Polymorph
- Ko-fi: https://ko-fi.com/knightwitch
- PayPal: https://www.paypal.com/paypalme/knightwitch
- Patreon: https://www.patreon.com/TheKnightWitch
- Discord: https://discord.gg/jZxncZuTRy

## Reporting bugs

Use this repository's issue tracker once public issue reporting is enabled. Include:

- Polymorph version;
- Windows version;
- input media dimensions, frame rate, duration, and approximate file size when relevant;
- selected Polymorph settings;
- what you expected to happen;
- what actually happened;
- reproducible steps.

Do not upload private media unless you intentionally want to make it available to other people reading the report.

---

Polymorph © 2026 Knight Witch™ / Amanda Ivans.
