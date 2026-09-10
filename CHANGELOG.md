# Changelog

## POLY-2026-09-10-017 — 2026-09-10 03:02 PDT — Harden verified update downloads

### Summary

- Hardened the automatic updater without changing the visible update flow or any conversion behavior.
- Automatic installation now requires the exact canonical installer asset `Polymorph_Setup_v<version>.exe` and its exact `.exe.sha256` companion from the same official GitHub release.
- Restricted automatic update downloads to HTTPS release URLs under `github.com/Knight-Witch/Polymorph/releases/download/`.
- Replaced whole-file installer hashing with bounded streaming download plus incremental SHA-256 hashing, avoiding an unnecessary ~85 MB in-memory buffer.
- Added explicit maximum download sizes for checksum and installer assets and delete partial downloads on failure.
- Added strict checksum parsing: valid 64-character SHA-256 required; when the checksum line includes a filename, it must match the selected installer exactly.
- Added unit coverage for exact asset pairing, wrong checksum assets, official URL restriction, checksum filename validation, streamed hashing, and oversized-download rejection.
- GIF, MP4, file-size optimizer, framing, preview, UI layout, and installer privilege behavior were not changed.
- Incremented the development tester to `0.1.0-dev.7`.

### Touched files

- `src/polymorph/update_service.py`
- `tests/test_update_service.py`
- `src/polymorph/__init__.py`
- `src/polymorph/constants.py`
- `pyproject.toml`
- `installer/Polymorph.iss`
- `docs/ARCHITECTURE.md`
- `MASTER.md`
- `PRE_FLIGHT_Check.md`
- `CHANGELOG.md`

### Rollback

- Revert this commit to restore the dev.6 updater behavior while leaving the decimal-MB conversion fix intact.

### Test notes

- New updater tests are network-independent and use in-memory fake responses for streaming behavior.
- Windows unit/toolchain/frozen-EXE/installer gates must pass before dev.7 becomes the current development tester.
- No human media-quality retest is required because conversion code is untouched.

## POLY-2026-09-10-016 — 2026-09-10 02:48 PDT — Normalize file-size ceilings to decimal MB

### Summary

- Corrected the user-defined file-size ceiling so `MB` now means decimal megabytes: 1 MB = 1,000,000 bytes.
- The prior calculation used `1024 * 1024`, so a displayed `99 MB` ceiling actually allowed 103,809,024 bytes and could exceed a platform's decimal 100 MB upload limit.
- Added a small centralized size-unit helper and direct unit tests for decimal MB conversion.
- Kept the file-size optimizer search strategy unchanged; only the byte ceiling supplied to it changes.
- Kept GIF quality 100, gifski 1.32.0, `yuv420p`, explicit source FPS/frame preservation, infinite looping, output-dimension verification, MP4 encoding, framing, and UI layout unchanged.
- Incremented the development tester to `0.1.0-dev.6`.

### Touched files

- `src/polymorph/size_units.py`
- `src/polymorph/converter.py`
- `tests/test_size_units.py`
- `src/polymorph/__init__.py`
- `src/polymorph/constants.py`
- `pyproject.toml`
- `installer/Polymorph.iss`
- `docs/ARCHITECTURE.md`
- `MASTER.md`
- `PRE_FLIGHT_Check.md`
- `CHANGELOG.md`

### Rollback

- Revert this commit to restore binary-MiB interpretation of the `MB` ceiling and the dev.5 version metadata.

### Test notes

- Pure unit conversion is covered directly: `99 MB -> 99,000,000 bytes` and fractional decimal MB values round deterministically.
- Because the corrected ceiling is stricter than prior builds, size-constrained outputs may be slightly smaller in spatial resolution; that is expected and not a GIF-quality regression.
- Windows run #12 completed successfully through unit tests, pinned toolchain verification, frozen application smoke test, installer compilation, checksum generation, and artifact upload.
- Dev.6 installer SHA-256 was independently recomputed after artifact download and matched the generated checksum.

## POLY-2026-09-10-015 — 2026-09-10 02:20 PDT — Restore gifski 1.32.0 and confirm frame-preservation tradeoff

### Summary

