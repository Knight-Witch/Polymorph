# Polymorph Pre-Flight Log

## PFC-2026-09-11-024 — Replace synthesized adaptive frames with exact source-frame decimation

- Target files: `src/polymorph/adaptive_converter.py`, `src/polymorph/motion_planner.py`, new `src/polymorph/gif_timing.py`, adaptive/UI wording, planner/timing/orchestration tests, Windows toolchain smoke coverage, version metadata, architecture/UX/status/reference/diagnostic docs, and required tracking files.
- Relevant history checked: `PROJECT_CONTRACT.md`, `MASTER.md`, `PRE_FLIGHT_Check.md`, `CHANGELOG.md`, `docs/ARCHITECTURE.md`, `docs/UX_SPEC.md`, `HISTORY/REFERENCE_GIF_CONVERTER.md`, `HISTORY/DIAGNOSTICS/GIF_ADAPTIVE_MOTION_2026-09-10.md`, current `converter.py`, `adaptive_converter.py`, `motion_planner.py`, integrity/size-optimizer/UI/build paths, and completed dev.12 Windows + Viper validation.
- Human validation incorporated: dev.12 Favor resolution again completed Viper at `1552x1552 • 93.6 MB • 25 FPS`. The user-supplied dev.11 and dev.12 GIFs are byte-for-byte identical: 93,630,962 bytes, SHA-256 `dbfd1be7211b801f3a3a8d0ffaaf1058a1974f6b27141ef5f3be5ce55452e5af`, 375 frames at 40 ms, 15.0 s.
- Diagnosis: the synthetic even-timestamp branch is exhausted for Viper; optical-flow and blend-generated frames do not create enough gifski savings. A second control-flow defect was also identified: after a candidate passed the sample prediction but failed the final realized-gain veto, dev.10-dev.12 returned the baseline instead of continuing to deeper candidates.
- Recommended action: replace only experimental Favor-resolution synthesis with exact integer-stride source-frame retention; test stride 2 then stride 3 nearest-first, keep real encoded sample cost and the 8% predicted/final gain floors, continue to the next stride after a failed full fit, and losslessly patch only the final GIF delay when the source frame count is not divisible by the stride so total loop duration/angular speed remain exact.
- Viper timing plan: stride 2 retains 188 original frames, uses 187 ordinary 80 ms intervals plus one 40 ms loop-closure interval, totaling exactly 15.0 s; average displayed rate is 12.5333 FPS. No optical-flow or blended image synthesis is used.
- Connected modules reviewed: Preserve-motion delegation, GIF smart-fit search, exact frame/duration verification, gifski 1.32.0 quality/extra/width/repeat arguments, framing filters, MP4 boundary, adaptive completion readout, packaging and build smoke.
- Conflict risks: ~12.53 FPS may be visibly too choppy despite constant angular speed; GIF delay-parser/patch correctness; FFmpeg `select`/timestamp filtering could alter expected retained-frame count; source-frame-count remainder handling; extra adaptive measurement time.
- Versioning: increment development tester from `0.1.0-dev.12` to `0.1.0-dev.13`.
- Unchanged: Preserve-motion GIF encoder/optimizer, MP4 encoder/optimizer, framing, updater, preview, visual skin, gifski dependency, 99 MB decimal ceiling, quality 100, and public release state.

## PFC-2026-09-11-023 — Test lower-complexity uniform temporal blending

- Target files: `src/polymorph/adaptive_converter.py`, Windows adaptive toolchain smoke coverage, development version metadata, adaptive architecture/UX/status/diagnostic docs, and required tracking files.
- Relevant history checked: `PROJECT_CONTRACT.md`, `MASTER.md`, `PRE_FLIGHT_Check.md`, `CHANGELOG.md`, `docs/ARCHITECTURE.md`, `docs/UX_SPEC.md`, `HISTORY/REFERENCE_GIF_CONVERTER.md`, `HISTORY/DIAGNOSTICS/GIF_ADAPTIVE_MOTION_2026-09-10.md`, current adaptive converter/planner/integrity/size optimizer/UI/toolchain paths, and completed dev.11 Windows + Viper validation.
- Human validation incorporated: dev.11 Favor resolution again completed the real Viper workload at `1552x1552 • 93.6 MB • 25 FPS`; the supplied GIF verifies 375 frames at uniform 40 ms timing over 15.0 s, so all 20/16.67/14.29/12.5 FPS optical-flow candidates were correctly rejected and Preserve motion was retained.
- Diagnosis: lowering the optical-flow cadence further is not justified. Motion-compensated synthetic frames remain too expensive for gifski to earn the existing 8% spatial-gain threshold even at 12.5 FPS.
- Local probe: using the dev.11 full-frame Viper GIF as a 25 FPS source surrogate, exact-timestamp `minterpolate=mi_mode=blend` at 20 FPS produced essentially the same uniform adjacent-frame cadence energy as the prior MCI path, and 768 px crop checks showed no obvious new periodic motion jump or gross ghosting in the sampled face/hair/cape/sword regions.
- Connected modules reviewed: measured candidate-cost gate, 8% final actual-gain veto, exact planned frame-count integrity checks, GIF smart-fit search, Preserve-motion boundary, MP4 path, framing, packaged app/UI readout, and Windows toolchain smoke.
- Conflict risks: temporal blending may introduce subtle ghosting/softening on thin or overlapping geometry; blend-resampled frames may still fail to save enough bytes; accidental regression of the validated Preserve-motion path.
- Recommended action: keep the dev.11 FPS ladder, measured byte-cost authority, 8% predicted/final gain thresholds, 2048 px soft target, and fallback behavior unchanged; change only Favor-resolution reduced-FPS synthesis from motion-compensated MCI to exact-timestamp linear temporal blending; rebuild and retain the lower-FPS result only if the existing measured gates prove a real spatial benefit.
- Versioning: increment development tester from `0.1.0-dev.11` to `0.1.0-dev.12`.
- Unchanged: Preserve-motion GIF encoder/optimizer, gifski 1.32.0/quality 100/Y4M behavior, cadence ladder, MP4, framing, updater, preview, UI layout, visual skin, and public release state.

