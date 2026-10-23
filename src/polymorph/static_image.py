"""Still-image conversion without changing Polymorph's proven animation encoders.

Pillow preserves embedded ICC profiles and alpha, applies EXIF orientation exactly
once, and writes PNG or static WebP. File-size fitting changes only resolution.
"""
from __future__ import annotations

import io
from math import ceil
import shutil
import tempfile
import threading
from pathlib import Path
from typing import Callable

from PIL import Image, ImageCms, ImageOps, UnidentifiedImageError

from .geometry import FrameGeometry, _axis_position, native_geometry_for_size, scaled_dimensions, validate_requested_resolution
from .models import ConversionResult, ConversionSettings, FramingMode, MediaInfo, OutputFormat, SizingMode
from .size_units import mb_to_bytes

STILL_EXTENSIONS = {".png", ".jpg", ".jpeg", ".bmp", ".tif", ".tiff"}


class StillImageError(RuntimeError):
    pass


class StillImageCancelled(StillImageError):
    """Raised when the user interrupts a still-image batch."""
    pass


def is_still_image(path: Path) -> bool:
    path = Path(path)
    if path.suffix.lower() in STILL_EXTENSIONS:
        return True
    if path.suffix.lower() != ".webp":
        return False
    try:
        with Image.open(path) as image:
            return getattr(image, "n_frames", 1) == 1
    except (OSError, ValueError):
        return False


def probe_still_image(path: Path) -> MediaInfo:
    path = Path(path)
    try:
        with Image.open(path) as image:
            if getattr(image, "n_frames", 1) != 1:
                raise StillImageError("An animated image was passed to the still-image reader.")
            width, height = image.size
            # EXIF orientation 5-8 rotates through 90 degrees, swapping axes.
            if image.getexif().get(274, 1) in (5, 6, 7, 8):
                width, height = height, width
    except (UnidentifiedImageError, OSError, ValueError) as exc:
        raise StillImageError(f"Could not read still image: {path.name}: {exc}") from exc
    return MediaInfo(path=path, width=width, height=height, frame_count=1,
                     duration_s=0.0, is_still=True)


def _load_oriented_image(path: Path) -> tuple[Image.Image, bytes | None]:
    try:
        with Image.open(path) as source:
            if getattr(source, "n_frames", 1) != 1:
                raise StillImageError("Animated inputs cannot use static PNG/WebP output.")
            icc = source.info.get("icc_profile")
            image = ImageOps.exif_transpose(source)
    except (UnidentifiedImageError, OSError, ValueError) as exc:
        raise StillImageError(f"Could not decode {path.name}: {exc}") from exc

    # A tagged CMYK JPEG must be color-converted rather than having its raw
    # CMYK components interpreted as RGB. Other tagged RGB pixels and their ICC
    # profiles remain paired without a silent color-space conversion.
    if image.mode == "CMYK" and not icc:
        raise StillImageError(
            "This CMYK image has no embedded color profile; accurate RGB conversion "
            "is not possible. Export an sRGB copy with a profile first."
        )
    if image.mode == "CMYK" and icc:
        try:
            source_profile = ImageCms.ImageCmsProfile(io.BytesIO(icc))
            destination = ImageCms.ImageCmsProfile(ImageCms.createProfile("sRGB"))
            image = ImageCms.profileToProfile(
                image, source_profile, destination, outputMode="RGB"
            )
            icc = destination.tobytes()
        except (OSError, ValueError) as exc:
            raise StillImageError("CMYK color-profile conversion failed; refusing inaccurate color output.") from exc
    elif image.mode not in ("RGB", "RGBA", "L", "LA"):
        image = image.convert("RGBA" if "transparency" in image.info or image.mode == "P" and "transparency" in image.info else "RGB")

    # WebP and PNG both support alpha. Do not composite away transparency.
    if image.mode == "LA":
        image = image.convert("RGBA")
    return image, icc


def _frame_image(image: Image.Image, settings: ConversionSettings) -> Image.Image:
    framing = settings.framing
    if framing.mode is FramingMode.ORIGINAL or not framing.ratio:
        return image
    geometry = native_geometry_for_size(image.width, image.height, framing)
    if framing.mode is FramingMode.CROP:
        return image.crop((geometry.crop_x, geometry.crop_y,
                           geometry.crop_x + geometry.crop_width,
                           geometry.crop_y + geometry.crop_height))
    # FIT: the padding is opaque user-selected color; any alpha within the
    # original image survives because paste() is deliberately called without a mask.
    # Shared video geometry rounds to even sizes. For odd-pixel stills,
    # restore a ratio-correct canvas large enough to contain every pixel.
    # Even-size files continue to use the exact existing shared geometry.
    canvas_width, canvas_height = geometry.width, geometry.height
    pad_x, pad_y = geometry.pad_x, geometry.pad_y
    if image.width % 2 or image.height % 2:
        canvas_width = max(canvas_width, image.width)
        canvas_height = max(canvas_height, image.height)
        if canvas_width / canvas_height < framing.ratio:
            canvas_width = ceil(canvas_height * framing.ratio)
        else:
            canvas_height = ceil(canvas_width / framing.ratio)
        pad_x = _axis_position(canvas_width - image.width, framing.offset_x)
        pad_y = _axis_position(canvas_height - image.height, framing.offset_y)
    canvas = Image.new("RGBA" if "A" in image.getbands() else "RGB",
                       (canvas_width, canvas_height), framing.background)
    canvas.paste(image, (pad_x, pad_y))
    return canvas


