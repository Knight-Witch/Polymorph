# Windows Build

The Windows development build is produced by GitHub Actions on the `dev` branch.

The workflow:

1. Installs Python dependencies.
2. Downloads the pinned Gyan FFmpeg 9.0.1 Essentials Windows build and verifies its published SHA-256.
3. Builds gifski 1.32.0 from crates.io with Cargo.
4. Runs a toolchain smoke test that creates an animated WebP and verifies the exact bundled FFmpeg/ffprobe/gifski can decode it, apply Crop/Scale/Fit-style filters, stream YUV4MPEG into gifski, encode H.264, and retain the test frame count.
5. Generates a temporary placeholder icon if no final icon is present.
6. Packages Polymorph with PyInstaller in one-directory mode.
7. Compiles a per-user Inno Setup installer.
8. Generates a SHA-256 checksum.
9. Uploads both the installer and unpacked application as workflow artifacts.

No public GitHub Release is created by the development workflow.