## PFC-2026-09-11-022 — Extend measured Favor resolution cadence ladder

- Target files: adaptive motion planner tests, Windows adaptive toolchain smoke coverage, development version metadata, adaptive architecture/UX/status/diagnostic docs, and required tracking files.
- Relevant history checked: `PROJECT_CONTRACT.md`, `MASTER.md`, `PRE_FLIGHT_Check.md`, `CHANGELOG.md`, `docs/ARCHITECTURE.md`, `docs/UX_SPEC.md`, `HISTORY/REFERENCE_GIF_CONVERTER.md`, `HISTORY/DIAGNOSTICS/GIF_ADAPTIVE_MOTION_2026-09-10.md`, current `motion_planner.py`, `adaptive_converter.py`, current tests/build smoke, version metadata, and completed dev.10 Windows + Viper validation.
- Human validation incorporated: dev.10 Favor resolution completed the real Viper workload at `1552x1552 • 93.6 MB • 25 FPS`, proving the measured 20 FPS and 16.67 FPS candidates were correctly rejected and Preserve motion was retained when neither earned the required spatial gain.
- Diagnosis: dev.10 behaved correctly, but its 16.67 FPS automatic floor was an arbitrary search boundary. It did not answer whether the user's explicit Favor-resolution preference could earn a worthwhile result at a slightly deeper but still perfectly uniform GIF cadence.
- Connected modules reviewed: measured candidate gate, final actual-gain veto, uniform `minterpolate` path, exact frame-count integrity checks, GIF smart-fit search, Preserve-motion boundary, MP4 path, framing, packaged app/UI readout, and Windows toolchain smoke.
- Conflict risks: longer Favor-resolution conversion time from two additional measurement probes; 14.29/12.5 FPS may be visually less smooth despite even cadence; accidentally lowering FPS without a real spatial payoff.
- Recommended action: keep all dev.10 measured-cost and final-gain safeguards unchanged; extend only the clean candidate floor to 12.5 FPS so a 25 FPS source tries `20 -> 16.67 -> 14.29 -> 12.5`, selecting the first/highest cadence that demonstrably predicts >=8% linear spatial gain; otherwise preserve 25 FPS.
- Versioning: increment development tester from `0.1.0-dev.10` to `0.1.0-dev.11`.
- Unchanged: Preserve-motion GIF encoder/optimizer, gifski 1.32.0/quality 100/Y4M behavior, adaptive interpolation settings, 8% measured-gain threshold, 2048 px soft target, MP4, framing, updater, preview, visual skin, and public release state.

## PFC-2026-09-10-021 — Measure adaptive GIF byte cost before sacrificing FPS

- Target files: adaptive motion planner/converter/tests, adaptive UI completion readout, Windows adaptive smoke coverage, development version metadata, architecture/UX/status/adaptive-diagnostic docs, and required tracking files.
- Relevant history checked: `PROJECT_CONTRACT.md`, `MASTER.md`, `PRE_FLIGHT_Check.md`, `CHANGELOG.md`, `docs/ARCHITECTURE.md`, `docs/UX_SPEC.md`, `HISTORY/REFERENCE_GIF_CONVERTER.md`, `HISTORY/DIAGNOSTICS/GIF_ADAPTIVE_MOTION_2026-09-10.md`, current adaptive converter/motion planner/size optimizer/size units/integrity/UI worker/toolchain smoke paths, and the completed dev.9 Windows + Viper human validation.
- Human validation incorporated: dev.9 Favor resolution looked really good at full output resolution, but remained `1552x1552`; its completion line reported `89.2 MB` using the known binary-MiB display calculation, corresponding to roughly 93.5 decimal MB and the GIF optimizer's 93 MB acceptance region.
- Diagnosis: the dev.9 planner assumed spatial gain from the 25/20 frame-count ratio, but motion-interpolated frames are materially more expensive for gifski than untouched source frames. A lower frame count therefore does not guarantee proportional byte savings or spatial recovery.
- Connected modules reviewed: proven Preserve-motion GIF path, dev.8 smart-fit search, adaptive integrity verification, uniform interpolation, MP4 path, framing, decimal size units, UI settings/worker, packaging, updater boundaries.
- Conflict risks: extra conversion time from candidate measurement encodes; 16.67 FPS may be visually less desirable even with even interpolation; accidentally retaining reduced FPS without real spatial benefit; accidental regression of Preserve motion.
- Recommended action: measure each clean lower cadence with a real encode at the Preserve-motion dimensions; choose the highest FPS that predicts at least about 8% linear gain against the patched-Python 97/99 target; extend a 25 FPS source's automatic ladder from 20 FPS to 16.67 FPS only when 20 does not earn the gain; apply a final actual-gain veto/fallback to Preserve motion; report decimal MB and actual output FPS in the completion line.
- Versioning: increment development tester from `0.1.0-dev.9` to `0.1.0-dev.10`.
- Unchanged: Preserve-motion encoder/optimizer settings, GIF quality 100/gifski 1.32.0/Y4M behavior, MP4 encoding/sizing, framing, updater, preview behavior, existing visual skin, and public release state.

