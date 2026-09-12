# UX Specification

## Primary flow

Files -> Output Format -> Sizing Constraint -> GIF Priority -> Framing -> Polymorph

## Window and interaction ergonomics

- Default development window opens at 1080x800 so the full right-side control rail has enough vertical room after the GIF-priority section was added.
- Minimum window size is 900x700; users can still resize freely above that floor.
- Core form controls have minimum visual heights so labels and field values do not collapse or clip when the window is resized.
- Primary controls expose concise hover tooltips rather than adding permanent explanatory text to the interface.
- Tooltips cover the file queue/preview, output formats, sizing modes and fields, GIF priority choices, framing controls, output folder, and conversion action.
- Existing footer icon controls retain their service-specific hover tooltips.

## Main preview

- Animated source preview is the visual centerpiece.
- Original mode shows the full source.
- Crop mode shows the selected ratio and supports drag-to-reposition; dragging behaves as moving the visible source image.
- Fit mode preserves the full source and pads to the chosen ratio; supports drag-to-reposition and background color.

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
- Source content cannot be upscaled above native size.
- Adaptive GIF frame reduction is disabled because the user has already chosen the spatial target explicitly.

## GIF priority

Visible only as meaningful controls for GIF + Fit under file size.

### Preserve motion

- Default.
- Keeps the source frame rate and every source frame.
- Uses spatial resolution as the file-size tradeoff.

### Favor resolution

- Experimental source-frame-decimation behavior introduced in dev.13 and carried into dev.14 unchanged.
- The user does not enter an FPS or target pixel size.
- Polymorph first creates the normal Preserve-motion fitted result.
- Dev.9-dev.12 proved that uniformly synthesized intermediate frames can consume enough GIF bytes to erase the expected resolution gain, so dev.13 stops synthesizing frames entirely.
- Polymorph now tests exact every-Nth-source-frame decimation nearest the original motion first and measures the real gifski byte cost at the Preserve-motion dimensions.
- A candidate must predict at least about 8% linear-resolution gain before Polymorph runs the full adaptive size search.
- For a 25 FPS source, dev.13 tests retaining every second source frame first (~12.5 FPS nominal), then every third frame (~8.33 FPS nominal) only if needed.
- Frame sacrifice is deterministic across the spin rather than periodic 1/2-step deletion. If the source frame count is not divisible by the stride, Polymorph shortens only the final GIF frame delay so the loop closes at the original total duration/angular speed.
- No optical-flow warping or temporal blending is used in dev.13.
- If a candidate passes the byte-cost prediction but its full adaptive fit still fails to realize at least about 8% larger dimensions, Polymorph continues to the next source-frame stride instead of immediately returning Preserve motion.
- Preferred spatial target remains native resolution capped at 2048 px; Polymorph never upscales above native framed geometry.

## Completion readout

- Development adaptive UI reports the actual result dimensions, decimal MB, and effective average output FPS.
- A decimated loop may have one shorter closure delay when the source frame count is not divisible by the chosen stride; the displayed FPS is therefore `output frames / original duration`.
- `MB` means decimal megabytes consistently with the file-size ceiling.

## Footer

Icon-only controls with hover tooltips:

- Check for updates
- View source on GitHub
- Support me on Ko-fi
- Support me on Patreon
- Join the Discord

The service glyphs are monochrome so the footer remains visually restrained. The final Polymorph application emblem is a separate asset and remains deferred.

## Deferred

- ETA/time remaining.
- Advanced codec controls.
- Parallel jobs.
