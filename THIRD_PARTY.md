# Third-Party Components

Polymorph bundles or invokes third-party software under licenses separate from the Knight Witch Community Source License.

## FFmpeg / ffprobe 9.0.1

- Project: https://ffmpeg.org/
- Bundled Windows build: FFmpeg 9.0.1 Essentials build by Gyan Doshi.
- Binary archive SHA-256: `49a73bdf0850092a252ac4641d922f3048d63ed113e196cc65ce1e4f7fb33e85`.
- Purpose: animated WebP decode, probing, filtering, scaling, framing, YUV4MPEG output, and H.264/MP4 encode.
- License used by the bundled build: GPLv3.
- Corresponding source: see `THIRD_PARTY_SOURCE.md`.

## gifski 1.32.0

- Project: https://github.com/ImageOptim/gifski
- Purpose: high-quality GIF encoding from YUV4MPEG data streamed by FFmpeg.
- License: AGPL-3.0-or-later.
- Corresponding source: see `THIRD_PARTY_SOURCE.md`.

## PySide6 / Qt for Python 6.11.2

- Project: https://doc.qt.io/qtforpython-6/
- Purpose: Windows desktop UI.
- Distribution option used by Polymorph: LGPLv3.
- Qt/PySide shared libraries remain dynamically loaded; Polymorph does not prohibit replacement or reverse engineering of those libraries for debugging modifications to them.
- Source and license information: see `THIRD_PARTY_SOURCE.md`.

## CPython 3.12.10

- Purpose: packaged Python runtime used by the frozen Windows application.
- License: Python Software Foundation License Version 2 and included historical notices.
- The official Windows 3.12.10 build bundles OpenSSL 3.0.16.

## OpenSSL 3.0.16

- Purpose: TLS/cryptographic runtime used by Python networking.
- License: Apache License 2.0.

## PyInstaller 6.22.3

- Purpose: build-time creation of the frozen Windows application and bootloader.
- Licensing: GPL-2.0-or-later with the PyInstaller Bootloader Exception; embedded runtime hooks/modules may use Apache-2.0 as documented by PyInstaller.

## Polymorph Regular / Bold

Polymorph Regular and Polymorph Bold are original first-party typefaces owned by Amanda Ivans / Knight Witch. They are covered by the project's main Knight Witch Community Source License v1.0 rather than a third-party font license. See `FIRST_PARTY_ASSETS.md`.

## Inter and Cinzel

- Inter is used for body/UI typography.
- Cinzel is an emergency display fallback.
- Both are distributed under the SIL Open Font License 1.1; their OFL texts ship with the application.

## Lucide Icons

- Project: https://github.com/lucide-icons/lucide
- Purpose: interface glyphs.
- License: ISC for Lucide artwork; some upstream Feather-derived glyphs are MIT as documented by Lucide.

## Simple Icons

- Project: https://github.com/simple-icons/simple-icons
- Purpose: GitHub, Ko-fi, Patreon, and Discord footer glyphs.
- License: CC0 1.0 Universal for the icon artwork repository. Brand names and logos may remain subject to their respective trademark rules.

## NSIS 3.12.0

- Project: https://nsis.sourceforge.io/
- Purpose: build-only creation of the Windows installer; NSIS is not bundled with Polymorph.
- License details: https://nsis.sourceforge.io/Docs/AppendixI.html

The installed Polymorph application includes the applicable license and notice texts under its `licenses` directory. Exact source locations are listed in `THIRD_PARTY_SOURCE.md`.
