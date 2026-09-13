# Polymorph Master

This file is the compact repo-wide status/index. For the current task and exact next step, read `ACTIVE_CONTEXT.md` instead.

## Current state

- Repository: `Knight-Witch/Polymorph`
- Target: Windows 10/11 x64
- Development branch: `dev`
- Current runtime version: `0.1.0-dev.23`
- Public release: none yet
- Current phase: branded UI fidelity. Core conversion/framing/adaptive behavior is considered functionally complete for current v1 scope.

## Protected validated state

- GIF Preserve motion: human-validated quality/smoothness, exact source-frame/timing intent, decimal-MB ceiling behavior, FFmpeg -> YUV4MPEG -> gifski 1.32.0, quality 100, `--extra`, infinite repeat, no source upscale.
- GIF Favor resolution: explicit opt-in, validated on Viper plus two harder HeroForge variants using exact original-source-frame stride candidates, measured-gain gating, ~8 FPS automatic floor, exact loop-closure timing repair and no optical-flow/blended frames.
- MP4: human-validated H.264 output and established size-search behavior.
- Framing: Original/Crop/Fit share one geometry resolver; Crop/Fit preview and real exports are human-validated end to end. Crop zoom shrinks the retained source window; Fit preserves the full source aspect ratio.
- Windows external tools: ffmpeg/gifski/ffprobe run without focus-stealing console flashes.
- Updater: official GitHub release assets only, exact installer + `.sha256`, bounded HTTPS download and SHA-256 verification, no background daemon/startup task.

Detailed engine behavior lives in `docs/ARCHITECTURE.md`. Canonical OG/adaptive evidence lives in the targeted files under `HISTORY/`.

## Branded UI state

- Canonical visual/behavior spec: `docs/UX_SPEC.md`.
- Approved mockup is the active visual target.
- Composition: two columns; queue + dominant preview on the left, compact settings/action rail on the right.
- Design geometry `1260x820`; supported minimum `920x640`. dev.21 proportional shrink behavior is human-accepted.
- Palette: near-black/charcoal, ivory, champagne gold, restrained crimson.
- dev.22 added vector-first branded icons with PNG fallback.
- dev.23 makes display typography self-contained. Approved Trajan Regular/Bold assets are bundled/registered before UI construction; friends do not need Trajan installed separately. Inter is the body/UI face; Cinzel is an emergency development fallback only.
- Header: `POLYMORPH` + `Media conversion magic — by Knight Witch™`; version stays in footer.
- Primary action copy: `POLYMORPH`.
- Queue actions, playback controls, sizing modes, GIF priority, framing radios, output-folder behavior and footer links are real functionality, not decorative mockup placeholders.
- Working/loading animation is intentionally deferred until current layout/typography fidelity is accepted. Arcane-circle and D20 concepts remain open.

## Build/test posture

- Canonical build: `.github/workflows/windows-dev-build.yml`.
- Keep pinned FFmpeg 9.0.1 and gifski 1.32.0 unless evidence requires a deliberate migration.
- CI includes unit tests, pinned font/toolchain verification, adaptive integration, canonical GIF reference comparison, PyInstaller frozen-app smoke, Inno Setup installer, checksum and artifacts.
- Current dev.23 code commit `81150b0e7007969d260317c9383ed7bacb3362b9` passed Windows Dev Build run #54 (`34779195156`). Exact artifact identity and the current human gate are recorded in `ACTIVE_CONTEXT.md`.

## Routing index

- Current task / next gate: `ACTIVE_CONTEXT.md`
- Binding workflow/safety rules: `PROJECT_CONTRACT.md`
- Compact assistant instructions: `CHATGPT_PROJECT_INSTRUCTIONS.md`
- Engine/packaging architecture: `docs/ARCHITECTURE.md`
- UI/visual behavior: `docs/UX_SPEC.md`
- Patched-Python GIF reference: `HISTORY/REFERENCE_GIF_CONVERTER.md`
- GIF timing evidence: `HISTORY/DIAGNOSTICS/GIF_REFERENCE_TIMING_2026-09-10.md`
- Adaptive evidence: `HISTORY/DIAGNOSTICS/GIF_ADAPTIVE_MOTION_2026-09-10.md`
- Archived tracking snapshots: `HISTORY/PROJECT_LOGS/`

## Remaining v1 work

- Human-review dev.23 without separately installing Trajan; continue approved-mockup visual fidelity from that evidence.
- Human-test preview timeline scrubbing on normal Windows; offscreen frozen CI intentionally does not random-seek `QMovie` because that path can wedge the headless WebP plugin.
- Design/implement the working/loading animation after structural/typography acceptance.
- Decide final application emblem/icon.
- Before first public release: deliberate project-license choice, final release/package review, and code-signing/SmartScreen decision.

Deferred: advanced user FPS controls, ETA, advanced codec controls, parallel jobs, macOS/Linux packaging.
