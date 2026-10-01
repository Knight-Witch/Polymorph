from __future__ import annotations

from pathlib import Path
from typing import Callable

from PySide6.QtWidgets import QFileDialog, QPushButton


_INSTALLED = False
_ORIGINAL_QUEUE_THUMBNAIL: Callable | None = None
_ORIGINAL_REBUILD: Callable | None = None


def _choose_media_files(self) -> None:
    paths, _ = QFileDialog.getOpenFileNames(
        self,
        "Add media files",
        str(Path.home()),
        "Supported media (*.webp *.mp4);;Animated WebP (*.webp);;MP4 video (*.mp4)",
    )
    self._add_files([Path(path) for path in paths])


def _load_media_thumbnail(self) -> None:
    if _ORIGINAL_QUEUE_THUMBNAIL is None:
        raise RuntimeError("MP4 input support was used before installation")
    _ORIGINAL_QUEUE_THUMBNAIL(self)
    if self.path.suffix.lower() != ".mp4":
        return
    pixmap = self.thumb.pixmap()
    if pixmap is None or pixmap.isNull():
        self.thumb.setText("MP4")


def _rebuild_with_media_labels(window) -> None:
    if _ORIGINAL_REBUILD is None:
        raise RuntimeError("MP4 input support was used before installation")
    _ORIGINAL_REBUILD(window)
    for button in window.findChildren(QPushButton):
        if button.text() == "+ Add Files":
            button.setToolTip("Add one or more animated WebP or MP4 files to the conversion queue.")


def install_media_input_support() -> None:
    """Patch MP4 admission only after the accepted visual classes are installed."""
    global _INSTALLED, _ORIGINAL_QUEUE_THUMBNAIL, _ORIGINAL_REBUILD
    if _INSTALLED:
        return

    # These imports are intentionally lazy. Importing this module must never
    # preload branded_layout before app.py has installed the accepted visual
    # class patches; doing so caused a prior stale-UI package regression.
    from . import branded_layout as branded
    from .adaptive_main_window import MainWindow

    _ORIGINAL_QUEUE_THUMBNAIL = branded.QueueRow._load_thumbnail
    _ORIGINAL_REBUILD = branded.rebuild_brand_layout

    MainWindow._choose_files = _choose_media_files
    branded.QueueRow._load_thumbnail = _load_media_thumbnail
    branded.rebuild_brand_layout = _rebuild_with_media_labels
    _INSTALLED = True