## PFC-2026-09-10-020 — Add experimental adaptive GIF motion/resolution mode

- Target files: adaptive motion planner/converter/UI extension, models/integrity/tests, Windows toolchain and packaged-app smoke coverage, development version metadata, UX/architecture/status/reference/adaptive-diagnostic docs, and required tracking files.
- Relevant history checked: `PROJECT_CONTRACT.md`, `MASTER.md`, `PRE_FLIGHT_Check.md`, `CHANGELOG.md`, `docs/ARCHITECTURE.md`, `docs/UX_SPEC.md`, `HISTORY/REFERENCE_GIF_CONVERTER.md`, `HISTORY/DIAGNOSTICS/GIF_REFERENCE_TIMING_2026-09-10.md`, current converter/filters/size optimizer/size units/main window/smoke/toolchain paths, and the real Viper source/output diagnostics.
- Confirmed real-source evidence: Viper source is 2048x2048, 375 frames at 25 FPS over 15.0 s; OG output is 300 frames over the same duration. Ordinary 25 -> 20 FPS frame selection showed a repeating motion-change spike `[0.6891, 1.1577, 0.6898, 0.6899]`, while motion-compensated interpolation produced near-even phase energy `[0.7742, 0.7898, 0.7902, 0.7755]` and exactly 300 intended frames with end lookahead + trimming.
- Connected modules reviewed: proven Preserve-motion GIF path, dev.8 GIF smart-fit search, integrity validation, spatial Crop/Fit/Lanczos filter, MP4 path, file-size units, UI settings flow, packaging, and updater boundaries.
- Conflict risks: interpolation artifacts at full output resolution; increased conversion time from baseline + adaptive fitting; accidental regression of the default Preserve-motion path; missing `minterpolate` support in the pinned Windows FFmpeg build; unsupported variable-duration inputs.
- Recommended action: add explicit opt-in `Favor resolution` for GIF + file-size mode only; leave `Preserve motion` as default and route it through the proven converter unchanged; use a soft 2048 px target, roughly 8% minimum predicted linear gain, 20 FPS automatic floor, uniform GIF-centisecond cadence candidates, and motion interpolation instead of uneven deletion; gate with unit tests, Windows toolchain/package smoke tests, then full-resolution Viper human validation.
- Versioning: increment development tester from `0.1.0-dev.8` to `0.1.0-dev.9`.
- Unchanged: MP4 encoding/sizing, framing behavior, updater, preview behavior, existing visual skin, and public release state.

## PFC-2026-09-10-019 — Port patched-Python GIF smart-fit optimizer

- Target files: `src/polymorph/size_optimizer.py`, GIF file-size orchestration in `src/polymorph/converter.py`, optimizer tests, development version metadata, GIF reference/diagnostic/architecture/status docs, and required tracking files.
- Relevant history checked: `PROJECT_CONTRACT.md`, `MASTER.md`, `PRE_FLIGHT_Check.md`, `CHANGELOG.md`, `docs/ARCHITECTURE.md`, `HISTORY/REFERENCE_GIF_CONVERTER.md`, the completed CI timing diagnostic, current converter/geometry/size-unit paths, and the full user-tested patched `HeroForge_WebP_to_Reddit_GIF.py`.
- Canonical-source boundary: only the patched Python converter actually run by the user is behavioral evidence. The later Discord distribution package is unvalidated and excluded from parity decisions.
- Confirmed timing result recorded: patched-Python timing retained 41/50 frames and used 82.1878% of the bytes of an otherwise matched full-frame 25 FPS path; the derived 1.10305x linear factor maps the comparable 1592px result to 1756.06px, matching the OG 1756px result.
- Optimizer diagnosis: current Polymorph GIF search can stop at roughly 90.27 MB under a 99 MB ceiling because its current acceptance condition is based on `0.97 * 0.94`; the patched Python instead uses a 97 MB target and 93 MB acceptance floor, plus different measured-size and pass/fail-bracketing logic.
- Connected modules reviewed: GIF encoder/timing/integrity safeguards, shared size dispatcher, MP4 file-size search, geometry even-dimension handling, decimal-MB conversion, cancellation/progress behavior, installer/version metadata.
- Conflict risks: replacing the shared size search would alter already-human-validated MP4 sizing; changing encoder/timing/color settings alongside the optimizer would make the Viper comparison ambiguous.
- Recommended action: route GIF file-size mode through a pure port of the patched Python smart-fit search generalized by 97/99 and 93/99 threshold ratios; preserve six normal attempts and 128px emergency long-edge fallback without upscaling; retain the existing MP4 size search unchanged; add pure optimizer regression tests.
- Versioning: increment development tester from `0.1.0-dev.7` to `0.1.0-dev.8`.
- No GIF encoder-quality, source-FPS, frame-count, Y4M, MP4 encoder, framing, updater, or UI presentation change is included.

