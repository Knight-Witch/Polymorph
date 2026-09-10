# Polymorph Project Contract

## Editing rules

- Treat working conversion behavior as production behavior unless explicitly marked experimental.
- Diagnose before editing quality-critical conversion code.
- Preserve proven GIF behavior: FFmpeg -> YUV4MPEG streaming -> gifski, quality 100, extra effort, no temporary PNG frame pipeline, no deliberate frame-rate reduction.
- Optimize file-size-constrained outputs by resolution scaling, not frame dropping or hidden quality reduction.
- Do not upscale source content above native size.
- Keep UI, conversion engine, preview/framing, updater, and packaging concerns modular.
- Do not silently add background services, telemetry, startup tasks, cloud uploads, or administrator requirements.
- Keep the default UI novice-friendly; codec jargon belongs outside the primary interface.

## Tracking files

Before a committed project update, review:

1. `PROJECT_CONTRACT.md`
2. `MASTER.md`
3. `PRE_FLIGHT_Check.md`
4. `CHANGELOG.md`
5. Relevant files under `docs/`
6. Target files and directly connected modules

Every committed project update after bootstrap must update `CHANGELOG.md` and add a concise `PRE_FLIGHT_Check.md` entry.

## Release rules

- `main` is public/stable documentation and validated release code.
- Development work should occur on `dev` until validated.
- Public releases must include source, installer, checksum, dependency/license notes, and rollback/test notes.
- Auto-update checks must target only official Polymorph releases.
