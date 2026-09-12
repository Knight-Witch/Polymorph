from __future__ import annotations

import hashlib
import sys
from pathlib import Path

EXPECTED = {
    "Cinzel-wght.ttf": "d218a0b9c8879fd5a708872cc0ef357e507b35ca",
    "Inter-opsz-wght.ttf": "047c92f6e2212473dc436020afed689527076d44",
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
    for name, expected in EXPECTED.items():
        path = font_dir / name
        if not path.is_file():
            raise SystemExit(f"missing font asset: {path}")
        actual = git_blob_sha1(path)
        if actual != expected:
            raise SystemExit(
                f"font asset mismatch for {name}: expected {expected}, got {actual}"
            )
        print(f"verified {name} git-blob-sha1 {actual}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
