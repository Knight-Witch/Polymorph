# Polymorph Master

## Current state

- Project: Polymorph
- Repository: `Knight-Witch/Polymorph`
- Platform target: Windows 10/11 x64
- Current development version: `0.1.0-dev.16`
- No public stable release yet.
- MP4 is human-validated and remains unchanged.
- Preserve-motion GIF quality/smoothness, decimal-MB sizing, pinned gifski 1.32.0, updater hardening, first-launch geometry, and hover help are human-validated.
- Favor-resolution source-frame decimation is now validated on three real HeroForge workloads: Viper plus two kitbash/decal-heavy 500-frame variants including a 3072x3072 source. All selected stride 2 and produced substantial spatial gains with visually even/acceptable motion.
- Dev.16 addresses framing/preview correctness and Windows process focus-stealing before final visual skinning: hidden ffprobe execution, shared aspect-safe Crop/Fit placement, drag + zoom framing controls, and explicit selected radio indicators.

## Canonical conversion behavior

### GIF — Preserve motion

- Default mode.
- Input focus: animated WebP.
- FFmpeg -> YUV4MPEG -> gifski 1.32.0.
- gifski quality 100, `--extra`, explicit width, infinite repeat.
- Explicit `yuv420p` on the pinned FFmpeg 9.0.1 toolchain.
- Explicit source FPS to gifski with exact frame-count/timing verification.
- File-size mode changes spatial resolution, never hidden temporal quality.
- 99 MB means exactly 99,000,000 bytes.
- GIF file-size fitting uses the patched-Python smart-fit search introduced in dev.8.

### GIF — Favor resolution

- Explicit opt-in, available only for GIF + Fit under file size.
- Starts from the Preserve-motion fitted result.
- Tests exact original-source-frame strides nearest motion first: stride 2, then stride 3 while effective motion remains above the automatic 8 FPS floor.
- No optical-flow or blended synthetic frames are used in dev.13+.
- Real gifski sample byte cost at Preserve dimensions is authoritative.
- A candidate must predict about 8% linear spatial gain before a full fit and must realize about 8% after the fit.
- Preferred adaptive long edge remains native framed size capped at 2048 px; never source-upscale.
- If source frame count is not divisible by the stride, only the final GIF delay is shortened to preserve exact source duration/angular speed.
- Preserve quality 100, `--extra`, explicit width, infinite repeat, dev.8 smart-fit sizing, and post-encode integrity verification.
- Dev.15 diagnostics remain development instrumentation and write an adaptive JSON sidecar for Favor-resolution jobs.

### Confirmed real adaptive results

- Viper source: 2048x2048, 375 frames, 25 FPS, 15.0 s.
  - Preserve baseline: 1552x1552, 93,630,962 bytes, 375 frames.
  - Stride-2 sample at baseline dimensions: 51,558,287 bytes.
  - Favor result: 2048x2048, 82,147,387 bytes, 188 frames, 15.0 s, ~12.53 effective FPS.
  - Timing: 187 x 80 ms plus one 40 ms closure interval.
  - Human validation: frame rate/motion looked consistent.
- Kitbash/decal-heavy 2048 source: 500 frames / 20 s.
  - Preserve baseline edge 1312 px, 95,925,855 bytes.
  - Favor stride-2 result: 1810x1810, 97,223,964 bytes, 250 frames / 12.5 FPS.
  - Realized linear gain ~37.96%; every output frame is exactly 80 ms.
- Kitbash/decal-heavy 3072 source: 500 frames / 20 s.
  - Preserve baseline edge 1266 px, 95,361,393 bytes.
  - Favor stride-2 result: 1752x1752, 94,690,307 bytes, 250 frames / 12.5 FPS.
  - Realized linear gain ~38.39%; every output frame is exactly 80 ms.

### Correction to earlier adaptive interpretation

- The historical dev.13/dev.15 files that matched the Preserve baseline remain valid measurements of those output files, but they are no longer reliable proof that Favor resolution actually executed.
- The UI stylesheet did not provide an explicit checked-radio indicator: the selected option could appear to have no circle while the unselected option showed a hollow circle. A dev.15 screenshot proved the user believed Favor resolution was selected while the UI state was actually Preserve motion.
- The first diagnostic run with Favor resolution unambiguously active selected stride 2 successfully on Viper. The adaptive algorithm itself therefore does not require another policy change based on the earlier fallback interpretation.

### MP4

- H.264 / libx264, preset slow, CRF 16, yuv420p, +faststart.
- Source timing/frame sequence preserved.
- File-size search remains the separately human-validated implementation.
- Treat as done unless a real regression appears.

## Framing behavior — dev.16

- Original: source framing unchanged.
- Crop: target canvas is filled by an aspect-preserving source placement; overflow is clipped, never stretched.
- Fit: target canvas keeps the source aspect and pads uncovered area with the selected background color, never stretches the source.
- Preview and encode now use the same shared aspect-preserving placement model rather than separate Crop/Fit calculations.
- Crop/Fit support drag positioning and 100%-400% manual zoom. Mouse wheel over the preview also changes zoom.
- Manual zoom changes composition inside the framing canvas; it does not raise the native output-resolution ceiling or bypass no-upscale sizing rules.
- Center resets position but intentionally keeps the chosen zoom.

## Windows subprocess behavior — dev.16

- FFmpeg/gifski conversion processes already used `CREATE_NO_WINDOW`.
- The remaining focus-stealing console flashes were traced to ffprobe, which runs when media is loaded and during post-encode integrity checks.
- Dev.16 applies `CREATE_NO_WINDOW` to the shared ffprobe subprocess path as well.

## UI state

- Development window opens around 1080x800; minimum 900x700.
- Primary controls have concise hover tooltips.
- Dev.16 explicitly styles selected and unselected radio indicators so checked state is visually unambiguous.
- Final aesthetic skin, final Polymorph emblem, and final arcane progress treatment remain deferred until behavior is stable.

## Update policy

- Check only official GitHub releases from `Knight-Witch/Polymorph`.
- Require exact versioned installer plus matching `.sha256` companion.
- Download only official repository HTTPS release assets and verify SHA-256 before launch.
- No background service, startup daemon, unattended updater, telemetry, or cloud processing.

## Known follow-ups

- Windows CI must validate dev.16 unit tests, real bundled toolchain, adaptive integration, frozen-app framing/zoom smoke, packaging, and installer before human testing.
- Human dev.16 validation should confirm: no console flash on load/encode/optimize; checked radios are obvious; Crop actually crops without distortion; Fit pads without distortion; drag/zoom preview behavior matches encoded output.
- Favor-resolution performance optimization may be considered later; correctness is now established.
- First public release still requires final app icon/emblem, deliberate project-license choice, stable packaging/release workflow review, code-signing/SmartScreen decision, and release-facing README polish.

## Deferred

- User-configurable advanced FPS floor/target controls.
- ETA/time remaining.
- Advanced codec controls.
- Parallel jobs.
- Custom aspect-ratio workflow polish.
- Final aesthetic skin / emblem / arcane progress treatment.
- macOS/Linux packaging.
