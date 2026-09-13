# ChatGPT Project Instructions — Polymorph

Use this as the compact ChatGPT Project instruction set for `Knight-Witch/Polymorph`.

- Put `# TLDR` first in user-facing replies.
- Before material work, read `PROJECT_CONTRACT.md` and `ACTIVE_CONTEXT.md` on `dev`, then only the files explicitly routed there or directly required by the task. Do not preload full history, changelog, pre-flight, archived project logs, or unrelated engine files.
- `ACTIVE_CONTEXT.md` is the authoritative current-task router. `MASTER.md` is only a compact repo-wide index, not a transcript. Old detail lives in Git history and targeted `HISTORY/*` files.
- Diagnose before editing. Distinguish confirmed findings, supported inference and hypothesis. Preserve validated behavior unless new evidence requires a change.
- Development work is on `dev`. Do not use `main` as an experimental branch and do not create a public GitHub Release until Amanda explicitly approves release readiness.
- Use the connected GitHub account directly. Do not claim GitHub access is unavailable without actually trying the connector.
- Continue autonomously through safe diagnosis, implementation, CI, artifact inspection and documentation instead of stopping at intermediate narration checkpoints. Ask Amanda only for genuinely human actions or subjective visual confirmation.
- Use GitHub Actions/repo CI for Windows builds. Do not substitute local compilation for the canonical build. When Amanda needs a tester, retrieve the successful installer artifact and hand it to her directly rather than making her navigate Actions.
- UI/visual acceptance requires Amanda's visual confirmation. Runtime smoke success is not proof that typography, spacing, icon rendering, preview balance or animation looks right.
- Preserve the accepted responsive controller (`1260x820` design, `920x640` floor) unless a concrete regression proves it needs to change.
- Preserve the self-contained typography requirement: packaged testers carry the approved Trajan Regular/Bold assets and must not depend on a system font installation. Do not reopen that decision or replace it with outlines/system-font fallback unless Amanda explicitly asks.
- Preserve validated conversion behavior. Preserve-motion GIF never intentionally drops frames; Favor resolution may use only the already-validated explicit source-frame-decimation policy. Do not change adaptive logic from intuition; inspect any supplied `*_ADAPTIVE_DIAGNOSTIC.json` first.
- Preserve shared Crop/Fit preview/export geometry, no-upscale behavior, pinned FFmpeg 9.0.1 + gifski 1.32.0, decimal-MB semantics, updater safety and no-console Windows subprocess behavior unless evidence directly implicates them.
- Every committed repo update must update `CHANGELOG.md` and add a concise `PRE_FLIGHT_Check.md` record. Keep those root logs rolling/compact; archive older detail under `HISTORY/PROJECT_LOGS/` or rely on Git history rather than making future chats reread it.
- Update `ACTIVE_CONTEXT.md` whenever the current task, next gate, protected PASS state, active head/build, or required continuation files materially change.
- Update `MASTER.md` only for repo-wide state/architecture changes; do not turn it into a session log.
- If a test build is produced, record the commit, workflow run/result and useful artifact identity in `ACTIVE_CONTEXT.md` so the next chat does not have to rediscover it.
- Do not redo closed investigations merely because a new chat started. Follow the current router and reopen a closed area only when new evidence requires it.

Current task state must come from `ACTIVE_CONTEXT.md`, not from old chat history.
