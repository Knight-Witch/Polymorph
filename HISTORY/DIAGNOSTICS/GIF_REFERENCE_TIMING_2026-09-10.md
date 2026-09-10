# GIF Reference Timing Diagnostic — 2026-09-10

## Purpose

Measure the timing consequence of the patched Python converter that actually produced the user's known-good `1756x1756` GIF, without changing production Polymorph behavior.

## Canonical reference

Behavioral reference: user-supplied `HeroForge_WebP_to_Reddit_GIF.py` only.

The separately packaged Discord build has not been used or validated by the user and is not a behavioral reference for this investigation.

## Controlled test

Windows CI run `34467182268`, diagnostic commit `d447dc2015ed690ed286ddbaf30049d0dcd4f618`.

- FFmpeg: pinned Gyan 9.0.1 Essentials.
- gifski: 1.32.0.
- Source: 256x256 animated WebP, 50 frames, 25 FPS, 40 ms/frame, 2.0 s.
- Output: fixed 192x192.
- Held constant: Lanczos scaling, gifski quality 100, `--extra`, infinite repeat, explicit output width.
- Variable: patched-Python timing shape (FFmpeg `-r 25`, no gifski `--fps`) versus explicit gifski `--fps 25` full-frame timing.

## Results

| Variant | Y4M format | gifski FPS | Frames | Duration | Bytes |
| --- | --- | --- | ---: | ---: | ---: |
| Patched-Python timing | yuv420p | omitted | 41 | 2.0 s | 932,849 |
| Full-frame timing | yuv420p | 25 | 50 | 2.0 s | 1,135,021 |
| Patched-Python timing | yuv444p | omitted | 41 | 2.0 s | 918,247 |
| Full-frame timing | yuv444p | 25 | 50 | 2.0 s | 1,118,312 |

The literal no-`-pix_fmt` command shape from the Python reference does not run on the pinned Gyan FFmpeg 9.0.1 build because that build can retain a Y4M-incompatible automatic pixel format after filtering. That is a toolchain compatibility detail, not part of the timing result; the timing result reproduced under both explicit yuv420p and yuv444p.

## Quantified effect

For the yuv420p pair:

- Frame ratio: `41 / 50 = 0.82`.
- Byte ratio: `932,849 / 1,135,021 = 0.821878...`.
- Linear-resolution factor available from that byte saving: `sqrt(1 / 0.821878...) = 1.10305...`.
- `1592 * 1.10305 = 1756.06`.
- Human-known OG output: `1756x1756`.

The measured frame-resampling effect therefore predicts the observed OG spatial-resolution advantage essentially exactly when compared against the earlier 1592px Polymorph run that used the same larger effective byte allowance.

## Decision

- The OG `1756x1756` result is not a full-frame parity target.
- Production Polymorph keeps explicit source FPS plus exact frame-count/timing verification.
- Polymorph must not silently remove frames to gain spatial resolution.
- Future optimizer work may reclaim unused bytes only while preserving every source frame and GIF quality 100.
- Any future reduced-FPS mode must be explicit and user-selected.
