# Changelog

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
- Actual Windows build result pending GitHub Actions validation after commit.

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
- Qt runtime could not be exercised in the current Linux container because PySide6 is not installed and the container has no package-network access.
- Full Qt/Windows behavior remains unvalidated pending GitHub Actions build.

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

- 5/5 local core-engine tests pass.
- Python source syntax compilation passes.
- Actual FFmpeg/gifski conversion still requires Windows/reference-media validation.

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
