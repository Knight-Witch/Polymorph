from __future__ import annotations

import os
import shutil
import sys
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True, slots=True)
class Toolchain:
    ffmpeg: Path
    ffprobe: Path
    gifski: Path


def _candidate_roots() -> list[Path]:
    roots: list[Path] = []
    env = os.environ.get("POLYMORPH_TOOLS_DIR")
    if env:
        roots.append(Path(env))

    if getattr(sys, "frozen", False):
        exe_dir = Path(sys.executable).resolve().parent
        roots.extend([exe_dir / "tools", exe_dir / "_internal" / "tools", exe_dir / "_internal"])
    else:
        here = Path(__file__).resolve()
        roots.extend([here.parents[2] / "tools", here.parents[3] / "tools"])
    return roots


def _find(name: str) -> Path | None:
    executable = f"{name}.exe" if os.name == "nt" else name
    for root in _candidate_roots():
        candidate = root / executable
        if candidate.is_file():
            return candidate
    found = shutil.which(name)
    return Path(found) if found else None


def find_toolchain() -> Toolchain:
    ffmpeg = _find("ffmpeg")
    ffprobe = _find("ffprobe")
    gifski = _find("gifski")
    missing = [name for name, value in (("ffmpeg", ffmpeg), ("ffprobe", ffprobe), ("gifski", gifski)) if not value]
    if missing:
        raise FileNotFoundError(
            "Polymorph is missing required conversion components: " + ", ".join(missing)
        )
    return Toolchain(ffmpeg=ffmpeg, ffprobe=ffprobe, gifski=gifski)
