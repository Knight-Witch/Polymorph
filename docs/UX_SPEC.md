# UX Specification

## Primary flow

Files -> Output Format -> Sizing Constraint -> GIF Priority -> Framing -> Polymorph

## Window and interaction ergonomics

- Development window opens at 1080x800; minimum size is 900x700.
- Core controls keep minimum visual heights so values/labels do not collapse when resized.
- Primary controls use concise hover tooltips instead of permanent explanatory clutter.
- Selected radio buttons must have an unmistakable visible checked indicator. A checked state must never be represented by making the indicator disappear.
- External conversion/probe tools must not open console windows or steal focus during normal use.
- Final visual skin remains deferred until behavior is stable.

## Main preview

The animated preview is the visual centerpiece and is expected to represent the actual framing semantics, not merely approximate the target aspect ratio.

### Original

- Shows the source without framing changes.
- Drag and manual framing zoom are disabled.

### Crop to ratio

- The target frame is the selected aspect ratio.
- Source aspect ratio is always preserved.
- The source is scaled only enough to cover the target frame, then overflow is clipped.
- It must never stretch or squash the source to become the target ratio.
- Dragging moves the visible source composition under the frame.
- Zoom is available from 100% to 400% for deliberate tighter composition.
- Mouse wheel over the preview also adjusts zoom.

### Fit to ratio

- The target frame is the selected aspect ratio.
- Source aspect ratio is always preserved.
- At 100% framing zoom, the complete source is contained and the remaining canvas is padded with the chosen background color.
- Dragging repositions contained content within available padded space.
- Zoom is available from 100% to 400%; once zoom makes the source larger than a canvas axis, that axis may be intentionally cropped while the source itself remains undistorted.
- Mouse wheel over the preview also adjusts zoom.

### Position and zoom controls

- `Center` resets X/Y positioning but intentionally leaves zoom unchanged.
- The visible Zoom slider and mouse-wheel zoom control the same `FramingSettings.zoom` value.
- Preview and exported output use the same shared placement model, so the composition shown to the user should match the conversion result.

## Sizing modes

### Fit under file size

- Default ceiling: 99 MB, decimal.
- User specifies only the ceiling.
- Encoder quality remains fixed; output dimensions are adjusted to fit.
- Preserve motion keeps source timing/frame sequence fixed.
- Favor resolution may retain fewer original source frames only when measured byte savings buy a worthwhile spatial gain.

### Set resolution

- User specifies output pixel dimensions.
- Width/height stay linked to the active framed canvas ratio.
- File-size target is disabled.
- Output canvas cannot exceed its native framed size.
- Manual Crop/Fit zoom changes composition inside that canvas; it does not secretly increase the output-resolution ceiling.
- Favor-resolution temporal reduction is disabled because the user has explicitly chosen spatial output size.

## GIF priority

### Preserve motion

- Default.
- Keeps every source frame and the source frame rate.
- Uses spatial resolution as the file-size tradeoff.

### Favor resolution

- Explicit opt-in for GIF + Fit under file size.
- Polymorph first obtains the normal Preserve-motion fitted result.
- It then tests exact every-Nth-original-source-frame candidates, nearest motion first, and measures their actual gifski byte cost at the Preserve dimensions.
- A candidate must predict about 8% linear spatial gain before full fitting and must independently realize about 8% after fitting.
- For 25 FPS sources the automatic 8 FPS floor normally permits stride 2 (~12.5 FPS nominal) then stride 3 (~8.33 FPS nominal).
- No optical-flow or temporal-blend image synthesis is used in dev.13+.
- If source frame count is not divisible by the stride, only the last GIF delay is shortened to preserve original total duration/angular speed.
- Preferred adaptive spatial target is native framed size capped at 2048 px; no source upscaling.
- Human testing has validated stride-2 motion on Viper and two more complex 500-frame kitbash/decal-heavy workloads.

## Completion readout

- Development adaptive UI reports final dimensions, decimal MB, and effective average output FPS.
- A decimated loop may have one shorter closure delay; displayed FPS is output frames divided by original duration.
- Development Favor-resolution runs currently also report the `*_ADAPTIVE_DIAGNOSTIC.json` sidecar filename.
- Preserve-motion and MP4 do not emit the adaptive sidecar.

## Windows focus behavior

- Loading media may invoke ffprobe for metadata.
- Encoding/optimization may invoke ffprobe again for integrity checks.
- These probes, plus FFmpeg/gifski encode processes, must run without opening visible console windows or interrupting the user's active application.

## Footer

Icon-only controls with hover tooltips:

- Check for updates
- View source on GitHub
- Support me on Ko-fi
- Support me on Patreon
- Join the Discord

The final Polymorph application emblem is separate and remains deferred.

## Deferred

- Final visual skin and arcane progress treatment.
- Custom aspect-ratio workflow polish.
- ETA/time remaining.
- Advanced codec/adaptive controls.
- Parallel jobs.
