# Polymorph Master

## Current state

- Project: Polymorph
- Repository: `Knight-Witch/Polymorph`
- Platform target: Windows 10/11 x64
- Status: functional scaffold on `dev`; MP4 human-validated; Preserve-motion GIF quality/smoothness human-validated; decimal-MB ceiling validated; updater hardening validated; dev.9 full-resolution motion interpolation visually validated but failed to gain spatial resolution; dev.10 measured adaptive cadence selection pending Windows CI + Viper retest / no public release
- Current development version: `0.1.0-dev.10`

## Canonical conversion behavior

### GIF — Preserve motion

- Default mode.
- Input focus: animated WebP.
- Decode/process through FFmpeg.
- Stream YUV4MPEG directly to gifski 1.32.0.
- gifski quality 100, `--extra`, explicit width, infinite repeat.
- Production currently uses explicit `yuv420p` for deterministic compatibility on bundled FFmpeg 9.0.1.
- Explicitly pass source FPS to gifski and verify exact source frame count/timing.
- Do not intentionally drop, duplicate, or lower frames to meet a size target.
- In file-size mode, reduce spatial resolution only as needed to fit the user ceiling.
- User-entered MB ceilings are decimal; default `99 MB` means exactly 99,000,000 bytes.
- GIF file-size search uses the patched-Python smart-fit resolution algorithm introduced in dev.8.

### GIF — Favor resolution

- Experimental and must be explicitly selected by the user.
- Available only for GIF + Fit under file size.
- Starts from the Preserve-motion fitted result.
- Preferred long edge remains native resolution capped at 2048 px; never upscale.
- Reduced rates must use uniform GIF-centisecond cadences (`100 / N` FPS).
- Candidate rates are measured nearest the source FPS first rather than selected from frame-count math alone.
- For each candidate, Polymorph performs one real gifski encode at the Preserve-motion dimensions to measure the actual byte cost of motion-interpolated frames.
- The patched-Python 97/99 byte target is used to project how much spatial resolution that measured cost can realistically buy.
- A candidate must predict roughly 8% or greater linear spatial gain.
- The first/highest candidate that earns the gain is selected, minimizing temporal sacrifice.
- For a 25 FPS source, the current automatic cadence ladder is 20 FPS (50 ms) then 16.67 FPS (60 ms); automatic floor is 16.67 FPS.
- Uses FFmpeg motion interpolation rather than uneven frame deletion.
- Pads the final source frame for interpolation lookahead and trims to the exact planned output frame count.
- Keeps gifski quality 100, `--extra`, explicit width, infinite repeat, and post-encode integrity verification.
- After the full adaptive size fit, a second measured-gain guard discards the lower-FPS output and returns Preserve motion unless the finished image is actually about 8% larger linearly.

### MP4

- Output: H.264 MP4 for broad compatibility.
- Preserve source timing/frame sequence.
- High-quality encoder settings remain internal and hidden from normal UI.
- MP4 file-size search remains the previously human-validated implementation.
- Produced video should be cleanly loop-ready; actual repeat playback is controlled by the player/platform.
- Hands-on HeroForge media testing reported no MP4 quality issues.

## Human validation and OG reference

- The only canonical OG behavioral reference is the patched Python `HeroForge_WebP_to_Reddit_GIF.py` actually run by the user.
- The separately packaged Discord build is unvalidated and excluded from parity decisions.
- Width-corrected Polymorph GIF is visually on par with OG and was reported slightly smoother.
- Earlier full-frame dev.3 produced `1592x1592` under the old larger binary-MiB allowance.
- True-decimal 99 MB Preserve-motion Viper output is `1552x1552`; quality/smoothness remained good.
- OG result was `1756x1756` but real-source inspection confirmed it contains 300 frames from a 375-frame / 25 FPS / 15 s source, i.e. exactly 20 FPS.
- Controlled CI independently quantified the same timing effect and explained the spatial advantage; OG 1756px is not a valid full-frame parity target.
- Possible slight red/pink difference remains visually inconclusive and is not treated as a blocker.

## Adaptive motion validation

- Real Viper source: 2048x2048, 375 frames, 25 FPS, 15.0 s.
- Simple 25 -> 20 frame selection showed a strong repeating motion-change spike every fourth interval.
- Motion-compensated interpolation removed that periodic cadence spike in a 512px diagnostic.
- Dev.9 full-resolution 20 FPS interpolation was reported by the user as looking **really good**.
- Dev.9 still produced `1552x1552`, i.e. no spatial gain over Preserve motion.
- User-reported dev.9 completion size was `89.2 MB` under the then-existing binary-MiB display bug, corresponding to roughly 93.5 decimal MB and the optimizer's 93 MB acceptance region.
- Diagnosis: interpolated frames are materially more expensive for gifski than the naive 25/20 frame-count ratio predicted; frame-count math is therefore unsuitable as the authority for adaptive cadence selection.
- Dev.10 measures real encoded candidate cost before choosing FPS and adds a final actual-gain veto.

## v1 UI scope

- Drag/drop and Add Files.
- Multiple-file queue; one active conversion at a time.
- Animated live preview as visual centerpiece.
- Output: GIF / MP4.
- Sizing: Fit under file size / Set resolution.
- GIF priority in file-size GIF mode: Preserve motion / Favor resolution.
- Framing: Original / Crop / Fit.
- Ratio presets plus expandable aspect-ratio guide.
- Crop repositioning via preview drag.
- Fit background color and source positioning.
- Output folder chooser; default Downloads.
- Conversion progress percentage.
- Development adaptive completion readout reports dimensions, decimal MB, and actual effective FPS.
- Footer icon buttons: Check Updates, GitHub, Ko-fi, Patreon, Discord.
- Automatic update check while app is open; no service/daemon.

## Update policy

- Check only official GitHub releases from `Knight-Witch/Polymorph`.
- Require exact versioned installer plus matching `.sha256` companion.
- Download only official repository HTTPS release assets.
- Verify SHA-256 before launching installer.
- No background service, startup daemon, unattended updater, or silent install.

## Known follow-ups

- Run full Windows CI for dev.10, including the 16.67 FPS `minterpolate` smoke path and packaged adaptive UI smoke checks.
- Retest real Viper at GIF / Original / 99 MB / Favor resolution. The completion line now reports the actual selected FPS and decimal MB directly.
- If dev.10 selects 16.67 FPS, validate whether the lower clean cadence remains visually acceptable and whether it finally earns a meaningful spatial increase; if it does not, the measured-gain guard should return the 25 FPS Preserve-motion result instead.
- If adaptive behavior is validated, test at least one harder HeroForge spin with thin geometry/hair/transparent or overlapping elements before stable promotion.
- Favor resolution performs extra measurement encodes by design; optimize conversion time only after cadence/result behavior is validated.
- First public release still requires a deliberate project-license choice and final release packaging/release-workflow review.

## Deferred

- User-configurable advanced FPS floor/target controls.
- ETA/time remaining.
- Advanced codec controls.
- Parallel jobs.
- Final aesthetic skin and final Polymorph emblem.
- macOS/Linux packaging.
