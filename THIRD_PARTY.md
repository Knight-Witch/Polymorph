# Third-Party Components

Polymorph invokes third-party executables and uses third-party Python libraries. Their licenses remain separate from Polymorph's own source license.

## FFmpeg / ffprobe

- Project: https://ffmpeg.org/
- Windows development bundle: FFmpeg 9.0.1 Essentials build by Gyan Doshi.
- Build archive: `ffmpeg-9.0.1-essentials_build.7z`.
- Archive SHA-256: `49a73bdf0850092a252ac4641d922f3048d63ed113e196cc65ce1e4f7fb33e85`.
- FFmpeg source commit referenced by the build provider: `bf1b838f2a`.
- Purpose: animated WebP decode, filtering, scaling, padding/cropping, YUV4MPEG output, probing, and H.264/MP4 encode.
- Build license: GPLv3 as documented by the build provider.
- The exact release bundle and corresponding license/source notices must be retained for a public release.

## gifski

- Project: https://github.com/ImageOptim/gifski
- Bundled development version: 1.32.0.
- Purpose: high-quality GIF encoding from YUV4MPEG data streamed by FFmpeg.
- License: AGPL-3.0-or-later.
- Development rationale: dev.4 isolated stable 1.34.0 and produced a smaller maximum Viper resolution (`1532x1532`) than the human-validated 1.32.0 + `yuv420p` dev.3 result (`1592x1592`). Polymorph therefore returns to 1.32.0 while preserving source FPS/frame count explicitly.

## PySide6 / Qt for Python

- Project: https://doc.qt.io/qtforpython-6/
- Purpose: Windows desktop UI.
- License: LGPLv3/GPLv3/commercial options; release packaging must comply with the selected distribution terms.

## PyInstaller

- Project: https://pyinstaller.org/
- Purpose: Windows executable bundle creation.

## Cinzel

- Project source: Google Fonts / Cinzel.
- Purpose: Polymorph display typography.
- Bundled file: `Cinzel[wght].ttf`, pinned from google/fonts commit `45071f07c63e863a539442ef3562b71ab1f147a6`.
- Verified Git blob SHA-1: `d218a0b9c8879fd5a708872cc0ef357e507b35ca`.
- License: SIL Open Font License 1.1.
- The packaged font directory includes `OFL-Cinzel.txt`.

## Inter

- Project source: Google Fonts / Inter.
- Purpose: Polymorph body/UI typography.
- Bundled file: `Inter[opsz,wght].ttf`, pinned from google/fonts commit `e1d6480102fed30739fead0faee463101f892c8f`.
- Verified Git blob SHA-1: `047c92f6e2212473dc436020afed689527076d44`.
- License: SIL Open Font License 1.1.
- The packaged font directory includes `OFL-Inter.txt`.

## Simple Icons

- Project: https://github.com/simple-icons/simple-icons
- Purpose: monochrome GitHub, Ko-fi, Patreon, and Discord footer glyphs.
- License: CC0 1.0 Universal for the icon artwork repository. Brand names/logos may remain subject to their respective trademark rules.

No public binary release should be published until the exact bundled dependency versions and license notices are finalized.
