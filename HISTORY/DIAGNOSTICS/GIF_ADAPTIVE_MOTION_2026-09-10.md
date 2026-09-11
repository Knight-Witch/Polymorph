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
2. FFmpeg motion interpolation using:
   - `minterpolate=fps=20`
   - `mi_mode=mci`
   - `mc_mode=aobmc`
   - `me_mode=bidir`
   - `vsbmc=1`
   - cloned end padding for interpolation lookahead
   - exact output-frame trimming.

Both paths targeted 300 frames for the same 15-second spin.

## Cadence measurement

Per-frame grayscale absolute-difference energy was measured after downscaling the diagnostic outputs to 256x256.

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

## Visual spot check

Contact-sheet checks at front, side, back, cape/hair, sword and return-to-front positions did not show obvious interpolation corruption at 512px diagnostic scale.

## Endpoint handling

A bare `minterpolate=fps=20` ended one frame early on this source. The reliable pipeline is:

1. clone/pad the last source frame to give `minterpolate` lookahead;
2. interpolate at the selected uniform FPS;
3. trim to the mathematically expected frame count;
4. reset timestamps.

For the Viper source this produces exactly 300 evenly spaced frames at 20 FPS.

## Dev.9 full-resolution human validation

The user tested the real Viper source through dev.9 with `Favor resolution` selected.

- Motion/interpolation quality: reported as **really good** at full output resolution.
- Final dimensions: `1552x1552`, unchanged from Preserve motion.
- Reported completion size: `89.2 MB` in the dev.9 UI.
- The dev.9 completion readout still divided bytes by 1024^2 while labeling the value `MB`; therefore 89.2 displayed units correspond to roughly 93.5 decimal MB, immediately above the GIF optimizer's 93,000,000-byte acceptance floor.

### Diagnosis

The dev.9 planner assumed that reducing 25 FPS to 20 FPS would lower encoded cost roughly in proportion to frame count. That assumption was valid for the OG converter's simple frame resampling, but it is not valid for motion-interpolated frames: synthesized frames can be materially more expensive for gifski to palette/encode than untouched source frames.

As a result, dev.9 made a temporal sacrifice without earning a measurable spatial gain on Viper. The interpolation method itself passed the visual test; the planning heuristic did not.

## Dev.10 measured-planning validation

Dev.10 changed Favor resolution so real encoded sample cost, not frame-count math, decides whether a lower clean cadence is worth keeping. For a 25 FPS source it measured 20 FPS / 50 ms first and then 16.67 FPS / 60 ms.

The user retested the same Viper source and the final completion line was:

- `1552x1552`
- `93.6 MB` decimal
- `25 FPS`

This is the intended Preserve-motion fallback. Neither 20 FPS nor 16.67 FPS demonstrated enough measured byte savings to justify at least about 8% linear spatial gain, so Polymorph kept the original frame rate instead of sacrificing motion for no meaningful resolution benefit.

This validates the dev.10 guard behavior on the Viper workload: the adaptive mode no longer lowers FPS simply because the user selected Favor resolution.

## Dev.11 deeper clean-cadence search

The Viper result also proves that the dev.10 automatic floor was too shallow to answer the user's full Favor-resolution request. Dev.11 keeps the same measured-cost authority and final actual-gain veto, but extends the clean uniform cadence ladder before giving up.

For a 25 FPS source the candidates are now tried in this order:

- 20 FPS / 50 ms;
- 16.67 FPS / 60 ms;
- 14.29 FPS / 70 ms;
- 12.5 FPS / 80 ms.

The first/highest cadence whose real encoded sample predicts at least about 8% linear spatial gain is selected for the full adaptive size fit. If none earns the gain, the 25 FPS Preserve-motion output remains final. This preserves the user's stated priority: stay as close to source FPS as possible, move lower only when the measured spatial reward is actually worthwhile, and keep all reduced-FPS output on an even GIF cadence.

## Release boundary

- Preserve motion remains the default and keeps the proven full-frame path unchanged.
- Favor resolution remains experimental.
- No automatic mode may use uneven frame deletion.
- Full-resolution 20 FPS interpolation quality is human-validated on Viper.
- Dev.10's no-benefit fallback is human-validated on Viper.
- Dev.11 requires human validation only if it actually selects 14.29 FPS or 12.5 FPS; if it again returns 25 FPS, that confirms this interpolation strategy cannot buy a worthwhile spatial increase for this workload under the current 99 MB / quality-100 constraints.
