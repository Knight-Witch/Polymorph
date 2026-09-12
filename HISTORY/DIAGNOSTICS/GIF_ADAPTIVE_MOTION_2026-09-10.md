# GIF Adaptive Motion Diagnostic — 2026-09-10

## Purpose

Evaluate whether a lower-FPS GIF mode can preserve uniform turntable motion instead of reproducing the patched standalone converter's periodic frame-loss cadence, and whether that temporal trade actually buys meaningful spatial resolution under the 99 MB ceiling.

## Source

- Real user-supplied Viper HeroForge animated WebP.
- Native source: 2048x2048.
- 375 frames.
- 25 FPS.
- 15.0 seconds.
- Every source frame is 40 ms.

## Local motion probe

The source was decoded with Pillow and downsampled to a lossless 512x512 / 25 FPS diagnostic stream. Two 20 FPS conversions were compared:

1. Ordinary `fps=20` frame selection.
2. FFmpeg motion interpolation using `minterpolate=fps=20` with motion compensation, cloned end padding, and exact frame trimming.

Both paths targeted 300 frames for the same 15-second spin.

## Cadence measurement

### Ordinary 20 FPS frame selection

- Mean adjacent-frame difference: 0.8070.
- Standard deviation: 0.2877.
- Coefficient of variation: 0.3566.
- Difference energy by repeating four-interval phase: `[0.6891, 1.1577, 0.6898, 0.6899]`.

This shows a strong periodic motion jump: one interval in every four carries substantially more visual change than its neighbors.

### Motion-interpolated 20 FPS

- Mean adjacent-frame difference: 0.7825.
- Standard deviation: 0.1906.
- Coefficient of variation: 0.2436.
- Difference energy by repeating four-interval phase: `[0.7742, 0.7898, 0.7902, 0.7755]`.

The periodic spike is removed. Motion change is distributed evenly across the 20 FPS cadence.

## Dev.9 full-resolution human validation

The user tested the real Viper source through dev.9 with `Favor resolution` selected.

- Motion/interpolation quality: reported as **really good** at full output resolution.
- Final dimensions: `1552x1552`, unchanged from Preserve motion.
- Reported completion size: `89.2 MB` in the dev.9 UI.
- The dev.9 completion readout still divided bytes by 1024^2 while labeling the value `MB`; therefore 89.2 displayed units correspond to roughly 93.5 decimal MB.

Diagnosis: synthesized motion-interpolated frames are materially more expensive for gifski than the naive frame-count ratio predicts. Reducing frame count did not create the expected spatial budget.

## Dev.10 measured-planning validation

Dev.10 made real encoded sample cost authoritative and measured 20 FPS then 16.67 FPS before committing to any temporal sacrifice.

The user retested Viper and received:

- `1552x1552`
- `93.6 MB` decimal
- `25 FPS`

The fallback worked: no lower cadence was kept without a measured spatial payoff.

## Dev.11 deeper clean-cadence validation

Dev.11 extended optical-flow probing through 14.29 FPS and 12.5 FPS. The user again received:

- `1552x1552`
- `93.6 MB`
- `25 FPS`

The supplied GIF verifies 1552x1552, 375 frames, every frame 40 ms, 15.0 s total, 93,630,962 bytes.

## Dev.12 temporal-blend validation

Dev.12 replaced optical-flow synthesis with exact-timestamp linear temporal blending while keeping the same measured-cost gate and fallback logic.

The user again received:

- `1552x1552`
- `93.6 MB`
- `25 FPS`

The dev.11 and dev.12 user-supplied outputs are byte-for-byte identical:

- bytes: `93,630,962`;
- SHA-256: `dbfd1be7211b801f3a3a8d0ffaaf1058a1974f6b27141ef5f3be5ce55452e5af`;
- 375 frames;
- every frame 40 ms;
- 15.0 s total.

This is the concrete reason the repeated tests looked unchanged: the adaptive candidate was discarded and Polymorph copied the exact Preserve-motion baseline back out.

Two conclusions follow:

1. Synthetic even-timestamp frames do not create enough gifski savings on Viper to justify the desired spatial trade.
2. The dev.10-dev.12 control flow could also stop after a higher candidate passed the prediction gate but failed the final realized-gain veto, without continuing to deeper candidates. Dev.13 corrects that orchestration bug as part of the next isolated strategy.

## Dev.13 exact source-frame decimation

Dev.13 stops synthesizing intermediate frames entirely.

The new Favor-resolution strategy:

1. fit the proven 25 FPS Preserve-motion baseline;
2. keep every second original decoded source frame and measure its actual gifski cost at the baseline dimensions;
3. if that measured result predicts at least about 8% linear spatial gain, run the full smart-fit search using the exact stride-2 source frames;
4. if the final stride-2 fit still misses the realized-gain floor, continue to stride 3 rather than immediately returning the baseline;
5. retain quality 100, `--extra`, explicit width, 99 MB ceiling, and the dev.8 smart-fit size search unchanged.

### Why source-frame decimation is different

A 25 -> 20 FPS conversion cannot use only original source frames while also maintaining equal angular steps: 20 FPS requires positions every 1.25 source frames. Some form of synthesis or uneven 1/2-frame stepping is unavoidable.