## PFC-2026-09-10-018 — Add controlled standalone GIF parity diagnostic

- Target files: new CI-only GIF reference diagnostic, Windows development workflow, build/reference documentation, project status, and required tracking files.
- Relevant history checked: `PROJECT_CONTRACT.md`, `MASTER.md`, `PRE_FLIGHT_Check.md`, `CHANGELOG.md`, `docs/ARCHITECTURE.md`, `HISTORY/REFERENCE_GIF_CONVERTER.md`, `build/README.md`, current Windows workflow, current `src/polymorph/converter.py`, current `src/polymorph/probe.py`, the user-supplied known-good `HeroForge_WebP_to_Reddit_GIF.py`, and the supplied SHA-256 record for `HeroForge_WebP_to_Reddit_GIF_v1.0.0.zip`.
- Human validation incorporated: current decimal-MB/full-frame Viper output is `1552x1552` with otherwise good quality/smoothness; known-good standalone output remains `1756x1756`.
- Confirmed reference behavior: the supplied standalone Python uses Lanczos scaling, FFmpeg `-r <source fps>`, YUV4MPEG streaming, gifski quality 100/extra/repeat 0/explicit width, no gifski `--fps`, and its own 99M/97M/93M smart-fit thresholds.
- Documentation correction: the supplied Python does not specify `-pix_fmt`; the available package checksum identifies the shared ZIP but does not prove the exact Y4M pixel format or third-party binary build inside it. Earlier docs were too definitive about standalone 4:2:0 provenance and about timing being the complete cause of the 1756 result.
- Connected modules reviewed: production GIF invocation, post-encode frame/timing integrity guard, file-size optimizer, pinned FFmpeg/gifski toolchain, Windows smoke tests, MP4 path, installer build, updater boundaries.
- Conflict risks: modifying production timing or optimizer while still testing the reference would make the comparison ambiguous; allowing a diagnostic to leak into the installed app would violate the runtime boundary.
- Recommended action: add a build-only 25 FPS A/B that holds dimensions/quality/pixel format constant while toggling gifski `--fps`; separately record automatic/yuv420p/yuv444p Y4M behavior, tool versions, frame count, duration, and byte size; upload the diagnostic artifact; do not change production converter behavior.
- Versioning: no application version bump. Installed Polymorph remains `0.1.0-dev.7` because this update changes CI diagnostics/documentation only.
- Documentation/build-only update: no production Python conversion behavior, GIF/MP4 settings, optimizer, framing, updater runtime, UI, installer behavior, JavaScript, or manifest changed.

## PFC-2026-09-10-017 — Harden verified update downloads

- Target files: updater service, updater tests, development version metadata, architecture/status docs, required tracking files.
- Relevant history checked: `PROJECT_CONTRACT.md`, `MASTER.md`, `PRE_FLIGHT_Check.md`, `CHANGELOG.md`, `docs/ARCHITECTURE.md`, `docs/UX_SPEC.md`, current `src/polymorph/update_service.py`, current updater tests, installer filename/version metadata, and successful dev.6 Windows CI/artifact verification.
- Connected modules reviewed: GitHub latest-release endpoint, release asset naming, SHA-256 generation, installer launch path, update popup caller, per-user Inno installer, converter boundaries.
- Confirmed gaps: the updater accepted any Polymorph-named `.sha256` asset from the same release rather than requiring the exact companion checksum for the selected installer; installer hashing loaded the full executable into RAM; release asset downloads did not have explicit size bounds.
- Conflict risks: over-constraining asset naming could make future releases invisible to automatic installation; changing UI/update popup behavior at the same time would make updater-service validation less isolated.
- Recommended action: require canonical `Polymorph_Setup_v<version>.exe` plus exact `.exe.sha256` companion, restrict automatic downloads to HTTPS release URLs for the official repository, stream and hash downloads incrementally with explicit bounds, reject malformed/wrong-file checksums, and leave UI/conversion behavior unchanged.
- Versioning: increment development tester from `0.1.0-dev.6` to `0.1.0-dev.7`.

## PFC-2026-09-10-016 — Normalize file-size ceilings to decimal MB

