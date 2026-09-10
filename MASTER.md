# Polymorph Master

## Current state

- Project: Polymorph
- Repository: `Knight-Witch/Polymorph`
- Platform target: Windows 10/11 x64
- Status: functional scaffold on `dev`; MP4 human-validated; current GIF quality/smoothness human-validated; decimal-MB ceiling validated; updater hardening validated in Windows CI; standalone-reference parity diagnostic pending CI; no public release
- Current development version: `0.1.0-dev.7`

## Canonical conversion behavior

### GIF

- Input focus: animated WebP.
- Decode/process through FFmpeg.
- Stream FFmpeg output as YUV4MPEG directly to gifski 1.32.0.
- gifski quality: 100.
- gifski extra-effort mode enabled.
- Explicitly pass the FFmpeg output width to gifski so gifski does not apply its conservative default automatic downsize.
- Production currently uses explicit `yuv420p` for the Y4M stream on the pinned FFmpeg 9.0.1 Windows build.
- Explicitly pass the source FPS to gifski so the production path preserves the source frame sequence rather than relying on gifski's default video-input FPS.
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
- After correcting `99 MB` to the actual decimal 99,000,000-byte ceiling, the same Viper test produced `1552x1552`; quality/smoothness remained otherwise good.
- The known-good standalone output remains `1756x1756`. Its supplied Python source uses FFmpeg `-r <source fps>` and omits gifski `--fps`, but the exact contribution of that timing difference to the 1756 result is being measured directly rather than treated as settled inference.
- The supplied standalone Python source does not specify a YUV pixel format. The exact Y4M pixel format used by the separately packaged share build is not proven by the available package checksum alone, so standalone pixel-format provenance is currently marked unresolved.
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

- Run and inspect the CI-only standalone-reference timing diagnostic before making any further GIF parity or optimizer changes.
- If the timing diagnostic does not account for the observed spatial-resolution gap, next compare the exact third-party binaries/toolchain used by the known-good packaged standalone build against the pinned Polymorph toolchain.
- A later optimizer pass may try to reclaim small amounts of spatial resolution, but must not alter source FPS/frame count or reduce GIF quality unless the product explicitly exposes such a tradeoff.
- The completion/status size readout still uses a binary MiB calculation while labeling it `MB`; correct that in a UI-only polish pass so display units match the decimal ceiling.
- First public release still requires a deliberate project-license choice and final release packaging/release workflow review.

## Deferred

- Estimated time remaining.
- Power-user/advanced codec controls.
- Parallel encoding.
- Final aesthetic skin and final Polymorph emblem.
- macOS/Linux packaging.
