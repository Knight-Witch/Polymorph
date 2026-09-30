# Polymorph

**Media conversion magic by Knight Witch™**

Polymorph is a Windows desktop utility for converting animated WebP media into high-quality GIF or MP4 output, with file-size targeting, framing controls, and a live animated preview.

Everything runs locally on your PC. Polymorph does not upload your media to a cloud service and does not include telemetry.

## What Polymorph does

- Converts animated WebP to GIF or MP4.
- Preserves source animation timing by default.
- Offers an optional **Favor Resolution** GIF mode that can retain fewer original source frames only when measured encoding results show a worthwhile resolution gain.
- Targets a maximum output size in decimal MB or lets you choose exact output dimensions.
- Supports Original, Crop, and Fit framing.
- Preserves aspect ratio; Crop and Fit do not stretch the source.
- Supports Crop positioning and 100–300% Crop zoom.
- Shows a live animated preview of the selected framing.
- Processes a batch queue one file at a time.
- Checks the official Polymorph GitHub Releases page for newer versions.

## Platform

Polymorph 0.1.0 is intended for 64-bit Windows 10 and Windows 11.

## Install

Official Windows builds are published under this repository's **Releases** section.

For the first release, download:

- `Polymorph_Setup_v0.1.0.exe`
- `Polymorph_Setup_v0.1.0.exe.sha256`

Polymorph 0.1.0 is currently unsigned, so Windows SmartScreen may show an **Unknown Publisher** warning. The accompanying SHA-256 file lets you verify that the installer is the exact file published by Knight Witch.

## Basic use

1. Add one or more animated WebP files.
2. Choose GIF or MP4.
3. Choose a sizing mode:
   - **Fit under file size** — Polymorph adjusts spatial resolution to stay under the requested limit.
   - **Set resolution** — choose exact output dimensions without upscaling beyond the source.
4. For GIF file-size mode, choose **Preserve Motion** or **Favor Resolution**.
5. Choose Original, Crop, or Fit framing and an aspect ratio if needed.
6. Choose an output folder.
7. Press **POLYMORPH**.

## Privacy

Polymorph performs media conversion locally. There is no media-upload service, account requirement, telemetry service, or background daemon.

Update checks query only the official GitHub Releases endpoint for this repository.

## Source and license

Polymorph's own source is distributed under the **Knight Witch Community Source License v1.0** in [`LICENSE`](LICENSE).

This is a **source-available license, not an open-source license**. It permits personal, educational, hobby, and professional creative use—including commercial work created with Polymorph—while restricting redistribution, resale, repackaging, hosted-service use, and commercialization of Polymorph itself.

Third-party components retain their own licenses. See `THIRD_PARTY.md` and `THIRD_PARTY_SOURCE.md` for the release component inventory, notices, and corresponding source information.

## Official links

- GitHub: https://github.com/Knight-Witch/Polymorph
- Ko-fi: https://ko-fi.com/knightwitch
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
