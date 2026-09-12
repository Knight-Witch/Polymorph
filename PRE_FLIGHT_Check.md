# Polymorph Pre-Flight Log

Historical entries through dev.19 are preserved verbatim in [`HISTORY/PROJECT_LOGS/PRE_FLIGHT_THROUGH_DEV19.md`](HISTORY/PROJECT_LOGS/PRE_FLIGHT_THROUGH_DEV19.md). Earlier pre-dev.16 history also remains in the existing dev.15 archive.

## PFC-2026-09-12-031 — Match approved mockup density and interaction details

- Target files: `src/polymorph/ui/branded_layout.py`, `src/polymorph/ui/styles.py`, packaged smoke test, development version metadata, `MASTER.md`, and required tracking files.
- Required review completed before editing: `PROJECT_CONTRACT.md`, `MASTER.md`, `PRE_FLIGHT_Check.md`, `CHANGELOG.md`, `docs/ARCHITECTURE.md`, `docs/UX_SPEC.md`, current dev.19 branded layout/QSS/smoke implementation, current status/progress placeholder, and the user's side-by-side dev.19 versus approved mockup screenshot.
- Human diagnosis: dev.19 fixed the broad two-column premise but the right rail still clips horizontally and its stacked cards require extra height at default sizing; padding is too large; file count/actions do not share the Files title row; the file rows lack thumbnails/source metadata/actions; Framing and Aspect Ratio are not paired; status/footer/primary-action presentation is materially weaker than the approved mockup.
- User direction: treat the generated mockup as the UI specification rather than loose inspiration. Match its card density, icon/title/separator headers, side-by-side format controls, clean numeric inputs without spinner arrows, paired Framing/Aspect cards, compact Crop Zoom, richer file rows, two-line Ready strip, labeled footer links with separators, gradients, and more deliberate Cast Polymorph treatment.
- Queue behavior added is real rather than placeholder UI: rows show first-frame thumbnails plus source size/dimensions/runtime, and each overflow menu provides Open, Open file location, and Remove from queue. Header trash removes the selected queue item; `Clear All` remains queue-only and turns red on hover.
- Fit background support is retained in the engine but reduced to a small Fit-only utility instead of receiving the dedicated mockup card the user explicitly did not require.
- Layout safeguard: the right rail is fixed to a known width, vertically scrollable as needed, and its controls are capped to fit that viewport; packaged smoke must fail if horizontal scrolling is required.
- Typography remains Cinzel + Inter for this tester, with stronger letter spacing on the title/subtitle. The user intends to supply a closer final display font later; preferred desktop assets are TTF/OTF rather than WOFF/WOFF2.
- Loader behavior remains deferred. The large legacy ArcaneProgress placeholder is suppressed from the compact status strip so conversion cannot re-expand the layout before the real loader is designed.
- Conversion engine, adaptive GIF policy, FFmpeg/gifski settings, framing geometry, subprocess behavior, updater behavior, and pinned toolchain remain unchanged.
- Versioning: increment development tester from `0.1.0-dev.19` to `0.1.0-dev.20`.
