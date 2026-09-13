from __future__ import annotations

import os
import sys
from pathlib import Path


def _bootstrap_log(message: str) -> None:
    """Write startup checkpoints only when the packaged CI smoke log is configured."""
    target = os.environ.get("POLYMORPH_SMOKE_LOG")
    if not target:
        return
    try:
        path = Path(target)
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("a", encoding="utf-8") as handle:
            handle.write(f"BOOT {message}\n")
            handle.flush()
    except Exception:
        # Diagnostic logging must never prevent the real application from starting.
        pass


_bootstrap_log(f"entry argv={sys.argv!r}")
_bootstrap_log("importing polymorph.app")
try:
    from polymorph.app import main
except BaseException as exc:
    _bootstrap_log(f"polymorph.app import failed: {type(exc).__name__}: {exc}")
    raise
_bootstrap_log("imported polymorph.app")

if __name__ == "__main__":
    _bootstrap_log("calling polymorph.app.main")
    raise SystemExit(main())
