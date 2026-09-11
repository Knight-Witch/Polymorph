# Polymorph Master

## Current state

- Project: Polymorph
- Repository: `Knight-Witch/Polymorph`
- Platform target: Windows 10/11 x64
- Status: functional scaffold on `dev`; MP4 human-validated; Preserve-motion GIF quality/smoothness human-validated; decimal-MB ceiling validated; updater hardening validated; dev.9 adaptive Favor resolution mode pending Windows CI + full-resolution human validation / no public release
- Current development version: `0.1.0-dev.9`

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

- Experimental in dev.9 and must be explicitly selected by the user.
- Available only for GIF + Fit under file size.
- Starts from the Preserve-motion fitted result to determine whether FPS sacrifice is worthwhile.
- Uses a soft preferred long edge of native resolution capped at 2048 px.
- Requires roughly 8% predicted linear spatial gain before reducing FPS.
- Automatic FPS floor is 20 FPS.
- Reduced rates must use uniform GIF-centisecond cadences (`100 / N` FPS).
- Chooses the highest eligible FPS reaching at least 95% of the soft spatial target; if none does, chooses the lowest permitted viable rate.
- Uses FFmpeg motion interpolation rather than uneven frame deletion.
- Pads the final source frame for interpolation lookahead and trims to the exact planned output frame count.
- Never upscales beyond native framed geometry.
- Keeps gifski quality 100, `--extra`, explicit width, infinite repeat, and post-encode integrity verification.

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

## Adaptive motion diagnostic

- Real Viper source: 2048x2048, 375 frames, 25 FPS, 15.0 s.
- Simple 25 -> 20 frame selection showed a strong repeating motion-change spike every fourth interval.
- Motion-compensated interpolation removed that periodic cadence spike in a 512px diagnostic.
- Motion-interpolated diagnostic generated exactly 300 intended frames after end padding + exact trimming.
- Visual spot checks at diagnostic scale did not show obvious corruption around sword, hair, cape, silhouette, front/side/back views.
- Full-resolution human validation is still required before stable promotion.

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
- Footer icon buttons: Check Updates, GitHub, Ko-fi, Patreon, Discord.
- Automatic update check while app is open; no service/daemon.

## Update policy

- Check only official GitHub releases from `Knight-Witch/Polymorph`.
- Require exact versioned installer plus matching `.sha256` companion.
- Download only official repository HTTPS release assets.
- Verify SHA-256 before launching installer.
- No background service, startup daemon, unattended updater, or silent install.

## Known follow-ups

- Run full Windows CI for dev.9, including bundled `minterpolate` smoke coverage and packaged adaptive UI smoke checks.
- Human-test Favor resolution on the real Viper source at 99 MB; inspect full-resolution motion/interpolation artifacts and report final dimensions/file size.
- If Viper interpolation is clean, validate at least one harder HeroForge spin with thin geometry/hair/transparent or overlapping elements before stable promotion.
- Favor resolution currently performs a baseline full-frame fit before the adaptive fit; optimize conversion time only after behavior is validated.
- Completion/status size readout still uses binary MiB while labeling it `MB`; correct that in a UI-only pass.
- First public release still requires a deliberate project-license choice and final release packaging/release-workflow review.

## Deferred

- User-configurable advanced FPS floor/target controls.
- ETA/time remaining.
- Advanced codec controls.
- Parallel jobs.
- Final aesthetic skin and final Polymorph emblem.
- macOS/Linux packaging.