- Human dev.4 retest produced `1532x1532`, regressing from dev.3's `1592x1592`; gifski 1.34.0 is therefore not retained for this workload.
- Re-read the exact standalone converter and gifski's Y4M implementation. The standalone used FFmpeg `-r <source fps>` but omitted gifski `--fps`; gifski defaults Y4M/video input to 20 FPS and its Y4M decoder skips frames when required to meet that target.
- This confirms the main reason the standalone converter could produce a larger `1756x1756` GIF under the same byte ceiling: it was not preserving the complete source frame sequence.
- Preserving source FPS/frame count is a hard Polymorph requirement, so the standalone `1756x1756` result is no longer treated as the correct spatial-resolution parity target.
- Restored the bundled development gifski dependency from 1.34.0 to the better-performing, previously human-validated 1.32.0 build.
- Kept `yuv420p`, explicit source FPS, gifski quality 100, extra effort, infinite repeat, explicit width, post-encode dimension/frame/timing verification, file-size optimizer, and MP4 path unchanged.
- Updated architecture/history/status documentation to distinguish standalone visual-quality parity from Polymorph's stricter frame-preservation requirement.
- Incremented the development tester to `0.1.0-dev.5`.

### Touched files

- `.github/workflows/windows-dev-build.yml`
- `src/polymorph/__init__.py`
- `src/polymorph/constants.py`
- `pyproject.toml`
- `installer/Polymorph.iss`
- `THIRD_PARTY.md`
- `build/README.md`
- `docs/ARCHITECTURE.md`
- `HISTORY/REFERENCE_GIF_CONVERTER.md`
- `MASTER.md`
- `PRE_FLIGHT_Check.md`
- `CHANGELOG.md`

### Rollback

- Revert this commit to return to the gifski 1.34.0 dev.4 experiment. Converter and MP4 logic are identical across dev.4 and dev.5.

### Test notes

- Root-cause diagnosis is supported by the exact standalone command and gifski's Y4M decoder source.
- No converter code or optimizer code changed in this update.
- Windows unit/toolchain/frozen-EXE/installer gates passed for dev.5; no further Viper quality retest is required solely to re-establish the already human-validated dev.3 GIF engine behavior.

## POLY-2026-09-10-014 — 2026-09-10 01:12 PDT — Test stable gifski 1.34.0

### Summary

- Human dev.3 retest reported good animation smoothness and a `1592x1592` Viper GIF, only slightly above the prior `1570x1570` result and still materially below the canonical standalone `1756x1756` output.
- Color remained too subtle to judge reliably.
- Re-read the standalone converter and confirmed it only enforces gifski `>=1.32.0`; it does not establish that the successful standalone output used exactly 1.32.0.
- Identified Polymorph's exact 1.32.0 pin as the next isolated upstream mismatch.
- Updated only the bundled development gifski dependency to stable 1.34.0. The 1.34.0 release notes document palette-quality improvements from a newer `libimagequant`.
- Converter code, GIF command line, `yuv420p` Y4M handoff, source-FPS safeguard, explicit gifski width, quality 100, extra effort, repeat behavior, post-encode integrity checks, size optimizer, and MP4 path were not changed.
- Updated development packaging/documentation and incremented the tester to `0.1.0-dev.4`.

### Touched files

- `.github/workflows/windows-dev-build.yml`
- `src/polymorph/__init__.py`
- `src/polymorph/constants.py`
- `pyproject.toml`
- `installer/Polymorph.iss`
- `THIRD_PARTY.md`
- `build/README.md`
- `HISTORY/REFERENCE_GIF_CONVERTER.md`
- `MASTER.md`
- `PRE_FLIGHT_Check.md`
- `CHANGELOG.md`

### Rollback

- Revert this commit to restore gifski 1.32.0 and the dev.3 tester metadata. Converter/MP4 code is identical across the two builds.

### Test notes

- This is an isolated dependency A/B, not an optimizer change.
- Windows unit/toolchain/frozen-EXE/installer gates passed before dev.4 was handed to the user.
- Human retest used the same Viper source and established that 1.34.0 was worse for this workload.

## POLY-2026-09-10-013 — 2026-09-10 00:45 PDT — Pin GIF Y4M to yuv420p

### Summary

- Windows CI run #8 proved that literal removal of GIF `-pix_fmt` is not reliable on the pinned FFmpeg 9.0.1 Windows build: after Polymorph's filter graph, FFmpeg retained a non-Y4M-compatible intermediate and `yuv4mpegpipe` refused to write its header.
- Replaced the failed auto-negotiation experiment with explicit `yuv420p`, reproducing the canonical standalone converter's effective 4:2:0 Y4M handoff deterministically.
- Kept the validated GIF settings unchanged: source FPS handoff, gifski quality 100, extra effort, infinite repeat, explicit output width, and post-encode dimension/frame/timing verification.
- Kept the file-size optimizer unchanged so the Viper retest isolates the pixel-format difference.
- Kept the human-validated MP4 path unchanged.
- Fixed the Windows smoke test's failure-cleanup pipe handling so it no longer asks `communicate()` to read an already closed FFmpeg stdout pipe.
- Updated the durable GIF reference history with the failed no-pixel-format probe and deterministic `yuv420p` decision.
- Incremented the development tester to `0.1.0-dev.3`; dev.2 never produced an installer because its smoke gate failed.

