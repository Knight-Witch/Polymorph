# Changelog

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
- New packaged-app gate will run on the Windows CI artifact before Inno Setup compiles the installer.
- Human HeroForge media validation remains required after the CI gate passes.

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
- Full Qt interaction remains pending hands-on Windows testing.

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
- Exact bundled toolchain behavior remains gated by the new Windows smoke-test step; installer artifact is not accepted if that step fails.

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
- Full output verification still requires the Windows dev build against real HeroForge animated WebPs.

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

- 8/8 local non-GUI tests pass.
- Python source syntax compilation passes.
- Full Qt/Windows interaction remains pending hands-on testing.

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
- Actual quality behavior remains subject to reference-media Windows validation.

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
