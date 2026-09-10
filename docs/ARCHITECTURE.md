# Architecture

## Boundaries

- `src/polymorph/converter.py`: conversion orchestration only.
- `src/polymorph/probe.py`: media metadata and WebP RIFF fallback parsing.
- `src/polymorph/integrity.py`: post-encode dimension/frame-count/timing verification.
- `src/polymorph/geometry.py`: deterministic Crop/Fit geometry and no-upscale validation.
- `src/polymorph/filters.py`: FFmpeg filter construction.
- `src/polymorph/ui/`: novice-facing desktop UI and live preview.
- `src/polymorph/update_service.py`: release check, checksum verification, installer launch.
- `build/`: executable packaging.
- `installer/`: per-user Windows installer.

## Conversion ordering

1. Probe source dimensions, duration, frame count, and nominal frame rate.
2. Resolve framing geometry.
3. Resolve user sizing constraint.
4. Decode/filter via FFmpeg.
5. Encode via gifski (GIF) or H.264 (MP4).
6. Probe the candidate output and verify exact requested dimensions, exact frame count, and bounded timing drift.
7. In file-size mode, inspect actual output size and retry at a lower/higher resolution as needed.
8. Copy the best valid result to the chosen output folder.

## File-size units

- User-entered `MB` ceilings are decimal: 1 MB = 1,000,000 bytes.
- Internal optimizer headroom may target below the ceiling, but an accepted output may never exceed the requested decimal byte limit.

## GIF reference boundary

- FFmpeg performs framing/Lanczos scaling and streams YUV4MPEG directly to gifski.
- The pinned Windows build explicitly uses `yuv420p` for the GIF Y4M stream. The standalone reference omitted `-pix_fmt`, but its working path effectively used 4:2:0; literal omission is not reliable on FFmpeg 9.0.1 after Polymorph's filter graph.
- gifski receives the requested output width explicitly, quality 100, extra effort, infinite repeat, and explicit source FPS.
- Explicit source FPS is an intentional divergence from the original standalone script. That script sent the source FPS to FFmpeg with `-r` but omitted gifski `--fps`; gifski therefore used its default 20 FPS target for Y4M/video input and resampled by dropping/duplicating frames.
- Polymorph must not reproduce that larger-resolution result by silently reducing frame count. Spatial resolution is optimized only after frame preservation is fixed.
- Post-encode validation requires the requested dimensions, exact frame count, and bounded timing drift.

## Resource policy

- Queue can contain many files.
- Only one conversion runs at a time in v1.
- No background service.
- No cloud processing.
- No telemetry.
