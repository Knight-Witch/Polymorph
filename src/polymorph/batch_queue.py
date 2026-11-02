"""Pure conversion queue planning; GUI selection never mutates a running job."""
from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Mapping

from .geometry import linked_dimensions, native_geometry
from .models import ConversionSettings, MediaInfo, SizingMode


@dataclass(frozen=True, slots=True)
class BatchJob:
    source: Path
    settings: ConversionSettings


def resolve_shared_resolution(
    settings: ConversionSettings, info: MediaInfo, axis: str, pixels: int
) -> ConversionSettings:
    """Apply one requested axis to each source's independently framed geometry.

    If a source is smaller than the common target, cap at its own native
    dimensions rather than upscaling. Preserve selected framing/zoom/crop.
    """
    result = deepcopy(settings)
    if result.sizing_mode is not SizingMode.RESOLUTION:
        result.requested_width = None
        result.requested_height = None
        return result
    if axis not in ("width", "height"):
        raise ValueError("Shared resolution axis must be width or height")
    native = native_geometry(info, result.framing)
    width, height = linked_dimensions(native.width, native.height, int(pixels), axis)
    result.requested_width = width
    result.requested_height = height
    return result


def build_jobs(
    paths: list[Path],
    per_file: Mapping[Path, ConversionSettings],
    shared: ConversionSettings,
    apply_to_all: bool,
    axis: str,
    pixels: int,
    probe: Callable[[Path], MediaInfo],
) -> list[BatchJob]:
    """Freeze a deep-copied plan before the worker thread begins."""
    jobs = []
    for path in paths:
        if apply_to_all:
            settings = resolve_shared_resolution(shared, probe(path), axis, pixels)
        else:
            settings = deepcopy(per_file.get(path, shared))
        jobs.append(BatchJob(path, settings))
    return jobs
