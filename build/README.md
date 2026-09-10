# Windows Build

The Windows development build is produced by GitHub Actions on the `dev` branch.

The workflow:

1. Installs Python dependencies.
2. Downloads the pinned Gyan FFmpeg 9.0.1 Essentials Windows build and verifies its published SHA-256.
3. Builds gifski 1.32.0 from crates.io with Cargo.
4. Runs the normal toolchain smoke test against animated WebP, GIF, MP4, framing filters, and exact frame retention.
5. Runs a CI-only standalone-reference timing diagnostic at 25 FPS. It compares the supplied standalone command shape (FFmpeg `-r`, no gifski `--fps`) against an otherwise matched explicit-25-FPS gifski path, records dimensions/frame count/duration/file size/tool versions, and also records automatic/yuv420p/yuv444p Y4M behavior where supported.
6. Uploads the diagnostic JSON and tiny comparison media as `Polymorph-gif-reference-diagnostic`.
7. Generates a temporary placeholder icon if no final icon is present.
8. Packages Polymorph with PyInstaller in one-directory mode.
9. Launches the actual packaged `Polymorph.exe` in Qt offscreen mode and verifies bundled-tool discovery, footer SVG resources, animated WebP live-preview decoding, and linked 16:9 resolution controls.
10. Compiles a per-user Inno Setup installer.
11. Generates a SHA-256 checksum.
12. Uploads both the installer and unpacked application as workflow artifacts.

The reference diagnostic is build-only. It does not change the installed application's GIF, MP4, optimizer, framing, updater, preview, or UI behavior.

No public GitHub Release is created by the development workflow.
