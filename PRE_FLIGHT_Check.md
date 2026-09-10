# Polymorph Pre-Flight Log

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
