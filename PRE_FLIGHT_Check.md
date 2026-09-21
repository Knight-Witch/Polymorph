# Polymorph Pre-Flight Log

## PFC-2026-09-21-002 — Repository licensing

- Target files: `LICENSE`, `README.md`, tracking records.
- Reviewed `PROJECT_CONTRACT.md`, current README license placeholder, and `THIRD_PARTY.md`.
- Confirmed the project license must not purport to relicense FFmpeg, gifski, PySide6/Qt, PyInstaller, or other third-party components.
- Selected the Knight Witch Community Source License v1.0 for Knight Witch-owned source.
- Normal personal/professional use and commercial output creation remain permitted; redistribution/commercialization of the software itself remains restricted.
- No conversion behavior, quality settings, packaging, updater, background service, cloud behavior, or runtime source changed.
- No runtime testing required for this documentation-only update.

## PFC-2026-09-09-001 — Repository bootstrap

- Target files: repository contract, project status, changelog/pre-flight tracking, architecture/UX docs, third-party dependency notes.
- Existing project history checked: repository was empty; no prior Polymorph history existed.
- Reference behavior checked: previously validated WebP -> GIF pipeline requirements were recorded as canonical behavior.
- Connected modules reviewed: Witch Dock remains a separate project and was not modified.
- Conflict risks: accidentally coupling Polymorph to Witch Dock; failing to preserve the validated GIF pipeline; public binary distribution before dependency/license review.
- Recommended action: keep application development isolated on `dev` and publish only validated builds.
