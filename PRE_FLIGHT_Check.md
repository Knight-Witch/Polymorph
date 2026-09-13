# Polymorph Pre-Flight Log

Historical entries through dev.19 are preserved verbatim in [`HISTORY/PROJECT_LOGS/PRE_FLIGHT_THROUGH_DEV19.md`](HISTORY/PROJECT_LOGS/PRE_FLIGHT_THROUGH_DEV19.md). Earlier pre-dev.16 history also remains in the existing dev.15 archive.

## PFC-2026-09-12-033 — Harden dev.21 packaged preview smoke teardown

- Trigger: Windows Dev Build run #40 passed all 54 unit tests, pinned FFmpeg/gifski verification, adaptive integration, GIF reference comparison, and PyInstaller packaging, then stalled for the remainder of the 30-minute job specifically inside the frozen-app UI smoke step.
- Diagnosis: the hang is isolated to the new dev.21 preview/playback smoke path rather than conversion behavior. The packaged offscreen Qt process remained alive during animated WebP playback/seek teardown.
- Fix: switch the preview `QMovie` from `CacheAll` to `CacheNone`, pause running playback before deterministic frame seeks, and force the dedicated `--smoke-test` process to terminate after it has written its result instead of relying on native media/plugin teardown.
- CI safeguard: the packaged smoke process now has its own 120-second timeout and is force-killed with its smoke log printed if it exceeds that bound, preventing another full-job timeout from hiding the failure point.
- No conversion, adaptive GIF, framing/export geometry, output sizing, updater, or user-facing dev.21 styling behavior changes in this hardening pass.
- Version remains `0.1.0-dev.21` because no dev.21 tester installer was produced by the failed run.

## PFC-2026-09-12-032 — Match dev.21 directly to the approved concept markup

- Target files: branded layout/widgets/styles, animated preview, packaged smoke test, user-supplied concept icons, development version metadata, `MASTER.md`, and required tracking files.
- Required review completed before editing: `PROJECT_CONTRACT.md`, `MASTER.md`, `PRE_FLIGHT_Check.md`, `CHANGELOG.md`, `docs/ARCHITECTURE.md`, `docs/UX_SPEC.md`, current dev.20 branded layout/QSS/smoke implementation, `preview.py`, base/adaptive window wiring, the approved concept image, the user's annotated side-by-side dev.20 screenshot, and the supplied Trajan/icon assets.
- Human diagnosis: dev.20 is materially closer but still differs in vertical alignment, title hierarchy/tracking, card-header divider rules, preview chrome, primary-action alignment, footer spacing/metadata, and responsive behavior. The dev.20 right rail still expects scrolling to reveal the primary action at smaller heights, and the Fit-only `Fill` control expands the framing card unexpectedly.
- Typography direction: prefer system-installed `Trajan Pro` for `POLYMORPH`, mixed-case `Media conversion magic — by Knight Witch™`, card headings, and primary action; keep bundled Cinzel only as a legal packaged fallback and Inter for body/UI text. The user supplied Trajan binaries are Adobe-proprietary and therefore are intentionally not committed to the public repository; the app will use Trajan automatically when it is installed on Windows.
- Tracking ratios are based on the user's Photoshop reference: title uses very wide tracking, subtitle moderately wide tracking, card headings use restrained tracking with bold weight, and the primary action returns from `Cast Polymorph` to `POLYMORPH` with the same display language as the application title.
- Card geometry: busy cards retain icon/title/divider treatment but content is indented to the same visual column as the heading text. Crop Zoom and Output Folder intentionally omit the divider. User-supplied resize/priority/crop/aspect/folder/trash/update artwork replaces the improvised equivalents where applicable.
- Preview: remove the redundant Preview heading and gray nested surface; draw media against the preview-card background with a tight square border. Add a real play/pause control, seekable source-frame timeline, seconds readout, in-view `FRAME n / total` readout, and a bottom divider before source/framed-max metadata. Playback is preview-only and does not change export timing.
- Footer/status: combine Ready/status and spaced labeled service links into one top row, add a divider, then place the version bottom-left and `Polymorph 2026, Knight Witch™` bottom-right.
- Responsive behavior: remove dependency on a vertically scrolling settings rail. Below the 1260×820 design size, a resize controller proportionally reduces typography, padding/control dimensions, queue-row geometry, preview minimums, and rail width down to the supported 920×640 floor. Frozen-app smoke must reject a clipped primary action at the minimum size.
- Fit background color remains in the engine model but the branded `Fill` button is hidden/removed from the v1 branded UI per user direction; Fit therefore uses the current/default background color without expanding the Framing card.
- Visual texture is synthesized at runtime with deterministic low-opacity grain layered over the existing gradients; no external film-grain asset is required.
- Conversion engine, adaptive GIF policy, framing geometry, output sizing, updater, subprocess behavior, and pinned FFmpeg/gifski toolchain remain unchanged.
- Versioning: increment development tester from `0.1.0-dev.20` to `0.1.0-dev.21`.

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
