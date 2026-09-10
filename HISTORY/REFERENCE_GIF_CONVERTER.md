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

## Current boundary

- Production Polymorph preserves every source frame and must not reproduce OG frame resampling silently.
- OG 1756px is not a valid full-frame 99 MB parity target.
- Dev.8 ports the patched Python's smart-fit resolution search into GIF file-size mode while retaining full-frame timing and quality safeguards.
- Any future lower-FPS mode must be explicit and user-selected.
