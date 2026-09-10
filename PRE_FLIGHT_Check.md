# Polymorph Pre-Flight Log

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

- Target files: `src/polymorph/{constants,models,probe,geometry,filters,tools,converter}.py`, tests, `pyproject.toml`, tracking docs.
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
