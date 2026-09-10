# Polymorph Master

## Current state

- Project: Polymorph
- Repository: `Knight-Witch/Polymorph`
- Platform target: Windows 10/11 x64
- Status: functional scaffold on `dev`; MP4 human-validated; GIF quality/frame behavior human-validated; gifski 1.34.0 parity tester pending Windows build / no public release
- Current development version: `0.1.0-dev.4`

## Canonical conversion behavior

### GIF

- Input focus: animated WebP.
- Decode/process through FFmpeg.
- Stream FFmpeg output as YUV4MPEG directly to gifski.
- gifski quality: 100.
- gifski extra-effort mode enabled.
- Explicitly pass the FFmpeg output width to gifski so gifski does not apply its conservative default automatic downsize.
- Use explicit `yuv420p` for the Y4M stream on the pinned FFmpeg 9.0.1 Windows build; literal auto-negotiation failed CI and the standalone reference effectively used the normal 4:2:0 Y4M path.
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
- First hands-on HeroForge media test reported no MP4 quality issues.

## Human validation

- Width-corrected GIF is visually on par with the standalone converter and may be slightly smoother.
- `yuv420p` dev.3 preserved smoothness and moved the Viper result only from `1570x1570` to `1592x1592`; the canonical standalone result remains `1756x1756`.
- The possible slight red/pink shift remains visually inconclusive.
- Next isolated parity variable is the bundled gifski version: dev.3 used 1.32.0; dev.4 tests stable 1.34.0 without changing converter logic.

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

## Known follow-ups

- File-size mode currently interprets the UI's `MB` value using binary MiB bytes. Before release, normalize the user-facing ceiling to decimal MB so `99 MB` means 99,000,000 bytes and cannot overshoot a platform's decimal 100 MB limit.
- If gifski 1.34.0 does not materially recover the remaining Viper resolution gap, compare the standalone timing/encoder invocation and then the optimizer search exactly; do not change multiple variables at once.

## Deferred

- Estimated time remaining.
- Power-user/advanced codec controls.
- Parallel encoding.
- Final aesthetic skin and final Polymorph emblem.
- macOS/Linux packaging.
