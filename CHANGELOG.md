# Changelog

Historical entries through dev.23 are preserved verbatim in [`HISTORY/PROJECT_LOGS/CHANGELOG_THROUGH_DEV23.md`](HISTORY/PROJECT_LOGS/CHANGELOG_THROUGH_DEV23.md). Root tracking is intentionally rolling/compact; use archived detail only when a current task needs it.

## POLY-2026-09-13-044 — 2026-09-13 21:15 PDT — Record successful dev.24 custom-font tester

### Summary

- Windows Dev Build run #57 / run ID `34805017987` completed successfully from implementation commit `c4f9e1962716a56650366964acff806f61ae38b0`.
- All canonical gates passed: custom Polymorph font verification, 54 unit tests, pinned FFmpeg 9.0.1 + gifski 1.32.0 toolchain verification, adaptive integration, standalone GIF reference comparison, PyInstaller frozen application build, packaged application smoke, Inno Setup installer compilation, installer SHA-256 generation, and both artifact uploads.
- Packaged smoke confirmed the bundled Polymorph Regular/Bold display faces register inside the frozen app, the branded UI initializes successfully, responsive geometry/control wiring remains intact, and the footer reports dev.24 correctly.
- Successful installer artifact is `Polymorph-dev-installer`, artifact ID `10332274291`, artifact ZIP digest `sha256:6e18bc546f065b29bf7b193e8bd84a6972c434f6a3c672bdf7a8572dd1bcbf26`.
- The downloaded tester ZIP independently hashes to the same SHA-256 digest.
- The technical gate is complete. The next gate is Amanda's human visual comparison of the custom font against the approved mockup using the intentionally unchanged dev.23 sizes/tracking/spacing.
- Documentation-only handoff update. No runtime code, UI behavior, font bytes, typography measurements, conversion/framing/adaptive logic, package inputs, installer behavior, updater behavior, toolchain pins, `main`, or public release changed.
- Runtime remains `0.1.0-dev.24`.

## POLY-2026-09-13-043 — 2026-09-13 21:09 PDT — Align dev.24 package/version anchors after packaged smoke

### Summary

- Diagnosed Windows Dev Build run #56 / run ID `34804686496`: the corrected Polymorph font assets verified successfully, all 54 unit tests passed, conversion/adaptive/GIF reference gates passed, PyInstaller froze the app successfully, and packaged smoke confirmed both bundled Polymorph display faces registered correctly.
- The only packaged-smoke failure was stale version metadata: the frozen UI footer still reported `0.1.0-dev.23` because `src/polymorph/constants.py` had not been advanced with `src/polymorph/__init__.py`.
- Found the same stale dev.23 anchor in `pyproject.toml` and `installer/Polymorph.iss`; align all three to dev.24 in one packaging-only fix.
- Add `assets/fonts/*.xz` to setuptools package-data so the custom display assets are included in normal Python package builds as well as the existing PyInstaller whole-assets bundle.
- No font bytes, font registration behavior, typography measurements, layout geometry, conversion logic, framing logic, adaptive GIF behavior, updater behavior or subprocess handling changed.
- Runtime remains `0.1.0-dev.24`; this commit makes package metadata, visible footer version and installer version agree with that runtime candidate.

### Validation notes

- Run #56 provides direct evidence that the repaired custom font transport and Qt registration are good: packaged smoke printed `PASS packaged Polymorph display fonts and Inter body font` before stopping at the footer-version assertion.
- Next gate is a fresh full Windows Dev Build from the version-alignment commit. Human visual review remains required after a successful installer exists.

## POLY-2026-09-13-042 — 2026-09-13 20:58 PDT — Repair dev.24 custom-font asset transport

### Summary

- Diagnosed Windows Dev Build run #55 / run ID `34797309292`: it failed before tests/runtime because the first connector-created XZ font blobs were not valid XZ byte streams. The failure was isolated to repository binary transport, not the supplied font files, Qt registration, or any UI measurement.
- Replaced the invalid transport blobs with verified display-only subsets generated from Amanda's exact supplied `Polymorph` Regular/Bold TTFs. The subset preserves the original glyph outlines, metrics, family/subfamily naming and kerning for every character currently used by Polymorph's branded display text.
- Correct bundled XZ Git blob identities are now `e868cf74e450f2e3b69c2d3116d05f18d1499e15` (Regular) and `a794e9faebeb424e783ba1de4028a350e929113f` (Bold).
- Decompressed shipped subset SHA-256 values are `5aeb68e5a95011f9a21c1c19d81514f04ad8ff23623f6e54ec20921d2ad2ef2c` (Regular) and `d437ef4599771311a175d3e7832c041eb76058e26a7e826dc1ea09547a111e3a` (Bold).
- Original supplied source provenance remains recorded separately: Regular `e3d1bf414bdd0b517989e89ea3350acafdd90b61322c6c6ec8c7390a9f6ea188`; Bold `aea401e914959cd4638cec82c0a7328a5d84b8d79d942c850052b10a18cca511`.
- Updated the CI verifier to validate the corrected repository blobs and the exact decompressed subset bytes Qt will register.
- No typography point size, tracking, responsive scaling, card spacing or layout geometry changed. `styles.py` remains untouched.
- Runtime remains `0.1.0-dev.24`; this is a packaging/asset-transport repair to the same visual candidate.
- Protected conversion, framing, adaptive GIF, updater, subprocess, responsive-layout and icon behavior remain unchanged.

### Validation notes

- The corrected binary blobs were created through GitHub's base64 blob path and GitHub returned the exact locally predicted Git blob SHA-1 values for both assets.
- Run #55 is intentionally retained as failed evidence for the rejected transport method. Windows run #56 later verified both corrected assets successfully and reached packaged smoke.

## POLY-2026-09-13-041 — 2026-09-13 18:40 PDT — Replace Trajan with custom Polymorph display family

### Summary

- Replaced the dev.23 Trajan display dependency with Amanda's supplied custom `Polymorph` Regular and Bold TTF faces.
- Preserved the existing approved typography measurements exactly: no `styles.py` title/subtitle/card/button point sizes, tracking, responsive scaling, card spacing, or layout geometry changed in this pass.
- The initial implementation attempted to store the supplied font bytes losslessly as bundled XZ assets and register the decompressed bytes directly with Qt through `QFontDatabase.addApplicationFontFromData`, keeping the installed app self-contained without requiring a Windows font install.
- Custom Regular source SHA-256: `e3d1bf414bdd0b517989e89ea3350acafdd90b61322c6c6ec8c7390a9f6ea188`.
- Custom Bold source SHA-256: `aea401e914959cd4638cec82c0a7328a5d84b8d79d942c850052b10a18cca511`.
- Windows CI no longer downloads Trajan. It verifies the bundled custom-font transport assets and continues to fetch/pin Inter plus emergency-fallback Cinzel.
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
- Windows CI run #55 later rejected the first repository transport blobs before runtime; POLY-2026-09-13-042 records the isolated transport repair.

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
