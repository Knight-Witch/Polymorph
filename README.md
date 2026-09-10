# Polymorph

Polymorph is a Windows desktop media-transmutation utility focused on simple, high-quality animated WebP conversion and social-media framing.

> Current status: early development. No public installer has been released yet.

## Goals

- High-fidelity animated WebP -> GIF conversion using the proven FFmpeg -> YUV4MPEG -> gifski pipeline.
- High-quality animated WebP -> MP4 conversion.
- Preserve source frames, playback smoothness, and timing.
- GIF output loops indefinitely.
- Two mutually exclusive sizing modes:
  - **Fit under file size** (default: 99 MB): keep encoder quality fixed and reduce only output resolution as needed.
  - **Set resolution**: keep the requested pixel dimensions and do not also chase a file-size target.
- Never upscale source content above 100%.
- Original / Crop / Fit framing modes with live animated preview.
- Batch queue with one active conversion at a time.
- Local-only conversion. Media is not uploaded.
- Automatic update checks while the app is open; no background service or startup daemon.

## Repository

This repository is the canonical source and release home for Polymorph.

- Source: https://github.com/Knight-Witch/Polymorph
- Releases: https://github.com/Knight-Witch/Polymorph/releases

## Development

Polymorph is being built with Python + PySide6. External conversion engines remain separate executables invoked by Polymorph:

- FFmpeg / ffprobe
- gifski 1.32.0+

The project intentionally keeps conversion logic separate from UI code so quality-critical encoder behavior can be tested independently.

## License

A project license will be selected before the first public binary release. Third-party components retain their own licenses; see `THIRD_PARTY.md`.