- Target files: file-size unit helper, converter ceiling calculation, unit tests, development version metadata, architecture/status docs, required tracking files.
- Relevant history checked: `PROJECT_CONTRACT.md`, `MASTER.md`, `PRE_FLIGHT_Check.md`, `CHANGELOG.md`, `docs/ARCHITECTURE.md`, current `src/polymorph/converter.py`, `src/polymorph/models.py`, current sizing UI, and dev.5 Windows CI/artifact results.
- Connected modules reviewed: file-size optimizer, user `MB` input, conversion result byte accounting, GIF frame/FPS safeguards, MP4 path, installer/version metadata.
- Confirmed bug: the UI labels the ceiling in `MB`, but the converter multiplied by `1024 * 1024`, making `99 MB` equal 103,809,024 bytes and allowing a nominal 99 MB job to exceed a platform's decimal 100 MB upload limit.
- Conflict risks: correcting the ceiling will slightly reduce spatial resolution for outputs that were previously using the extra binary-MiB allowance; altering optimizer thresholds at the same time would make that expected change harder to audit.
- Recommended action: define decimal megabytes centrally as 1,000,000 bytes, use that helper only for the user-defined ceiling, add direct unit coverage, and leave optimizer search behavior, GIF quality/frame preservation, MP4 encoding, framing, and UI layout unchanged.
- Versioning: increment development tester from `0.1.0-dev.5` to `0.1.0-dev.6`.

## PFC-2026-09-10-015 — Restore gifski 1.32.0 and document frame-preservation tradeoff

- Target files: Windows gifski build dependency, development version metadata, GIF architecture/history/status docs, third-party/build docs, required tracking files.
- Relevant history checked: `PROJECT_CONTRACT.md`, `MASTER.md`, `PRE_FLIGHT_Check.md`, `CHANGELOG.md`, `HISTORY/REFERENCE_GIF_CONVERTER.md`, `docs/ARCHITECTURE.md`, current Windows workflow, current converter, current third-party/build docs, the exact standalone `HeroForge_WebP_to_Reddit_GIF.py`, and gifski 1.34.0 CLI/Y4M source handling.
- Human validation: dev.4 changed only gifski 1.32.0 -> 1.34.0 and regressed the same Viper conversion from dev.3's `1592x1592` to `1532x1532`.
- Confirmed root cause of the larger standalone `1756x1756` result: the standalone wrote source FPS into Y4M with FFmpeg `-r` but omitted gifski `--fps`; gifski defaults Y4M/video input to 20 FPS and its Y4M decoder skips frames when required to meet that target.
- Connected modules reviewed: GIF invocation, `yuv420p` handoff, explicit source-FPS argument, exact frame-count/timing integrity guard, file-size optimizer, MP4 path, Windows toolchain smoke gate, installer/version metadata.
- Conflict risks: chasing `1756x1756` as a spatial parity target would require sacrificing the user's explicit no-frame-loss requirement or changing another quality dimension; changing optimizer logic now would confuse the confirmed timing tradeoff.
- Recommended action: restore gifski 1.32.0, keep dev.3's `yuv420p` + explicit source FPS + exact frame verification, record the standalone converter as visual-quality but not frame-preservation canonical, and do not alter optimizer or MP4 behavior in this update.
- Versioning: increment development tester to `0.1.0-dev.5`; dev.5 returns to the best human-validated GIF dependency behavior while retaining the current safeguards.
- Follow-up remains separate: normalize UI `MB` from binary MiB to decimal MB before release; later optimizer work may reclaim small spatial gains but may not drop frames or lower GIF quality.

## PFC-2026-09-10-014 — Test stable gifski 1.34.0 against canonical GIF output

- Target files: Windows gifski build dependency, development version metadata, third-party/build docs, canonical GIF reference/history, status/tracking docs.
- Relevant history checked: `PROJECT_CONTRACT.md`, `MASTER.md`, `PRE_FLIGHT_Check.md`, `CHANGELOG.md`, `HISTORY/REFERENCE_GIF_CONVERTER.md`, `docs/ARCHITECTURE.md`, current Windows workflow, `THIRD_PARTY.md`, `build/README.md`, current converter, and the validated standalone `HeroForge_WebP_to_Reddit_GIF.py` from File Library.
- Human validation: dev.3 retained good animation smoothness and produced `1592x1592`, only 22 px above dev.1's `1570x1570` and still materially below the standalone `1756x1756`; color difference remains inconclusive.
- Confirmed reference gap: the standalone script requires only gifski `>=1.32.0` and does not record the exact encoder version used for the successful output; Polymorph had pinned the minimum 1.32.0 exactly.
- External dependency check: gifski 1.34.0 is the current stable release and documents palette-quality improvements from a newer `libimagequant`.
- Connected modules reviewed: GIF invocation, `yuv420p` Y4M handoff, size optimizer, post-encode integrity checks, MP4 path, Windows toolchain smoke test, packaging and installer version metadata.
- Conflict risks: altering encoder version and optimizer/timing behavior simultaneously would make the A/B result ambiguous.
- Recommended action: change only bundled gifski `1.32.0 -> 1.34.0`, leave converter code/optimizer/MP4 untouched, rebuild as `0.1.0-dev.4`, then retest the same Viper source.
- Follow-up remains separate: if 1.34.0 does not materially recover the gap, compare standalone timing/encoder invocation before editing optimizer behavior.

## PFC-2026-09-10-013 — Pin GIF Y4M to yuv420p after failed auto-negotiation

