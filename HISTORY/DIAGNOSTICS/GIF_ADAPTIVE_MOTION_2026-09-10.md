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

## Dev.10 planning correction

Favor resolution now uses measured encoded cost rather than frame-count math as the authority:

1. produce the normal Preserve-motion fitted GIF;
2. consider lower uniform GIF cadences nearest the source FPS first;
3. encode each candidate once at the Preserve-motion dimensions;
4. measure the actual gifski byte cost of those interpolated frames;
5. project achievable spatial size against the patched-Python 97/99 byte target;
6. accept the first/highest candidate that predicts at least about 8% linear-resolution gain;
7. run the full adaptive size search only for that candidate;
8. discard the reduced-FPS output if the finished result still fails to achieve about 8% actual linear gain.

For a 25 FPS source, the current clean-cadence ladder is:

- 20 FPS / 50 ms;
- 16.67 FPS / 60 ms.

The automatic floor is therefore 16.67 FPS in dev.10. The 20 FPS candidate is still preferred whenever its real encoded byte cost earns the required gain; Polymorph only steps lower when 20 FPS demonstrably does not.

## Release boundary

- Preserve motion remains the default and keeps the proven full-frame path unchanged.
- Favor resolution remains experimental.
- No automatic mode may use uneven frame deletion.
- Full-resolution 20 FPS interpolation quality is human-validated on Viper.
- The next human validation target is dev.10's measured cadence selection, especially whether Viper chooses 16.67 FPS and whether that lower clean cadence remains visually acceptable while finally increasing spatial resolution.
