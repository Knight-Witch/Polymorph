# Third-Party Components

Polymorph invokes third-party executables and uses third-party Python libraries. Their licenses remain separate from Polymorph's own Knight Witch Community Source License.

## FFmpeg / ffprobe

- Project: https://ffmpeg.org/
- Bundled Windows version: FFmpeg 9.0.1 Essentials build by Gyan Doshi.
- Build archive: `ffmpeg-9.0.1-essentials_build.7z`.
- Archive SHA-256: `49a73bdf0850092a252ac4641d922f3048d63ed113e196cc65ce1e4f7fb33e85`.
- FFmpeg source commit identified for the bundled build: `bf1b838f2a`.
- Purpose: animated WebP decode, filtering, scaling, padding/cropping, YUV4MPEG output, probing, and H.264/MP4 encode.
- Build license: GPLv3 as documented by the build provider.
- Packaged license text: `licenses/GPL-3.0.txt`.
- Corresponding source availability: `THIRD_PARTY_SOURCE.md`; the public release also attaches the identified source archive.

## gifski

- Project: https://github.com/ImageOptim/gifski
- Bundled version: 1.32.0.
- Purpose: high-quality GIF encoding from YUV4MPEG data streamed by FFmpeg.
- License: AGPL-3.0-or-later.
- Packaged license text: `licenses/AGPL-3.0-gifski.txt`.
- Corresponding source availability: `THIRD_PARTY_SOURCE.md`; the public release also attaches the exact 1.32.0 Cargo source package.

## PySide6 / Qt for Python

- Project: https://doc.qt.io/qtforpython-6/
- Bundled version: 6.11.2.
- Purpose: Windows desktop UI.
- Distribution option used by Polymorph: LGPLv3.
- Packaged license texts: `licenses/LGPL-3.0-Qt.txt` and `licenses/GPL-3.0.txt`.
- Official source location: `THIRD_PARTY_SOURCE.md`.
- Qt/PySide libraries are dynamically loaded shared libraries. Polymorph does not prohibit replacement or reverse engineering of those libraries for debugging modifications to them.

## CPython

- Version: 3.12.10.
- Purpose: packaged Python runtime used by the frozen Windows application.
- License: Python Software Foundation License Version 2 and included historical notices.
- Packaged license text: `licenses/PYTHON-3.12.10.txt`.
- The official Windows 3.12.10 build bundles OpenSSL 3.0.16.

## OpenSSL

- Version: 3.0.16 as bundled by the official CPython 3.12.10 Windows build.
- Purpose: TLS/cryptographic runtime used by Python networking.
- License: Apache License 2.0.
- Packaged license text: `licenses/OPENSSL-3.0.16.txt`.

## PyInstaller

- Build version: 6.22.3.
- Purpose: Windows executable bundle creation and bootloader.
- Licensing: GPL-2.0-or-later with the PyInstaller Bootloader Exception; embedded runtime hooks/modules may use Apache-2.0 as documented by PyInstaller.
- Packaged license text: `licenses/PYINSTALLER-6.22.3.txt`.

## Pillow

- Bundled runtime/build version: 12.3.0.
- Purpose: static PNG/WebP conversion, alpha/ICC preservation, EXIF orientation and icon generation.
- License: Pillow's permissive PIL Software License (MIT-CMU style).
- Packaged notice: `licenses/PILLOW-12.3.0.txt`.
- Source: https://github.com/python-pillow/Pillow/tree/12.3.0 .

## Polymorph Regular / Bold

- Original first-party typefaces owned by Amanda Ivans / Knight Witch.
- Purpose: Polymorph display/title typography.
- Packaged as losslessly compressed application subsets.
- Covered by the Knight Witch Community Source License v1.0; no separate third-party font license applies.
- See `FIRST_PARTY_ASSETS.md`.

## Cinzel

- Project source: Google Fonts / Cinzel.
- Purpose: emergency display fallback only if Polymorph's bundled Regular/Bold assets cannot be loaded.
- Bundled file: `Cinzel[wght].ttf`, pinned from google/fonts commit `45071f07c63e863a539442ef3562b71ab1f147a6`.
- Verified Git blob SHA-1: `d218a0b9c8879fd5a708872cc0ef357e507b35ca`.
- License: SIL Open Font License 1.1.
- Packaged notice: `polymorph/assets/fonts/OFL-Cinzel.txt`.

## Inter

- Project source: Google Fonts / Inter.
- Purpose: Polymorph body/UI typography.
- Bundled file: `Inter[opsz,wght].ttf`, pinned from google/fonts commit `e1d6480102fed30739fead0faee463101f892c8f`.
- Verified Git blob SHA-1: `047c92f6e2212473dc436020afed689527076d44`.
- License: SIL Open Font License 1.1.
- Packaged notice: `polymorph/assets/fonts/OFL-Inter.txt`.

## Lucide Icons

- Project: https://github.com/lucide-icons/lucide
- Purpose: section/navigation glyphs in the branded interface.
- License: ISC for Lucide artwork; some upstream Feather-derived glyphs are MIT as documented by Lucide's license.
- Packaged notice: `polymorph/assets/LUCIDE_LICENSE.txt`.

## Simple Icons

- Project: https://github.com/simple-icons/simple-icons
- Purpose: monochrome GitHub, Ko-fi, Patreon, and Discord footer glyphs.
- License: CC0 1.0 Universal for the icon artwork repository. Brand names/logos may remain subject to their respective trademark rules.

## NSIS

- Build-only compiler version: 3.12.0.
- Purpose: creation of the Windows installer; NSIS is not bundled with Polymorph.
- License: NSIS components are distributed under the licenses documented by the NSIS project, with its main source under the zlib/libpng license. Commercial use is expressly permitted by the zlib/libpng terms.

Exact source locations and public source availability are documented in `THIRD_PARTY_SOURCE.md`.
