# Polymorph Pre-Flight Log

Historical entries through dev.23 are preserved verbatim in [`HISTORY/PROJECT_LOGS/PRE_FLIGHT_THROUGH_DEV23.md`](HISTORY/PROJECT_LOGS/PRE_FLIGHT_THROUGH_DEV23.md). Root tracking is intentionally rolling/compact; older detail is not mandatory startup reading.

## PFC-2026-09-13-040 — Establish compact cross-chat continuation system

- Required review completed before editing: current `PROJECT_CONTRACT.md`, `MASTER.md`, top/current tracking, `docs/ARCHITECTURE.md`, `docs/UX_SPEC.md`, dev.23 font implementation, current `dev` head/CI/artifacts, and the compact `ACTIVE_CONTEXT.md` / ChatGPT instruction pattern already proven in `Knight-Witch/KnightWitch.Heroforge`.
- Diagnosis: Polymorph had durable technical documentation but no small authoritative current-task router, so a new chat still had to reconstruct too much state from `MASTER.md`, changelog/pre-flight entries and conversation handoffs.
- Add root `ACTIVE_CONTEXT.md` as the authoritative baton between chats: current task, exact dev candidate/build/artifact, protected PASS state, minimum continuation set and next human gate only.
- Add `CHATGPT_PROJECT_INSTRUCTIONS.md` with the compact operating rules: TLDR first, diagnose before editing, use GitHub directly, work on `dev`, preserve validated conversion/UI boundaries, continue autonomously, use repo CI, hand tester artifacts directly to Amanda, and require human visual acceptance when appearance matters.
- Rewrite `PROJECT_CONTRACT.md` around the same efficient bootstrap used by Witch Dock: contract -> active context -> only routed/target files. Full history/changelog/pre-flight archives are explicitly non-default reading.
- Compact `MASTER.md` back into a repo-wide status/routing index. Preserve the exact pre-compaction dev.23 snapshot under `HISTORY/PROJECT_LOGS/MASTER_DEV23_SNAPSHOT.md`.
- Preserve exact pre-rollover root tracking as `PRE_FLIGHT_THROUGH_DEV23.md` and `CHANGELOG_THROUGH_DEV23.md`; reset root logs to rolling current entries.
- `ACTIVE_CONTEXT.md` records dev.23 code head `81150b0e7007969d260317c9383ed7bacb3362b9`, Windows run #54 PASS, installer artifact identity, the self-contained bundled-Trajan requirement, and the immediate human visual gate so the next chat does not redo the font investigation.
- Documentation-only handoff change. No runtime code, UI behavior, conversion/framing/adaptive policy, version metadata, packaging inputs, updater behavior, toolchain pin, installer behavior, `main`, or public release changes.
- Runtime version remains `0.1.0-dev.23`.