def _encode(image: Image.Image, path: Path, output_format: OutputFormat,
            icc: bytes | None, webp_lossless: bool) -> None:
    if output_format is OutputFormat.PNG:
        image.save(path, format="PNG", optimize=True, compress_level=9,
                   **({"icc_profile": icc} if icc else {}))
    else:
        if image.mode not in ("RGB", "RGBA"):
            image = image.convert("RGBA" if "A" in image.getbands() else "RGB")
        image.save(path, format="WEBP", quality=95, method=6,
                   lossless=webp_lossless, exact=True,
                   **({"icc_profile": icc} if icc else {}))


def convert_still_image(source: Path, settings: ConversionSettings, output: Path,
                        cancelled: threading.Event,
                        progress: Callable[[float, str], None] | None = None) -> ConversionResult:
    if settings.output_format not in (OutputFormat.PNG, OutputFormat.WEBP):
        raise StillImageError("Still images require PNG or WebP output.")
    image, icc = _load_oriented_image(source)
    framed = _frame_image(image, settings)
    width, height = framed.size
    passes = 0

    def encode_candidate(scale: float, path: Path) -> tuple[int, int, int]:
        nonlocal passes
        if cancelled.is_set():
            raise StillImageCancelled("Cancelled")
        target = (width, height) if scale >= 1 else scaled_dimensions(
            FrameGeometry(width, height), scale
        )
        target = (min(width, target[0]), min(height, target[1]))
        candidate = framed if target == (width, height) else framed.resize(target, Image.Resampling.LANCZOS)
        _encode(candidate, path, settings.output_format, icc, settings.webp_lossless)
        passes += 1
        if progress:
            progress(min(0.95, passes / 10), "Optimizing image")
        return path.stat().st_size, *target

    with tempfile.TemporaryDirectory(prefix="polymorph-still-") as temp_dir:
        directory = Path(temp_dir)
        suffix = settings.output_format.value
        trial = directory / f"trial.{suffix}"
        best = directory / f"best.{suffix}"

        if settings.sizing_mode is SizingMode.RESOLUTION:
            if not settings.requested_width or not settings.requested_height:
                raise StillImageError("Set resolution requires pixel dimensions.")
            # Shared geometry check ensures no upscaling and retained framing ratio.
            scale = validate_requested_resolution(FrameGeometry(width, height),
                                                   settings.requested_width, settings.requested_height)
            encoded_size, final_width, final_height = encode_candidate(scale, trial)
            shutil.copyfile(trial, best)
        elif settings.sizing_mode is SizingMode.NATIVE:
            encoded_size, final_width, final_height = encode_candidate(1.0, trial)
            shutil.copyfile(trial, best)
        else:
            ceiling = mb_to_bytes(settings.max_mb)
            if ceiling <= 0:
                raise StillImageError("Maximum file size must be greater than zero.")
            encoded_size, final_width, final_height = encode_candidate(1.0, trial)
            if encoded_size <= ceiling:
                shutil.copyfile(trial, best)
            else:
                low, high = 0.0, 1.0
                found = False
                # Bounded binary search: highest measured resolution under the
                # requested decimal-MB ceiling. Compression settings stay fixed.
                for _ in range(9):
                    if cancelled.is_set():
                        raise StillImageCancelled("Cancelled")
                    scale = (low + high) / 2
                    size, w, h = encode_candidate(scale, trial)
                    if size <= ceiling:
                        low = scale
                        encoded_size, final_width, final_height = size, w, h
                        shutil.copyfile(trial, best)
                        found = True
                    else:
                        high = scale
                if not found:
                    raise StillImageError(
                        "Cannot meet the file-size limit with resolution reduction alone."
                    )
        if cancelled.is_set():
            raise StillImageCancelled("Cancelled")

        # Read back actual output dimensions/profile/alpha before publishing.
        with Image.open(best) as check:
            check.load()
            if check.size != (final_width, final_height) or getattr(check, "n_frames", 1) != 1:
                raise StillImageError("Static output verification failed (dimensions or frame count).")
            if icc and check.info.get("icc_profile") != icc:
                raise StillImageError("Static output verification failed (ICC color profile).")
            if "A" in framed.getbands() and "A" not in check.getbands():
                # libwebp omits redundant alpha for fully opaque RGBA images.
                # Check alpha at the actual encoded resolution, not input size.
                encoded_pixels = (framed if framed.size == (final_width, final_height)
                                  else framed.resize((final_width, final_height), Image.Resampling.LANCZOS))
                minimum_alpha, _ = encoded_pixels.getchannel("A").getextrema()
                if minimum_alpha < 255:
                    raise StillImageError("Static output verification failed (transparency lost).")
        output.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(best, output)
    if progress:
        progress(1.0, "Encoding")
    return ConversionResult(source=source, output=output, width=final_width,
                            height=final_height, size_bytes=encoded_size,
                            frames=1, duration_s=0.0, passes=passes)
