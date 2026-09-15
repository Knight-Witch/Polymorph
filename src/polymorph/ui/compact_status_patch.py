from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QLabel, QWidget

from . import visual_patch as _visual


_INSTALLED = False
_original_runtime_geometry = _visual._refine_runtime_geometry


def _compact_aware_runtime_geometry(window, scale: float) -> None:
    """Keep the enlarged Ready ring without stealing the minimum-size rail budget."""
    _original_runtime_geometry(window, scale)
    if scale > 0.76:
        return

    status = window.findChild(QWidget, "StatusCard")
    if status is None:
        return
    for label in status.findChildren(QLabel):
        if not bool(label.property("polymorphStatusRing")):
            continue
        ring_size = 24
        label.setFixedSize(ring_size, ring_size)
        label.setPixmap(_visual._status_ring_pixmap(ring_size))
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        break


def install_compact_status_patch() -> None:
    global _INSTALLED
    if _INSTALLED:
        return
    _INSTALLED = True
    _visual._refine_runtime_geometry = _compact_aware_runtime_geometry
