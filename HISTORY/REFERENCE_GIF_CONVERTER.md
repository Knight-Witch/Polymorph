# Canonical GIF Converter Reference

## Source

The validated standalone `HeroForge_WebP_to_Reddit_GIF.py` used immediately before Polymorph is the behavioral reference for GIF quality.

## Proven behavior to preserve

- FFmpeg streams YUV4MPEG directly to gifski; no PNG frame folder.
- gifski quality `100`.
- gifski `--extra` enabled.
- GIF repeat `0` / infinite loop.
- FFmpeg performs Lanczos scaling before gifski.
- gifski is explicitly passed `--width <FFmpeg output width>` so it cannot apply its conservative automatic animation downsize.
- The standalone FFmpeg command did not explicitly set a YUV pixel format. In the validated reference environment this effectively yielded the normal 4:2:0 Y4M handoff. The pinned Polymorph FFmpeg 9.0.1 Windows build must use explicit `yuv420p` because leaving the format unset can retain an RGB intermediate that `yuv4mpegpipe` rejects.
- File-size fitting changes resolution rather than hidden quality settings.
- Fixed 99 MB reference constants were `LIMIT_BYTES = 99_000_000`, `TARGET_BYTES = 97_000_000`, `ACCEPT_LOW_BYTES = 93_000_000`, `MAX_ATTEMPTS = 6`, and `MIN_LONG_EDGE = 128`.

## Polymorph timing safeguards retained intentionally

Polymorph explicitly supplies the source FPS to gifski and verifies output dimensions, frame count, and timing after encoding. Those safeguards are retained because they protect the no-frame-loss requirement and the user reported the Polymorph result as at least as smooth as the standalone output.

## Human validation history

### 2026-09-09 — first Polymorph tester

- MP4 output: visually excellent; no issue reported.
- Initial GIF output: visibly blurrier, grainier, and substantially downscaled because Polymorph omitted gifski `--width`.

### 2026-09-10 — width-corrected GIF

- GIF quality: reported fantastic and visually identical to the standalone result, possibly slightly smoother framewise.
- Remaining difference: Polymorph output was `1570x1570`; standalone output was `1756x1756` under the same nominal size target.
- Possible very subtle red/pink color difference was observed but not considered confirmed.
- The Polymorph GIF shown in Windows Explorer was already about `93.8 MB`, so the remaining resolution gap cannot be treated as simple unused file-size headroom.
- Concrete remaining pipeline difference: Polymorph forced `yuv444p`; the standalone reference effectively used a 4:2:0 Y4M handoff.

### 2026-09-10 — failed automatic Y4M negotiation probe

- Dev `0.1.0-dev.2` removed the forced pixel format to mimic the standalone command literally.
- Windows CI run #8 failed before packaging because FFmpeg 9.0.1 retained a non-Y4M-compatible format after filtering and `yuv4mpegpipe` refused to write its header.
- The failure confirmed that literal omission is not deterministic on the pinned Windows build.
- Next isolated tester uses explicit `yuv420p`, which preserves the intended 4:2:0 handoff while keeping the rest of the validated pipeline unchanged.
