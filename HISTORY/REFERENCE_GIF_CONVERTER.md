# Canonical GIF Converter Reference

## Canonical source

The only behavioral reference for the known-good OG result is the user-tested patched Python file `HeroForge_WebP_to_Reddit_GIF.py`.

A separate Discord distribution package was created later, but the user has not run or validated that package. It must not be used as evidence for the OG result or for production parity decisions.

## Exact behavior in the patched Python reference

- FFmpeg streams YUV4MPEG directly to gifski; no PNG frame folder.
- FFmpeg performs Lanczos scaling.
- FFmpeg uses `-r <source fps>` before Y4M output.
- The Python reference does not specify `-pix_fmt`.
- gifski quality `100`.
- gifski `--extra` enabled.
- GIF repeat `0` / infinite loop.
- gifski receives explicit `--width <FFmpeg output width>`.
- The Python reference does not pass gifski `--fps`.
- File-size fitting changes spatial resolution rather than encoder quality.
- Fixed reference constants: `LIMIT_BYTES = 99_000_000`, `TARGET_BYTES = 97_000_000`, `ACCEPT_LOW_BYTES = 93_000_000`, `MAX_ATTEMPTS = 6`, `MIN_LONG_EDGE = 128`.
- Smart-fit search uses measured byte size, square-root area prediction, 0.985 safety factor, a forced 4% downward move after failure, midpoint reclamation between passing/failing scales, and stops when a passing result reaches at least 93,000,000 bytes.

## Timing divergence — directly measured

Windows CI run #14 (`34467182268`) reproduced the patched Python timing shape against an otherwise matched full-frame path using gifski 1.32.0.

At yuv420p:

- Source: 50 frames, 25 FPS, 2.0 s.
- Patched-Python timing: 41 frames, 2.0 s, 932,849 bytes.
- Full-frame explicit 25 FPS: 50 frames, 2.0 s, 1,135,021 bytes.
- Frame ratio: 82%.
- Byte ratio: 82.1878%.
- Linear-resolution factor from byte ratio: 1.10305x.
- Comparable human full-frame result: 1592px.
- `1592 * 1.10305 = 1756.06`.
- Known OG result: 1756px.

The measured timing effect predicts the OG spatial-resolution advantage essentially exactly. The same frame/byte behavior reproduced under yuv444p, so this timing conclusion does not depend on the unresolved automatic pixel-format behavior of the patched Python command on different FFmpeg builds.

Durable measurements are recorded in `HISTORY/DIAGNOSTICS/GIF_REFERENCE_TIMING_2026-09-10.md`.

## Real-source confirmation

The user later supplied the actual Viper source WebP plus the OG output GIF. Direct inspection confirmed:

- source WebP: 2048x2048, 375 frames, every frame 40 ms, exactly 25 FPS, 15.0 s;
- OG GIF: 1756x1756, 300 frames, approximately the same 15.0 s duration;
- frame retention: exactly 80%;
- effective OG cadence: exactly 20 FPS.

The OG GIF frame-delay pattern contains 40 ms intervals with periodic 80 ms gaps, matching the subtle micro-skip pattern expected from frame removal rather than evenly spaced synthesized 20 FPS motion. This independently confirms the CI timing diagnosis on the real workload.

## Human validation history

### First Polymorph tester

- MP4: visually excellent; no issue reported.
- Initial GIF: blurrier/grainier and much smaller because Polymorph omitted gifski explicit width.

### Width-corrected GIF

- Quality reported fantastic and visually identical to OG, possibly slightly smoother.
- Polymorph: 1570x1570; OG: 1756x1756.

### yuv420p retest

- Smoothness remained good.
- Result moved to 1592x1592 under the earlier binary-MiB ceiling implementation.
- Color difference remained too subtle to judge confidently.

### gifski 1.34.0 retest

- Changed only gifski 1.32.0 -> 1.34.0.
- Same Viper conversion regressed to 1532x1532.
- 1.32.0 was restored.

### Decimal-MB retest

- After correcting displayed 99 MB to exactly 99,000,000 bytes, same Viper conversion produced 1552x1552.
- Quality/smoothness otherwise remained good.

### Patched-Python optimizer parity retest

- Dev.8 ported the patched Python smart-fit resolution search while preserving every source frame.
- The same Viper conversion remained 1552x1552.
- Conclusion: the current full-frame result is byte-limited by retaining 375 frames, not materially limited by the optimizer search.

## Adaptive resolution-favoring history

- Preserve motion remains the default and continues to retain every source frame.
- Dev.9 introduced explicit Favor resolution and used motion interpolation to synthesize even 20 FPS motion. The user reported the motion looked really good, but the output remained 1552x1552.
- Dev.10 made actual gifski sample cost authoritative and fell back to the 25 FPS baseline when lower synthetic cadences could not buy the required spatial gain.
- Dev.11 extended optical-flow candidates through 12.5 FPS; the result remained the exact 25 FPS baseline.
- Dev.12 replaced optical-flow synthesis with temporal blending; the dev.11 and dev.12 user outputs were byte-for-byte identical 25 FPS baselines, proving the candidate path was again discarded.
- Synthetic intermediate frames therefore do not currently provide a useful compression/resolution trade on Viper.

## Dev.13 exact-decimation boundary

Dev.13 changes only the experimental Favor-resolution strategy. It no longer creates synthetic frames.

- Candidate plans retain every Nth original source frame.
- Real gifski sample cost remains authoritative.
- The patched-Python spatial smart-fit search, quality 100, `--extra`, explicit width, yuv420p handoff, and 99 MB ceiling remain unchanged.
- For a constant-speed turntable, integer-stride source-frame retention keeps every retained image on a real source angle.
- When source frame count is not divisible by the stride, the last loop interval spans fewer source-angle steps than the ordinary interval. Dev.13 compensates by losslessly shortening only the final GIF delay so angular speed and total loop duration remain exact.
- Viper stride 2 therefore retains 188 original frames: 187 intervals at 80 ms plus one 40 ms closure interval, totaling exactly 15.0 s.
- The output's average displayed FPS is `188 / 15 = 12.5333`, but there is no periodic 1/2-frame-step deletion cadence and no blended/warped image synthesis.

## Current boundary

- Preserve motion must not reproduce OG frame resampling silently.
- OG 1756px is not a valid full-frame 99 MB parity target.
- Favor resolution may reduce retained frames only because the user explicitly selected that tradeoff.
- The experimental mode must not use the OG's periodic uneven frame-loss cadence.
- Dev.13's exact source-frame decimation + loop-delay correction requires human validation before it can be considered stable.
- Any future advanced FPS control remains deferred until the adaptive automatic mode is validated.