### Touched files

- `src/polymorph/converter.py`
- `src/polymorph/__init__.py`
- `src/polymorph/constants.py`
- `build/verify_toolchain.py`
- `pyproject.toml`
- `installer/Polymorph.iss`
- `HISTORY/REFERENCE_GIF_CONVERTER.md`
- `docs/ARCHITECTURE.md`
- `MASTER.md`
- `PRE_FLIGHT_Check.md`
- `CHANGELOG.md`

### Rollback

- Revert this commit to return to the failed `0.1.0-dev.2` auto-negotiation experiment. The prior validated tester remains commit `3305139` / dev.1.

### Test notes

- Run #8 failure was diagnosed from the exact Windows job log before editing.
- New unit/toolchain/frozen-EXE/installer gates passed before dev.3 was handed to the user.
- Human A/B validation confirmed smoothness remained good and recovered only a small amount of spatial resolution.

## POLY-2026-09-10-012 — 2026-09-10 00:30 PDT — Restore canonical Y4M handoff for GIF

### Summary

- Recorded the successful human retest of the width-corrected GIF: visual quality now matches the standalone converter and may be slightly smoother framewise.
- Recorded the remaining measured scale difference: Polymorph `1570x1570` versus standalone `1756x1756` at the same nominal size target, plus only a possible subtle red/pink color difference.
- Rechecked the actual size context before editing: the Polymorph result shown in Windows Explorer is already about `93.8 MB`, so the remaining scale difference is not plausibly explained by simple unused file-size headroom.
- Compared the GIF pixel handoff against the canonical standalone converter and found the remaining material difference: Polymorph forced `yuv444p`; the standalone FFmpeg command did not force a YUV pixel format before `yuv4mpegpipe`.
- Removed only the forced GIF-path `yuv444p` so the Y4M handoff again matches the validated standalone pipeline.
- Preserved Polymorph's explicit source-FPS handoff, gifski quality 100, extra effort, infinite repeat, explicit output width, post-encode dimensions, exact frame count, and timing verification.
- Updated the Windows toolchain smoke test to exercise the same negotiated Y4M handoff and verify both dimensions and frame count.
- Left file-size optimizer logic and the already human-validated MP4 path unchanged so the next Viper comparison isolates this variable.
- Added `HISTORY/REFERENCE_GIF_CONVERTER.md` as the durable canonical standalone reference record.
- Incremented the development tester to `0.1.0-dev.2` so the replacement installer is distinguishable from the prior build.

### Touched files

- `src/polymorph/converter.py`
- `src/polymorph/__init__.py`
- `src/polymorph/constants.py`
- `build/verify_toolchain.py`
- `pyproject.toml`
- `installer/Polymorph.iss`
- `HISTORY/REFERENCE_GIF_CONVERTER.md`
- `docs/ARCHITECTURE.md`
- `MASTER.md`
- `PRE_FLIGHT_Check.md`
- `CHANGELOG.md`

### Rollback

- Revert this commit to restore the forced `yuv444p` GIF handoff and the `0.1.0-dev.1` tester metadata. MP4 behavior is unchanged by this commit.

### Test notes

- The canonical standalone script was re-read before editing.
- Current dev conversion optimizer was reviewed and deliberately left unchanged for isolation.
- Windows unit/toolchain/frozen-EXE/installer gates passed for the working follow-up build.

## POLY-2026-09-09-011 — 2026-09-09 23:57 PDT — Restore canonical gifski output width

### Summary

