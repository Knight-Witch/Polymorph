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
- Favor resolution may intentionally reduce GIF FPS only through uniform motion interpolation when doing so yields a worthwhile spatial gain.

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

- Experimental in dev.9 pending full-resolution human validation.
- The user does not enter an FPS or target pixel size.
- Polymorph uses a soft 2048 px preferred long-edge target, capped by native source size.
- It only sacrifices FPS when the predicted linear-resolution gain is about 8% or greater.
- Automatic FPS never goes below 20 FPS in this first implementation.
- Lower rates are restricted to uniform GIF-centisecond cadences (`100 / N` FPS) so every output frame has the same duration.
- Polymorph chooses the highest eligible FPS that reaches at least 95% of the soft spatial target; if none reaches it, the lowest permitted viable FPS is used to honor the user's resolution preference.
- Frame reduction is produced with motion interpolation, not uneven deletion.
- No upscaling above native framed geometry.

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
