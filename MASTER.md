# Polymorph Master

## Current state

- Project: Polymorph
- Repository: `Knight-Witch/Polymorph`
- Platform target: Windows 10/11 x64
- Status: functional scaffold on `dev`; MP4 human-validated; Preserve-motion GIF quality/smoothness human-validated; decimal-MB ceiling validated; updater hardening validated; dev.9 full-resolution interpolation visually validated; dev.10-dev.13 adaptive tests all returned the Preserve-motion Viper baseline; dev.14 first-launch layout/tooltips human-validated; dev.15 adds adaptive decision tracing + a real process-level adaptive integration gate without changing conversion decisions / no public release
- Current development version: `0.1.0-dev.15`

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
- Dev.9-dev.12 proved that uniformly synthesized lower-FPS frames can erase the expected byte savings under gifski, so dev.13 does not synthesize intermediate frames.
- Dev.13 measures exact source-frame decimation candidates instead: every 2nd source frame first, then every 3rd frame while the effective motion remains above the automatic 8 FPS floor.
- Candidate samples are encoded at the Preserve-motion dimensions and measured by real gifski byte cost.
- The patched-Python 97/99 byte target is used to project how much spatial resolution that measured cost can realistically buy.
- A candidate must predict roughly 8% or greater linear spatial gain before the full adaptive size search runs.
- If a full candidate fit fails the same realized-gain test, Polymorph continues to the next deeper stride rather than immediately returning the baseline.
- If the source frame count is not divisible by the selected stride, only the final GIF delay is shortened to the exact source-frame remainder so the loop keeps its original total duration/angular speed.
- Keeps gifski quality 100, `--extra`, explicit width, infinite repeat, dev.8 smart-fit sizing, and post-encode integrity verification.
- Dev.14 changes only presentation/hover help.
- Dev.15 changes only development diagnostics around the same decisions: Favor-resolution runs emit an adaptive JSON sidecar containing baseline/pass sizes, stride probe sizes, predicted gain, full-fit results/errors, and the final selection/fallback reason.

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
- Motion-compensated interpolation removed that periodic cadence spike in a 512px diagnostic.
- Dev.9 full-resolution 20 FPS motion interpolation was reported by the user as looking **really good**, but still produced `1552x1552`, i.e. no spatial gain.
- Dev.10 changed selection to measured candidate cost and final actual-gain veto; Viper returned `1552x1552 • 93.6 MB • 25 FPS`.
- Dev.11 extended optical-flow probing through 12.5 FPS; Viper again returned the identical 25 FPS baseline.
- Dev.12 replaced optical flow with lower-complexity temporal blending; Viper again returned the exact same output. The dev.11 and dev.12 user-supplied GIFs are byte-for-byte identical: 93,630,962 bytes, SHA-256 `dbfd1be7211b801f3a3a8d0ffaaf1058a1974f6b27141ef5f3be5ce55452e5af`, 375 frames at 40 ms.
- Dev.13 switched to original-source-frame decimation. For Viper stride 2 would retain 188 original frames with 187 x 80 ms intervals plus one 40 ms loop closure.
- The user-supplied dev.13 output nevertheless returned the **exact same Preserve-motion file** again: 1552x1552, 93,630,962 bytes, 375 frames at 40 ms, SHA-256 `dbfd1be7211b801f3a3a8d0ffaaf1058a1974f6b27141ef5f3be5ce55452e5af`.
- Therefore dev.13 did not select a source-decimated candidate. The final file alone cannot distinguish whether stride probes were rejected by measured byte economics, a full-fit result missed the 8% gain floor, or the real Viper path hit an adaptive encode/integrity error that was intentionally caught before fallback.
- Dev.15 addresses that diagnostic gap rather than changing the algorithm again. It records each real encode attempt/rejection and adds a synthetic real-toolchain integration gate that must prove the adaptive orchestration can select a lower-frame result when the byte savings genuinely support it.

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
- Development adaptive completion readout reports dimensions, decimal MB, actual effective FPS, and—only for dev.15 Favor-resolution diagnostics—the generated sidecar filename.
- Footer icon buttons: Check Updates, GitHub, Ko-fi, Patreon, Discord.
- Automatic update check while app is open; no service/daemon.
- Dev.14 first-launch geometry is 1080x800 with a 900x700 minimum so the GIF-priority section no longer crushes the settings rail at the old 720px default height.
- Dev.14 enforces minimum visual heights for sections/radio/input controls and adds concise hover tooltips to primary controls while preserving the existing restrained UI.
- Human validation confirmed the dev.14 default sizing renders correctly and the new hover tooltips work as intended.

## Update policy

- Check only official GitHub releases from `Knight-Witch/Polymorph`.
- Require exact versioned installer plus matching `.sha256` companion.
- Download only official repository HTTPS release assets.
- Verify SHA-256 before launching installer.
- No background service, startup daemon, unattended updater, or silent install.

## Known follow-ups

- Run the real Viper once through dev.15 Favor resolution and inspect the generated `*_ADAPTIVE_DIAGNOSTIC.json`; do not change adaptive thresholds/timing again until that trace identifies the concrete rejection/error stage.
- Require the dev.15 Windows process-level adaptive integration gate to select a lower-frame, >=8%-larger result on its deterministic synthetic workload before handing out the tester.
- If the Viper trace shows the measured stride itself does not buy >=8% spatial gain, treat that as a real GIF-compression limitation rather than a control-flow bug and reconsider the product tradeoff deliberately.
- If the trace shows an adaptive encode/integrity failure, fix only that concrete failure and retain the existing measured-gain safeguards.
- If adaptive behavior is eventually validated, test at least one harder HeroForge spin with thin geometry/hair/transparent or overlapping elements before stable promotion.
- Favor resolution performs extra measurement encodes by design; optimize conversion time only after cadence/result behavior is validated.
- First public release still requires a deliberate project-license choice and final release packaging/release-workflow review.

## Deferred

- User-configurable advanced FPS floor/target controls.
- ETA/time remaining.
- Advanced codec controls.
- Parallel jobs.
- Final aesthetic skin and final Polymorph emblem.
- macOS/Linux packaging.
