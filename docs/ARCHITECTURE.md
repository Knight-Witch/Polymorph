# Architecture

## Boundaries

- `src/polymorph/converter.py`: proven conversion orchestration.
- `src/polymorph/adaptive_converter.py`: experimental GIF motion/resolution balancing layered over the proven converter; preserve-motion calls the base behavior unchanged.
- `src/polymorph/diagnostic_adaptive_converter.py`: development observation wrapper around `AdaptiveConverter`; records decisions/measurements but does not change them.
- `src/polymorph/motion_planner.py`: adaptive source-frame decimation and measured-gain planning math.
- `src/polymorph/gif_timing.py`: pure GIF frame-delay inspection/patching used only to preserve exact loop closure timing after source-frame decimation.
- `src/polymorph/probe.py`: media metadata and WebP RIFF fallback parsing; ffprobe is launched with `CREATE_NO_WINDOW` on Windows.
- `src/polymorph/integrity.py`: post-encode dimension/frame-count/timing verification.
- `src/polymorph/geometry.py`: deterministic shared Crop/Fit/zoom geometry and no-upscale validation used by both export and preview.
- `src/polymorph/size_optimizer.py`: pure GIF smart-fit scale selection ported from the user-tested patched Python reference.
- `src/polymorph/filters.py`: proven spatial FFmpeg filter construction driven from shared framing geometry.
- `src/polymorph/ui/preview.py`: animated preview renderer driven from the same native framing geometry as export.
- `src/polymorph/ui/main_window.py`: novice-facing desktop UI and queue/framing state.
- `src/polymorph/ui/adaptive_main_window.py`: development UI extension for GIF priority, Crop zoom, decimal-MB/effective-FPS completion reporting, and diagnostic traces.
- `src/polymorph/ui/branded_layout.py`: presentation composition layer that reparents the already-wired functional widgets into the branded two-column workspace/control-rail layout without duplicating conversion state.
- `src/polymorph/ui/fonts.py`: bundled Cinzel/Inter registration and application-font setup; missing assets degrade to stylesheet fallbacks in source checkouts.
- `src/polymorph/ui/styles.py`: shared branded QSS applied after the functional and branded layout are constructed.
- `src/polymorph/update_service.py`: official-release discovery, exact asset pairing, bounded streaming download, checksum verification, installer launch.
- `build/verify_font_assets.py`: verifies the pinned Google Fonts downloads by Git blob SHA-1 before the frozen application is built.
- `build/`: executable packaging and CI-only diagnostics, including real-toolchain adaptive-selection and pinned-font gates.
- `installer/`: per-user Windows installer.

## Branded UI composition boundary

- `MainWindow` and `AdaptiveMainWindow` continue to create and wire the functional controls first.
- `rebuild_brand_layout()` runs only after that construction completes. It reuses those exact widget instances for files, preview, output format, sizing, GIF priority, aspect ratio, Crop zoom, output folder, progress, and conversion action.
- The visible Original/Crop/Fit branded radios synchronize to the existing `frame_mode` combo. The combo remains the established framing-state bridge consumed by existing enabled-state and framing callbacks.
- The branded composition therefore changes ownership/layout, not conversion semantics.
- Unsupported mockup concepts are not represented as fake controls. New visual controls must either drive existing state or implement a real action.
- `apply_brand_skin()` runs after the layout rebuild and changes only visual state/object names/window geometry.
- This separation keeps later loader/button animation work outside the converter and framing engine.

## Bundled font pipeline

- The Windows workflow downloads Cinzel and Inter from immutable google/fonts commit URLs.
- `build/verify_font_assets.py` computes the Git blob SHA-1 for each downloaded TTF and fails the build if it does not match the expected upstream blob identity.
- Matching SIL OFL text files are downloaded from the same pinned commits.
- `build/Polymorph.spec` already packages the complete `src/polymorph/assets` directory, so the downloaded font files and notices are included in the frozen application.
- `load_brand_fonts()` registers the packaged TTFs with Qt before `MainWindow` is constructed and sets Inter as the application body font. QSS selects Cinzel for display/primary-action roles.
- Packaged smoke fails if either font asset is missing or Qt cannot register both logical families.

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

## Shared framing geometry

