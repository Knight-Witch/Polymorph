# GIF Adaptive Validation — 2026-09-12

## Purpose

Close the dev.15 Favor-resolution diagnostic question with real Windows/HeroForge evidence and correct the interpretation of the earlier Preserve-baseline outputs.

## Radio-state discovery

The dev.15 diagnostic wrapper was designed to write a JSON sidecar after every successful GIF + Fit-under-file-size + Favor-resolution conversion, even if the adaptive converter eventually returned the Preserve baseline.

The first user run produced the familiar 1552x1552 / 375-frame Viper output but no diagnostic JSON. A screenshot of the completed dev.15 UI revealed why: the stylesheet did not explicitly draw a checked radio indicator. The selected radio could appear with no circle while the unselected radio showed a hollow circle. The user believed Favor resolution was selected, but the actual UI state in the screenshot was Preserve motion.

Therefore the earlier dev.13/dev.15 files that matched the Preserve baseline remain valid measurements of those files, but they are not reliable evidence that the Favor-resolution branch actually executed. The previous diagnostic hypothesis that source-frame decimation must have been rejected is superseded by the confirmed UI-state ambiguity.

Dev.16 fixes the radio presentation so selected state is explicit and visible.

## Confirmed Viper Favor-resolution run

Source:

- 2048x2048
- 375 frames
- 25 FPS
- 15.0 seconds
- 40 ms source-frame duration

Measured Preserve baseline:

- 1552x1552
- 93,630,962 bytes
- 375 frames

Stride-2 sample encoded at the same 1552x1552 baseline dimensions:

- 51,558,287 bytes

The measured savings passed the existing 8% predicted-gain gate and the full adaptive fit selected stride 2.

Final Favor-resolution result:

- 2048x2048
- 82,147,387 bytes
- 188 retained original source frames
- exactly 15.0 seconds
- effective average rate 188 / 15 = 12.5333 FPS
- 187 frame delays at 80 ms plus one 40 ms final loop-closure delay

The user watched the result and reported the frame rate/motion looked consistent. The selected mode therefore recovered the full native 2048 spatial result from a 1552 Preserve baseline while retaining deterministic original source frames and exact loop duration.

## Harder kitbash/decal regression workloads

Two variants of a more complex HeroForge capture were then tested. The scene contains many kitbash parts and decals. One source is 2K-class and the second is a 3K capture.

### 2048 source variant

Source:

- 2048x2048
- 500 frames
- 25 FPS
- 20.0 seconds

Preserve baseline:

- 1312 px long edge
- 95,925,855 bytes

Stride-2 sample:

- 53,423,709 bytes

Favor result:

- 1810x1810
- 97,223,964 bytes
- 250 frames
- 12.5 FPS
- realized linear gain ~37.96%
- every GIF frame delay exactly 80 ms

### 3072 source variant

Source:

- 3072x3072
- 500 frames
- 25 FPS
- 20.0 seconds

Preserve baseline:

- 1266 px long edge
- 95,361,393 bytes

Stride-2 sample:

- 52,696,591 bytes

Favor result:

- 1752x1752
- 94,690,307 bytes
- 250 frames
- 12.5 FPS
- realized linear gain ~38.39%
- every GIF frame delay exactly 80 ms

The user reported the frames looked even. Because 500 divides exactly by stride 2, these loops do not require a shortened final closure delay.

## Conclusion

The current dev.13+ source-frame-decimation architecture is validated on three real workloads with different spatial/detail characteristics. Stride 2 produced large spatial gains and acceptable/even perceived motion in each confirmed Favor-resolution test. The adaptive algorithm should not be changed further without new contrary evidence.

The next work is product cleanup rather than adaptive-policy experimentation: framing/preview correctness, invisible-radio styling, focus-stealing child-process suppression, final visual skin, and later conversion-time optimization.