- Target files: GIF FFmpeg Y4M handoff, Windows toolchain smoke test, development version metadata, canonical GIF reference/history, architecture/status/tracking docs.
- Relevant history checked: `PROJECT_CONTRACT.md`, `MASTER.md`, `PRE_FLIGHT_Check.md`, `CHANGELOG.md`, `HISTORY/REFERENCE_GIF_CONVERTER.md`, `docs/ARCHITECTURE.md`, current `src/polymorph/converter.py`, current `build/verify_toolchain.py`, version metadata, and Windows run #8 failure logs.
- Connected modules reviewed: GIF size optimizer, gifski width/FPS/quality/repeat arguments, post-encode dimension/frame/timing integrity checks, MP4 path, installer metadata, Windows smoke pipeline.
- Confirmed run #8 failure: literal omission of `-pix_fmt` caused pinned FFmpeg 9.0.1 to retain a non-Y4M-compatible format after filtering; `yuv4mpegpipe` refused its header before gifski received valid input. The smoke script also produced a closed-stdout reader warning during failure cleanup.
- Conflict risks: changing optimizer thresholds at the same time would invalidate the controlled comparison; changing MP4 would disturb a human-validated path.
- Recommended action: explicitly use `yuv420p` for GIF Y4M, matching the canonical reference's effective 4:2:0 handoff while remaining deterministic on the pinned Windows toolchain; fix only the smoke-test pipe cleanup; leave optimizer and MP4 untouched.
- Versioning: increment tester from `0.1.0-dev.2` to `0.1.0-dev.3` because dev.2 never produced a valid installer.
- Follow-up remains separate: normalize UI `MB` to decimal bytes and compare optimizer search behavior only after this 4:2:0 parity build is human-tested.

## PFC-2026-09-10-012 — Restore canonical Y4M handoff for GIF

- Target files: GIF FFmpeg handoff, Windows toolchain smoke test, development version metadata, canonical GIF reference/history, architecture/status/tracking docs.
- Relevant history checked: `PROJECT_CONTRACT.md`, `MASTER.md`, `PRE_FLIGHT_Check.md`, `CHANGELOG.md`, `docs/ARCHITECTURE.md`, current `converter.py`, current `build/verify_toolchain.py`, and the validated standalone `HeroForge_WebP_to_Reddit_GIF.py` from File Library.
- Connected modules reviewed: GIF size optimizer, gifski width/FPS arguments, post-encode dimension/frame/timing integrity checks, MP4 path, installer version metadata, Windows smoke pipeline.
- Human validation: width-corrected Polymorph GIF was reported fantastic and visually identical to the standalone result, possibly smoother; measured output remained `1570x1570` versus standalone `1756x1756`, with only a possible subtle red/pink difference.
- Diagnosis: the current Polymorph GIF shown in Windows Explorer is already about `93.8 MB`, so the remaining resolution gap is not plausibly explained by simple unused file-size headroom alone. The canonical standalone FFmpeg command does not force a YUV pixel format before `yuv4mpegpipe`; Polymorph uniquely forced `yuv444p`.
- Conflict risks: changing optimizer thresholds simultaneously would make the A/B result ambiguous; changing MP4 would disturb an already-validated output path.
- Recommended action: remove only the forced GIF-path `yuv444p`, preserve explicit source FPS, gifski quality/extra/repeat/width settings and integrity verification, update the smoke test to exercise the same handoff, and retest the same HeroForge Viper source before touching optimizer logic.
- Versioning: development tester incremented from `0.1.0-dev.1` to `0.1.0-dev.2` so the replacement installer is unambiguous.
- Follow-up remains separate: normalize user-facing `MB` from binary MiB to decimal MB before release.

## PFC-2026-09-09-011 — Restore canonical gifski output width

- Target files: GIF encode command, output-integrity validation, integrity tests, architecture/status/tracking docs.
- Relevant history checked: `PROJECT_CONTRACT.md`, `MASTER.md`, `PRE_FLIGHT_Check.md`, `CHANGELOG.md`, `docs/ARCHITECTURE.md`, current converter/integrity tests, the validated standalone `HeroForge_WebP_to_Reddit_GIF.py`, and gifski 1.32.0 CLI/Y4M source behavior.
- Human validation: MP4 output was reported visually excellent with no issue; GIF output was reported substantially blurrier, grainier in gradients, and much smaller in actual pixel dimensions than the standalone result.
- Confirmed regression: the standalone converter explicitly passed `--width <FFmpeg output width>` to gifski; Polymorph omitted it. gifski 1.32.0 documents a default animation size limit of about 800x600 when width is unset.
- Intentional behavior retained: explicit source FPS handoff and post-encode temporal integrity checks remain because gifski's video/Y4M path otherwise defaults to 20 FPS and may resample frames.
- Connected modules reviewed: FFmpeg framing/scale filter, gifski CLI invocation, media probe, output integrity validation, file-size optimizer.
- Conflict risks: changing multiple GIF-quality variables at once would hide the root cause; MP4 is already human-validated and must remain untouched.
- Recommended action: restore only explicit gifski width control, require actual output dimensions to equal requested dimensions, rebuild, and retest the same HeroForge Viper source before changing any other GIF color/timing settings.
- Follow-up logged separately: user-facing `MB` currently uses binary MiB bytes and should be normalized to decimal MB before release; not changed in this regression-isolation patch.