- First hands-on HeroForge media comparison validated MP4 visually with no reported issue.
- The same test found the Polymorph GIF substantially blurrier, grainier in gradients, and much smaller in actual pixel dimensions than the immediately preceding standalone converter result.
- Compared Polymorph against the validated standalone `HeroForge_WebP_to_Reddit_GIF.py` and confirmed Polymorph had omitted the reference converter's explicit gifski `--width` argument.
- Restored explicit gifski width control so gifski cannot apply its default conservative automatic animation downsize.
- Extended output integrity validation to require actual encoded dimensions to exactly match the dimensions Polymorph requested, in addition to existing exact frame-count and bounded-duration checks.
- Added regression coverage for output-dimension mismatch.
- Retained Polymorph's explicit source-FPS handoff and temporal integrity checks; those protect the no-frame-loss requirement and are not part of the confirmed quality regression.
- MP4 encoding settings, framing behavior, UI, updater, and installer architecture were not changed.
- Logged the separate binary-MiB-vs-decimal-MB ceiling issue for a later isolated fix.

### Touched files

- `src/polymorph/converter.py`
- `src/polymorph/integrity.py`
- `tests/test_integrity.py`
- `docs/ARCHITECTURE.md`
- `MASTER.md`
- `PRE_FLIGHT_Check.md`
- `CHANGELOG.md`

### Rollback

- Revert this commit to restore the pre-fix GIF path; MP4 remains unaffected either way.

### Test notes

- Root cause is directly supported by the standalone converter and gifski CLI behavior.
- Windows gates passed before the replacement installer was handed back for Viper retest.
- Human visual validation confirmed the corrected GIF quality was excellent.

## POLY-2026-09-09-010 — 2026-09-09 19:45 PDT — Record successful Windows smoke-gated build

### Summary

- Recorded successful Windows run #6 for commit `b3cfdda`.
- The frozen `Polymorph.exe` smoke gate passed before installer compilation.
- Inno Setup, SHA-256 generation, and artifact uploads also passed.
- The dev installer is 88,997,108 bytes and its recomputed local SHA-256 matches the generated checksum: `ef1ba4562be7d81ac70a4b261ad204e98f8da2c114cdc836b0ee972df1675177`.
- Marked the current dev build ready for hands-on HeroForge animated-WebP testing.
- Documentation-only update; no Python, workflow, installer definition, JavaScript, manifest, or runtime behavior changed.

### Touched files

- `MASTER.md`
- `PRE_FLIGHT_Check.md`
- `CHANGELOG.md`

### Rollback

- Revert this documentation commit only; the validated `b3cfdda` tester binary remains unchanged.

### Test notes

- Windows CI run #6 completed successfully from checkout through artifact upload.
- Packaged-app smoke test passed bundled-tool discovery, SVG resource loading, Qt animated-WebP live preview, and linked 16:9 resolution controls.
- Human Windows validation with real HeroForge animated WebP media followed successfully.

## POLY-2026-09-09-009 — 2026-09-09 19:34 PDT — Gate installer on packaged application smoke test

### Summary

- Added a hidden CI-only `--smoke-test` application path.
- The actual frozen `Polymorph.exe` now must prove it can resolve bundled FFmpeg/ffprobe/gifski, load packaged footer SVGs, construct the main window, decode an animated WebP into the live preview, and maintain linked 16:9 resolution controls.
- Reused the synthetic animated WebP from the existing toolchain smoke test rather than introducing a second media generator.
- Installer compilation is blocked if the packaged-app smoke test fails.
- Normal GUI/drag-to-open behavior is unchanged unless the hidden smoke-test flag is explicitly supplied.

### Touched files

- `src/polymorph/app.py`
- `src/polymorph/smoke_test.py`
- `build/verify_toolchain.py`
- `.github/workflows/windows-dev-build.yml`
- `build/README.md`
- `MASTER.md`
- `PRE_FLIGHT_Check.md`
- `CHANGELOG.md`

### Rollback

- Revert this commit to remove the packaged-EXE gate and restore the prior build workflow.

### Test notes

- Unit/toolchain tests remain upstream of PyInstaller.
- Packaged-app gate passed on Windows run #6 before Inno Setup compiled the installer.
- Human HeroForge media validation was subsequently completed.

## POLY-2026-09-09-008 — 2026-09-09 19:25 PDT — First-pass UI usability polish

### Summary

- Linked fixed-resolution width and height automatically to the active framed aspect ratio, while retaining no-upscale limits.
- Changed Crop preview dragging so the visible image follows the user's drag direction; Fit offset semantics remain unchanged.
- Replaced development footer text placeholders with monochrome GitHub, Ko-fi, Patreon, Discord, and update icons plus hover tooltips.
- Added packaged SVG resource lookup for source and frozen builds and documented Simple Icons attribution.
- Final Polymorph application emblem remains deferred; the generated development app icon is unchanged.

### Touched files