- `native_geometry_for_size()` is the single source of truth for Original/Crop/Fit framing geometry from source pixel dimensions.
- Encoder paths call the same logic through `native_geometry(info, framing)`; the animated preview calls `native_geometry_for_size()` directly from the current frame dimensions.
- Crop returns a source crop rectangle with the requested aspect ratio. Drag offsets choose that crop window within the source.
- Crop zoom is a framing zoom, not an output upscale. At zoom >1, the retained source crop window shrinks proportionally and the native framed maximum shrinks with it. This preserves the project-wide no-upscale rule.
- Fit never stretches source content. It computes a larger target canvas, keeps source content at its native aspect ratio, and positions that content inside padding according to the same offsets used by the FFmpeg `pad` filter.
- Because preview and export use the same geometry object, a framing mismatch must now originate downstream of the shared geometry rather than from duplicate UI/backend math.

## Windows subprocess behavior

- FFmpeg and gifski encoding subprocesses use `CREATE_NO_WINDOW` on Windows.
- ffprobe is invoked on initial media probing and after encode passes for integrity verification. Dev.16 applies the same `CREATE_NO_WINDOW` flag to those `subprocess.run` calls so GUI use does not flash/steal focus with a console window.
- Non-Windows platforms receive a zero creation flag and retain normal subprocess behavior.

## Development adaptive tracing

- The diagnostic wrapper does not alter conversion ordering or selection policy.
- `DiagnosticAdaptiveConverter` records:
  - source/native geometry and byte ceiling;
  - every baseline/adaptive encode pass with dimensions and real byte size;
  - stride metadata and expected frame timing;
  - sample-probe errors;
  - full adaptive-fit results/errors;
  - measured predicted gain and realized gain classification;
  - final selected result or Preserve-motion fallback.
- Each development Favor-resolution run writes `*_ADAPTIVE_DIAGNOSTIC.json` beside the output GIF. Preserve-motion and MP4 runs do not create the sidecar.
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
- Favor resolution applies only to GIF + file-size mode.
- Preferred spatial target is the native framed long edge capped at 2048 px.
- Dev.9-dev.12 proved that uniformly synthesized intermediate frames can erase the expected GIF byte savings even when the output frame count is reduced.
- Dev.13 therefore stops synthesizing frames. Candidate plans retain only original decoded source frames at a constant integer stride.
- Candidates are tried nearest the source motion first. For a 25 FPS source the automatic floor of 8 FPS yields stride 2 (~12.5 FPS nominal) and then stride 3 (~8.33 FPS nominal).
- Frame-count-only math is used only as an optimistic cheap screen. Real gifski sample size at the Preserve-motion dimensions remains authoritative.
- The measured sample projects achievable spatial size against the patched-Python 97/99 target. A candidate must predict at least about 8% linear gain.
- The planner never requests dimensions above native framed geometry or the 2048 px soft target.
- A selected candidate must independently realize the same minimum gain after the full smart-fit search or Polymorph continues to the next stride.
- Real dev.15 Viper and two kitbash/decal-heavy HeroForge variants selected stride 2 successfully, so the current policy is considered technically validated pending ordinary release hardening rather than algorithm redesign.

## Exact source-frame decimation and loop timing

- Dev.13+ does not use `minterpolate`, optical flow, temporal blending, or periodic 1/2-frame-step deletion.
- For stride `N`, FFmpeg retains frames `0, N, 2N, ...` from the decoded source and establishes a nominal `source_fps / N` Y4M cadence for gifski.
- Retained image data therefore comes only from original source frames; no synthetic blended/warped frames are introduced.
- Most output frame delays are exactly `N * source_frame_delay`.
- If the source frame count is not divisible by `N`, the final retained frame has a smaller source-angle remainder before the loop returns to frame 0. Polymorph patches only that final GIF delay to `remainder_steps * source_frame_delay`.
- This preserves the original total loop duration and constant source angular speed instead of creating a periodic micro-skip. Example: Viper stride 2 retains 188 frames, uses 187 intervals at 80 ms and one 40 ms closure interval, totaling the original 15.0 seconds.
- When the source frame count divides evenly by the stride, every output delay remains uniform. The two 500-frame / stride-2 regression variants contain exactly 250 frames at 80 ms each.
- GIF image data is not rewritten by the closure patch; only the final Graphic Control Extension delay field changes when needed.
- Post-encode verification checks the complete delay pattern as well as dimensions/frame count/duration.

## Adaptive process integration gate

- `build/verify_adaptive_converter.py` runs against the exact pinned Windows FFmpeg 9.0.1 + gifski 1.32.0 toolchain before packaging.
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
- CI integration emits `build-smoke/adaptive-integration.json` and uploads it as `Polymorph-adaptive-integration`.

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
