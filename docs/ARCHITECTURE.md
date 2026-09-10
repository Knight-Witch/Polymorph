# Architecture

## Boundaries

- `src/polymorph/converter.py`: conversion orchestration only.
- `src/polymorph/probe.py`: media metadata and WebP RIFF fallback parsing.
- `src/polymorph/integrity.py`: post-encode dimension/frame-count/timing verification.
- `src/polymorph/geometry.py`: deterministic Crop/Fit geometry and no-upscale validation.
- `src/polymorph/filters.py`: FFmpeg filter construction.
- `src/polymorph/ui/`: novice-facing desktop UI and live preview.
- `src/polymorph/update_service.py`: official-release discovery, exact asset pairing, bounded streaming download, checksum verification, installer launch.
- `build/`: executable packaging and CI-only conversion diagnostics.
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
- Production Polymorph currently pins `yuv420p` for deterministic Y4M compatibility on the bundled FFmpeg 9.0.1 build.
- The supplied standalone Python reference does not specify `-pix_fmt`; therefore its exact negotiated Y4M pixel format, and especially the pixel format used inside the separately packaged share ZIP, must not be inferred without direct evidence.
- gifski receives the requested output width explicitly, quality 100, extra effort, infinite repeat, and explicit source FPS in the production Polymorph path.
- The supplied standalone reference instead sends source FPS to FFmpeg with `-r` and omits gifski `--fps`. gifski's video/Y4M default behavior makes frame-rate resampling a supported explanation for some or all of the larger standalone spatial result, but the amount of the effect is being measured by an isolated CI diagnostic before it is treated as the complete root cause.
- Production Polymorph must not silently reduce frame count to reclaim spatial resolution. Spatial resolution is optimized only after frame preservation is fixed.
- Post-encode validation requires the requested dimensions, exact frame count, and bounded timing drift.

## CI-only GIF reference diagnostic

- `build/compare_gif_reference.py` creates a deterministic 25 FPS animated WebP and runs matched FFmpeg -> YUV4MPEG -> gifski 1.32.0 variants.
- It compares reference-style gifski invocation without `--fps` against explicit 25 FPS gifski invocation while holding output dimensions, quality, extra effort, looping, and Y4M pixel format constant.
- It separately records automatic, `yuv420p`, and `yuv444p` Y4M behavior where supported.
- The report records tool versions, frame counts, durations, and encoded byte sizes and is uploaded as a build artifact.
- This diagnostic is never packaged into or invoked by the installed application.

## Update safety

- Update discovery uses only the official `Knight-Witch/Polymorph` GitHub latest-release endpoint.
- Automatic installation requires the exact canonical installer asset `Polymorph_Setup_v<version>.exe` and its exact companion `.sha256` asset.
- Release download URLs must be HTTPS GitHub release URLs for the Polymorph repository.
- Downloads are streamed to disk with explicit size bounds; the installer is hashed incrementally rather than loaded into memory as one buffer.
- The checksum file must contain a valid SHA-256 digest and, when it names a file, that filename must match the installer exactly.
- A failed or mismatched update is deleted and never launched.
- No updater daemon, startup task, background service, or unattended installer execution is used.

## Resource policy

- Queue can contain many files.
- Only one conversion runs at a time in v1.
- No background service.
- No cloud processing.
- No telemetry.