- `src/polymorph/geometry.py`
- `src/polymorph/resources.py`
- `src/polymorph/assets/*.svg`
- `src/polymorph/ui/main_window.py`
- `src/polymorph/ui/preview.py`
- `src/polymorph/ui/resolution_linker.py`
- `src/polymorph/ui/styles.py`
- `tests/test_geometry.py`
- `pyproject.toml`
- `build/Polymorph.spec`
- `THIRD_PARTY.md`
- `docs/UX_SPEC.md`
- `PRE_FLIGHT_Check.md`
- `CHANGELOG.md`

### Rollback

- Revert this commit to restore independent resolution fields, prior Crop drag semantics, and text-placeholder footer controls.

### Test notes

- Linked-dimension math is covered by unit tests for 16:9 width/height driving and native-size clamping.
- SVG resource inclusion is declared both as Python package data and explicit PyInstaller data.
- Packaged Qt smoke tests subsequently confirmed resource and preview loading.

## POLY-2026-09-09-007 — 2026-09-09 19:22 PDT — Pin and smoke-test smaller FFmpeg Essentials build

### Summary

- Replaced the mutable/latest full BtbN FFmpeg download in the dev build workflow with the exact Gyan FFmpeg 9.0.1 Essentials archive.
- Added verification against the provider-published SHA-256 before extraction.
- Added a build-time animated WebP smoke test covering ffprobe frame counting, Crop/Scale/Pad filters, YUV4MPEG streaming into gifski, infinite-loop GIF encoding, H.264 MP4 encoding, and output frame-count preservation.
- Recorded the exact development FFmpeg bundle/source reference in third-party documentation.
- No application conversion settings or UI behavior changed.

### Touched files

- `.github/workflows/windows-dev-build.yml`
- `build/verify_toolchain.py`
- `build/README.md`
- `THIRD_PARTY.md`
- `MASTER.md`
- `PRE_FLIGHT_Check.md`
- `CHANGELOG.md`

### Rollback

- Revert this commit to restore the previous BtbN master GPL build acquisition.

### Test notes

- Provider documentation confirms the Essentials build includes libwebp and libx264 and all internal Windows FFmpeg components.
- Exact bundled toolchain behavior is gated by the Windows smoke-test step; installer artifacts are not accepted if that step fails.

## POLY-2026-09-09-006 — 2026-09-09 19:12 PDT — Correct PyInstaller repository root

### Summary

- Fixed the Windows build failure in `build/Polymorph.spec` by resolving the repository root from PyInstaller's `SPECPATH` directory correctly.
- No converter, UI, dependency, installer, or runtime behavior changed.

### Touched files

- `build/Polymorph.spec`
- `PRE_FLIGHT_Check.md`
- `CHANGELOG.md`

### Rollback

- Revert this commit to restore the previous spec path calculation.

### Test notes

- Windows run #1 passed unit tests, FFmpeg acquisition, gifski 1.32.0 compilation, and placeholder icon generation before failing at PyInstaller with `script 'D:\\a\\Polymorph\\run_polymorph.py' not found`.
- The corrected root resolves to the checked-out repository directory `D:\\a\\Polymorph\\Polymorph`.
- Windows run #3 subsequently passed all build, installer, checksum, and artifact-upload steps.

## POLY-2026-09-09-005 — 2026-09-09 19:09 PDT — Verify frame/timing integrity after encoding

### Summary

- Made source probing tolerant of ffprobe decoder failure when animated WebP RIFF metadata already supplies valid dimensions, frame count, and duration.
- Added explicit nominal FPS storage instead of relying only on frame-count/duration reconstruction.
- Added post-encode integrity verification requiring exact frame-count preservation and bounded duration drift.
- Added tests for RIFF-only fallback and temporal integrity rules.

### Touched files

- `src/polymorph/models.py`
- `src/polymorph/probe.py`
- `src/polymorph/integrity.py`
- `src/polymorph/converter.py`
- `tests/test_probe_fallback.py`
- `tests/test_integrity.py`
- `docs/ARCHITECTURE.md`
- `PRE_FLIGHT_Check.md`
- `CHANGELOG.md`

### Rollback

- Revert this commit to return to pre-verification probing/encoding behavior.

### Test notes

- Pure integrity/probe logic is covered by unit tests.
- Full output verification is also exercised in the Windows toolchain/frozen application pipeline.

## POLY-2026-09-09-004 — 2026-09-09 18:28 PDT — Windows development packaging

### Summary

