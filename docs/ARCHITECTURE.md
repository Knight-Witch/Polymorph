# Architecture

## Boundaries

- `src/polymorph/converter.py`: proven conversion orchestration.
- `src/polymorph/adaptive_converter.py`: experimental GIF motion/resolution balancing layered over the proven converter; preserve-motion calls the base behavior unchanged.
- `src/polymorph/diagnostic_adaptive_converter.py`: dev.15-only observation wrapper around `AdaptiveConverter`; records decisions/measurements but does not change them.
- `src/polymorph/motion_planner.py`: adaptive source-frame decimation and measured-gain planning math.
- `src/polymorph/gif_timing.py`: pure GIF frame-delay inspection/patching used only to preserve exact loop closure timing after source-frame decimation.
- `src/polymorph/probe.py`: media metadata and WebP RIFF fallback parsing.
- `src/polymorph/integrity.py`: post-encode dimension/frame-count/timing verification.
- `src/polymorph/geometry.py`: deterministic Crop/Fit geometry and no-upscale validation.
- `src/polymorph/size_optimizer.py`: pure GIF smart-fit scale selection ported from the user-tested patched Python reference.
- `src/polymorph/filters.py`: proven spatial FFmpeg filter construction.
- `src/polymorph/ui/main_window.py`: existing novice-facing desktop UI and live preview.
- `src/polymorph/ui/adaptive_main_window.py`: development UI extension for GIF priority plus decimal-MB/effective-FPS completion reporting; dev.15 uses the diagnostic wrapper only for development Favor-resolution traces.
- `src/polymorph/update_service.py`: official-release discovery, exact asset pairing, bounded streaming download, checksum verification, installer launch.
- `build/`: executable packaging and CI-only diagnostics, including the dev.15 real-toolchain adaptive-selection integration gate.
- `installer/`: per-user Windows installer.

## Conversion ordering

1. Probe source dimensions, duration, frame count, frame durations, and nominal frame rate.
2. Resolve framing geometry.
3. Resolve user sizing constraint.
4. For Preserve motion, use the proven converter path unchanged.
5. For Favor resolution in GIF file-size mode, first obtain the full-frame fitted result as the spatial/byte baseline.
6. Require a constant-frame-rate source whose frame duration is exactly representable in GIF centiseconds.
7. Build exact source-frame decimation candidates nearest the source motion first: keep every 2nd frame, then every 3rd frame while the resulting motion remains above the automatic floor.
8. Reject candidates whose ideal retained-frame-count ceiling cannot possibly meet the minimum useful spatial gain.
9. Encode each surviving candidate once at the already-fitted baseline dimensions and measure its actual gifski byte cost.
10. When a measured candidate predicts at least about 8% linear spatial gain toward the 2048 px/native soft target, run the normal GIF smart-fit search using that exact source-frame stride.
11. If the full adaptive fit does not realize the same minimum gain, continue to the next deeper decimation candidate instead of immediately falling back to Preserve motion.
12. Patch only the final GIF frame delay when the source frame count is not divisible by the selected stride so the loop closes at the original duration/angular speed.
13. Probe output and verify requested dimensions, exact retained frame count, exact internal/final GIF delay pattern, and bounded duration drift.
14. If no candidate survives both measured gates, return the Preserve-motion baseline unchanged.

## Development adaptive tracing

- Dev.15 does not alter steps 1-14 above.
- `DiagnosticAdaptiveConverter` wraps the same `AdaptiveConverter` and records:
  - source/native geometry and byte ceiling;
  - every baseline/adaptive encode pass with dimensions and real byte size;
  - stride metadata and expected frame timing;
  - sample-probe errors;
  - full adaptive-fit results/errors;
  - measured predicted gain and realized gain classification;
  - final selected result or Preserve-motion fallback.
