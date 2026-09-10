# Canonical GIF Converter Reference

## Source and provenance

The known-good standalone `HeroForge_WebP_to_Reddit_GIF.py` supplied by the user is the visual-quality reference for GIF output. The separately shared Discord package is identified by SHA-256:

`f8f422ca350e32378979ec3110a69fa7daefdbd1005ac9937416f76e0bb71ecb  HeroForge_WebP_to_Reddit_GIF_v1.0.0.zip`

The available checksum identifies that ZIP but does not expose or prove the exact third-party binaries or command line contained inside it. Do not infer packaged pixel-format/toolchain details from the checksum alone.

## Exact behavior visible in the supplied Python reference

- FFmpeg streams YUV4MPEG directly to gifski; no PNG frame folder.
- FFmpeg performs Lanczos scaling.
- FFmpeg uses `-r <source fps>` before the Y4M output.
- The supplied Python reference does **not** specify `-pix_fmt`.
- gifski quality `100`.
- gifski `--extra` enabled.
- GIF repeat `0` / infinite loop.
- gifski is explicitly passed `--width <FFmpeg output width>` so it cannot apply its conservative automatic animation downsize.
- The supplied Python reference does **not** pass gifski `--fps`.
- File-size fitting changes spatial resolution rather than a quality flag.
- Fixed 99 MB reference constants are `LIMIT_BYTES = 99_000_000`, `TARGET_BYTES = 97_000_000`, `ACCEPT_LOW_BYTES = 93_000_000`, `MAX_ATTEMPTS = 6`, and `MIN_LONG_EDGE = 128`.
- The reference smart-fit search uses measured byte size, square-root area prediction, a 0.985 safety factor, a forced 4% downward move after a failure, midpoint reclamation between known passing/failing scales, and an acceptable stop band beginning at 93,000,000 bytes.

## Timing divergence under investigation

The supplied standalone command sends source FPS to FFmpeg with `-r` but gives gifski no explicit `--fps`. Polymorph explicitly supplies source FPS to gifski and verifies exact output frame count/timing.

gifski's Y4M/video path has a default target FPS when `--fps` is omitted, so frame-rate resampling is a strong supported explanation for why the standalone result can spend more of the same byte budget on spatial resolution. However, the earlier documentation overstated this as the fully confirmed cause of the `1756x1756` result without first running an otherwise-identical A/B through the exact bundled development toolchain.

A CI-only diagnostic now performs that controlled A/B at 25 FPS and records output frame count, duration, byte size, and tool versions. Production behavior is unchanged until those measurements are inspected.

## Human validation history

### 2026-09-09 — first Polymorph tester

- MP4 output: visually excellent; no issue reported.
- Initial GIF output: visibly blurrier, grainier, and substantially downscaled because Polymorph omitted gifski `--width`.

### 2026-09-10 — width-corrected GIF

- GIF quality: reported fantastic and visually identical to the standalone result, possibly slightly smoother framewise.
- Remaining difference: Polymorph output was `1570x1570`; standalone output was `1756x1756` under the same nominal size target.
- Possible very subtle red/pink color difference was observed but not considered confirmed.

### 2026-09-10 — yuv420p human retest

- Smoothness remained good.
- Viper output increased from `1570x1570` to `1592x1592` under the earlier binary-MiB ceiling implementation, still below standalone `1756x1756`.
- Color remained too subtle to judge confidently.

### 2026-09-10 — gifski 1.34.0 human retest

- Dev.4 changed only gifski from 1.32.0 to 1.34.0.
- The same Viper conversion regressed to `1532x1532`.
- Conclusion: 1.34.0 does not improve this workload's size efficiency; 1.32.0 was restored.

### 2026-09-10 — decimal-MB human retest

- After the user-facing 99 MB ceiling was corrected to exactly 99,000,000 bytes, the same Viper conversion produced `1552x1552`.
- Quality/smoothness was otherwise still good.
- The result remains materially below the known-good standalone `1756x1756`, so spatial parity remains an active diagnostic question rather than being dismissed from the target solely on inference.

## Current diagnostic boundary

- Do not modify the production converter to mimic the standalone timing until the controlled A/B report is inspected.
- Do not alter the file-size optimizer during the timing A/B.
- If omitting gifski `--fps` produces the expected frame reduction and a corresponding byte reduction, quantify that effect before deciding whether any optional user-facing tradeoff belongs in Polymorph.
- If the timing effect does not account for the observed Viper resolution gap, the next investigation is exact third-party toolchain/package provenance, followed by optimizer parity.
