# UX Specification

## Primary flow

Files -> Output Format -> Sizing Constraint -> GIF Priority -> Framing -> Polymorph

## Branded application composition

- The approved mockup is the active visual specification, not loose inspiration.
- Runtime uses a two-column composition: dominant left workspace with media queue above preview; compact right settings rail.
- The right rail is a fixed composition of `OUTPUT FORMAT`, `SIZING`, `GIF PRIORITY`, paired `FRAMING` / `ASPECT RATIO`, `CROP ZOOM`, `OUTPUT FOLDER`, then the primary `POLYMORPH` action.
- Unsupported mockup-only controls are not added as fake UI. Every visible interactive control must either drive established application state or implement a real action.
- Queue actions live with the queue. `FILES` and the file count are grouped together at the left of the header; Add Files / trash / separator / `Clear All` form a right-side action cluster. Clear removes queue entries only; it never deletes source files.
- The visible framing selector is Original / Crop / Fit radio controls synchronized to the existing framing state used by preview/export logic.
- Header lockup is `POLYMORPH` then mixed-case `Media conversion magic — by Knight Witch™`. Version metadata belongs in the footer, not the header.
- Display typography prefers any Qt-visible Trajan family (`Trajan Pro 3`, `Trajan Pro`, etc.); bundled Cinzel is the redistributable fallback. Inter is the bundled body/UI family.
- Current palette is near-black/charcoal, ivory, champagne gold and restrained crimson. Cards use dark layered gradients, subtle warm illumination, deterministic grain, small-radius etched borders and restrained red selection states.
- Loader/progress art is not part of the current fidelity pass. Arcane-circle and D20 concepts remain later design work.

## Typography ratios

- The user's Photoshop references are the visual basis rather than literal Qt point-size values.
- `POLYMORPH`: all caps, Trajan-preferred, roughly the 120 pt reference with +350 Photoshop tracking; implementation should read distinctly wide-spaced and premium.
- Subtitle/byline: `Media conversion magic — by Knight Witch™`, mixed/proper case, roughly the 50/120 title-size ratio and +300 tracking reference.
- Card headings: Trajan-preferred Bold, roughly the 75/120 reference ratio with restrained +100-style tracking, balanced against the denser desktop control rail.
- Primary `POLYMORPH` action uses the same display/tracking language as the application title.
- Body/control copy remains Inter for clarity and accessibility.

## Window and responsive behavior

- Design geometry: `1260x820`.
- Supported minimum: `920x640`.
- Below the design size, UI typography, margins, control geometry, queue rows, preview minimums and right-rail width scale down proportionally. The window should not hide the primary action or require a vertical rail scrollbar simply because the user makes the window smaller.
- Human dev.21 review accepted this proportional scaling behavior; preserve it unless later testing identifies a concrete regression.
- Enlarging the window may provide more preview/workspace room but should not create visually meaningless blank expanses inside controls.
- Resolution/file-size fields intentionally have no spinner arrows; users type the values directly.
- Radio buttons use conventional hollow-circle / centered-dot semantics, including disabled state.

## Card layout and alignment

- Busy cards use: supplied small gold icon + Trajan-style heading, then a thin divider, then the controls.
- Output Format, Sizing, GIF Priority and Aspect Ratio content should visually align beneath the heading text column rather than beginning underneath the icon.
- Framing is the intentional exception because the three compact radio choices need even horizontal distribution.
- Crop Zoom and Output Folder do not use the heading divider; they are intentionally simpler cards.
- Card padding stays tight. Avoid nested card-inside-card surfaces unless a distinct functional boundary genuinely requires them.
- Surface corners are small-radius, not bubbly.

## File queue

- Each media row shows a first-frame thumbnail, filename, original decimal file size, source dimensions and runtime.
- Selected row receives restrained crimson emphasis.
- Overflow ellipsis is deliberately large enough to read as an action menu.
- Overflow menu provides real actions: Open, Open file location, Remove from queue.
- Queue header trash removes the selected item. `Clear All` is text-style and turns crimson/red on hover.

## Main preview

