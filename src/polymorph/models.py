from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path


class OutputFormat(str, Enum):
    GIF = "gif"
    MP4 = "mp4"


class SizingMode(str, Enum):
    FILE_SIZE = "file_size"
    RESOLUTION = "resolution"


class FramingMode(str, Enum):
    ORIGINAL = "original"
    CROP = "crop"
    FIT = "fit"


class GifMotionMode(str, Enum):
    PRESERVE = "preserve"
    FAVOR_RESOLUTION = "favor_resolution"


@dataclass(slots=True)
class MediaInfo:
    path: Path
    width: int
    height: int
    frame_count: int
    duration_s: float
    frame_durations_ms: list[int] = field(default_factory=list)
    nominal_fps: float = 0.0

    @property
    def fps(self) -> float:
        if self.nominal_fps > 0:
            return self.nominal_fps
        if self.duration_s <= 0 or self.frame_count <= 0:
            return 0.0
        return self.frame_count / self.duration_s


@dataclass(slots=True)
class FramingSettings:
    mode: FramingMode = FramingMode.ORIGINAL
    ratio: float | None = None
    offset_x: float = 0.0  # -1 .. +1
    offset_y: float = 0.0  # -1 .. +1
    background: str = "#000000"
    zoom: float = 1.0  # Crop only; >=1.0, never used to upscale output content.


@dataclass(slots=True)
class ConversionSettings:
    output_format: OutputFormat = OutputFormat.GIF
    sizing_mode: SizingMode = SizingMode.FILE_SIZE
    max_mb: float = 99.0
    requested_width: int | None = None
    requested_height: int | None = None
    output_dir: Path | None = None
    framing: FramingSettings = field(default_factory=FramingSettings)
    gif_motion_mode: GifMotionMode = GifMotionMode.PRESERVE


@dataclass(slots=True)
class ConversionResult:
    source: Path
    output: Path
    width: int
    height: int
    size_bytes: int
    frames: int
    duration_s: float
    passes: int
