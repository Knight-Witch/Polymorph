# Architecture

## Boundaries

- `src/polymorph/converter.py`: conversion orchestration only.
- `src/polymorph/probe.py`: media metadata and WebP RIFF fallback parsing.
- `src/polymorph/geometry.py`: deterministic Crop/Fit geometry and no-upscale validation.
- `src/polymorph/filters.py`: FFmpeg filter construction.
- `src/polymorph/ui/`: novice-facing desktop UI and live preview.
- `src/polymorph/update_service.py`: release check, checksum verification, installer launch.
- `build/`: executable packaging.
- `installer/`: per-user Windows installer.

## Conversion ordering

1. Probe source dimensions, duration, and frame count.
2. Resolve framing geometry.
3. Resolve user sizing constraint.
4. Decode/filter via FFmpeg.
5. Encode via gifski (GIF) or H.264 (MP4).
6. In file-size mode, inspect actual output size and retry at a lower/higher resolution as needed.
7. Copy the best valid result to the chosen output folder.

## Resource policy

- Queue can contain many files.
- Only one conversion runs at a time in v1.
- No background service.
- No cloud processing.
- No telemetry.