- Wired the canonical Ko-fi, Patreon, and Discord destinations into the footer.
- Added PyInstaller one-directory packaging with bundled FFmpeg, ffprobe, and gifski binaries.
- Added a deliberately temporary generated `.ico` for development builds.
- Added a per-user Inno Setup installer targeting `%LOCALAPPDATA%\\Programs\\Polymorph` with optional desktop shortcut and no administrator requirement.
- Added a Windows GitHub Actions development build that runs tests, obtains the conversion toolchain, builds the app and installer, generates SHA-256, and uploads workflow artifacts.
- Development workflow does not publish a GitHub Release.

### Touched files

- `src/polymorph/constants.py`
- `build/**`
- `installer/Polymorph.iss`
- `.github/workflows/windows-dev-build.yml`
- `PRE_FLIGHT_Check.md`
- `CHANGELOG.md`

### Rollback

- Revert the packaging commit; application/core dev code remains on the prior `dev` head.

### Test notes

- Packaging definitions reviewed for one-directory dependency placement and per-user install behavior.
- Windows run #3 produced a successful installer artifact (~126.6 MB) and unpacked application artifact (~435 MB before ZIP compression).

## POLY-2026-09-09-003 — 2026-09-09 18:28 PDT — Functional desktop UI and updater scaffold

### Summary

- Added PySide6 main window with multi-file queue, drag/drop, animated WebP preview, GIF/MP4 selection, mutually exclusive sizing modes, framing controls, output folder selection, and conversion progress.
- Added live Original / Crop / Fit preview with drag repositioning and Fit background color.
- Added aspect-ratio guide dialog and development footer controls for updates, GitHub, Ko-fi, Patreon, and Discord.
- Added automatic update checks while the app is open and verified installer download support; no background service/daemon.
- Added a lightweight placeholder arcane progress animation so final sigil styling can be swapped in without restructuring the UI.
- Preview uses non-caching animation playback so large source animations are not intentionally retained frame-by-frame in RAM.

### Touched files

- `src/polymorph/app.py`
- `src/polymorph/ui/**`
- `src/polymorph/update_service.py`
- `run_polymorph.py`
- `tests/test_update_service.py`
- `PRE_FLIGHT_Check.md`
- `CHANGELOG.md`

### Rollback

- Revert the UI/updater commit; core conversion modules remain independently testable.

### Test notes

- 8/8 local non-GUI tests passed at the time.
- Python source syntax compilation passed.
- Packaged Qt/Windows interaction is now covered by the frozen-app smoke gate.

## POLY-2026-09-09-002 — 2026-09-09 18:28 PDT — Core conversion engine scaffold

### Summary

- Added modular media probe, WebP RIFF fallback parser, framing geometry, FFmpeg filter construction, tool discovery, and conversion orchestration.
- Preserved the canonical FFmpeg -> YUV4MPEG -> gifski path with quality 100, extra effort, infinite repeat, no PNG intermediates, and explicit source FPS handoff to avoid gifski's default 20 FPS resampling.
- Added H.264 MP4 output scaffold.
- Added file-size-constrained resolution optimization, fixed-resolution no-upscale validation, collision-safe output naming, and a variable-frame-duration safeguard that refuses silent GIF resampling.
- Added unit tests for framing geometry and RIFF parsing.

### Touched files

- `src/polymorph/{__init__,constants,models,probe,geometry,filters,tools,converter}.py`
- `tests/**`
- `pyproject.toml`
- `.gitignore`
- `PRE_FLIGHT_Check.md`
- `CHANGELOG.md`
- `MASTER.md`

### Rollback

- Revert the core scaffold commit; `main` remains documentation-only/unreleased.

### Test notes

- Core-engine unit tests pass.
- Actual output quality has since been human-validated against real HeroForge media.

## POLY-2026-09-09-001 — 2026-09-09 18:28 PDT — Repository bootstrap

### Summary

- Established Polymorph as a standalone public repository.
- Defined the project contract, canonical conversion priorities, v1 UX scope, architecture boundaries, and third-party dependency notes.
- Witch Dock was not modified.

### Touched files

- `README.md`
- `PROJECT_CONTRACT.md`
- `MASTER.md`
- `PRE_FLIGHT_Check.md`
- `CHANGELOG.md`
- `THIRD_PARTY.md`
- `docs/ARCHITECTURE.md`
- `docs/UX_SPEC.md`

### Rollback

- Revert the bootstrap documentation commit.

### Test notes

- Documentation-only bootstrap; no public executable, installer, or runtime behavior released.
