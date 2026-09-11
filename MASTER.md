# Polymorph Master

## Current state

- Project: Polymorph
- Repository: `Knight-Witch/Polymorph`
- Platform target: Windows 10/11 x64
- Status: functional scaffold on `dev`; MP4 human-validated; Preserve-motion GIF quality/smoothness human-validated; decimal-MB ceiling validated; updater hardening validated; dev.9 full-resolution interpolation visually validated; dev.10/dev.11 measured adaptive fallbacks human-validated; dev.12 tests lower-complexity uniform temporal blending for Favor resolution / no public release
- Current development version: `0.1.0-dev.12`

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
- For each candidate, Polymorph performs one real gifski encode at the Preserve-motion dimensions to measure actual encoded byte cost before deciding whether any FPS sacrifice is worthwhile.
- The patched-Python 97/99 byte target is used to project how much spatial resolution that measured cost can realistically buy.
- A candidate must predict roughly 8% or greater linear spatial gain.
- The first/highest candidate that earns the gain is selected, minimizing temporal sacrifice.
- For a 25 FPS source, the current automatic cadence ladder is 20 FPS (50 ms), 16.67 FPS (60 ms), 14.29 FPS (70 ms), then 12.5 FPS (80 ms).
- Dev.12 uses exact-timestamp linear temporal blending for reduced-FPS candidates instead of optical-flow motion compensation. The cadence remains uniform; no periodic source-frame deletion is used.
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
- Dev.9 full-resolution 20 FPS motion interpolation was reported by the user as looking **really good**.
- Dev.9 still produced `1552x1552`, i.e. no spatial gain over Preserve motion.
- User-reported dev.9 completion size was `89.2 MB` under the then-existing binary-MiB display bug, corresponding to roughly 93.5 decimal MB and the optimizer's 93 MB acceptance region.
- Diagnosis: motion-compensated synthesized frames are materially more expensive for gifski than the naive frame-count ratio predicted; frame-count math is therefore unsuitable as the authority for adaptive cadence selection.
- Dev.10 switched to measured candidate cost and final actual-gain veto.
- Human dev.10 Viper result was `1552x1552 • 93.6 MB • 25 FPS`, confirming both 20 FPS and 16.67 FPS were correctly rejected when they could not buy a meaningful spatial increase.
- Human dev.11 Viper result was again `1552x1552 • 93.6 MB • 25 FPS`, confirming 14.29 FPS and 12.5 FPS optical-flow candidates also failed to earn the 8% spatial-gain threshold.
- Local comparison against the full-frame dev.11 Viper GIF showed exact-timestamp linear temporal blending produces essentially the same uniform 20 FPS cadence as motion compensation in measured adjacent-frame energy, while avoiding optical-flow warping/detail synthesis. Dev.12 tests whether that lower-complexity resampling is materially more compressible under gifski.

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

- Run full Windows CI for dev.12, including the 12.5 FPS uniform-blend smoke path and packaged adaptive UI smoke checks.
- Retest real Viper at GIF / Original / 99 MB / Favor resolution. Completion exposes final dimensions, decimal MB, and selected effective FPS.
- If dev.12 selects a reduced FPS, validate both spatial gain and whether temporal blending introduces visible ghosting/softening around thin geometry, hair, sword edges, cape/silhouette, and the loop seam.
- If dev.12 again returns 25 FPS, treat that as evidence that synthesized even-timestamp frames in general do not provide enough gifski savings on Viper; the next design branch should evaluate mathematically exact source-frame decimation cadences rather than keep lowering interpolated FPS.
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
