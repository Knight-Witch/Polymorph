# Polymorph Master

## Current state

- Project: Polymorph
- Repository: `Knight-Witch/Polymorph`
- Platform target: Windows 10/11 x64
- Status: functional scaffold on `dev`; MP4 human-validated; Preserve-motion GIF quality/smoothness human-validated; decimal-MB ceiling validated; updater hardening validated; dev.14 first-launch layout/tooltips human-validated; dev.15 diagnostics proved exact source-frame decimation works on real HeroForge media; Viper plus two kitbash/decal-heavy variants are human/diagnostically validated; dev.16 fixes framing-preview parity, adds crop zoom, makes radio selection explicit, and suppresses ffprobe console flashes / no public release
- Current development version: `0.1.0-dev.16`

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

- Explicit opt-in; Preserve motion remains the default.
- Available only for GIF + Fit under file size.
- Starts from the Preserve-motion fitted result.
- Preferred long edge remains native resolution capped at 2048 px; never upscale.
- Dev.9-dev.12 proved that uniformly synthesized lower-FPS frames can erase the expected byte savings under gifski, so dev.13+ does not synthesize intermediate frames.
- Exact source-frame decimation candidates are measured instead: every 2nd source frame first, then every 3rd frame while effective motion remains above the automatic 8 FPS floor.
- Candidate samples are encoded at the Preserve-motion dimensions and measured by real gifski byte cost.
- The patched-Python 97/99 byte target is used to project how much spatial resolution that measured cost can realistically buy.
- A candidate must predict roughly 8% or greater linear spatial gain before the full adaptive size search runs.
- If a full candidate fit fails the same realized-gain test, Polymorph continues to the next deeper stride rather than immediately returning the baseline.
- If the source frame count is not divisible by the selected stride, only the final GIF delay is shortened to the exact source-frame remainder so the loop keeps its original total duration/angular speed.
- Keeps gifski quality 100, `--extra`, explicit width, infinite repeat, dev.8 smart-fit sizing, and post-encode integrity verification.
- Dev.15 added development diagnostics around the same decisions: Favor-resolution runs emit an adaptive JSON sidecar containing baseline/pass sizes, stride probe sizes, predicted gain, full-fit results/errors, and the final selection/fallback reason.
- Real dev.15 validation confirmed stride 2 can be selected on Viper and on two more complex kitbash/decal-heavy HeroForge spins when measured byte savings support it.

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

- Real Viper source: 2048x2048, 375 frames, 25 FPS, 15.0 s, every source frame 40 ms.
- Simple 25 -> 20 frame selection showed a strong repeating motion-change spike every fourth interval.
- Motion-compensated interpolation removed that periodic cadence spike in a 512px diagnostic, but dev.9-dev.12 synthetic-frame approaches did not buy spatial resolution on the real workload.
- Dev.13 switched to original-source-frame decimation. For Viper stride 2 retains 188 original frames with 187 x 80 ms intervals plus one 40 ms loop closure.
- Earlier dev.13-era user tests that appeared to show Favor resolution falling back to the Preserve-motion baseline are no longer reliable evidence of an adaptive failure because the then-current radio-button styling made the checked state visually ambiguous; at least one later dev.15 run intended as Favor resolution was proven from the UI screenshot to still have Preserve motion selected.
- Dev.15 diagnostics removed that ambiguity. A confirmed Viper Favor-resolution run selected stride 2 and returned the full native `2048x2048`, 188 frames, exactly 15.0 s, ~12.53 effective FPS, and 82,147,387 bytes. The user reported the motion/frame rate looked consistent.
- Viper's measured stride-2 sample at the Preserve baseline dimensions was 51,558,287 bytes versus the 93,630,962-byte full-frame baseline, enough to recover the entire native 2048px spatial ceiling.
- A harder 2048px kitbash/decal-heavy variant with 500 frames / 20 s selected stride 2 and produced `1810x1810`, 250 frames at exactly 80 ms each, ~97.22 MB.
- A 3072px variant of the same complex scene also selected stride 2 and produced `1752x1752`, 250 frames at exactly 80 ms each, ~94.69 MB.
- Those two 500-frame sources divide evenly by stride 2, so no shortened final closure delay is required; their frame cadence is exactly uniform.
- The real HeroForge validation set therefore covers Viper plus two high-detail kitbash/decal-heavy variants and supports keeping the current adaptive selection policy unchanged.

## Framing behavior

- Original preserves the source framing.
- Crop trims to the selected aspect ratio without distortion; the preview and encoder now share the exact same geometry resolver.
- Crop supports drag repositioning and a 100-300% zoom control. Zoom reduces the retained source crop window rather than upscaling output content, preserving the no-upscale rule.
- Fit preserves the complete source aspect ratio and expands the canvas with user-selectable padding color; drag repositioning moves the source within available padding.
- Dev.16 replaces the preview's separate Crop/Fit geometry implementation with the same `native_geometry` rules used by FFmpeg filter construction so the preview cannot silently stretch while export uses different math.

## v1 UI scope

- Drag/drop and Add Files.
- Multiple-file queue; one active conversion at a time.
- Animated live preview as visual centerpiece.
- Output: GIF / MP4.
- Sizing: Fit under file size / Set resolution.
- GIF priority in file-size GIF mode: Preserve motion / Favor resolution.
- Framing: Original / Crop / Fit.
- Ratio presets plus expandable aspect-ratio guide.
- Crop repositioning via preview drag plus crop zoom.
- Fit background color and source positioning.
- Output folder chooser; default Downloads.
- Conversion progress percentage.
- Development adaptive completion readout reports dimensions, decimal MB, actual effective FPS, and the generated diagnostic sidecar filename for Favor-resolution traces.
- Footer icon buttons: Check Updates, GitHub, Ko-fi, Patreon, Discord.
- Automatic update check while app is open; no service/daemon.
- Dev.14 first-launch sizing/tooltips were human-validated.
- Dev.16 explicitly styles checked radio indicators so selection state is no longer visually ambiguous.

## Windows subprocess behavior

- FFmpeg and gifski encoding subprocesses already use `CREATE_NO_WINDOW` on Windows.
- Dev.16 applies the same flag to ffprobe, eliminating the remaining console flashes when loading media and during post-encode integrity probes.

## Update policy

- Check only official GitHub releases from `Knight-Witch/Polymorph`.
- Require exact versioned installer plus matching `.sha256` companion.
- Download only official repository HTTPS release assets.
- Verify SHA-256 before launching installer.
- No background service, startup daemon, unattended updater, or silent install.

## Known follow-ups

- Human-test dev.16 Crop and Fit preview/export parity, including drag positioning and crop zoom, before treating framing as fully validated.
- Confirm ffprobe no longer flashes a console window in the packaged Windows build.
- Favor resolution performs extra measurement encodes by design; conversion-time optimization can now be investigated because behavior is validated, but it must not change selected outputs.
- Final aesthetic skin, arcane progress treatment, and application emblem remain separate from functional framing work.
- First public release still requires a deliberate project-license choice and final release packaging/release-workflow review.

## Deferred

- User-configurable advanced FPS floor/target controls.
- ETA/time remaining.
- Advanced codec controls.
- Parallel jobs.
- Final aesthetic skin and final Polymorph emblem.
- macOS/Linux packaging.
