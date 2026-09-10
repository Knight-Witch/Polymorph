from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

from PIL import Image, ImageDraw

FRAME_COUNT = 6
FPS = 25
EXPECTED_SIZE = (80, 64)


def run(cmd: list[str], **kwargs) -> subprocess.CompletedProcess:
    proc = subprocess.run(cmd, capture_output=True, check=False, **kwargs)
    if proc.returncode != 0:
        stderr = proc.stderr.decode(errors="replace") if isinstance(proc.stderr, bytes) else (proc.stderr or "")
        stdout = proc.stdout.decode(errors="replace") if isinstance(proc.stdout, bytes) else (proc.stdout or "")
        raise RuntimeError(f"Command failed ({proc.returncode}): {' '.join(cmd)}\n{stderr}\n{stdout}")
    return proc


def stream_info(ffprobe: Path, path: Path) -> tuple[int, int, int]:
    proc = run([
        str(ffprobe), "-v", "error", "-count_frames", "-select_streams", "v:0",
        "-show_entries", "stream=width,height,nb_read_frames", "-of", "json", str(path),
    ])
    payload = json.loads(proc.stdout.decode("utf-8"))
    streams = payload.get("streams") or []
    if not streams:
        raise RuntimeError(f"ffprobe returned no video stream for {path.name}")
    stream = streams[0]
    return (
        int(stream.get("width") or 0),
        int(stream.get("height") or 0),
        int(stream.get("nb_read_frames") or 0),
    )


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


def verify(ffmpeg: Path, ffprobe: Path, gifski: Path, sample_out: Path | None = None) -> None:
    with tempfile.TemporaryDirectory(prefix="polymorph-toolchain-") as tmp:
        root = Path(tmp)
        source = root / "source.webp"
        gif_out = root / "out.gif"
        mp4_out = root / "out.mp4"
        make_animated_webp(source)

        if sample_out is not None:
            sample_out.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, sample_out)

        source_w, source_h, source_frames = stream_info(ffprobe, source)
        if source_frames != FRAME_COUNT or (source_w, source_h) != (96, 96):
            raise RuntimeError(
                f"Animated WebP decode mismatch: expected 96x96/{FRAME_COUNT} frames, "
                f"got {source_w}x{source_h}/{source_frames}"
            )

        common = [
            str(ffmpeg), "-hide_banner", "-loglevel", "error", "-i", str(source),
            "-map", "0:v:0", "-an",
            "-vf", "crop=80:80:8:8,scale=64:64:flags=lanczos,pad=80:64:8:0:color=black,setsar=1",
            "-fps_mode", "passthrough",
        ]

        # The standalone reference effectively handed gifski a 4:2:0 Y4M stream.
        # Pin that compatible format because FFmpeg 9.0.1 may otherwise retain RGB
        # after filtering, which yuv4mpegpipe refuses.
        ffmpeg_proc = subprocess.Popen(
            common + ["-pix_fmt", "yuv420p", "-f", "yuv4mpegpipe", "pipe:1"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        assert ffmpeg_proc.stdout is not None
        gifski_proc = subprocess.Popen(
            [
                str(gifski), "--fps", str(FPS), "--quality", "100", "--extra",
                "--repeat", "0", "--width", str(EXPECTED_SIZE[0]), "-o", str(gif_out), "-",
            ],
            stdin=ffmpeg_proc.stdout,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        ffmpeg_proc.stdout.close()
        _, gifski_err = gifski_proc.communicate()
        ffmpeg_err = ffmpeg_proc.stderr.read() if ffmpeg_proc.stderr else b""
        ffmpeg_rc = ffmpeg_proc.wait()
        if ffmpeg_rc != 0 or gifski_proc.returncode != 0:
            raise RuntimeError(
                "GIF streaming smoke test failed\n"
                f"ffmpeg={ffmpeg_rc}: {ffmpeg_err.decode(errors='replace')}\n"
                f"gifski={gifski_proc.returncode}: {gifski_err.decode(errors='replace')}"
            )

        gif_w, gif_h, gif_frames = stream_info(ffprobe, gif_out)
        if (gif_w, gif_h) != EXPECTED_SIZE or gif_frames != FRAME_COUNT:
            raise RuntimeError(
                f"GIF smoke mismatch: expected {EXPECTED_SIZE[0]}x{EXPECTED_SIZE[1]}/{FRAME_COUNT} frames, "
                f"got {gif_w}x{gif_h}/{gif_frames}"
            )

        run(common + [
            "-c:v", "libx264", "-preset", "slow", "-crf", "16", "-pix_fmt", "yuv420p",
            "-movflags", "+faststart", "-y", str(mp4_out),
        ])
        mp4_w, mp4_h, mp4_frames = stream_info(ffprobe, mp4_out)
        if (mp4_w, mp4_h) != EXPECTED_SIZE or mp4_frames != FRAME_COUNT:
            raise RuntimeError(
                f"MP4 smoke mismatch: expected {EXPECTED_SIZE[0]}x{EXPECTED_SIZE[1]}/{FRAME_COUNT} frames, "
                f"got {mp4_w}x{mp4_h}/{mp4_frames}"
            )

        print(
            f"Toolchain smoke test passed: {EXPECTED_SIZE[0]}x{EXPECTED_SIZE[1]}, "
            f"{FRAME_COUNT}/{FRAME_COUNT} frames in GIF and MP4"
        )


def main() -> int:
    tools = Path(sys.argv[1] if len(sys.argv) > 1 else "tools")
    sample_out = Path(sys.argv[2]) if len(sys.argv) > 2 else None
    suffix = ".exe" if sys.platform.startswith("win") else ""
    verify(
        tools / f"ffmpeg{suffix}",
        tools / f"ffprobe{suffix}",
        tools / f"gifski{suffix}",
        sample_out,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
