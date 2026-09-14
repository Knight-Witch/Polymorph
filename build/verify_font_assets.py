from __future__ import annotations

import hashlib
import lzma
import sys
from pathlib import Path

EXPECTED_GIT_BLOBS = {
    "Polymorph-Regular.ttf.xz": "e868cf74e450f2e3b69c2d3116d05f18d1499e15",
    "Polymorph-Bold.ttf.xz": "a794e9faebeb424e783ba1de4028a350e929113f",
    "Cinzel-wght.ttf": "d218a0b9c8879fd5a708872cc0ef357e507b35ca",
    "Inter-opsz-wght.ttf": "047c92f6e2212473dc436020afed689527076d44",
}

# The shipped Polymorph assets are display-only subsets generated from Amanda's
# supplied source TTFs. These hashes identify the decompressed subset bytes that
# Qt actually registers in the packaged application.
EXPECTED_DECOMPRESSED_SHA256 = {
    "Polymorph-Regular.ttf.xz": "5aeb68e5a95011f9a21c1c19d81514f04ad8ff23623f6e54ec20921d2ad2ef2c",
    "Polymorph-Bold.ttf.xz": "d437ef4599771311a175d3e7832c041eb76058e26a7e826dc1ea09547a111e3a",
}

# Original user-supplied source identities are recorded separately from the
# package subsets so provenance remains explicit without pretending the full
# source files are shipped in the public repository.
SOURCE_SHA256 = {
    "Polymorph Regular": "e3d1bf414bdd0b517989e89ea3350acafdd90b61322c6c6ec8c7390a9f6ea188",
    "Polymorph Bold": "aea401e914959cd4638cec82c0a7328a5d84b8d79d942c850052b10a18cca511",
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

    for logical_name, digest in SOURCE_SHA256.items():
        print(f"source provenance {logical_name} sha256 {digest}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
