# Changelog

## POLY-2026-09-21-002 — Repository licensing

### Summary

- Added `LICENSE` with the Knight Witch Community Source License v1.0.
- Updated `README.md` to document the selected source license.
- Normal personal and professional use is permitted, including commercial work product created with Polymorph; redistribution, repackaging, hosted-service use of the software itself, and software commercialization remain reserved.
- Existing `THIRD_PARTY.md` remains authoritative for FFmpeg/ffprobe, gifski, PySide6/Qt, PyInstaller, and other third-party components.
- No conversion, UI, packaging, update, or runtime behavior changed.

### Commits

- License: `3a155f70665a36c96251b1706b81bc4da9b3779d`
- README: `01e802d7eb0dd67d17e4a3f7901fe4b3f2b9a56d`

### Test notes

Documentation-only licensing change. No executable or installer was modified.

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