## PFC-2026-09-09-010 — Record packaged-app validation

- Target files: `MASTER.md`, `PRE_FLIGHT_Check.md`, `CHANGELOG.md` only.
- Relevant history checked: `PROJECT_CONTRACT.md`, `MASTER.md`, `PRE_FLIGHT_Check.md`, `CHANGELOG.md`, `docs/ARCHITECTURE.md`, and Windows run #6 results for commit `b3cfdda`.
- Connected modules reviewed: packaged-EXE smoke result, installer build result, artifact metadata, and locally recomputed installer SHA-256.
- Confirmed result: Windows run #6 passed unit tests, pinned toolchain verification, PyInstaller, the frozen `Polymorph.exe` smoke gate, Inno Setup, checksum generation, and both artifact uploads.
- Conflict risks: prematurely calling the application publicly validated before a real HeroForge animated WebP is tested by a human on Windows.
- Recommended action: hand the `b3cfdda` dev installer to the user for hands-on validation; keep `main` and public releases unchanged.
- Documentation-only update: no Python, workflow, installer definition, JavaScript, manifest, or runtime behavior changed.

## PFC-2026-09-09-009 — Packaged application smoke gate

- Target files: application entrypoint, new packaged smoke-test module, toolchain sample retention, Windows workflow, build/tracking docs.
- Relevant history checked: `PROJECT_CONTRACT.md`, `MASTER.md`, `PRE_FLIGHT_Check.md`, `CHANGELOG.md`, `docs/ARCHITECTURE.md`, `docs/UX_SPEC.md`, current build workflow, resource loader, resolution linker, and app entrypoint on `dev`.
- Connected modules reviewed: frozen-tool discovery, packaged SVG resource lookup, `MainWindow` construction, Qt animated-WebP preview, linked-resolution controls, PyInstaller output path.
- Confirmed gap: successful PyInstaller/installer builds did not yet prove the frozen executable itself could start and resolve its packaged runtime resources.
- Conflict risks: hidden smoke path interfering with normal CLI file-open behavior; headless Qt platform issues; passing build despite missing WebP image plugin/assets/tools.
- Recommended action: add a hidden `--smoke-test` path used only by CI, run the actual frozen EXE in Qt offscreen mode, and block installer compilation if bundled tools/resources/live preview/linked sizing fail.

## PFC-2026-09-09-008 — First-pass UI usability polish

- Target files: live preview, linked-resolution helper, footer icon resources/loading, UI stylesheet, tests, packaging data declaration, UX/dependency/tracking docs.
- Relevant history checked: `PROJECT_CONTRACT.md`, `MASTER.md`, `PRE_FLIGHT_Check.md`, `CHANGELOG.md`, `docs/ARCHITECTURE.md`, `docs/UX_SPEC.md`, current UI files and PyInstaller spec on `dev`.
- Connected modules reviewed: framed native dimensions, fixed-resolution validation, Crop/Fit offset semantics, frozen-resource path, footer destinations.
- Confirmed UX issues: width/height could be entered independently and conflict with framing; Crop preview dragging moved the crop window rather than the visible image; footer still used letter/text placeholders.
- Conflict risks: introducing hidden upscaling through linked dimensions, preview/backend offset disagreement, SVG assets missing from packaged build.
- Recommended action: link dimensions deterministically to framed native ratio, invert only Crop drag semantics, package monochrome SVG resources explicitly, leave final app emblem separate.

## PFC-2026-09-09-007 — Pin and validate smaller FFmpeg Essentials toolchain

- Target files: Windows build workflow, `build/verify_toolchain.py`, build/dependency docs, project status/tracking docs.
- Relevant history checked: `PROJECT_CONTRACT.md`, `MASTER.md`, `PRE_FLIGHT_Check.md`, `CHANGELOG.md`, `docs/ARCHITECTURE.md`, `docs/UX_SPEC.md`, `THIRD_PARTY.md`, and the current Windows workflow on `dev`.
- Connected modules reviewed: tool discovery paths, GIF YUV4MPEG/gifski path, MP4 libx264 path, framing filter requirements, PyInstaller bundle paths.
- Confirmed size issue: successful dev app was ~435 MB unpacked; FFmpeg and ffprobe alone were ~313 MB. Successful installer artifact was ~126.6 MB.
- Candidate verified from provider documentation: Gyan FFmpeg 9.0.1 Essentials is a 64-bit static GPLv3 build, includes libwebp/libx264, and retains all FFmpeg internal Windows components.
- Conflict risks: smaller build missing a conversion capability, mutable third-party downloads, supply-chain mismatch, silent frame loss.
- Recommended action: pin the exact 9.0.1 Essentials archive and SHA-256; run an animated-WebP-to-GIF/MP4 smoke test against the exact bundled binaries before packaging.

## PFC-2026-09-09-006 — Correct PyInstaller repository root

