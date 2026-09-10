from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

from PIL import Image, ImageDraw

SOURCE_SIZE = (256, 256)
OUTPUT_SIZE = (192, 192)
FRAME_COUNT = 50
FPS = 25
FRAME_MS = 40
REFERENCE_PACKAGE_SHA256 = "f8f422ca350e32378979ec3110a69fa7daefdbd1005ac9937416f76e0bb71ecb"


def tool_version(path: Path, arg: str) -> str:
    proc = subprocess.run([str(path), arg], capture_output=True, text=True, check=False)
    text = (proc.stdout or proc.stderr or "").strip().splitlines()
    return text[0] if text else f"exit {proc.returncode}"


def make_source(path: Path) -> None:
    frames: list[Image.Image] = []
    for index in range(FRAME_COUNT):
        image = Image.new("RGB", SOURCE_SIZE)
        pixels = image.load()
        for y in range(SOURCE_SIZE[1]):
            for x in range(SOURCE_SIZE[0]):
                pixels[x, y] = (
                    (x * 3 + index * 7) % 256,
                    (y * 2 + index * 5) % 256,
                    ((x + y) * 2 + index * 11) % 256,
                )
        draw = ImageDraw.Draw(image)
        offset = (index * 5) % 210
        draw.rectangle((offset, 24, offset + 42, 74), fill=(245, 232, 210))
        draw.ellipse((150 - offset // 3, 140, 205 - offset // 3, 195), fill=(15, 15, 20))
        frames.append(image)

    frames[0].save(
        path,
        save_all=True,
        append_images=frames[1:],
        duration=[FRAME_MS] * FRAME_COUNT,
        loop=0,
        lossless=True,
        format="WEBP",
    )


def parse_rate(value: str | None) -> float:
    if not value or value in {"0/0", "N/A"}:
        return 0.0
    if "/" in value:
        num, den = value.split("/", 1)
        try:
            denominator = float(den)
            return float(num) / denominator if denominator else 0.0
        except ValueError:
            return 0.0
    try:
        return float(value)
    except ValueError:
        return 0.0


def probe(ffprobe: Path, path: Path) -> dict:
    cmd = [
        str(ffprobe),
        "-v", "error",
        "-count_frames",
        "-select_streams", "v:0",
        "-show_entries", "stream=width,height,nb_read_frames,avg_frame_rate,r_frame_rate,duration:format=duration",
        "-of", "json",
        str(path),
    ]
    proc = subprocess.run(cmd, capture_output=True, text=True, check=False)
    if proc.returncode != 0:
        raise RuntimeError(proc.stderr.strip() or f"ffprobe failed for {path.name}")
    payload = json.loads(proc.stdout)
    streams = payload.get("streams") or []
    if not streams:
        raise RuntimeError(f"ffprobe returned no stream for {path.name}")
    stream = streams[0]
    fmt = payload.get("format") or {}
    duration_raw = stream.get("duration") or fmt.get("duration") or 0
    try:
        duration = float(duration_raw)
    except (TypeError, ValueError):
        duration = 0.0
    return {
        "width": int(stream.get("width") or 0),
        "height": int(stream.get("height") or 0),
        "frames": int(stream.get("nb_read_frames") or 0),
        "duration_s": duration,
        "avg_fps": parse_rate(stream.get("avg_frame_rate")),
        "r_fps": parse_rate(stream.get("r_frame_rate")),
        "bytes": path.stat().st_size,
    }


def encode_variant(
    ffmpeg: Path,
    ffprobe: Path,
    gifski: Path,
    source: Path,
    output: Path,
    *,
    pixel_format: str | None,
    gifski_fps: int | None,
) -> dict:
    ffmpeg_cmd = [
        str(ffmpeg),
        "-hide_banner",
        "-loglevel", "error",
        "-i", str(source),
        "-vf", f"scale={OUTPUT_SIZE[0]}:{OUTPUT_SIZE[1]}:flags=lanczos",
        "-r", f"{FPS}/1",
    ]
    if pixel_format:
        ffmpeg_cmd += ["-pix_fmt", pixel_format]
    ffmpeg_cmd += ["-f", "yuv4mpegpipe", "pipe:1"]

    gifski_cmd = [str(gifski)]
    if gifski_fps is not None:
        gifski_cmd += ["--fps", str(gifski_fps)]
    gifski_cmd += [
        "--quality", "100",
        "--extra",
        "--repeat", "0",
        "--width", str(OUTPUT_SIZE[0]),
        "--output", str(output),
        "-",
    ]

    ffmpeg_log = output.with_suffix(".ffmpeg.log")
    gifski_log = output.with_suffix(".gifski.log")
    output.unlink(missing_ok=True)

    with ffmpeg_log.open("wb") as ff_err, gifski_log.open("wb") as gif_err:
        ff = subprocess.Popen(
            ffmpeg_cmd,
            stdout=subprocess.PIPE,
            stderr=ff_err,
            stdin=subprocess.DEVNULL,
        )
        assert ff.stdout is not None
        gif = subprocess.Popen(
            gifski_cmd,
            stdin=ff.stdout,
            stdout=subprocess.DEVNULL,
            stderr=gif_err,
        )
        ff.stdout.close()
        gif_rc = gif.wait()
        ff_rc = ff.wait()

    result = {
        "ok": ff_rc == 0 and gif_rc == 0 and output.exists(),
        "pixel_format": pixel_format or "automatic",
        "gifski_fps": gifski_fps,
        "ffmpeg_returncode": ff_rc,
        "gifski_returncode": gif_rc,
        "ffmpeg_command": ffmpeg_cmd,
        "gifski_command": gifski_cmd,
    }
    if result["ok"]:
        result.update(probe(ffprobe, output))
    else:
        result["ffmpeg_error"] = ffmpeg_log.read_text(errors="replace")[-4000:]
        result["gifski_error"] = gifski_log.read_text(errors="replace")[-4000:]
    return result


def comparison(a: dict, b: dict) -> dict:
    if not a.get("ok") or not b.get("ok"):
        return {"available": False}
    return {
        "available": True,
        "frame_ratio_a_over_b": a["frames"] / max(b["frames"], 1),
        "byte_ratio_a_over_b": a["bytes"] / max(b["bytes"], 1),
        "frame_delta": a["frames"] - b["frames"],
        "byte_delta": a["bytes"] - b["bytes"],
    }


def main() -> int:
    tools = Path(sys.argv[1] if len(sys.argv) > 1 else "tools")
    out_dir = Path(sys.argv[2] if len(sys.argv) > 2 else "build-smoke/gif-reference")
    out_dir.mkdir(parents=True, exist_ok=True)

    suffix = ".exe" if sys.platform.startswith("win") else ""
    ffmpeg = tools / f"ffmpeg{suffix}"
    ffprobe = tools / f"ffprobe{suffix}"
    gifski = tools / f"gifski{suffix}"

    source = out_dir / "reference-source-25fps.webp"
    make_source(source)

    variants: dict[str, dict] = {}
    definitions = [
        ("literal_reference", None, None),
        ("yuv420p_reference_no_gifski_fps", "yuv420p", None),
        ("yuv420p_full_frame_gifski_25fps", "yuv420p", FPS),
        ("yuv444p_reference_no_gifski_fps", "yuv444p", None),
        ("yuv444p_full_frame_gifski_25fps", "yuv444p", FPS),
    ]
    for name, pixel_format, gifski_fps in definitions:
        variants[name] = encode_variant(
            ffmpeg,
            ffprobe,
            gifski,
            source,
            out_dir / f"{name}.gif",
            pixel_format=pixel_format,
            gifski_fps=gifski_fps,
        )

    ref420 = variants["yuv420p_reference_no_gifski_fps"]
    full420 = variants["yuv420p_full_frame_gifski_25fps"]
    if not ref420.get("ok") or not full420.get("ok"):
        raise RuntimeError("Required yuv420p timing-control variants did not encode successfully")
    if full420["frames"] != FRAME_COUNT:
        raise RuntimeError(
            f"Explicit 25 FPS gifski path did not preserve all frames: {full420['frames']}/{FRAME_COUNT}"
        )
    if ref420["frames"] >= FRAME_COUNT:
        raise RuntimeError(
            "Reference-style gifski invocation without --fps did not reduce the 25 FPS source frame count as expected"
        )

    report = {
        "purpose": "CI-only controlled comparison of the supplied standalone GIF timing invocation against Polymorph's explicit full-frame gifski timing.",
        "reference_package_sha256": REFERENCE_PACKAGE_SHA256,
        "source": {
            "width": SOURCE_SIZE[0],
            "height": SOURCE_SIZE[1],
            "frames": FRAME_COUNT,
            "fps": FPS,
            "frame_ms": FRAME_MS,
            "duration_s": FRAME_COUNT / FPS,
        },
        "output_dimensions": {"width": OUTPUT_SIZE[0], "height": OUTPUT_SIZE[1]},
        "toolchain": {
            "ffmpeg": tool_version(ffmpeg, "-version"),
            "ffprobe": tool_version(ffprobe, "-version"),
            "gifski": tool_version(gifski, "--version"),
        },
        "variants": variants,
        "comparisons": {
            "420_reference_vs_fullframe": comparison(ref420, full420),
            "444_reference_vs_fullframe": comparison(
                variants["yuv444p_reference_no_gifski_fps"],
                variants["yuv444p_full_frame_gifski_25fps"],
            ),
            "literal_reference_vs_420_reference": comparison(
                variants["literal_reference"],
                ref420,
            ),
        },
    }
    report_path = out_dir / "reference-timing.json"
    report_path.write_text(json.dumps(report, indent=2), encoding="utf-8")

    print(json.dumps({
        "report": str(report_path),
        "reference_frames": ref420["frames"],
        "fullframe_frames": full420["frames"],
        "reference_bytes": ref420["bytes"],
        "fullframe_bytes": full420["bytes"],
        "literal_reference_ok": variants["literal_reference"]["ok"],
        "yuv444p_reference_ok": variants["yuv444p_reference_no_gifski_fps"]["ok"],
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
