# Architecture

## Boundaries

- `src/polymorph/converter.py`: proven conversion orchestration.
- `src/polymorph/adaptive_converter.py`: explicit Favor-resolution GIF balancing layered over the proven converter; Preserve motion delegates to base behavior unchanged.
- `src/polymorph/diagnostic_adaptive_converter.py`: development observation wrapper around `AdaptiveConverter`; records decisions/measurements but does not change them.
- `src/polymorph/motion_planner.py`: adaptive source-frame decimation and measured-gain planning math.
- `src/polymorph/gif_timing.py`: GIF frame-delay inspection/patching for exact adaptive loop closure.
- `src/polymorph/probe.py`: media metadata and WebP RIFF fallback parsing; external ffprobe launches are hidden on Windows.
- `src/polymorph/integrity.py`: post-encode dimension/frame-count/timing verification.
- `src/polymorph/geometry.py`: framed native geometry, linked no-upscale sizing, and shared aspect-preserving content placement used by both preview and encoder.
- `src/polymorph/filters.py`: FFmpeg framing/filter construction from the shared placement model.
- `src/polymorph/size_optimizer.py`: GIF smart-fit scale selection ported from the user-tested patched Python reference.
- `src/polymorph/ui/preview.py`: animated preview; Crop/Fit placement uses the same geometry helper as the encoder.
- `src/polymorph/ui/main_window.py`: novice-facing queue/settings UI plus Crop/Fit drag/zoom controls.
- `src/polymorph/ui/adaptive_main_window.py`: development GIF-priority extension and decimal-MB/effective-FPS reporting.
- `src/polymorph/update_service.py`: official-release discovery, exact asset pairing, bounded streaming download, checksum verification, installer launch.
- `build/`: packaging and CI-only diagnostics/integration gates.
- `installer/`: per-user Windows installer.

## Framing model

Framing is split into two concepts so composition and output sizing do not fight each other.

1. `native_geometry()` determines the framing canvas at the source's native scale. Original keeps the source canvas. Crop produces the largest target-ratio canvas that fits inside the source bounds. Fit produces the smallest target-ratio canvas that contains the full source.
2. `content_placement()` places the source image inside that canvas without changing its aspect ratio. Crop starts from a cover scale; Fit starts from a contain scale. The user zoom multiplier is applied only after that base scale.
3. Position offsets are normalized from -1 to +1 on each axis. When content is smaller than the canvas they align within the padded space; when content is larger they choose which cropped edge is visible.
4. Preview draws the complete source into this placement rectangle and clips it to the canvas.
5. The FFmpeg filter path applies the same model: aspect-preserving source scale when needed, crop any overflow, pad any uncovered Fit canvas, then perform the final output-resolution scale.

This ordering is intentional. The source is never resized independently in X/Y to force a target ratio. A 1:1 source remains geometrically 1:1 inside a 16:9 Crop/Fit composition; the 16:9 result comes from clipping or padding, not distortion.

### Manual framing zoom

- Crop/Fit expose 100%-400% zoom.
- Zoom changes only source composition inside the native framing canvas.
- The native framing canvas and no-upscale output ceiling do not grow with zoom.
- Drag offsets and zoom are stored in `FramingSettings` and therefore travel through preview and conversion as the same settings.
- Center resets offsets while preserving the chosen zoom.

## Conversion ordering

1. Probe source dimensions, duration, frame count, frame durations, and nominal frame rate.
2. Resolve framing canvas and content placement.
3. Resolve user sizing constraint.
4. Build aspect-safe FFmpeg Crop/Fit filters, then apply final spatial output scaling.
5. For Preserve motion, use the proven converter path unchanged.
6. For Favor resolution in GIF file-size mode, obtain the full-frame fitted result as the spatial/byte baseline.
7. Require a constant-frame-rate source whose frame duration is exactly representable in GIF centiseconds.
8. Build exact source-frame decimation candidates nearest the source motion first: keep every 2nd frame, then every 3rd frame while resulting motion remains above the automatic floor.
9. Reject candidates whose ideal retained-frame-count ceiling cannot possibly meet the minimum useful spatial gain.
10. Encode each surviving candidate once at the fitted baseline dimensions and measure real gifski byte cost.
11. When a measured candidate predicts at least about 8% linear spatial gain toward the 2048 px/native soft target, run the normal GIF smart-fit search using that source-frame stride.
12. If the full adaptive fit does not realize the same minimum gain, continue to the next deeper candidate.
13. Patch only the final GIF frame delay when source frame count is not divisible by the stride so the loop closes at the original duration/angular speed.
14. Probe output and verify dimensions, retained frame count, delay pattern, and bounded duration drift.
15. If no adaptive candidate survives both measured gates, return the Preserve-motion baseline unchanged.

