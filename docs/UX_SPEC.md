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
- Display typography is self-contained: the supplied Polymorph Regular and Bold assets are bundled inside the application and registered with Qt before the UI is constructed. The user does not need the font installed on Windows. Inter is the bundled body/UI family; Cinzel remains only an emergency fallback if the branded display assets cannot be loaded.
- Current palette is near-black/very-dark blue-charcoal, ivory, cool white-gold/champagne and restrained crimson. Cards use smooth dark gradients, subtle neutral etched borders and restrained red selection states; they should not read as yellow-gold, grainy, or as a warm gold-to-black fade.
- Branded SVG icons must remain crisp at Windows high-DPI scale. Render vectors at final device-pixel size rather than rasterizing small and scaling them up.
- Loader/progress art is not part of the current fidelity pass. Arcane-circle and D20 concepts remain later design work.

## Typography ratios

- The user's Photoshop references are the visual basis rather than literal Qt point-size values.
- `POLYMORPH`: all caps, bundled Polymorph Regular, roughly the 120 pt reference with +350 Photoshop tracking; implementation should read distinctly wide-spaced and premium.
- Subtitle/byline: `Media conversion magic — by Knight Witch™`, bundled Polymorph Regular, mixed/proper case, roughly the 50/120 title-size ratio and +300 tracking reference.
- Card headings: bundled Polymorph Bold with restrained tracking and a deliberately compact desktop scale; they should be smaller than the dev.25/run-#84 tester while remaining clearly stronger than Inter body text.
- Primary `POLYMORPH` action uses the same bundled Polymorph display/tracking language as the application title.
- Body/control copy remains Inter for clarity and accessibility.

## Window and responsive behavior

- Design geometry: `1260x820`.
- Supported minimum: `920x640`.
- Below the design size, UI typography, margins, control geometry, queue rows, preview minimums and right-rail width scale down proportionally. The window should not hide the primary action or require a vertical rail scrollbar simply because the user makes the window smaller.
- Human dev.21 review accepted this proportional scaling behavior; preserve it unless later testing identifies a concrete regression.
- Enlarging the window may provide more preview/workspace room but should not create visually meaningless blank expanses inside controls.
- Resolution/file-size fields intentionally have no spinner arrows; users type the values directly.
- The max-MB field and the two resolution fields use the same responsive width and the same dark surface color. Disabled resolution fields may mute text/border contrast, but should not look like a differently colored panel.
- Radio buttons use conventional hollow-circle / centered-dot semantics, including disabled state.

## Card layout and alignment

- Busy cards use: supplied small cool-white-gold icon + Polymorph Bold heading, then a thin divider, then the controls.
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

- Ready/status is a two-line block: `Ready` with clearly smaller contextual text such as `2 files imported. Choose your settings and begin.`
- The Ready/loading ring is intentionally much larger than the dev.25/run-#84 tester, visually comparable to the approved mockup's status indicator.
- Service controls are labeled, not icon-only, and are spaced with visible separators: Check for Updates, GitHub, Ko-fi, Patreon, Discord.
- Footer links need breathing room; avoid a dense icon/text cluster.
- A horizontal divider separates the service/status row from metadata.
- Bottom-left: `Polymorph v<version>`.
- Bottom-right: `Polymorph 2026, Knight Witch™`.

## Primary action

- Main copy is `POLYMORPH`, not `Cast Polymorph`.
- A much smaller secondary line directly beneath it reads `CONVERT MEDIA`.
- The action fills the available right-rail action width and should be visually substantial/tall rather than a narrow strip stranded above blank space.
- Primary action uses a deep crimson/black gradient, cool white-gold/champagne border/highlight, bundled Polymorph Regular tracked title and restrained static sigil/line decoration.
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
