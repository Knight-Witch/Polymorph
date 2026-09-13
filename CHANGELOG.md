# Changelog

Historical entries through dev.23 are preserved verbatim in [`HISTORY/PROJECT_LOGS/CHANGELOG_THROUGH_DEV23.md`](HISTORY/PROJECT_LOGS/CHANGELOG_THROUGH_DEV23.md). Root tracking is intentionally rolling/compact; use archived detail only when a current task needs it.

## POLY-2026-09-13-040 — 2026-09-13 16:47 PDT — Add compact cross-chat handoff architecture

### Summary

- Added `ACTIVE_CONTEXT.md` as Polymorph's authoritative current-task router, mirroring the low-context continuation pattern now used successfully for Witch Dock/HeroForge work.
- Added `CHATGPT_PROJECT_INSTRUCTIONS.md` so future chats can bootstrap from a small durable instruction set instead of rebuilding workflow rules from conversation history.
- Reworked `PROJECT_CONTRACT.md` so required startup is now: contract -> active context -> only routed/target files. Full master/history/changelog/pre-flight reads are no longer the default.
- Compacted `MASTER.md` to a repo-wide status and routing index while preserving its exact pre-compaction dev.23 contents in `HISTORY/PROJECT_LOGS/MASTER_DEV23_SNAPSHOT.md`.
- Rolled the root pre-flight/changelog after dev.23. Exact prior contents are preserved as `HISTORY/PROJECT_LOGS/PRE_FLIGHT_THROUGH_DEV23.md` and `HISTORY/PROJECT_LOGS/CHANGELOG_THROUGH_DEV23.md`.
- Recorded the exact current handoff state in `ACTIVE_CONTEXT.md`: dev.23 code commit, successful Windows run #54, installer artifact identity, protected conversion/framing/adaptive state, accepted responsive behavior, self-contained bundled Trajan requirement, and the next human visual gate.
- The next chat should **not** restart the Trajan/system-font investigation or closed conversion investigations. It should first hand over/use the successful dev.23 tester as needed, obtain human visual feedback, and continue only the presentation work implicated by that feedback.
- Documentation-only change. No runtime code, UI behavior, conversion/framing/adaptive logic, version metadata, packaging inputs, updater behavior, toolchain pin, installer behavior, `main`, or public release changed.
- Runtime version remains `0.1.0-dev.23`.

### Documentation changed

- `ACTIVE_CONTEXT.md` (new)
- `CHATGPT_PROJECT_INSTRUCTIONS.md` (new)
- `PROJECT_CONTRACT.md`
- `MASTER.md`
- `PRE_FLIGHT_Check.md`
- `CHANGELOG.md`
- `HISTORY/PROJECT_LOGS/PRE_FLIGHT_THROUGH_DEV23.md` (exact snapshot)
- `HISTORY/PROJECT_LOGS/CHANGELOG_THROUGH_DEV23.md` (exact snapshot)
- `HISTORY/PROJECT_LOGS/MASTER_DEV23_SNAPSHOT.md` (exact snapshot)
- `HISTORY/PROJECT_LOGS/README.md`

### Validation notes

- This commit intentionally changes documentation/continuation routing only. The successful dev.23 runtime candidate remains code commit `81150b0e7007969d260317c9383ed7bacb3362b9`, already green in Windows Dev Build run #54.
- Future chats should use `ACTIVE_CONTEXT.md` as the handoff baton and fetch historical archives only when the current task explicitly needs them.