## Windows child-process policy

External media tools must never steal focus from the user.

- FFmpeg and gifski `Popen` calls use `CREATE_NO_WINDOW` on Windows.
- Dev.16 applies the same flag to the shared ffprobe `subprocess.run()` path.
- Because the same probe helper is used when media is loaded and after encode candidates for integrity checks, this removes the console flashes previously seen both at load time and during encoding/optimization.
- Standard output/error are still captured or piped as needed; hiding the console does not suppress diagnostic data.

## GIF file-size search

- GIF file-size mode follows the patched Python smart-fit search while preserving the selected temporal plan.
- At 99 MB: hard limit 99,000,000 bytes; target 97,000,000; acceptance floor 93,000,000.
- Other ceilings scale target/acceptance by the same 97/99 and 93/99 ratios.
- Failed encodes use square-root area prediction with 0.985 safety and at least a 4% downward move.
- Passing/failing bounds allow midpoint reclamation upward.
- A passing output at or above the acceptance floor stops the search.
- Normal search is capped at six attempts; 128 px emergency long-edge fallback remains.
- MP4 keeps its separately validated size search.

## Adaptive GIF motion planning

- Preserve motion remains default and keeps source FPS/frame count.
- Favor resolution is explicit opt-in for GIF + file-size mode.
- Preferred adaptive long edge is native framed size capped at 2048 px.
- Dev.9-dev.12 showed synthesized lower-FPS frames can erase expected GIF byte savings.
- Dev.13+ therefore retains only original decoded source frames at constant integer strides.
- For 25 FPS, the automatic 8 FPS floor permits stride 2 (~12.5 FPS nominal) then stride 3 (~8.33 FPS nominal).
- Frame-count math is only an optimistic cheap screen. Real gifski sample size at Preserve dimensions is authoritative.
- Measured and final realized gain must each clear about 8% linearly.
- No candidate may request dimensions above native framed geometry or the 2048 px adaptive target.

## Exact source-frame decimation and loop timing

- No `minterpolate`, optical flow, temporal blending, or periodic 1/2-frame-step deletion is used in dev.13+.
- Stride `N` retains source frames `0, N, 2N, ...` and establishes a nominal `source_fps / N` cadence.
- Most output delays are exactly `N * source_frame_delay`.
- If the source count is not divisible by `N`, only the last GIF Graphic Control Extension delay is shortened to the source-frame remainder.
- Example Viper stride 2: 188 retained frames, 187 intervals at 80 ms plus one 40 ms closure interval = exactly 15.0 s.
- Post-encode verification checks complete delay pattern, dimensions, frame count, and duration.

## Development adaptive tracing and integration gate

- `DiagnosticAdaptiveConverter` records source/native geometry, byte ceiling, baseline/adaptive encode sizes, candidate stride/timing, sample errors, full-fit results/errors, measured/realized gain, and final selection/fallback.
- Development Favor-resolution runs write `*_ADAPTIVE_DIAGNOSTIC.json` beside the GIF; diagnostic I/O never changes conversion success.
- `build/verify_adaptive_converter.py` runs the actual adaptive orchestration against pinned Windows FFmpeg 9.0.1 + gifski 1.32.0 and fails unless a deterministic workload produces a lower-frame, >=8%-larger result under the same byte ceiling.
- Real human validation now independently confirms selection on Viper and two kitbash/decal-heavy 500-frame workloads.

## File-size units

- User-entered MB is decimal: 1 MB = 1,000,000 bytes.
- Accepted output may never exceed the requested ceiling.
- Development completion reporting also uses decimal MB.

## GIF reference boundary

- Canonical OG behavior comes only from the user-tested patched `HeroForge_WebP_to_Reddit_GIF.py`.
- Preserve motion receives explicit width, quality 100, extra effort, infinite repeat, and explicit source FPS.
- The OG omitted gifski `--fps`; controlled CI and real Viper inspection confirmed this sacrificed temporal samples and explains most of its spatial advantage.
- Preserve motion must not reproduce that hidden frame loss.
- Favor resolution may reduce retained frames only because the user explicitly selects that tradeoff and uses deterministic source-frame stride plus exact loop correction.

## Update and resource safety

- Update discovery uses only the official repository release endpoint and exact installer/checksum pairing.
- Downloads are HTTPS-only for official release assets, bounded, streamed, and incrementally hashed.
- Failed/mismatched updates are never launched.
- Queue can contain many files, but only one conversion runs at a time in v1.
- No background service, startup task, cloud processing, or telemetry.
