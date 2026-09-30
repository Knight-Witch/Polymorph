# Third-Party Source Availability

Polymorph 0.1.0 bundles or invokes third-party components under their own licenses. This file identifies the source corresponding to the public Windows release. These third-party rights are separate from the Knight Witch Community Source License that applies to Polymorph's own code.

## FFmpeg / ffprobe 9.0.1

Polymorph ships the checksum-pinned Gyan Essentials build used by the validated release pipeline.

- Binary archive: `ffmpeg-9.0.1-essentials_build.7z`
- Binary archive SHA-256: `49a73bdf0850092a252ac4641d922f3048d63ed113e196cc65ce1e4f7fb33e85`
- Source commit identified for the bundled build: `bf1b838f2a`
- Corresponding source: https://github.com/FFmpeg/FFmpeg/archive/bf1b838f2a.tar.gz
- Upstream project: https://ffmpeg.org/
- License used by the bundled build: GPLv3

The public `v0.1.0` GitHub Release will also attach an FFmpeg source archive for the source revision identified above.

## gifski 1.32.0

- Exact bundled version: `1.32.0`
- Exact Cargo source package: https://crates.io/api/v1/crates/gifski/1.32.0/download
- Upstream source tag: https://github.com/ImageOptim/gifski/tree/1.32.0
- License: AGPL-3.0-or-later

The public `v0.1.0` GitHub Release will also attach the exact Cargo source package used for this version.

## PySide6 / Qt for Python 6.11.2

Polymorph uses the official PyPI wheels under the LGPLv3 option and dynamically loads the bundled Qt/PySide shared libraries.

- Version: `6.11.2`
- Official source archive: https://download.qt.io/official_releases/QtForPython/pyside6/PySide6-6.11.2-src/pyside-setup-everywhere-src-6.11.2.tar.xz
- Upstream source: https://code.qt.io/cgit/pyside/pyside-setup.git/
- Qt source: https://code.qt.io/cgit/qt/qt5.git/
- License used for distribution: LGPLv3

The installed application includes the LGPLv3 and GPLv3 license texts. Polymorph does not prohibit replacement or reverse engineering of the Qt/PySide shared libraries for debugging modifications to those libraries.

## CPython 3.12.10

- Version: `3.12.10`
- Source: https://github.com/python/cpython/archive/refs/tags/v3.12.10.tar.gz
- Release page: https://www.python.org/downloads/release/python-31210/
- License: Python Software Foundation License Version 2 and included historical notices

The Windows CPython 3.12.10 distribution bundles OpenSSL 3.0.16.

## OpenSSL 3.0.16

- Source: https://github.com/openssl/openssl/archive/refs/tags/openssl-3.0.16.tar.gz
- License: Apache License 2.0

## PyInstaller 6.22.3

- Build version: `6.22.3`
- Source: https://github.com/pyinstaller/pyinstaller/archive/refs/tags/v6.22.3.tar.gz
- Licensing: GPL-2.0-or-later with the PyInstaller Bootloader Exception; embedded runtime hooks/modules may use Apache-2.0 as described in PyInstaller's `COPYING.txt`.

## Fonts and icons

Cinzel and Inter are distributed under the SIL Open Font License 1.1 and their OFL texts ship with the application. Lucide attribution/license text ships with the application. Simple Icons artwork is CC0 1.0; third-party brand names and logos remain subject to their respective trademark rights.

Knight Witch's Polymorph display-font assets are covered separately by the project's own rights and are not relicensed by the third-party licenses listed here.

## Build-only installer compiler

The Windows release build uses Inno Setup 6.4.3. Inno Setup is used only to produce the installer and is not bundled as part of Polymorph.

For the complete component inventory and purposes, see `THIRD_PARTY.md`. Full license texts used by the packaged release are installed with the application.
