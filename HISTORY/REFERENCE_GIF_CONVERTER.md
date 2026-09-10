# Canonical GIF Converter Reference

## Source

The validated standalone `HeroForge_WebP_to_Reddit_GIF.py` used immediately before Polymorph is the visual-quality reference for GIF output, but its timing behavior is not fully canonical because it did not preserve the source frame sequence through gifski.

## Proven behavior to preserve

- FFmpeg streams YUV4MPEG directly to gifski; no PNG frame folder.
- gifski quality `100`.
- gifski `--extra` enabled.
- GIF repeat `0` / infinite loop.
- FFmpeg performs Lanczos scaling before gifski.
- gifski is explicitly passed `--width <FFmpeg output width>` so it cannot apply its conservative automatic animation downsize.
- The standalone FFmpeg command did not explicitly set a YUV pixel format. In the validated reference environment this effectively yielded the normal 4:2:0 Y4M handoff. The pinned Polymorph FFmpeg 9.0.1 Windows build uses explicit `yuv420p` because leaving the format unset can retain an RGB intermediate that `yuv4mpegpipe` rejects.
- File-size fitting changes spatial resolution rather than hidden quality settings.
- Fixed 99 MB reference constants were `LIMIT_BYTES = 99_000_000`, `TARGET_BYTES = 97_000_000`, `ACCEPT_LOW_BYTES = 93_000_000`, `MAX_ATTEMPTS = 6`, and `MIN_LONG_EDGE = 128`.

## Standalone timing behavior — important divergence

The standalone pipeline used:

- FFmpeg `-r <source fps>` before `yuv4mpegpipe`.
- gifski with no explicit `--fps` argument.

In gifski, `--fps` defaults to `20` for video/Y4M input. Its Y4M decoder compares source-frame timing with the requested target rate and skips frames as needed. Therefore the standalone converter's larger final spatial resolution was achieved in part because gifski resampled the Y4M animation toward 20 FPS rather than retaining every source frame.

Polymorph intentionally does not reproduce this behavior. It explicitly supplies the source FPS to gifski and verifies output dimensions, exact frame count, and bounded duration drift after encoding. The user reported the Polymorph output as smoother than the standalone result, consistent with this difference.

## Human validation history

### 2026-09-09 — first Polymorph tester

- MP4 output: visually excellent; no issue reported.
- Initial GIF output: visibly blurrier, grainier, and substantially downscaled because Polymorph omitted gifski `--width`.

### 2026-09-10 — width-corrected GIF

- GIF quality: reported fantastic and visually identical to the standalone result, possibly slightly smoother framewise.
- Remaining difference: Polymorph output was `1570x1570`; standalone output was `1756x1756` under the same nominal size target.
- Possible very subtle red/pink color difference was observed but not considered confirmed.

### 2026-09-10 — failed automatic Y4M negotiation probe

- Dev `0.1.0-dev.2` removed the forced pixel format to mimic the standalone command literally.
- Windows CI failed before packaging because FFmpeg 9.0.1 retained a non-Y4M-compatible format after filtering and `yuv4mpegpipe` refused to write its header.
- Dev.3 therefore used explicit `yuv420p`, preserving the intended 4:2:0 handoff while keeping the rest of the validated pipeline unchanged.

### 2026-09-10 — yuv420p human retest

- Smoothness remained good.
- Viper output increased only from `1570x1570` to `1592x1592`, still below the standalone `1756x1756` result.
- Color remained too subtle to judge confidently.

### 2026-09-10 — gifski 1.34.0 human retest

- Dev.4 changed only gifski from 1.32.0 to 1.34.0.
- The same Viper conversion regressed to `1532x1532`.
- Conclusion: 1.34.0 does not improve this workload's size efficiency; restore 1.32.0.

### 2026-09-10 — resolution-gap root cause confirmed from source

- Re-reading the exact standalone command exposed the important timing mismatch: FFmpeg was given source FPS with `-r`, but gifski was not passed `--fps`.
- gifski's CLI defaults video/Y4M input to 20 FPS, and its Y4M decoder explicitly skips frames when the source rate exceeds the requested target rate.
- This explains both observations at once: the standalone converter could afford a larger `1756x1756` spatial frame within the same byte budget, while Polymorph's full-frame output around `1592x1592` looked smoother.
- Polymorph's design requirement is to preserve frames. The standalone `1756x1756` result is therefore no longer considered the correct spatial-resolution parity target unless a future optional frame-rate mode is explicitly added.
