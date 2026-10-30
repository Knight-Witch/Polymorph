# Polymorph 0.2.1 — Conversion reliability fixes

This update fixes some failed MP4 conversions to GIF and animated WebP. Both encoders can consolidate redundant stored frames without shortening playback; the previous exact-count check sometimes rejected valid results.

- Validate dimensions and full playback duration even when encoders optimize redundant stored frames for MP4 → GIF/WebP.
- Preserve both **Fit under file size** and **Set resolution**, default full source motion, image-quality policies and Original/Crop/Fit framing.
- Handle entirely static MP4 clips when exporting an animated WebP.
- Show clearer failure details when output verification legitimately fails.
- Updated What's New message: **“Fixed some failed conversion bugs!”**. The existing Knight Witch support message, signature, Ko-fi and PayPal buttons and links are unchanged. View What's New remains available in the footer.

Media processing remains entirely local. Windows codec pins remain FFmpeg 9.0.1 and gifski 1.32.0.

## Updating

The in-app updater reads official public releases. If an exact matching incremental update is published, it uses checksum verification; otherwise it offers the checksum-verified full installer. Close Polymorph before running the installer so Windows can replace the existing executable.

## Installer and verification

Download `Polymorph_Setup_v0.2.1.exe` and `Polymorph_Setup_v0.2.1.exe.sha256` from the official [v0.2.1 release](https://github.com/Knight-Witch/Polymorph/releases/tag/v0.2.1). The unsigned executable may trigger SmartScreen **Unknown Publisher**. Windows 10/11 x64 is supported. Third-party licenses/source availability: `THIRD_PARTY.md` and `THIRD_PARTY_SOURCE.md`.
