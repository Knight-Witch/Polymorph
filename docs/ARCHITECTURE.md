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

## GIF reference boundary

- FFmpeg performs framing/Lanczos scaling and streams YUV4MPEG directly to gifski.
- Do not force a GIF-path YUV pixel format unless a validated reference proves it is beneficial; the canonical standalone converter left the Y4M pixel format negotiated by FFmpeg.
- gifski receives the requested output width explicitly, quality 100, extra effort, infinite repeat, and explicit source FPS.

## Resource policy

- Queue can contain many files.
- Only one conversion runs at a time in v1.
- No background service.
- No cloud processing.
- No telemetry.
