# Polymorph Project Contract

**Status:** Binding development contract  
**Scope:** `Knight-Witch/Polymorph`, all active development work  
**Purpose:** Preserve validated media behavior while keeping future-chat startup context small and exact.

## Required bootstrap

Before material code, architecture, packaging, UI, migration, or committed documentation work:

1. Read this `PROJECT_CONTRACT.md`.
2. Read `ACTIVE_CONTEXT.md` on `dev`.
3. Read only the policy/history/source files routed by `ACTIVE_CONTEXT.md` or directly required by the task.
4. Inspect the target files and directly connected modules before editing.

Do **not** automatically reread the full `MASTER.md`, full changelog, full pre-flight log, archived project logs, diagnostics, or unrelated conversion/UI files. Git history is durable memory; old detail should be fetched only when materially relevant.

## Branch and release boundaries

- `dev` is the development/integration branch and normal tester source.
- `main` is public/stable documentation and validated release code. Do not use it as an experimental branch.
- No public GitHub Release is created until Amanda explicitly approves release readiness.
- Normal promotion order is: diagnose/reference -> Dev implementation -> static/unit/integration validation -> packaged Windows CI -> human visual/functional gate when relevant -> explicit release/promotion decision.
- Existing validated behavior is protected until a replacement has passed its required gate.

## Diagnose before editing

Determine what Polymorph actually does before changing behavior. Do not guess conversion, framing, Qt, packaging, or updater behavior when source, diagnostics, CI or a narrow reproduction can answer the question.

Classify technical claims as:

- **Confirmed** — observed in source/runtime/CI or validated by test.
- **Supported inference** — strongly supported but not directly proven.
- **Hypothesis** — plausible and unverified.

Preserve known-working timing, frame selection, encoding flags, sizing thresholds, geometry, polling, state sequencing, rollback, updater checks, UI wiring and responsive behavior unless testing proves a change is safe.

## Protected conversion behavior

- Preserve-motion GIF is the default and intentionally preserves source frames/timing. Use FFmpeg -> YUV4MPEG -> gifski, quality 100, `--extra`, infinite repeat, explicit width/source FPS, pinned gifski 1.32.0 and pinned FFmpeg 9.0.1. File-size fitting reduces spatial resolution rather than silently reducing motion or quality.
- Favor resolution is explicit opt-in and may reduce retained frames only through the validated exact-source-frame decimation policy documented in `docs/ARCHITECTURE.md`. Do not substitute optical flow, blending, hidden FPS changes or unmeasured heuristics.
- User-entered MB ceilings are decimal. Never upscale source content above native framed geometry.
- Original/Crop/Fit preview and export share the same framing geometry. Do not fork duplicate preview/export math.
- MP4, updater hardening and Windows no-console subprocess behavior are considered validated for current v1 scope unless new evidence directly implicates them.
- If Amanda supplies an adaptive diagnostic JSON, inspect it before any adaptive algorithm change.

## UI and visual acceptance

- `docs/UX_SPEC.md` is the canonical branded UI specification. The approved mockup is the active visual target, not loose inspiration.
- Packaged testers are self-contained for typography: the approved Trajan Regular/Bold faces are bundled and loaded by Polymorph; friends must not need a system font installation. Inter remains the body/UI face.
- Preserve human-accepted responsive behavior unless a concrete regression requires a change.
- Runtime correctness is not proof of visual correctness. Amanda's visual confirmation is required when typography, spacing, icon rendering, preview balance, gradients, animation or other appearance is part of acceptance.
- Do not add mockup-only controls that do not map to real application state or a real action.

## Build and tester discipline

- Use repository GitHub Actions as the canonical Windows build path; do not substitute a local compilation for release/test evidence.
- Every meaningful build must preserve the existing unit, toolchain, adaptive integration, GIF reference, PyInstaller frozen-app smoke, installer and checksum gates unless a documented diagnosis proves a gate itself is invalid.
- When Amanda needs a tester, retrieve the successful installer artifact and give it to her directly rather than sending her to the Actions UI.
- Record useful commit/run/artifact identity in `ACTIVE_CONTEXT.md` after meaningful build milestones so the next chat does not rediscover it.

## Durable documentation without context bloat

- `ACTIVE_CONTEXT.md` is the small current-task router. Keep only the present goal, protected PASS state, current candidate/build, next gate, and minimum continuation set.
- `MASTER.md` is a compact repo-wide architecture/status index, not a running investigation transcript.
- `CHANGELOG.md` and `PRE_FLIGHT_Check.md` are rolling current logs. Older detailed entries belong under `HISTORY/PROJECT_LOGS/` or in Git history.
- `docs/ARCHITECTURE.md` holds canonical technical behavior; `docs/UX_SPEC.md` holds canonical UI behavior.
- Targeted `HISTORY/*` files hold durable evidence/reference detail and are read only when routed by the current task.

Every committed repository update must update `CHANGELOG.md` and add a concise `PRE_FLIGHT_Check.md` record. Documentation-only changes must explicitly state that no runtime/version/package/public behavior changed.

Update `ACTIVE_CONTEXT.md` whenever the active task, next gate, protected state, active candidate/build, or minimum continuation set materially changes.

## Working style

Put `# TLDR` first. Diagnose before editing. Continue autonomously through safe investigation, implementation, CI and documentation instead of stopping at intermediate narration checkpoints. Use GitHub directly when available; do not claim connector access is missing without actually trying it.

Ask Amanda only for genuinely human actions or subjective validation. Do not make her repeat diagnostics or manually inspect build infrastructure when the repository/tools can answer the question.

## Final operating principle

Keep startup context tiny, treat `ACTIVE_CONTEXT.md` as the baton between chats, preserve validated behavior, build on `dev`, require human visual gates where appearance matters, and use Git/history as durable memory rather than mandatory prompt payload.
