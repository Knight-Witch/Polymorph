# GIF Adaptive Motion Diagnostic — 2026-09-10

## Purpose

Evaluate whether a lower-FPS GIF mode can preserve uniform turntable motion instead of reproducing the patched standalone converter's periodic frame-loss cadence.

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

Contact-sheet checks at front, side, back, cape/hair, sword and return-to-front positions did not show obvious interpolation corruption at 512px diagnostic scale. Full-resolution human validation is still required before the adaptive mode is considered release-ready.

## Endpoint handling

A bare `minterpolate=fps=20` ended one frame early on this source. The reliable pipeline is:

1. clone/pad the last source frame to give `minterpolate` lookahead;
2. interpolate at the selected uniform FPS;
3. trim to the mathematically expected frame count;
4. reset timestamps.

For the Viper source this produces exactly 300 evenly spaced frames.

## Adaptive planning decision

Development mode uses a soft spatial target rather than blindly chasing source-native resolution:

- preferred long edge: native size capped at 2048 px;
- automatic FPS floor: 20 FPS;
- lower-FPS candidates must use uniform GIF centisecond delays (`100 / N` FPS);
- require about 8% predicted linear-resolution improvement before sacrificing FPS;
- choose the highest uniform FPS that reaches at least 95% of the soft spatial target;
- if no eligible rate reaches the target, choose the lowest permitted viable rate to maximize the requested resolution bias;
- never upscale beyond native source geometry.

For the real Viper workload, a 1552px full-frame result at 25 FPS predicts a useful gain at uniform 20 FPS, so the adaptive planner selects 20 FPS.

## Release boundary

- Preserve motion remains the default and keeps the proven full-frame path unchanged.
- Favor resolution is experimental in dev.9.
- No automatic mode may use uneven frame deletion.
- Full-resolution Viper testing is required before promotion to stable.
