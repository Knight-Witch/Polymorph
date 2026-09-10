# Polymorph Pre-Flight Log

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
- Confirmed bug: the UI labels the ceiling in `MB`, but the converter multiplied by `1024 * 1024`, making `99 MB` equal 103,809,024 bytes and allowing a nominal 99 MB job to exceed a platform's decimal 100 MB limit.
- Conflict risks: correcting the ceiling will slightly reduce spatial resolution for outputs that were previously using the extra binary-MiB allowance; altering optimizer thresholds at the same time would make that expected change harder to audit.
- Recommended action: define decimal megabytes centrally as 1,000,000 bytes, use that helper only for the user-defined ceiling, add direct unit coverage, and leave optimizer search behavior, GIF quality/frame preservation, MP4 encoding, framing, and UI layout unchanged.
- Versioning: increment development tester from `0.1.0-dev.5` to `0.1.0-dev.6`.

## PFC-2026-09-10-015 — Restore gifski 1.32.0 and document frame-preservation tradeoff

- Target files: Windows gifski build dependency, development version metadata, GIF architecture/history/status docs, third-party/build docs, required tracking files.
- Relevant history checked: `PROJECT_CONTRACT.md`, `MASTER.md`, `PRE_FLIGHT_Check.md`, `CHANGELOG.md`, `HISTORY/REFERENCE_GIF_CONVERTER.md`, `docs/ARCHITECTURE.md`, current Windows workflow, current converter, current third-party/build docs, the exact standalone `HeroForge_WebP_to_Reddit_GIF.py`, and gifski 1.34.0 CLI/Y4M source handling.
- Human validation: dev.4 changed only gifski 1.32.0 -> 1.34.0 and regressed the same Viper conversion from dev.3's `1592x1592` to `1532x1532`.
- Confirmed root cause of the larger standalone `1756x1756` result: the standalone wrote source FPS into Y4M with FFmpeg `-r` but omitted gifski `--fps`; gifski defaults Y4M/video input to 20 FPS and its Y4M decoder skips frames to resample toward that target.
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
- Diagnosis: the current Polymorph GIF shown in Windows Explorer is already about `93.8 MB`, so the remaining resolution gap is not plausibly explained by unused size headroom alone. The canonical standalone FFmpeg command does not force a YUV pixel format before `yuv4mpegpipe`; Polymorph uniquely forced `yuv444p`.
- Conflict risks: changing optimizer thresholds simultaneously would make the A/B result ambiguous; changing MP4 would disturb an already-validated output path.
- Recommended action: remove only the forced GIF-path `yuv444p`, preserve explicit source FPS, gifski quality/extra/repeat/width settings and integrity verification, update the smoke test to exercise the same handoff, and retest the same Viper source before touching optimizer logic.
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
- Connected modules reviewed: frozen tool discovery, packaged SVG resource lookup, `MainWindow` construction, Qt animated-WebP preview, linked-resolution controls, PyInstaller output path.
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
