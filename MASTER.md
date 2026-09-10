# Polymorph Master

## Current state

- Project: Polymorph
- Repository: `Knight-Witch/Polymorph`
- Platform target: Windows 10/11 x64
- Status: functional scaffold on `dev`; MP4 human-validated; GIF quality/smoothness human-validated; decimal-MB ceiling validated; updater hardening validated; patched-Python timing gap directly quantified; dev.8 full-frame GIF optimizer parity build pending Windows CI / no public release
- Current development version: `0.1.0-dev.8`

## Canonical conversion behavior

### GIF

- Input focus: animated WebP.
- Decode/process through FFmpeg.
- Stream FFmpeg output as YUV4MPEG directly to gifski 1.32.0.
- gifski quality: 100.
- gifski extra-effort mode enabled.
- Explicitly pass the FFmpeg output width to gifski so gifski does not apply its conservative default automatic downsize.
- Production currently uses explicit `yuv420p` for deterministic Y4M compatibility on the pinned FFmpeg 9.0.1 Windows build.
- Explicitly pass source FPS to gifski and verify exact output frame count/timing.
- Infinite GIF repeat.
- Do not intentionally drop, duplicate, or lower frames to meet a size target.
- In file-size mode, reduce spatial resolution only as needed to fit the user ceiling.
- User-entered MB ceilings are decimal; default `99 MB` means exactly 99,000,000 bytes.
- Dev.8 ports the user-tested patched Python smart-fit resolution search for GIF file-size mode while retaining Polymorph's full-frame timing safeguards.

### MP4

- Output: H.264 MP4 for broad compatibility.
- Preserve source timing/frame sequence.
- High-quality encoder settings are internal and hidden from normal UI.
- MP4 file-size search remains the previously human-validated Polymorph implementation; dev.8 does not change it.
- Produced video should be cleanly loop-ready; actual repeat playback is controlled by the player/platform.
- First hands-on HeroForge media test reported no MP4 quality issues.

## Human validation and OG reference

- The only canonical OG behavioral reference is the patched Python `HeroForge_WebP_to_Reddit_GIF.py` actually run by the user.
- The separately packaged Discord build is unvalidated by the user and is not used as behavioral evidence.
- Width-corrected Polymorph GIF is visually on par with the patched Python result and was reported slightly smoother.
- Earlier full-frame dev.3 produced `1592x1592` under the old larger binary-MiB allowance.
- After correcting the ceiling to a true decimal 99 MB, the same Viper source produced `1552x1552`; quality/smoothness remained good.
- The patched Python OG result was `1756x1756` under the earlier effective allowance.
- Windows CI A/B proved the patched Python timing shape (FFmpeg `-r`, no gifski `--fps`) retained 41/50 frames and consumed 82.1878% of the bytes of an otherwise matched full-frame 25 FPS path.
- That byte ratio yields a 1.10305x linear-resolution factor; `1592 * 1.10305 = 1756.06`, matching the OG result essentially exactly.
- Therefore the OG spatial advantage is quantitatively explained by frame resampling. Polymorph will not reproduce that silently.
- Possible slight red/pink difference remains visually inconclusive and is not treated as a blocker.

## GIF file-size optimizer

- Patched Python fixed reference thresholds at a 99 MB ceiling: limit 99,000,000 bytes, target 97,000,000, acceptable floor 93,000,000, six normal attempts, 128 px emergency long-edge floor.
- Dev.8 generalizes those ratios to arbitrary user ceilings while preserving their exact behavior at 99 MB.
- The patched Python's measured-size square-root prediction, 0.985 safety factor, guaranteed 4% downward move after failure, pass/fail midpoint reclamation, and acceptance-band stop are preserved.
- Only GIF file-size mode uses this reference search. MP4 sizing is intentionally unchanged.

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
- Require exact versioned installer plus matching `.sha256` companion.
- Download only official repository HTTPS release assets.
- Verify SHA-256 before launching installer.
- No background service, startup daemon, unattended updater, or silent install.

## Known follow-ups

- Validate dev.8 on Windows CI, then run the same Viper 99 MB GIF test to measure how much full-frame spatial resolution the patched-Python smart-fit search safely reclaims.
- Completion/status size readout still uses binary MiB while labeling it `MB`; correct that in a UI-only pass after dev.8 validation.
- First public release still requires a deliberate project-license choice and final release packaging/release-workflow review.

## Deferred

- Estimated time remaining.
- Power-user/advanced codec controls.
- Parallel encoding.
- Final aesthetic skin and final Polymorph emblem.
- macOS/Linux packaging.
