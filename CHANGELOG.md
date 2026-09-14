# Changelog

Historical entries through dev.23 are preserved verbatim in [`HISTORY/PROJECT_LOGS/CHANGELOG_THROUGH_DEV23.md`](HISTORY/PROJECT_LOGS/CHANGELOG_THROUGH_DEV23.md). Root tracking is intentionally rolling/compact; use archived detail only when a current task needs it.

## POLY-2026-09-13-041 — 2026-09-13 18:40 PDT — Replace Trajan with custom Polymorph display family

### Summary

- Replaced the dev.23 Trajan display dependency with Amanda's supplied custom `Polymorph` Regular and Bold TTF faces.
- Preserved the existing approved typography measurements exactly: no `styles.py` title/subtitle/card/button point sizes, tracking, responsive scaling, card spacing, or layout geometry changed in this pass.
- Stored the supplied font bytes losslessly as bundled XZ assets and register the decompressed bytes directly with Qt through `QFontDatabase.addApplicationFontFromData`, keeping the installed app self-contained without requiring a Windows font install.
- Custom Regular source SHA-256: `e3d1bf414bdd0b517989e89ea3350acafdd90b61322c6c6ec8c7390a9f6ea188`.
- Custom Bold source SHA-256: `aea401e914959cd4638cec82c0a7328a5d84b8d79d942c850052b10a18cca511`.
- Windows CI no longer downloads Trajan. It verifies the exact bundled custom-font transport blobs, verifies their decompressed source hashes, and continues to fetch/pin Inter plus emergency-fallback Cinzel.
- Packaged smoke now requires `Polymorph Regular`, `Polymorph Bold`, Inter and Cinzel registration and requires `polymorphDisplaySource == "bundled-polymorph"`.
- Canonical UX/project-contract language now identifies the supplied Polymorph family as the display face. Cinzel is fallback-only.
- Runtime version advanced to `0.1.0-dev.24`.
- Protected conversion, framing, adaptive GIF, updater, subprocess, responsive-layout and icon behavior were not changed.
- Next gate is the normal Windows dev build followed by Amanda's visual comparison against the approved mockup; optical size/tracking changes, if any, wait for that human check.

### Files changed

- `src/polymorph/assets/fonts/Polymorph-Regular.ttf.xz` (new)
- `src/polymorph/assets/fonts/Polymorph-Bold.ttf.xz` (new)
- `src/polymorph/ui/fonts.py`
- `src/polymorph/smoke_test.py`
- `src/polymorph/__init__.py`
- `build/verify_font_assets.py`
- `.github/workflows/windows-dev-build.yml`
- `docs/UX_SPEC.md`
- `THIRD_PARTY.md`
- `PROJECT_CONTRACT.md`
- `ACTIVE_CONTEXT.md`
- `PRE_FLIGHT_Check.md`
- `CHANGELOG.md`

### Validation notes

- Uploaded font metadata was inspected before implementation: both faces report family `Polymorph`, with `Regular` and `Bold` subfamilies respectively.
- This sandbox does not have PySide6 installed, so local Qt registration was not claimed. The repository's packaged Windows smoke test remains the authoritative font-registration/package gate.
- Windows CI is pending immediately after this implementation commit.

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
