# Polymorph 0.3.0 — Batch conversions

**Fixed:** Some conversion failure bugs

**NEW: Batch conversions!**

Upload multiple files and batch convert, with options for:

- **Globally-applied settings:** Share output format, framing, file-size ceiling, or one width/height target. With Set resolution, each file retains its aspect ratio; its other dimension is calculated independently without upscaling.
- **Individually-applied settings per-video:** Select each file, set output format, sizing, framing, aspect and crop, and move to the next without losing those settings. Then convert the whole queue.
- Convert every loaded file or a Ctrl/Shift-selected subset with one action, tracked overall progress and a local per-file result/error log.

Also includes improved conversion failure diagnostics, MP4→GIF/WebP integrity checks and typed widths such as 700 pixels. Still images and animations remain separate batch types.

The What's New dialog uses the requested batch message and retains the original Knight Witch support text, signature, Ko-fi and PayPal buttons and URLs. Media conversion remains entirely local. The high-fidelity GIF default, pinned FFmpeg 9.0.1 and gifski 1.32.0 are unchanged.

## Updating and installing

The in-app updater checks the [official public releases](https://github.com/Knight-Witch/Polymorph/releases). If no exact-compatible verified incremental patch is available, it offers the checksum-verified full installer. Close Polymorph before installing to release the existing EXE.

Download `Polymorph_Setup_v0.3.0.exe` and its `.sha256` from [v0.3.0](https://github.com/Knight-Witch/Polymorph/releases/tag/v0.3.0). Windows 10/11 x64. This unsigned installer may trigger SmartScreen. Third-party licenses and corresponding FFmpeg/gifski source are documented in `THIRD_PARTY.md` and `THIRD_PARTY_SOURCE.md`.
