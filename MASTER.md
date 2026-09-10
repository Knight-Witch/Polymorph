# Polymorph Master

## Current state

- Project: Polymorph
- Repository: `Knight-Witch/Polymorph`
- Platform target: Windows 10/11 x64
- Status: functional scaffold on `dev`; MP4 human-validated; GIF quality/frame behavior human-validated; decimal-MB ceiling validated in Windows CI; updater hardening pending Windows CI; no public release
- Current development version: `0.1.0-dev.7`

## Canonical conversion behavior

### GIF

- Input focus: animated WebP.
- Decode/process through FFmpeg.
- Stream FFmpeg output as YUV4MPEG directly to gifski 1.32.0.
- gifski quality: 100.
- gifski extra-effort mode enabled.
- Explicitly pass the FFmpeg output width to gifski so gifski does not apply its conservative default automatic downsize.
- Use explicit `yuv420p` for the Y4M stream on the pinned FFmpeg 9.0.1 Windows build.
- Explicitly pass the source FPS to gifski so the Y4M stream is not silently resampled to gifski's default 20 FPS.
- Infinite GIF repeat.
- Do not intentionally drop, duplicate, or lower frames to meet a size target.
- In file-size mode, reduce spatial resolution only as needed to fit the user ceiling.
- User-entered MB ceilings are decimal; the default `99 MB` means exactly 99,000,000 bytes.

### MP4

- Output: H.264 MP4 for broad compatibility.
- Preserve source timing/frame sequence.
- High-quality encoder settings are internal and hidden from normal UI.
- In file-size mode, resolution is the variable used to meet the ceiling; do not silently lower frame rate.
- Produced video should be cleanly loop-ready; actual repeat playback is controlled by the player/platform.
- First hands-on HeroForge media test reported no MP4 quality issues.

## Human validation

- Width-corrected GIF is visually on par with the standalone converter and was reported slightly smoother.
- `yuv420p` dev.3 retained the good smoothness and produced `1592x1592` on the Viper test under the earlier binary-MiB ceiling implementation.
- gifski 1.34.0 dev.4 regressed the same test to `1532x1532`; 1.32.0 is restored from dev.5 onward.
- Canonical standalone output was `1756x1756`, but the standalone timing pipeline was not frame-preserving: it omitted gifski `--fps`, causing Y4M/video input to be resampled toward gifski's default 20 FPS. That larger spatial resolution is therefore not a parity target for Polymorph's full-frame mode.
- Possible slight red/pink difference remains visually inconclusive and is not currently treated as a blocker.

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

## Update policy

- Check only official GitHub releases from `Knight-Witch/Polymorph`.
- Require the exact versioned installer and its matching `.sha256` companion before offering automatic installation.
- Download assets only from the official repository's HTTPS release path.
- Verify SHA-256 before launching the installer.
- No background service, startup daemon, unattended updater, or silent install.

## Known follow-ups

- A later optimizer pass may try to reclaim small amounts of spatial resolution, but must not alter source FPS/frame count or reduce GIF quality.
- The completion/status size readout still uses a binary MiB calculation while labeling it `MB`; correct that in a UI-only polish pass so display units match the decimal ceiling.
- First public release still requires a deliberate project-license choice and final release packaging/release workflow review.

## Deferred

- Estimated time remaining.
- Power-user/advanced codec controls.
- Parallel encoding.
- Final aesthetic skin and final Polymorph emblem.
- macOS/Linux packaging.
