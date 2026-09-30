from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QLabel, QWidget

from . import visual_patch as _visual


_INSTALLED = False
_original_runtime_geometry = _visual._refine_runtime_geometry
_original_button_apply_scale = _visual.RefinedPolymorphButton.apply_scale


def _compact_button_apply_scale(self, scale: float) -> None:
    """Apply the compact action height on the synchronous responsive code path."""
    _original_button_apply_scale(self, scale)
    if scale <= 0.76:
        self.setFixedHeight(max(42, round(55 * scale)))


def _compact_aware_runtime_geometry(window, scale: float) -> None:
    """Preserve the richer normal-size treatment while protecting the 920x640 footer footprint."""
    _original_runtime_geometry(window, scale)
    if scale > 0.76:
        return

    # Keep the enlarged Ready ring at normal sizes but return it to the proven
    # compact footprint at the minimum responsive breakpoint.
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
    _visual.RefinedPolymorphButton.apply_scale = _compact_button_apply_scale
    _visual._refine_runtime_geometry = _compact_aware_runtime_geometry
