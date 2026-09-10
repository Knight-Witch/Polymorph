from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path

from PIL import Image, ImageDraw

FRAME_COUNT = 6
FPS = 25


def run(cmd: list[str], **kwargs) -> subprocess.CompletedProcess:
    proc = subprocess.run(cmd, capture_output=True, check=False, **kwargs)
    if proc.returncode != 0:
        stderr = proc.stderr.decode(errors="replace") if isinstance(proc.stderr, bytes) else (proc.stderr or "")
        stdout = proc.stdout.decode(errors="replace") if isinstance(proc.stdout, bytes) else (proc.stdout or "")
        raise RuntimeError(f"Command failed ({proc.returncode}): {' '.join(cmd)}\n{stderr}\n{stdout}")
    return proc


def frame_count(ffprobe: Path, path: Path) -> int:
    proc = run([
        str(ffprobe), "-v", "error", "-count_frames", "-select_streams", "v:0",
        "-show_entries", "stream=nb_read_frames", "-of", "json", str(path),
    ])
    payload = json.loads(proc.stdout.decode("utf-8"))
    streams = payload.get("streams") or []
    if not streams:
        raise RuntimeError(f"ffprobe returned no video stream for {path.name}")
    return int(streams[0].get("nb_read_frames") or 0)


def make_animated_webp(path: Path) -> None:
    frames: list[Image.Image] = []
    for i in range(FRAME_COUNT):
        img = Image.new("RGB", (96, 96), (14 + i * 12, 28 + i * 8, 46 + i * 5))
        draw = ImageDraw.Draw(img)
        x = 8 + i * 12
        draw.rectangle((x, 28, x + 22, 50), fill=(240, 220 - i * 10, 180 + i * 8))
        frames.append(img)
    frames[0].save(
        path,
        save_all=True,
        append_images=frames[1:],
        duration=[40] * FRAME_COUNT,
        loop=0,
        lossless=True,
        format="WEBP",
    )


def verify(ffmpeg: Path, ffprobe: Path, gifski: Path) -> None:
    with tempfile.TemporaryDirectory(prefix="polymorph-toolchain-") as tmp:
        root = Path(tmp)
        source = root / "source.webp"
        gif_out = root / "out.gif"
        mp4_out = root / "out.mp4"
        make_animated_webp(source)

        source_frames = frame_count(ffprobe, source)
        if source_frames != FRAME_COUNT:
            raise RuntimeError(f"Animated WebP decode mismatch: expected {FRAME_COUNT}, got {source_frames}")

        common = [
            str(ffmpeg), "-hide_banner", "-loglevel", "error", "-i", str(source),
            "-map", "0:v:0", "-an",
            "-vf", "crop=80:80:8:8,scale=64:64:flags=lanczos,pad=80:64:8:0:color=black,setsar=1",
            "-fps_mode", "passthrough",
        ]

        ffmpeg_proc = subprocess.Popen(
            common + ["-pix_fmt", "yuv444p", "-f", "yuv4mpegpipe", "pipe:1"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        assert ffmpeg_proc.stdout is not None
        gifski_proc = subprocess.Popen(
            [
                str(gifski), "--fps", str(FPS), "--quality", "100", "--extra",
                "--repeat", "0", "-o", str(gif_out), "-",
            ],
            stdin=ffmpeg_proc.stdout,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        ffmpeg_proc.stdout.close()
        _, ffmpeg_err = ffmpeg_proc.communicate()
        _, gifski_err = gifski_proc.communicate()
        if ffmpeg_proc.returncode != 0 or gifski_proc.returncode != 0:
            raise RuntimeError(
                "GIF streaming smoke test failed\n"
                f"ffmpeg={ffmpeg_proc.returncode}: {ffmpeg_err.decode(errors='replace')}\n"
                f"gifski={gifski_proc.returncode}: {gifski_err.decode(errors='replace')}"
            )
        if not gif_out.exists() or frame_count(ffprobe, gif_out) != FRAME_COUNT:
            raise RuntimeError("GIF smoke test did not preserve all frames")

        run(common + [
            "-c:v", "libx264", "-preset", "slow", "-crf", "16", "-pix_fmt", "yuv420p",
            "-movflags", "+faststart", "-y", str(mp4_out),
        ])
        if not mp4_out.exists() or frame_count(ffprobe, mp4_out) != FRAME_COUNT:
            raise RuntimeError("MP4 smoke test did not preserve all frames")

        print(f"Toolchain smoke test passed: {FRAME_COUNT}/{FRAME_COUNT} frames in GIF and MP4")


def main() -> int:
    tools = Path(sys.argv[1] if len(sys.argv) > 1 else "tools")
    suffix = ".exe" if sys.platform.startswith("win") else ""
    verify(tools / f"ffmpeg{suffix}", tools / f"ffprobe{suffix}", tools / f"gifski{suffix}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