- Target files: `build/Polymorph.spec`, tracking docs.
- Relevant history checked: `PROJECT_CONTRACT.md`, `MASTER.md`, `PRE_FLIGHT_Check.md`, `CHANGELOG.md`, `docs/ARCHITECTURE.md`, `docs/UX_SPEC.md` on `dev`.
- Connected modules reviewed: Windows Actions checkout path, `run_polymorph.py` entrypoint, bundled tool paths, installer input directory.
- Confirmed regression: first Windows build reached PyInstaller after tests/FFmpeg/gifski succeeded, then failed because `SPECPATH` was treated as a file path and traversed one parent too far.
- Conflict risks: changing dependency/tool placement unnecessarily while fixing only repository-root resolution.
- Recommended action: change only the spec root from `Path(SPECPATH).parent.parent` to `Path(SPECPATH).parent`; retain all other packaging behavior.

## PFC-2026-09-09-005 — Post-encode temporal integrity guard

- Target files: `models.py`, `probe.py`, new `integrity.py`, converter integration, tests, architecture/tracking docs.
- Relevant history checked: `PROJECT_CONTRACT.md`, `MASTER.md`, `PRE_FLIGHT_Check.md`, `CHANGELOG.md`, `docs/ARCHITECTURE.md`, `docs/UX_SPEC.md` on `dev`.
- Connected modules reviewed: source FPS handoff, RIFF metadata fallback, GIF/MP4 encoder paths, output probing.
- Conflict risks: source ffprobe failure preventing otherwise-valid HeroForge WebP metadata reads; nominal FPS drift; encoder silently dropping/duplicating frames; tiny container/GIF timing quantization causing false failures.
- Recommended action: retain RIFF metadata when ffprobe fails, carry nominal FPS explicitly, and verify exact output frame count plus a small duration tolerance after every encode candidate.

## PFC-2026-09-09-004 — Windows development packaging

- Target files: build spec/icon generator, Inno Setup installer, GitHub Actions Windows workflow, canonical footer URLs, tracking docs.
- Relevant history checked: `PROJECT_CONTRACT.md`, `MASTER.md`, `PRE_FLIGHT_Check.md`, `CHANGELOG.md`, `docs/ARCHITECTURE.md`, `docs/UX_SPEC.md` on `dev`.
- Connected modules reviewed: frozen-tool discovery paths, app entrypoint, updater release expectations, third-party dependency notes, current dev version.
- Conflict risks: bundling wrong tool binaries, requiring admin rights, publishing an unvalidated binary, updater mistaking a dev artifact for a release, placeholder icon being mistaken for final branding.
- Recommended action: produce workflow artifacts only; install per-user under LocalAppData; generate a clearly temporary icon; do not create a public release yet.

## PFC-2026-09-09-003 — Functional desktop UI and updater scaffold

- Target files: `src/polymorph/app.py`, `src/polymorph/ui/**`, `src/polymorph/update_service.py`, tests, tracking docs.
- Relevant history checked: `PROJECT_CONTRACT.md`, `MASTER.md`, `PRE_FLIGHT_Check.md`, `CHANGELOG.md`, `docs/ARCHITECTURE.md`, `docs/UX_SPEC.md` on `dev`.
- Connected modules reviewed: core converter settings/results, toolchain availability, geometry/framing behavior, GitHub release naming, conversion worker lifecycle.
- Conflict risks: UI changing encoder behavior, drag/drop interception, large preview RAM use, unsafe cross-thread UI calls, updater acting in background or without verification.
- Recommended action: keep encoder isolated; stream preview frames without full-animation caching; use Qt signals for thread-safe updater handoff; no service/daemon; require release checksum before installer launch.

## PFC-2026-09-09-002 — Core conversion engine scaffold

- Target files: `src/polymorph/{__init__,constants,models,probe,geometry,filters,tools,converter}.py`, tests, `pyproject.toml`, tracking docs.
- Relevant history checked: `PROJECT_CONTRACT.md`, `MASTER.md`, `PRE_FLIGHT_Check.md`, `CHANGELOG.md`, `docs/ARCHITECTURE.md`, `docs/UX_SPEC.md`.
- Reference behavior checked: validated FFmpeg -> YUV4MPEG -> gifski behavior, including explicit source FPS handoff to prevent gifski's default 20 FPS resampling.
- Connected modules reviewed: WebP probe fallback, framing geometry, filter construction, tool discovery, size optimizer.
- Conflict risks: frame-rate resampling, variable-duration WebP timing loss, color/timing drift, false no-upscale guarantees, resolution optimizer silently degrading other quality dimensions.
- Recommended action: keep on `dev`; validate with known HeroForge WebPs before merge/release.

## PFC-2026-09-09-001 — Repository bootstrap

- Target files: repository contract, project status, changelog/pre-flight tracking, architecture/UX docs, third-party dependency notes.
- Existing project history checked: repository was empty; no prior Polymorph history existed.
- Reference behavior checked: previously validated WebP -> GIF pipeline requirements were recorded as canonical behavior.
- Connected modules reviewed: Witch Dock remains a separate project and was not modified.
- Conflict risks: accidentally coupling Polymorph to Witch Dock; failing to preserve the validated GIF pipeline; public binary distribution before dependency/license review.
- Recommended action: keep application development isolated on `dev` and publish only validated builds.
