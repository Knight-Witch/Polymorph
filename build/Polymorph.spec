# -*- mode: python ; coding: utf-8 -*-
from pathlib import Path

# PyInstaller exposes SPECPATH as the directory containing this spec file.
root = Path(SPECPATH).parent
icon = root / "build" / "polymorph_placeholder.ico"

a = Analysis(
    [str(root / "run_polymorph.py")],
    pathex=[str(root / "src")],
    binaries=[
        (str(root / "tools" / "ffmpeg.exe"), "tools"),
        (str(root / "tools" / "ffprobe.exe"), "tools"),
        (str(root / "tools" / "gifski.exe"), "tools"),
    ],
    datas=[
        (str(root / "THIRD_PARTY.md"), "."),
    ],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name="Polymorph",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    console=False,
    icon=str(icon) if icon.exists() else None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=False,
    upx_exclude=[],
    name="Polymorph",
)
