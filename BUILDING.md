# Building Polymorph 0.1.0

The official Windows release is produced from the validated Knight Witch release toolchain. The public source is intentionally limited to the stable product and does not include private development diagnostics, historical test fixtures, or internal CI configuration.

## Validated toolchain

- Windows x64
- Python 3.12.10
- PySide6 6.11.2
- PyInstaller 6.22.3
- Pillow 12.3.0 (build-only icon generation)
- FFmpeg / ffprobe 9.0.1 Essentials build
- gifski 1.32.0
- NSIS 3.12.0 (installer compiler only)

## Python environment

From the repository root:

```powershell
python -m pip install --upgrade pip
python -m pip install . pyinstaller==6.22.3 pillow==12.3.0
```

## Conversion tools

Create a `tools` directory containing:

```text
tools/
  ffmpeg.exe
  ffprobe.exe
  gifski.exe
```

The official release uses the FFmpeg 9.0.1 Essentials archive identified in `THIRD_PARTY.md` and gifski 1.32.0. Exact source locations are documented in `THIRD_PARTY_SOURCE.md`.

## Font assets

The public repository includes the first-party Polymorph display-font subsets used by the application. Inter and Cinzel are fetched from the pinned Google Fonts revisions documented by the project and placed in `src/polymorph/assets/fonts/` together with their OFL notices before packaging.

The expected runtime filenames are:

```text
Polymorph-Regular.ttf.xz
Polymorph-Bold.ttf.xz
Inter-opsz-wght.ttf
Cinzel-wght.ttf
OFL-Inter.txt
OFL-Cinzel.txt
```

## License texts

Before packaging, populate `legal/` with the applicable GPLv3, AGPLv3, LGPLv3, CPython 3.12.10, OpenSSL 3.0.16, and PyInstaller 6.22.3 license texts. These files are bundled into the installed application's `licenses` directory.

## Build the application

Generate the application icon, then freeze the app:

```powershell
python build\make_app_icon.py
pyinstaller --noconfirm --clean build\Polymorph.spec
```

The result is created under `dist\Polymorph\`.

## Build the installer

Install NSIS 3.12.0, then from the `installer` directory run:

```powershell
makensis.exe Polymorph.nsi
```

The installer is written as:

```text
installer\Output\Polymorph_Setup_v0.1.0.exe
```

Generate a SHA-256 checksum for the installer before distribution.

## Official releases

Official release binaries are published only through this repository's GitHub Releases. A locally built copy is not an official Knight Witch release and should not be presented or redistributed as one except where the project license expressly permits it.
