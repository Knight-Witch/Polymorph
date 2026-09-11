from __future__ import annotations

import copy
from pathlib import Path

from PySide6.QtWidgets import QButtonGroup, QLabel, QRadioButton, QVBoxLayout

from ..adaptive_converter import AdaptiveConverter
from ..converter import ConversionCancelled
from ..models import GifMotionMode
from ..size_units import bytes_to_mb
from ..tools import find_toolchain
from .main_window import ConversionWorker, MainWindow as BaseMainWindow


class AdaptiveConversionWorker(ConversionWorker):
    """Dev worker that reports decimal MB and the actual resulting frame rate."""

    def run(self) -> None:
        for path in self.files:
            if self.isInterruptionRequested():
                break
            self.fileStarted.emit(str(path))
            try:
                result = self.converter.convert(
                    path,
                    copy.deepcopy(self.settings),
                    self._progress,
                )
                summary = (
                    f"{result.width}×{result.height} • "
                    f"{bytes_to_mb(result.size_bytes):.1f} MB"
                )
                if result.duration_s > 0 and result.frames > 0:
                    fps = result.frames / result.duration_s
                    fps_text = f"{fps:.2f}".rstrip("0").rstrip(".")
                    summary += f" • {fps_text} FPS"
                self.fileFinished.emit(str(path), summary)
            except ConversionCancelled:
                self.failed.emit(str(path), "Cancelled")
                break
            except Exception as exc:
                self.failed.emit(str(path), str(exc))


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
            "Measure clean, evenly resampled GIF frame rates and only sacrifice motion "
            "when the real encoded result can buy a meaningfully larger image."
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

    def _start_conversion(self) -> None:
        if not self.converter or not self.files:
            return
        self.worker = AdaptiveConversionWorker(
            self.converter,
            list(self.files),
            self._make_settings(),
            self,
        )
        self.worker.progressChanged.connect(self._progress_changed)
        self.worker.fileStarted.connect(
            lambda p: self.status_label.setText(f"Polymorphing {Path(p).name}…")
        )
        self.worker.fileFinished.connect(self._file_finished)
        self.worker.failed.connect(self._file_failed)
        self.worker.finished.connect(self._conversion_finished)
        self.progress.setValue(0)
        self.arcane_progress.set_progress(0)
        self.arcane_progress.setVisible(True)
        self.arcane_progress.set_active(True)
        self.cancel_btn.setVisible(True)
        self.worker.start()
        self._sync_enabled_state()
