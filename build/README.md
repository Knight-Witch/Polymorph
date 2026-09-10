# Windows Build

The Windows development build is produced by GitHub Actions on the `dev` branch.

The workflow:

1. Installs Python dependencies.
2. Downloads a pinned FFmpeg Windows build.
3. Builds gifski 1.32.0 from crates.io with Cargo.
4. Generates a temporary placeholder icon if no final icon is present.
5. Packages Polymorph with PyInstaller in one-directory mode.
6. Compiles a per-user Inno Setup installer.
7. Generates a SHA-256 checksum.
8. Uploads both the installer and unpacked application as workflow artifacts.

No public GitHub Release is created by the development workflow.
