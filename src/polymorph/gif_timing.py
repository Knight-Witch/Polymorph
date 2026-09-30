from __future__ import annotations

from pathlib import Path


class GifTimingError(RuntimeError):
    pass


def _skip_subblocks(data: bytes | bytearray, pos: int) -> int:
    length = len(data)
    while True:
        if pos >= length:
            raise GifTimingError("Unexpected end of GIF sub-block data.")
        size = data[pos]
        pos += 1
        if size == 0:
            return pos
        pos += size
        if pos > length:
            raise GifTimingError("Truncated GIF sub-block data.")


def frame_delay_offsets(data: bytes | bytearray) -> list[int]:
    """Return byte offsets of frame-delay fields in GIF Graphic Control Extensions."""
    if len(data) < 13 or bytes(data[:6]) not in {b"GIF87a", b"GIF89a"}:
        raise GifTimingError("Not a valid GIF file.")

    packed = data[10]
    pos = 13
    if packed & 0x80:
        table_entries = 1 << ((packed & 0x07) + 1)
        pos += table_entries * 3

    delays: list[int] = []
    pending_delay: int | None = None
    length = len(data)

    while pos < length:
        marker = data[pos]
        if marker == 0x3B:
            break

        if marker == 0x21:
            if pos + 2 >= length:
                raise GifTimingError("Truncated GIF extension.")
            label = data[pos + 1]
            if label == 0xF9:
                if pos + 7 >= length or data[pos + 2] != 4 or data[pos + 7] != 0:
                    raise GifTimingError("Malformed GIF Graphic Control Extension.")
                pending_delay = pos + 4
                pos += 8
                continue

            pos += 2
            if pos >= length:
                raise GifTimingError("Truncated GIF extension block.")
            block_size = data[pos]
            pos += 1 + block_size
            if pos > length:
                raise GifTimingError("Truncated GIF extension block.")
            pos = _skip_subblocks(data, pos)
            continue

        if marker == 0x2C:
            if pos + 9 >= length:
                raise GifTimingError("Truncated GIF image descriptor.")
            image_packed = data[pos + 9]
            pos += 10
            if image_packed & 0x80:
                table_entries = 1 << ((image_packed & 0x07) + 1)
                pos += table_entries * 3
            if pos >= length:
                raise GifTimingError("Truncated GIF image data.")
            pos += 1
            pos = _skip_subblocks(data, pos)
            if pending_delay is None:
                raise GifTimingError("GIF frame has no Graphic Control Extension delay.")
            delays.append(pending_delay)
            pending_delay = None
            continue

        raise GifTimingError(f"Unexpected GIF block marker 0x{marker:02x}.")

    if not delays:
        raise GifTimingError("GIF contains no timed image frames.")
    return delays


def read_frame_delays_cs(path: Path) -> list[int]:
    data = path.read_bytes()
    offsets = frame_delay_offsets(data)
    return [data[offset] | (data[offset + 1] << 8) for offset in offsets]


def patch_last_frame_delay(path: Path, delay_centiseconds: int) -> None:
    """Patch only the final GIF frame delay without touching encoded image data."""
    if not 1 <= delay_centiseconds <= 0xFFFF:
        raise GifTimingError("GIF frame delay must be between 1 and 65535 centiseconds.")

    data = bytearray(path.read_bytes())
    offsets = frame_delay_offsets(data)
    offset = offsets[-1]
    data[offset] = delay_centiseconds & 0xFF
    data[offset + 1] = (delay_centiseconds >> 8) & 0xFF
    path.write_bytes(data)