- Animated source preview is the visual centerpiece.
- The preview card has no redundant `PREVIEW` label/header.
- Avoid a gray nested surface inside the preview card. The viewer background should visually merge with the parent dark card; only the actual media gets a tight outline.
- Media outline is square or effectively square so dark source corners never protrude past a rounded viewport border.
- Preview and export use the same framing geometry resolver; Crop/Fit must not stretch or distort source media.
- Original shows the full source.
- Crop trims to the selected ratio, supports drag-to-reposition, and exposes 100-300% crop zoom. Crop zoom reduces the retained source window rather than upscaling.
- Fit preserves complete source aspect ratio and expands the canvas to the chosen ratio. Background color remains in the engine model, but the branded v1 UI intentionally hides the old Fit `Fill` button because it changed card height unexpectedly.
- Preview playback controls are real: play/pause button, seekable source-frame timeline/grabber, elapsed/total seconds, and an in-image `FRAME n / total` readout.
- Playback controls are preview-only and do not alter export timing or frame selection.
- Human testing already validated Crop/Fit preview/export parity end to end.

## Sizing modes

### Fit under file size

- Default: 99 MB decimal.
- User specifies only the ceiling.
- Encoder quality remains fixed.
- Resolution is automatically adjusted to fit.
- Preserve motion keeps source timing/frame sequence fixed.
- Favor resolution may intentionally retain fewer original source frames only when real encoded measurements show a worthwhile spatial gain.

### Set resolution

- User specifies output pixel dimensions.
- Width and height stay linked to active framed aspect ratio; no extra aspect-lock control is exposed.
- File-size target is disabled.
- Source content cannot be upscaled above native framed size.
- Adaptive GIF frame reduction is disabled because the user chose the spatial target explicitly.

## GIF priority

Visible only when meaningful for GIF + Fit under file size.

### Preserve motion

- Default.
- Keeps every source frame and source timing.
- Uses spatial resolution as the file-size tradeoff.

### Favor resolution

- Exact source-frame decimation behavior from dev.13+ remains the canonical implementation.
- Polymorph first creates the normal Preserve-motion fitted result, then measures exact source-frame stride candidates at the fitted dimensions.
- Candidate must predict and then realize roughly 8% or greater linear spatial gain.
- For 25 FPS source, current candidates are stride 2 (~12.5 FPS nominal) then stride 3 (~8.33 FPS nominal) while above the automatic floor.
- Retained image data comes only from original source frames; no optical flow or temporal blending.
- Final GIF delay is shortened only when needed to preserve exact loop closure timing.
- Never upscale above native framed geometry; preferred long edge is capped at 2048 px.

## Status and footer

- Ready/status is a compact two-line block: `Ready` with smaller contextual text such as `2 files imported. Choose your settings and begin.`
- Service controls are labeled, not icon-only, and are spaced with visible separators: Check for Updates, GitHub, Ko-fi, Patreon, Discord.
- Footer links need breathing room; avoid a dense icon/text cluster.
- A horizontal divider separates the service/status row from metadata.
- Bottom-left: `Polymorph v<version>`.
- Bottom-right: `Polymorph 2026, Knight Witch™`.

## Primary action

- Copy is `POLYMORPH`, not `Cast Polymorph`.
- Primary action uses a deep crimson/black gradient, champagne-gold border/highlight, Trajan-style tracked title and restrained static sigil/line decoration.
- Idle state should feel premium rather than animated. Hover/press may wake the surface up immediately; the later loader/cast animation takes over only when conversion begins.

## Completion readout

- Development adaptive UI reports actual result dimensions, decimal MB and effective average output FPS.
- Development Favor-resolution runs currently report the diagnostic sidecar filename; the sidecar is temporary development instrumentation.
- Preserve-motion and MP4 runs do not create that diagnostic sidecar.

## Windows process behavior

- External probe/encode tools must not steal focus or flash console windows.
- FFmpeg/gifski and ffprobe use Windows `CREATE_NO_WINDOW`; human testing confirmed popup windows are gone.

## Deferred

- Final working/loading animation and cast-transition behavior.
- Final application emblem/icon.
- ETA/time remaining.
- Advanced codec controls.
- Parallel jobs.
