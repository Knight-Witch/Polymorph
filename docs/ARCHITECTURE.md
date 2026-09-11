# Architecture

## Boundaries

- `src/polymorph/converter.py`: proven conversion orchestration.
- `src/polymorph/adaptive_converter.py`: experimental GIF motion/resolution balancing layered over the proven converter; preserve-motion calls the base behavior unchanged.
- `src/polymorph/motion_planner.py`: pure adaptive-FPS candidate and measured-gain planning math.
- `src/polymorph/probe.py`: media metadata and WebP RIFF fallback parsing.
- `src/polymorph/integrity.py`: post-encode dimension/frame-count/timing verification, including explicit expected frame count for intentional uniform resampling.
- `src/polymorph/geometry.py`: deterministic Crop/Fit geometry and no-upscale validation.
- `src/polymorph/size_optimizer.py`: pure GIF smart-fit scale selection ported from the user-tested patched Python reference.
- `src/polymorph/filters.py`: proven spatial FFmpeg filter construction.
- `src/polymorph/ui/main_window.py`: existing novice-facing desktop UI and live preview.
- `src/polymorph/ui/adaptive_main_window.py`: development UI extension for GIF priority plus decimal-MB/effective-FPS completion reporting.
- `src/polymorph/update_service.py`: official-release discovery, exact asset pairing, bounded streaming download, checksum verification, installer launch.
- `build/`: executable packaging and CI-only diagnostics.
- `installer/`: per-user Windows installer.

## Conversion ordering

1. Probe source dimensions, duration, frame count, and nominal frame rate.
2. Resolve framing geometry.
3. Resolve user sizing constraint.
4. For Preserve motion, use the proven converter path unchanged.
5. For Favor resolution in GIF file-size mode, first obtain the full-frame fitted result as the spatial/byte baseline.
6. Build lower uniform GIF-cadence candidates nearest the source FPS first.
7. Reject candidates whose ideal frame-count-only ceiling cannot possibly meet the minimum useful spatial gain.
8. Encode each surviving candidate once at the already-fitted baseline dimensions and measure its actual gifski byte cost.
9. Select the first/highest candidate whose measured byte cost predicts at least about 8% linear spatial gain toward the patched-Python 97/99 byte target.
10. If no candidate earns that gain, return the Preserve-motion baseline unchanged.
11. If a candidate is worthwhile, run the normal GIF smart-fit search at that exact uniform resampled FPS.
12. Probe output and verify requested dimensions, exact planned frame count, and bounded duration drift.
13. Apply a final measured-gain veto: if the finished adaptive result is not at least about 8% larger linearly than the Preserve-motion baseline, discard it and return the baseline.

## File-size units

- User-entered `MB` ceilings are decimal: 1 MB = 1,000,000 bytes.
- Accepted output may never exceed the requested byte ceiling.
- The adaptive development completion readout also reports decimal MB rather than binary MiB mislabeled as MB.

## GIF file-size search

- GIF file-size mode follows the patched Python smart-fit search while preserving Polymorph's selected temporal plan.
- At a 99 MB ceiling the reference thresholds remain exact: 99,000,000-byte limit, 97,000,000-byte target, 93,000,000-byte acceptance floor.
- Other user ceilings scale those target/acceptance thresholds by the same 97/99 and 93/99 ratios.
- A failed encode predicts the next linear scale from the square root of target-bytes/measured-bytes, multiplies by 0.985, and guarantees at least a 4% downward move.
- Once passing/failing scale bounds exist, midpoint reclamation is used to move upward safely.
- A passing output at or above the acceptance floor stops the search.
- Normal search is capped at six attempts; the 128 px emergency long-edge fallback remains.
- MP4 keeps its existing, separately validated size-search implementation.

## Adaptive GIF motion planning

- Preserve motion remains default and keeps source FPS/frame count.
- Favor resolution applies only to GIF + file-size mode.
- Preferred spatial target is the native framed long edge capped at 2048 px.
- Current automatic FPS floor is 12.5 FPS (80 ms/frame), but the floor is never selected blindly.
- Candidate reduced rates must have an integer GIF centisecond delay: `fps = 100 / delay_cs`.
- Candidates are tried nearest the source FPS first. For a 25 FPS source the ladder is 20 FPS, 16.67 FPS, 14.29 FPS, then 12.5 FPS.
- The frame-count-only relationship `linear_scale ~= sqrt(source_fps / target_fps)` is retained only as an optimistic cheap screen; it is not trusted to select the final cadence.
- Actual selection is based on a real gifski encode at the baseline spatial dimensions because synthesized evenly timed frames can cost materially more bytes per frame than untouched source frames.
- The measured sample projects achievable spatial size against the patched-Python 97/99 target. A candidate must predict at least about 8% linear gain.
- The first/highest FPS that earns the gain wins, minimizing temporal sacrifice.
- The planner never requests dimensions above native framed geometry or the 2048 px soft target.
- Final adaptive output must independently realize the same minimum gain or it is discarded in favor of Preserve motion.
- Human dev.10 and dev.11 validation on Viper both returned `1552x1552 • 93.6 MB • 25 FPS`, confirming optical-flow candidates from 20 FPS through 12.5 FPS could not buy worthwhile spatial gain.

## Uniform motion resampling

- Reduced-FPS output is not made by periodically deleting source frames.
- Spatial Crop/Fit/Lanczos filtering remains unchanged and occurs before temporal resampling.
- Dev.12 uses FFmpeg `minterpolate` with `mi_mode=blend`, sampling exact uniformly spaced target timestamps by linear temporal blending rather than optical-flow motion compensation.
- This keeps every output interval the same duration and avoids the repeating short/long movement cadence caused by periodic source-frame deletion.
- A cloned end pad supplies interpolation lookahead.
- Output is trimmed to the exact mathematically expected frame count and timestamps are reset.
- gifski receives the same explicit target FPS used by the resampling stage.
- The measured candidate-cost gate and final 8% realized-gain veto remain authoritative, so a blend-resampled result is never kept merely because FPS was lowered.
- Windows toolchain smoke coverage requires the bundled FFmpeg build to support the current 12.5 FPS deepest clean cadence and exact planned reduced frame count.

## GIF reference boundary

- The canonical OG behavioral reference is only the user-tested patched Python `HeroForge_WebP_to_Reddit_GIF.py`.
- Production Preserve motion receives explicit width, quality 100, extra effort, infinite repeat, and explicit source FPS.
- Patched Python sends source FPS to FFmpeg with `-r` and omits gifski `--fps`.
- Controlled Windows CI proved that timing shape reduces a 50-frame/25-FPS source to 41 GIF frames over the same 2.0 s and uses about 82.19% of the full-frame byte cost at fixed dimensions.
- Real Viper source/output inspection separately confirmed 375 source frames at 25 FPS became 300 OG GIF frames over the same duration: exactly 20 FPS.
- Preserve motion must never silently reproduce that frame loss.
- Favor resolution may reduce FPS only because the user explicitly selects that tradeoff, and it must do so with uniform resampling rather than uneven deletion.

## Diagnostic evidence

- Patched-Python timing measurements: `HISTORY/DIAGNOSTICS/GIF_REFERENCE_TIMING_2026-09-10.md`.
- Adaptive cadence probe and human validation: `HISTORY/DIAGNOSTICS/GIF_ADAPTIVE_MOTION_2026-09-10.md`.

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
- Favor resolution intentionally does extra work: one Preserve-motion baseline fit plus one or more measured cadence probes and, only when justified, an adaptive size fit.
- No background service.
- No cloud processing.
- No telemetry.
