# Windows Build

The Windows development build is produced by GitHub Actions on the `dev` branch.

The workflow:

1. Installs Python dependencies.
2. Downloads the pinned Gyan FFmpeg 9.0.1 Essentials Windows build and verifies its published SHA-256.
3. Builds gifski 1.32.0 from crates.io with Cargo.
4. Runs the toolchain smoke test against animated WebP, Preserve-motion GIF, adaptive source-frame-decimated GIF, MP4, framing filters, exact full-frame retention, exact planned reduced-frame output, and lossless final-frame GIF delay patching for loop closure.
5. Runs a CI-only standalone-reference timing diagnostic at 25 FPS. It compares the patched-Python timing shape (FFmpeg `-r`, no gifski `--fps`) against an otherwise matched explicit-25-FPS gifski path and records dimensions/frame count/duration/file size/tool versions.
6. Uploads the diagnostic JSON and tiny comparison media as `Polymorph-gif-reference-diagnostic`.
7. Generates a temporary placeholder icon if no final icon is present.
8. Packages Polymorph with PyInstaller in one-directory mode.
9. Launches the actual packaged `Polymorph.exe` in Qt offscreen mode and verifies bundled-tool discovery, footer SVG resources, animated WebP live-preview decoding, adaptive GIF-priority controls, and linked 16:9 resolution controls.
10. Compiles a per-user Inno Setup installer.
11. Generates a SHA-256 checksum.
12. Uploads both the installer and unpacked application as workflow artifacts.

The reference timing diagnostic is build-only. Favor resolution is included in development builds for explicit human testing. Dev.13 no longer synthesizes intermediate frames: it tests exact every-Nth-source-frame decimation and patches only the final GIF delay when necessary to preserve the original loop duration/angular speed. Preserve motion remains unchanged.

No public GitHub Release is created by the development workflow.
