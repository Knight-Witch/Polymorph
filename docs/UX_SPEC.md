# UX Specification

## Primary flow

Files -> Output Format -> Sizing Constraint -> GIF Priority -> Framing -> Polymorph

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
- Favor resolution may intentionally reduce GIF FPS only through uniform motion interpolation when real encoded measurements show that doing so buys a worthwhile spatial gain.

### Set resolution

- User specifies output pixel dimensions.
- Width and height stay automatically linked to the active framed aspect ratio; no extra aspect-lock control is exposed.
- File-size target is disabled.
- Source content cannot be upscaled above native size.
- Adaptive GIF FPS is disabled because the user has already chosen the spatial target explicitly.

## GIF priority

Visible only as meaningful controls for GIF + Fit under file size.

### Preserve motion

- Default.
- Keeps the source frame rate and every source frame.
- Uses spatial resolution as the file-size tradeoff.

### Favor resolution

- Experimental in dev.10 pending validation of the lower clean cadence selected when 20 FPS is not worthwhile.
- The user does not enter an FPS or target pixel size.
- Polymorph first creates the normal Preserve-motion fitted result.
- It then tests lower uniform GIF cadences at that exact spatial size and measures the real gifski byte cost of the interpolated frames.
- The first/highest lower FPS that predicts at least about 8% real linear-resolution gain is eligible for a full adaptive size search.
- For a 25 FPS source, the automatic clean-cadence ladder is 20 FPS (50 ms) then 16.67 FPS (60 ms). The current automatic floor is 16.67 FPS.
- Lower rates are restricted to uniform GIF-centisecond cadences (`100 / N` FPS) so every output frame has the same duration.
- Frame reduction is produced with motion interpolation, not uneven deletion.
- A final measured-gain guard discards the lower-FPS result and returns the Preserve-motion output if the completed adaptive fit does not actually gain at least about 8% linear resolution.
- Preferred spatial target remains native resolution capped at 2048 px; Polymorph never upscales above native framed geometry.

## Completion readout

- Development adaptive UI reports the actual result dimensions, decimal MB, and effective output FPS.
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