- Each Favor-resolution run writes `*_ADAPTIVE_DIAGNOSTIC.json` beside the output GIF. Preserve-motion and MP4 runs do not create the sidecar.
- Diagnostic write failure never changes the conversion result.
- The sidecar is temporary development instrumentation and is not part of the intended stable output contract.

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
- Favor resolution applies only to GIF + file-size mode and remains experimental.
- Preferred spatial target is the native framed long edge capped at 2048 px.
- Dev.9-dev.12 proved that uniformly synthesized intermediate frames can erase the expected GIF byte savings even when the output frame count is reduced.
- Dev.13 therefore stops synthesizing frames. Candidate plans retain only original decoded source frames at a constant integer stride.
- Candidates are tried nearest the source motion first. For a 25 FPS source the automatic floor of 8 FPS yields stride 2 (~12.5 FPS nominal) and then stride 3 (~8.33 FPS nominal).
- Frame-count-only math is used only as an optimistic cheap screen. Real gifski sample size at the Preserve-motion dimensions remains authoritative.
- The measured sample projects achievable spatial size against the patched-Python 97/99 target. A candidate must predict at least about 8% linear gain.
- The planner never requests dimensions above native framed geometry or the 2048 px soft target.
- A selected candidate must independently realize the same minimum gain after the full smart-fit search or Polymorph continues to the next stride.

## Exact source-frame decimation and loop timing

- Dev.13+ does not use `minterpolate`, optical flow, temporal blending, or periodic 1/2-frame-step deletion.
- For stride `N`, FFmpeg retains frames `0, N, 2N, ...` from the decoded source and establishes a nominal `source_fps / N` Y4M cadence for gifski.
- Retained image data therefore comes only from original source frames; no synthetic blended/warped frames are introduced.
- Most output frame delays are exactly `N * source_frame_delay`.
- If the source frame count is not divisible by `N`, the final retained frame has a smaller source-angle remainder before the loop returns to frame 0. Polymorph patches only that final GIF delay to `remainder_steps * source_frame_delay`.
- This preserves the original total loop duration and constant source angular speed instead of creating a periodic micro-skip. Example: Viper stride 2 retains 188 frames, uses 187 intervals at 80 ms and one 40 ms closure interval, totaling the original 15.0 seconds.
- GIF image data is not rewritten by the closure patch; only the final Graphic Control Extension delay field changes.
- Post-encode verification checks the complete delay pattern as well as dimensions/frame count/duration.

## Adaptive process integration gate

- Dev.15 adds `build/verify_adaptive_converter.py` and runs it against the exact pinned Windows FFmpeg 9.0.1 + gifski 1.32.0 toolchain before packaging.
- The script creates a deterministic high-entropy 25 FPS animated WebP, measures full-resolution Preserve-motion and stride-2 byte cost, and chooses a byte ceiling where full-frame output must spatially downscale while stride 2 has enough real savings to be useful.
- It then runs the actual `Converter` and `AdaptiveConverter` file-size orchestration, not hand-written command approximations.
- CI fails unless Favor resolution returns fewer frames, stays under the same byte ceiling, and realizes at least the production 8% linear spatial-gain threshold over Preserve motion.
- This gate distinguishes control-flow/toolchain failures from a real workload whose GIF compression simply does not benefit enough from frame decimation.

## GIF reference boundary

- The canonical OG behavioral reference is only the user-tested patched Python `HeroForge_WebP_to_Reddit_GIF.py`.
- Production Preserve motion receives explicit width, quality 100, extra effort, infinite repeat, and explicit source FPS.
- Patched Python sends source FPS to FFmpeg with `-r` and omits gifski `--fps`.
- Controlled Windows CI proved that timing shape reduces a 50-frame/25-FPS source to 41 GIF frames over the same 2.0 s and uses about 82.19% of the full-frame byte cost at fixed dimensions.
- Real Viper source/output inspection separately confirmed 375 source frames at 25 FPS became 300 OG GIF frames over the same duration: exactly 20 FPS.
- Preserve motion must never silently reproduce that frame loss.
- Favor resolution may reduce retained frames only because the user explicitly selects that tradeoff; dev.13+ uses deterministic source-frame stride plus exact loop-timing correction rather than hidden periodic frame loss.

## Diagnostic evidence

- Patched-Python timing measurements: `HISTORY/DIAGNOSTICS/GIF_REFERENCE_TIMING_2026-09-10.md`.
- Adaptive cadence probe and human validation: `HISTORY/DIAGNOSTICS/GIF_ADAPTIVE_MOTION_2026-09-10.md`.
- Dev.15 CI integration emits `build-smoke/adaptive-integration.json` and uploads it as `Polymorph-adaptive-integration`.

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
- Favor resolution intentionally does extra work: one Preserve-motion baseline fit plus one or more measured stride probes and, only when justified, adaptive size fits.
- No background service.
- No cloud processing.
- No telemetry.
