# Polymorph Pre-Flight Log

Historical entries through dev.23 are preserved verbatim in [`HISTORY/PROJECT_LOGS/PRE_FLIGHT_THROUGH_DEV23.md`](HISTORY/PROJECT_LOGS/PRE_FLIGHT_THROUGH_DEV23.md). Root tracking is intentionally rolling/compact; older detail is not mandatory startup reading.

## PFC-2026-09-13-042 — Repair custom-font binary transport after run #55

- Windows Dev Build run #55 / run ID `34797309292` failed at `Prepare pinned Polymorph UI fonts` before unit tests, conversion tools, frozen app build or packaged smoke. The verifier proved the repository blobs matched the initially recorded Git identities, then `lzma.decompress` rejected the Regular asset as not-XZ. This isolates the defect to the connector-created binary transport rather than the supplied font files or UI implementation.
- Do not alter typography measurements in response to this failure. `styles.py` remains untouched; the dev.23 point sizes, tracking and responsive geometry remain the requested dev.24 baseline.
- Generate display-only subsets from Amanda's exact supplied `Polymorph Regular` / `Polymorph Bold` TTFs, preserving the original family/subfamily naming, glyph outlines, metrics and kerning for all characters currently used by branded display text.
- Package those subsets losslessly as XZ and commit them through GitHub's base64 blob path. GitHub returned the exact predicted blob SHA-1s: Regular `e868cf74e450f2e3b69c2d3116d05f18d1499e15`; Bold `a794e9faebeb424e783ba1de4028a350e929113f`.
- Verify decompressed shipped subset SHA-256 values in CI: Regular `5aeb68e5a95011f9a21c1c19d81514f04ad8ff23623f6e54ec20921d2ad2ef2c`; Bold `d437ef4599771311a175d3e7832c041eb76058e26a7e826dc1ea09547a111e3a`.
- Preserve original supplied source provenance separately: Regular `e3d1bf414bdd0b517989e89ea3350acafdd90b61322c6c6ec8c7390a9f6ea188`; Bold `aea401e914959cd4638cec82c0a7328a5d84b8d79d942c850052b10a18cca511`.
- Keep the existing runtime registration path: decompress the bundled XZ bytes in memory and register through `QFontDatabase.addApplicationFontFromData` before UI construction. Friends still do not need a Windows font install.
- Runtime remains `0.1.0-dev.24`; this repair changes only bundled display-font transport/verification and tracking documentation.
- Re-run the full canonical Windows workflow. Do not claim visual correctness from CI; Amanda remains the human gate after a successful installed tester exists.

## PFC-2026-09-13-041 — Replace Trajan with supplied Polymorph Regular/Bold

- Required bootstrap completed before material work: `PROJECT_CONTRACT.md` then `ACTIVE_CONTEXT.md`; only the routed UI/font/package files and directly required tracking/license/build files were read.
- Diagnosis: dev.23's display typography was isolated behind `fonts.py`/`tracked_font`; the established point sizes, absolute letter spacing and responsive geometry are independent of the font asset source. Therefore the requested swap does not require reopening `styles.py` measurements or any conversion/framing engine work.
- Inspected the supplied font metadata before implementation. Both files identify family `Polymorph`; the faces identify `Regular` and `Bold` subfamilies.
- Preserve all established typography measurements unchanged for the first custom-font tester. Visual/optical adjustments are deferred to Amanda's human review.
- Initial packaging attempted to bundle the exact supplied source bytes losslessly as `Polymorph-Regular.ttf.xz` and `Polymorph-Bold.ttf.xz`; Qt registration decompresses them in memory and uses `addApplicationFontFromData` before UI construction.
- Original Regular source SHA-256 is `e3d1bf414bdd0b517989e89ea3350acafdd90b61322c6c6ec8c7390a9f6ea188`; Bold source SHA-256 is `aea401e914959cd4638cec82c0a7328a5d84b8d79d942c850052b10a18cca511`.
- Remove Trajan download/use from the dev workflow. Retain pinned Inter for body/UI text and Cinzel only as an emergency fallback.
- Update packaged smoke so the build must register both Polymorph faces and report `bundled-polymorph` as the display source.
- Advance runtime version to `0.1.0-dev.24` and update canonical UX/project-contract documentation accordingly.
- This sandbox does not contain PySide6, so no local Qt-registration PASS is claimed. Canonical validation remains the Windows GitHub Actions build, packaged frozen-app smoke, installer/checksum gates, then human visual review.
- Protected PASS behavior remains unchanged: conversion, adaptive GIF policy, Crop/Fit geometry, updater hardening, no-console subprocess handling, dev.21 responsive geometry and dev.22 icon work are not reopened.

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
