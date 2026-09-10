# Third-Party Components

Polymorph invokes third-party executables and uses third-party Python libraries. Their licenses remain separate from Polymorph's own source license.

## FFmpeg / ffprobe

- Project: https://ffmpeg.org/
- Purpose: media decode, filtering, scaling, padding/cropping, and MP4 encode.
- License: depends on the exact distributed build configuration. The release process must record the bundled build and provide the corresponding license/source information.

## gifski

- Project: https://github.com/ImageOptim/gifski
- Minimum required version for the streaming pipeline: 1.32.0
- Purpose: high-quality GIF encoding from YUV4MPEG data streamed by FFmpeg.
- License: AGPL-3.0-or-later.

## PySide6 / Qt for Python

- Project: https://doc.qt.io/qtforpython-6/
- Purpose: Windows desktop UI.
- License: LGPLv3/GPLv3/commercial options; release packaging must comply with the selected distribution terms.

## PyInstaller

- Project: https://pyinstaller.org/
- Purpose: Windows executable bundle creation.

No public binary release should be published until the exact bundled dependency versions and license notices are finalized.
