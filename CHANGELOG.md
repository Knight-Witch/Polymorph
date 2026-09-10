# Changelog

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