A fixed integer source-frame stride avoids that problem. For Viper stride 2 retains frames `0, 2, 4, ... 374` — 188 original frames with no optical-flow or blend-generated image data.

Because 375 is odd, the last retained frame is only one source-frame step from the loop start while the ordinary retained-frame spacing is two steps. Dev.13 preserves constant angular speed by using:

- 187 ordinary intervals at 80 ms;
- one final closure interval at 40 ms;
- total duration exactly 15.0 s.

The image sequence therefore uses an even every-other-source-frame sacrifice across the spin, while the single loop-boundary delay reflects the actual smaller remaining source angle instead of forcing a periodic micro-skip or synthetic frame. The final GIF delay is patched losslessly in the Graphic Control Extension after gifski encoding; image data is untouched.

For Viper the resulting effective average rate is `188 / 15 = 12.5333 FPS`. The human test must decide whether that motion trade is acceptable for the spatial gain.

### Dev.13-era Viper result — later caveat

A dev.13-era user-supplied GIF was the exact Preserve-motion baseline:

- dimensions: `1552x1552`;
- bytes: `93,630,962`;
- frames: `375`;
- frame delay: `40 ms` for every frame;
- duration: `15.0 s`;
- SHA-256: `dbfd1be7211b801f3a3a8d0ffaaf1058a1974f6b27141ef5f3be5ce55452e5af`.

At the time, this was interpreted as proof that no source-decimated candidate survived. That conclusion is now weakened by a later UI discovery: the checked radio button had no visible selected mark, making `Preserve motion` and `Favor resolution` visually ambiguous. During dev.15 testing, a run the user believed was Favor resolution was proven from the UI screenshot to still have Preserve motion selected. Therefore the older dev.13 fallback file cannot, by itself, establish that the stride path was actually invoked.

## Dev.15 diagnostic boundary

Dev.15 does **not** change Favor-resolution conversion decisions. It adds two development-only diagnostics:

1. A `DiagnosticAdaptiveConverter` wrapper records every baseline/adaptive encode attempt, dimensions, bytes, stride metadata, predicted linear gain, full-fit result/error, and final selected/fallback result. Each Favor-resolution conversion writes a compact `*_ADAPTIVE_DIAGNOSTIC.json` sidecar beside the GIF.
2. Windows CI runs a deterministic, high-entropy animated-WebP integration workload through the actual `AdaptiveConverter` + pinned FFmpeg/gifski toolchain. The test dynamically chooses a byte cap where Preserve motion must spatially downscale but stride-2 fits cheaply enough to earn at least 8% linear resolution. CI fails unless the real adaptive orchestration actually returns the lower-frame/larger-image result.

The process-level CI integration passed and proved the orchestration can select stride 2 when measured byte economics support it.

## Confirmed real Viper Favor-resolution result

Once the radio selection was explicitly verified, the real Viper dev.15 diagnostic showed the adaptive path working as designed:

- source: `2048x2048`, 375 frames, 25 FPS, 15.0 s;
- Preserve baseline: `1552x1552`, 93,630,962 bytes;
- stride-2 sample at baseline dimensions: 51,558,287 bytes;
- selected result: `2048x2048`, 188 frames, 82,147,387 bytes;
- duration: exactly 15.0 s;
- timing: 187 frames at 80 ms plus one final 40 ms closure frame;
- effective average rate: 12.5333 FPS.

The stride sample's measured savings were large enough to recover the complete native 2048px spatial ceiling. The user visually checked the final GIF and reported that the frame rate/motion looked consistent.

## Harder HeroForge regression variants

Two additional variants of a much more complex HeroForge scene were tested. The scene contains heavy kitbash usage and many decals, providing a stronger spatial-detail/compression workload than Viper.

### 2048px / 500-frame variant

- source: 2048px class, 500 frames, 20.0 s;
- selected stride: 2;
- output: `1810x1810`;
- output frames: 250;
- output size: approximately 97.22 MB decimal;
- timing: every output frame exactly 80 ms.

The Preserve-motion baseline long edge was 1312px, so the selected result recovered about 38% linear resolution.

### 3072px / 500-frame variant

- source: 3072px class, 500 frames, 20.0 s;
- selected stride: 2;
- output: `1752x1752`;
- output frames: 250;
- output size: approximately 94.69 MB decimal;
- timing: every output frame exactly 80 ms.

The Preserve-motion baseline long edge was 1266px, so the selected result recovered about 38.4% linear resolution. Because 500 divides evenly by stride 2, both complex-scene variants need no shortened final closure delay and have perfectly uniform timing.

## Current release boundary

- Preserve motion remains the default and unchanged.
- The synthesized-frame branch from dev.9-dev.12 remains rejected for this workload because it did not buy spatial resolution.
- Exact source-frame decimation is now validated by deterministic CI plus three real HeroForge workloads: Viper and two kitbash/decal-heavy variants.
- Viper recovered the full 2048px native spatial ceiling and was visually reported as having consistent motion.
- Both 500-frame complex variants selected stride 2 and produced uniform 80 ms cadence with substantial (~38%) linear spatial gains over their Preserve baselines.
- The current adaptive thresholds, stride order, and timing policy should not be changed without new contradictory evidence.
- Remaining work is ordinary release hardening, UI/framing validation, and potential conversion-time optimization that preserves identical selection/output behavior.
