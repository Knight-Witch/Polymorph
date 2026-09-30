from __future__ import annotations

from PySide6.QtCore import QObject
from PySide6.QtWidgets import QSpinBox

from ..geometry import linked_dimensions


class ResolutionLinker(QObject):
    """Keep novice-facing width/height controls proportional without extra UI."""

    def __init__(self, width_spin: QSpinBox, height_spin: QSpinBox, parent=None) -> None:
        super().__init__(parent)
        self.width_spin = width_spin
        self.height_spin = height_spin
        self._native_width = max(2, width_spin.value())
        self._native_height = max(2, height_spin.value())
        self._syncing = False
        width_spin.valueChanged.connect(self._width_changed)
        height_spin.valueChanged.connect(self._height_changed)

    def set_native(self, width: int, height: int) -> None:
        self._native_width = max(2, width)
        self._native_height = max(2, height)
        self._apply(self.width_spin.value(), "width", update_limits=True)

    def _width_changed(self, value: int) -> None:
        if not self._syncing:
            self._apply(value, "width")

    def _height_changed(self, value: int) -> None:
        if not self._syncing:
            self._apply(value, "height")

    def _apply(self, value: int, driver: str, update_limits: bool = False) -> None:
        width, height = linked_dimensions(self._native_width, self._native_height, value, driver)
        self._syncing = True
        try:
            if update_limits:
                self.width_spin.setMaximum(self._native_width)
                self.height_spin.setMaximum(self._native_height)
            self.width_spin.setValue(width)
            self.height_spin.setValue(height)
        finally:
            self._syncing = False
