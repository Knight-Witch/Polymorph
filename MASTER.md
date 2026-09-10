# Polymorph Master

## Current state

- Project: Polymorph
- Repository: `Knight-Witch/Polymorph`
- Platform target: Windows 10/11 x64
- Status: functional scaffold on `dev`; Windows installer/toolchain pipeline validated; packaged-EXE smoke validation pending / no public release
- Current development version: `0.1.0-dev.1`

## Canonical conversion behavior

### GIF

- Input focus: animated WebP.
- Decode/process through FFmpeg.
- Stream FFmpeg output as YUV4MPEG directly to gifski 1.32.0+.
- gifski quality: 100.
- gifski extra-effort mode enabled.
- Infinite GIF repeat.
- Do not intentionally drop frames or lower frame rate to meet a size target.
- In file-size mode, reduce resolution only as needed to fit the user ceiling.
- Default user ceiling: 99 MB.

### MP4

- Output: H.264 MP4 for broad compatibility.
- Preserve source timing/frame sequence.
- High-quality encoder settings are internal and hidden from normal UI.
- In file-size mode, resolution is the variable used to meet the ceiling; do not silently lower frame rate.
- Produced video should be cleanly loop-ready; actual repeat playback is controlled by the player/platform.

## v1 UI scope

- Drag/drop and Add Files.
- Multiple-file queue; one active conversion at a time.
- Animated live preview as visual centerpiece.
- Output: GIF / MP4.
- Sizing: Fit under file size / Set resolution (mutually exclusive).
- Framing: Original / Crop / Fit.
- Ratio presets plus expandable aspect-ratio guide.
- Crop repositioning via preview drag.
- Fit background color and source positioning.
- Output folder chooser; default Downloads.
- Conversion progress percentage.
- Footer icon buttons: Check Updates, GitHub, Ko-fi, Patreon, Discord.
- Automatic update check while the app is open; no service/daemon.

## Deferred

- Estimated time remaining.
- Power-user/advanced codec controls.
- Parallel encoding.
- Final aesthetic skin and final Polymorph emblem.
- macOS/Linux packaging.
