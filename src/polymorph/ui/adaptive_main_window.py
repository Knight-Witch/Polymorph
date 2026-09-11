from __future__ import annotations

from PySide6.QtWidgets import QButtonGroup, QLabel, QRadioButton, QVBoxLayout

from ..adaptive_converter import AdaptiveConverter
from ..models import GifMotionMode
from ..tools import find_toolchain
from .main_window import MainWindow as BaseMainWindow


class MainWindow(BaseMainWindow):
    """Development UI extension for adaptive GIF motion/resolution balancing."""

    def __init__(self) -> None:
        super().__init__()
        if self.converter is not None:
            self.converter = AdaptiveConverter(find_toolchain())
        self._install_gif_priority_controls()
        self._sync_enabled_state()

    def _install_gif_priority_controls(self) -> None:
        layout = self.convert_btn.parentWidget().layout()
        insert_at = layout.indexOf(self.convert_btn)
        for index in range(layout.count()):
            widget = layout.itemAt(index).widget()
            if isinstance(widget, QLabel) and widget.text() == "Framing":
                insert_at = index
                break

        section = self._section("GIF priority")
        self.motion_preserve_radio = QRadioButton("Preserve motion")
        self.motion_favor_radio = QRadioButton("Favor resolution")
        self.motion_preserve_radio.setChecked(True)
        self.motion_preserve_radio.setToolTip(
            "Keep the source frame rate and every source frame."
        )
        self.motion_favor_radio.setToolTip(
            "When worthwhile, evenly resample motion to a uniform lower GIF frame rate "
            "so more of the file-size budget can be spent on spatial resolution."
        )
        self.motion_group = QButtonGroup(self)
        self.motion_group.addButton(self.motion_preserve_radio)
        self.motion_group.addButton(self.motion_favor_radio)

        motion_box = QVBoxLayout()
        motion_box.setContentsMargins(22, 0, 0, 0)
        motion_box.setSpacing(4)
        motion_box.addWidget(self.motion_preserve_radio)
        motion_box.addWidget(self.motion_favor_radio)

        layout.insertWidget(insert_at, section)
        layout.insertLayout(insert_at + 1, motion_box)

        self.gif_radio.toggled.connect(self._sync_enabled_state)
        self.mp4_radio.toggled.connect(self._sync_enabled_state)
        self.res_radio.toggled.connect(self._sync_enabled_state)

    def _sync_enabled_state(self) -> None:
        super()._sync_enabled_state()
        if not hasattr(self, "motion_preserve_radio"):
            return
        busy = self.worker is not None and self.worker.isRunning()
        enabled = (
            self.gif_radio.isChecked()
            and self.size_radio.isChecked()
            and not busy
        )
        self.motion_preserve_radio.setEnabled(enabled)
        self.motion_favor_radio.setEnabled(enabled)

    def _make_settings(self):
        settings = super()._make_settings()
        settings.gif_motion_mode = (
            GifMotionMode.FAVOR_RESOLUTION
            if self.motion_favor_radio.isChecked()
            else GifMotionMode.PRESERVE
        )
        return settings
