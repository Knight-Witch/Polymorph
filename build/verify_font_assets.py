from __future__ import annotations

import hashlib
import lzma
import sys
from pathlib import Path

EXPECTED_GIT_BLOBS = {
    "Polymorph-Regular.ttf.xz": "a903a35d54509ea4fa60e3920637da1014187fb4",
    "Polymorph-Bold.ttf.xz": "0b9367c7246b6dfd0761d513241cd9fafc962b4f",
    "Cinzel-wght.ttf": "d218a0b9c8879fd5a708872cc0ef357e507b35ca",
    "Inter-opsz-wght.ttf": "047c92f6e2212473dc436020afed689527076d44",
}

EXPECTED_DECOMPRESSED_SHA256 = {
    "Polymorph-Regular.ttf.xz": "e3d1bf414bdd0b517989e89ea3350acafdd90b61322c6c6ec8c7390a9f6ea188",
    "Polymorph-Bold.ttf.xz": "aea401e914959cd4638cec82c0a7328a5d84b8d79d942c850052b10a18cca511",
}


def git_blob_sha1(path: Path) -> str:
    data = path.read_bytes()
    header = f"blob {len(data)}\0".encode("ascii")
    return hashlib.sha1(header + data).hexdigest()


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: verify_font_assets.py <font-dir>", file=sys.stderr)
        return 2

    font_dir = Path(sys.argv[1])
    for name, expected in EXPECTED_GIT_BLOBS.items():
        path = font_dir / name
        if not path.is_file():
            raise SystemExit(f"missing font asset: {path}")
        actual = git_blob_sha1(path)
        if actual != expected:
            raise SystemExit(
                f"font asset mismatch for {name}: expected {expected}, got {actual}"
            )
        print(f"verified {name} git-blob-sha1 {actual}")

    for name, expected in EXPECTED_DECOMPRESSED_SHA256.items():
        path = font_dir / name
        try:
            font_data = lzma.decompress(path.read_bytes())
        except lzma.LZMAError as exc:
            raise SystemExit(f"invalid compressed font asset {path}: {exc}") from exc
        actual = hashlib.sha256(font_data).hexdigest()
        if actual != expected:
            raise SystemExit(
                f"decompressed font mismatch for {name}: expected {expected}, got {actual}"
            )
        print(f"verified {name} decompressed-sha256 {actual}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
