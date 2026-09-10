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
- The standalone FFmpeg command does not force a YUV pixel format before `yuv4mpegpipe`; that negotiated Y4M handoff is canonical unless testing proves otherwise.
- File-size fitting changes resolution rather than hidden quality settings.
- Fixed 99 MB reference constants were `LIMIT_BYTES = 99_000_000`, `TARGET_BYTES = 97_000_000`, `ACCEPT_LOW_BYTES = 93_000_000`, `MAX_ATTEMPTS = 6`, and `MIN_LONG_EDGE = 128`.

## Polymorph timing safeguards retained intentionally

Polymorph explicitly supplies the source FPS to gifski and verifies output frame count/timing after encoding. Those safeguards are retained because they protect the no-frame-loss requirement and the user reported the Polymorph result as at least as smooth as the standalone output.

## Human validation history

### 2026-09-09 — first Polymorph tester

- MP4 output: visually excellent; no issue reported.
- Initial GIF output: visibly blurrier, grainier, and substantially downscaled because Polymorph omitted gifski `--width`.

### 2026-09-10 — width-corrected GIF

- GIF quality: reported fantastic and visually identical to the standalone result, possibly slightly smoother framewise.
- Remaining difference: Polymorph output was `1570x1570`; standalone output was `1756x1756` under the same nominal size target.
- Possible very subtle red/pink color difference was observed but not considered confirmed.
- The Polymorph GIF shown in Windows Explorer was already about `93.8 MB`, so the remaining resolution gap cannot be treated as simple unused file-size headroom.
- Concrete remaining pipeline difference: Polymorph forced `yuv444p`; the standalone reference did not force a YUV format. The next isolated test restores the reference Y4M handoff while leaving the optimizer and MP4 path unchanged.
