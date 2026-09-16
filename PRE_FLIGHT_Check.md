# Polymorph Pre-Flight Log

Historical entries through dev.23 are preserved verbatim in [`HISTORY/PROJECT_LOGS/PRE_FLIGHT_THROUGH_DEV23.md`](HISTORY/PROJECT_LOGS/PRE_FLIGHT_THROUGH_DEV23.md). dev.24-dev.27 technical/visual history remains available in Git history; root tracking is intentionally rolling/compact.

## PFC-2026-09-16-068 — Motion Lab panel readability pass — FULL PASS

- PASS source review: change is limited to standalone Motion Lab styling at the entrypoint/theme layer.
- PASS styling intent: section headers use a brighter crimson/red treatment with stronger weight and a deep-red divider for clearer scanning.
- PASS styling intent: slider unused-track backgrounds are transparent; active red fill and existing handles remain visible.
- PASS CI: dedicated `Polymorph Motion Lab Build` run #10 / run ID `35064912753` succeeded on readability implementation commit `845b029df1027bf6f4fac2a3a346c5d04d32d134`.
- PASS CI: source smoke, PyInstaller portable build, packaged Windows smoke and artifact upload.
- Artifact `Polymorph-motion-lab`, ID `10433348032`, size 50,890,729 bytes, digest `sha256:59d479d9cba0a2bd1b830093c566b0dfa97d19d62a9aae7220a28c898c922af5`.
- PASS isolation: the normal Windows Dev Build path filter did not trigger because no production `src/**`, build, installer, pyproject or `run_polymorph.py` path changed; protected production run #109 remains FULL PASS.
- No production conversion, framing, adaptive, updater, subprocess, app-window, installer, runtime-version or public-release behavior changed.
- Next gate: Amanda visually reviews the packaged header/slider treatment.

## PFC-2026-09-16-067 — Motion Lab v7 scene-builder controls — FULL PASS

- PASS static: updated local Motion Lab editor/loader/rune/effects/lab sources parse without Python syntax errors.
- PASS architecture: changes remain isolated to standalone Motion Lab tooling; production conversion, framing, updater, encoder, installer and runtime version are untouched.
- PASS source design: workspace/preset schema remains backward compatible and adds explicit geometry pulse order plus new element fields with defaults.
- PASS source design: undo/redo captures complete multi-study workspaces and provides standard keyboard shortcuts.
- PASS source design: geometry pulse order is explicitly editable via drag/drop and remains limited to pulse-capable geometry.
- PASS source design: layers and groups are renameable without changing stable element IDs used by rendering/presets; expandable drag/drop group hierarchy reassigns link groups without altering z-order.
- PASS source design: mask opacity, transparent colors, loading-ring modes, tracer-tail controls, rune solid/outline/weight controls, and layer/effect enable toggles are persisted.
- PASS source design: center completion flash removed; automatic preview wrapping does not enter completion reveal/flash state.
- PASS CI: dedicated `Polymorph Motion Lab Build` run #9 / run ID `35060729400` succeeded on implementation commit `06750079ee2dfa837a56600011367f16cb87646b`.
- PASS CI: source smoke, PyInstaller portable build, packaged Windows smoke and artifact upload.
- Artifact `Polymorph-motion-lab`, ID `10431614039`, size 50,932,008 bytes, digest `sha256:41aed1fcdb226f028c76d962e97f5d36b7beaf9f8d2ad698a81e7cbf19b207f9`.
- PASS isolation: normal Windows Dev Build run #109 / run ID `35060729361` succeeded across unit tests, pinned FFmpeg/gifski, adaptive integration, GIF reference, production package smoke, installer, checksum and uploads.
- No production conversion, framing, adaptive, updater, subprocess, app-window, installer, runtime-version or public-release behavior changed.
