from __future__ import annotations

from pathlib import Path

APP_NAME = "Polymorph"
APP_VERSION = "0.1.0-dev.12"
APP_ORG = "Knight Witch"
REPO_URL = "https://github.com/Knight-Witch/Polymorph"
RELEASES_URL = f"{REPO_URL}/releases"
LATEST_RELEASE_API = "https://api.github.com/repos/Knight-Witch/Polymorph/releases/latest"

KOFI_URL = "https://ko-fi.com/knightwitch"
PATREON_URL = "https://www.patreon.com/TheKnightWitch"
DISCORD_URL = "https://discord.gg/jZxncZuTRy"

DEFAULT_MAX_MB = 99.0
FILE_SIZE_HEADROOM = 0.97
MAX_SIZE_PASSES = 6
MIN_SCALE = 0.10

SUPPORTED_INPUT_EXTENSIONS = {".webp"}

RATIO_PRESETS: list[tuple[str, float | None]] = [
    ("Original", None),
    ("1:1", 1.0),
    ("4:5", 4 / 5),
    ("3:4", 3 / 4),
    ("16:9", 16 / 9),
    ("9:16", 9 / 16),
    ("1.91:1", 1.91),
]

ASPECT_RATIO_GUIDE = [
    ("1:1", "Square posts, profile-style media, general-purpose sharing"),
    ("4:5", "Common portrait-oriented social feed format"),
    ("3:4", "General portrait imagery"),
    ("16:9", "Landscape video and widescreen previews"),
    ("9:16", "Vertical video, stories, reels, and short-form media"),
    ("1.91:1", "Wide landscape/social preview format"),
]


def default_output_dir() -> Path:
    downloads = Path.home() / "Downloads"
    return downloads if downloads.exists() else Path.home()
