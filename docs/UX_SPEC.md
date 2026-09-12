# UX Specification

## Primary flow

Files -> Output Format -> Sizing Constraint -> GIF Priority -> Framing -> Cast Polymorph

## Branded application composition

- The branded runtime uses a two-column composition instead of the old three-column development scaffold.
- The left workspace is dominant and contains the file queue above the animated preview.
- The right rail is a scrollable stack of distinct `OUTPUT FORMAT`, `SIZING`, `GIF PRIORITY`, `FRAMING`, `ASPECT RATIO`, and `OUTPUT FOLDER` cards, with `Cast Polymorph` anchored after the settings.
- Queue actions live with the queue: Add Files, Remove selected, and Clear queue. Clear removes queue entries only; it never deletes source files.
- The visible framing selector is Original / Crop / Fit radio controls. They are synchronized to the established framing state used by preview/export logic rather than introducing a second framing model.
- The header brand lockup is `POLYMORPH`, version, then `MEDIA CONVERSION MAGIC — BY KNIGHT WITCH™`.
- Mockup-only decorative slogans are intentionally excluded.
- Cinzel is the bundled display family for the title and primary action. Inter is the bundled body/UI family. Packaged builds include the pinned font files and SIL OFL notices.
- The current black/charcoal, ivory, champagne-gold, and restrained crimson palette remains the baseline visual direction.
- Loader/progress art is not part of this composition pass. The later magic-circle and D20 concepts remain separate design work.

## Window and interaction ergonomics

- The branded development window opens at 1280x880 so the preview remains dominant while the card rail can use readable 11pt body text.
- Minimum branded size is 1020x720; the right settings rail scrolls vertically when the window cannot show every card at once.
- Core form controls have minimum visual heights so labels and field values do not collapse or clip when the window is resized.
- Primary controls expose concise hover tooltips rather than adding permanent codec jargon to the interface.
- Tooltips cover the file queue/preview, output formats, sizing modes and fields, GIF priority choices, framing controls, output folder, and conversion action.
- Existing footer icon controls retain their service-specific hover tooltips.
- Radio buttons use conventional state styling: hollow circle when unselected, centered filled dot when selected. Disabled selected radios keep the same dot treatment in the dimmed disabled palette.

## Main preview

- Animated source preview is the visual centerpiece.
- Preview and export use the same framing geometry resolver; Crop/Fit must not stretch or distort source media.
- Original mode shows the full source.
- Crop mode trims the source to the selected ratio, supports drag-to-reposition, and exposes 100-300% crop zoom. Dragging behaves as moving the visible source image.
- Crop zoom reduces the retained source window rather than upscaling source content; the maximum export dimensions therefore shrink as zoom increases, preserving the no-upscale rule.
- Fit mode preserves the full source aspect ratio and expands the canvas to the chosen ratio with background padding; it supports drag-to-reposition within the available padding and a user-selected background color.
- Center resets source position within the current Crop/Fit framing but does not discard the chosen Crop zoom.
- Human dev.16/17 testing and subsequent real Crop/Fit exports validated preview/export framing parity end to end.

## Sizing modes

### Fit under file size

- Default: 99 MB.
- User specifies only the ceiling.
- Encoder quality remains fixed.
- Resolution is automatically adjusted to fit.
- Preserve motion keeps source timing/frame sequence fixed.
- Favor resolution may intentionally retain fewer source frames only when real encoded measurements show that doing so buys a worthwhile spatial gain.

### Set resolution

- User specifies output pixel dimensions.
- Width and height stay automatically linked to the active framed aspect ratio; no extra aspect-lock control is exposed.
- File-size target is disabled.
- Source content cannot be upscaled above native framed size.
- Adaptive GIF frame reduction is disabled because the user has already chosen the spatial target explicitly.

## GIF priority

Visible only as meaningful controls for GIF + Fit under file size.

### Preserve motion

- Default.
- Keeps the source frame rate and every source frame.
- Uses spatial resolution as the file-size tradeoff.

### Favor resolution

- Exact source-frame-decimation behavior introduced in dev.13 and validated with dev.15 diagnostics.
- The user does not enter an FPS or target pixel size.
- Polymorph first creates the normal Preserve-motion fitted result.
- Dev.9-dev.12 proved that uniformly synthesized intermediate frames can consume enough GIF bytes to erase the expected resolution gain, so dev.13+ stops synthesizing frames entirely.
- Polymorph tests exact every-Nth-source-frame decimation nearest the original motion first and measures the real gifski byte cost at the Preserve-motion dimensions.
- A candidate must predict at least about 8% linear-resolution gain before Polymorph runs the full adaptive size search.
- For a 25 FPS source, the current planner tests retaining every second source frame first (~12.5 FPS nominal), then every third frame (~8.33 FPS nominal) only if needed.
- Frame sacrifice is deterministic across the spin rather than periodic 1/2-step deletion. If the source frame count is not divisible by the stride, Polymorph shortens only the final GIF frame delay so the loop closes at the original total duration/angular speed.
- No optical-flow warping or temporal blending is used in dev.13+.
- If a candidate passes the byte-cost prediction but its full adaptive fit still fails to realize at least about 8% larger dimensions, Polymorph continues to the next source-frame stride instead of immediately returning Preserve motion.
- Preferred spatial target remains native resolution capped at 2048 px; Polymorph never upscales above native framed geometry.
- Real Viper plus two kitbash/decal-heavy HeroForge variants have selected stride 2 successfully; their motion was reported consistent, and the two 500-frame variants produced exactly uniform 80 ms frame timing.

## Completion readout

- Development adaptive UI reports the actual result dimensions, decimal MB, and effective average output FPS.
- A decimated loop may have one shorter closure delay when the source frame count is not divisible by the chosen stride; the displayed FPS is therefore `output frames / original duration`.
- `MB` means decimal megabytes consistently with the file-size ceiling.
- Development Favor-resolution runs currently report the filename of a compact `*_ADAPTIVE_DIAGNOSTIC.json` sidecar saved beside the GIF. The sidecar remains temporary developer instrumentation rather than part of the intended stable output contract.
- Preserve-motion and MP4 runs do not create that diagnostic sidecar.

## Windows process behavior

- External conversion/probe tools must not steal focus or flash console windows during ordinary GUI use.
- FFmpeg/gifski encoding already runs with Windows `CREATE_NO_WINDOW`.
- Dev.16 applies the same behavior to ffprobe, which is invoked when media loads and during output-integrity verification.
- Human dev.16 testing confirmed the popup windows no longer appear.

## Footer

Icon-only controls with hover tooltips:

- Check for updates
- View source on GitHub
- Support me on Ko-fi
- Support me on Patreon
- Join the Discord

The service glyphs are monochrome so the footer remains visually restrained. The final Polymorph application emblem is a separate asset and remains deferred.

## Deferred

- Final working/loading animation and cast-transition behavior.
- Final application emblem/icon.
- ETA/time remaining.
- Advanced codec controls.
- Parallel jobs.
