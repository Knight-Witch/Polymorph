# Architecture

## Boundaries

- `src/polymorph/converter.py`: conversion orchestration only.
- `src/polymorph/probe.py`: media metadata and WebP RIFF fallback parsing.
- `src/polymorph/integrity.py`: post-encode dimension/frame-count/timing verification.
- `src/polymorph/geometry.py`: deterministic Crop/Fit geometry and no-upscale validation.
- `src/polymorph/size_optimizer.py`: pure GIF smart-fit scale selection ported from the user-tested patched Python reference.
- `src/polymorph/filters.py`: FFmpeg filter construction.
- `src/polymorph/ui/`: novice-facing desktop UI and live preview.
- `src/polymorph/update_service.py`: official-release discovery, exact asset pairing, bounded streaming download, checksum verification, installer launch.
- `build/`: executable packaging and CI-only diagnostics.
- `installer/`: per-user Windows installer.

## Conversion ordering

1. Probe source dimensions, duration, frame count, and nominal frame rate.
2. Resolve framing geometry.
3. Resolve user sizing constraint.
4. Decode/filter via FFmpeg.
5. Encode via gifski (GIF) or H.264 (MP4).
6. Probe candidate output and verify requested dimensions, exact frame count, and bounded timing drift.
7. In file-size mode, inspect actual output size and retry at a resolution selected by the format-specific optimizer.
8. Copy the best valid result to the chosen output folder.

## File-size units

- User-entered `MB` ceilings are decimal: 1 MB = 1,000,000 bytes.
- Accepted output may never exceed the requested byte ceiling.

## GIF file-size search

- GIF file-size mode follows the patched Python smart-fit search while preserving Polymorph's full-frame encoder path.
- At a 99 MB ceiling the reference thresholds remain exact: 99,000,000-byte limit, 97,000,000-byte target, 93,000,000-byte acceptance floor.
- Other user ceilings scale those target/acceptance thresholds by the same 97/99 and 93/99 ratios.
- A failed encode predicts the next linear scale from the square root of target-bytes/measured-bytes, multiplies by 0.985, and guarantees at least a 4% downward move.
- Once a passing and failing scale bracket exist, midpoint reclamation is used to move upward safely.
- A passing output at or above the acceptance floor stops the search.
- Normal search is capped at six attempts. The patched 128 px emergency long-edge fallback is retained without permitting source upscaling.
- MP4 keeps its existing, separately validated size-search implementation.

## GIF reference boundary

- The canonical OG behavioral reference is only the user-tested patched Python `HeroForge_WebP_to_Reddit_GIF.py`.
- FFmpeg performs Lanczos scaling and streams YUV4MPEG directly to gifski.
- Production Polymorph currently pins `yuv420p` for deterministic compatibility on bundled FFmpeg 9.0.1.
- Production gifski receives explicit width, quality 100, extra effort, infinite repeat, and explicit source FPS.
- Patched Python sends source FPS to FFmpeg with `-r` and omits gifski `--fps`.
- Controlled Windows CI proved that timing shape reduces a 50-frame/25-FPS source to 41 GIF frames over the same 2.0 s. At fixed yuv420p dimensions/quality it used 82.1878% of the bytes of the 50-frame output.
- The derived 1.10305x linear-resolution multiplier maps the comparable 1592px full-frame result to 1756px, matching the OG output.
- Production Polymorph must not silently reduce frame count to reclaim spatial resolution.
- Post-encode validation requires requested dimensions, exact frame count, and bounded timing drift.

## CI-only GIF reference diagnostic

- `build/compare_gif_reference.py` creates a deterministic 25 FPS animated WebP and compares patched-Python timing against explicit full-frame timing.
- It holds dimensions, quality, extra effort, looping, and Y4M pixel format constant.
- Windows run #14 (`34467182268`) confirmed 41/50 frames and 82.1878% byte usage for the patched-Python timing path.
- Durable measurements are in `HISTORY/DIAGNOSTICS/GIF_REFERENCE_TIMING_2026-09-10.md`.
- This diagnostic is not packaged into or invoked by the installed app.

## Update safety

- Update discovery uses only the official latest-release endpoint.
- Automatic installation requires exact canonical installer + exact `.sha256` companion.
- Release download URLs must be HTTPS GitHub release URLs for this repository.
- Downloads are streamed with explicit size bounds and incrementally SHA-256 hashed.
- Failed or mismatched updates are deleted and never launched.
- No updater daemon, startup task, background service, or unattended installer execution.

## Resource policy

- Queue can contain many files.
- Only one conversion runs at a time in v1.
- No background service.
- No cloud processing.
- No telemetry.
