# UX Specification

## Primary flow

Files -> Output Format -> Sizing Constraint -> Framing -> Polymorph

## Main preview

- Animated source preview is the visual centerpiece.
- Original mode shows the full source.
- Crop mode shows the selected ratio and supports drag-to-reposition; dragging behaves as moving the visible source image.
- Fit mode preserves the full source and pads to the chosen ratio; supports drag-to-reposition and background color.

## Sizing modes

### Fit under file size

- Default: 99 MB.
- User specifies only the ceiling.
- Encoder quality, source timing, and frame sequence stay fixed.
- Resolution is automatically adjusted to fit.

### Set resolution

- User specifies output pixel dimensions.
- Width and height stay automatically linked to the active framed aspect ratio; no extra aspect-lock control is exposed.
- File-size target is disabled.
- Source content cannot be upscaled above native size.

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
