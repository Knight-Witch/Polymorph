# Polymorph 0.1.0

Polymorph 0.1.0 is the first public release of Knight Witch's Windows media-conversion utility for animated WebP and MP4 workflows.

## Highlights

- Animated WebP and MP4 input.
- High-quality GIF output with preserved source timing by default.
- High-fidelity MP4-to-GIF color handling for source-consistent output.
- MP4 output for platforms that support video.
- File-size targeting using spatial-resolution adjustment rather than silently lowering quality.
- Optional **Favor Resolution** GIF mode that may retain fewer original source frames only when measured results show a worthwhile resolution gain.
- Original, Crop, and Fit framing with shared preview/export geometry.
- Aspect-ratio presets and Crop zoom/repositioning.
- Live animated preview and queue-based batch processing.
- Local-only media processing with no telemetry or cloud upload service.
- Self-contained Windows installer.

## Install

Download the official release assets:
- `Polymorph_Setup_v0.1.0.exe`
- `Polymorph_Setup_v0.1.0.exe.sha256`

Polymorph 0.1.0 is unsigned. Windows SmartScreen may therefore display an **Unknown Publisher** warning. Verify the installer against the SHA-256 file published alongside it if desired.

## Supported platform
- 64-bit Windows 10
- 64-bit Windows 11

## GIF behavior

### Preserve Motion

This is the default GIF mode. Polymorph preserves the source frame sequence and timing and uses spatial resolution as the primary file-size tradeoff.

### Favor Resolution

When using GIF + Fit under file size, Favor Resolution may test lower source-frame cadences and keep one only when the measured encoded result provides a worthwhile increase in spatial resolution under the same size ceiling.

Polymorph uses original source frames for this mode; it does not synthesize intermediate frames with optical flow or frame blending.

## Framing

- **Original** keeps the full source framing.
- **Crop** trims to the selected aspect ratio without stretching and supports repositioning and Crop zoom.
- **Fit** preserves the complete source aspect ratio and expands the canvas to the selected ratio.

Preview and export use the same framing geometry.

## Privacy

Polymorph performs conversion locally on your computer. It does not upload source media, require an account, include telemetry or unnecessary bloat.
- This program contains ONLY the Polymorph application and its required runtime/support components (codecs, UI loader/dist. framework, installer,  etc).
- The update checker contacts the official GitHub Releases API for `Knight-Witch/Polymorph` only.

## Source and licensing

Polymorph source is available in this repository under the **Knight Witch Community Source License v1.0**. This is a source-available license, not an open-source license.

Third-party runtime/build components retain their own licenses. See `THIRD_PARTY.md` and `THIRD_PARTY_SOURCE.md` for notices and corresponding-source information.

## Integrity

Each official installer release includes a SHA-256 checksum file with the same base filename plus `.sha256`.

Official releases are published only from:

https://github.com/Knight-Witch/Polymorph/releases
