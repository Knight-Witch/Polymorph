from __future__ import annotations

import copy
from pathlib import Path

from PySide6.QtWidgets import QButtonGroup, QLabel, QPushButton, QRadioButton, QVBoxLayout

from ..converter import ConversionCancelled
from ..diagnostic_adaptive_converter import DiagnosticAdaptiveConverter
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
                diagnostic_path = getattr(self.converter, "last_diagnostic_path", None)
                if diagnostic_path:
                    summary += f" • diagnostic {Path(diagnostic_path).name}"
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
            self.converter = DiagnosticAdaptiveConverter(find_toolchain())
        self._install_gif_priority_controls()
        self._apply_layout_polish()
        self._install_hover_tooltips()
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

    def _apply_layout_polish(self) -> None:
        # The adaptive GIF-priority controls add a full section to the right rail.
        # The old 720px default was tall enough before that section existed but now
        # compresses line edits/radios on first launch. Give the normal layout the
        # vertical room it actually needs while retaining a smaller resizable floor.
        self.resize(1080, 800)
        self.setMinimumSize(900, 700)
        controls_layout = self.convert_btn.parentWidget().layout()
        controls_layout.setSpacing(10)

    def _install_hover_tooltips(self) -> None:
        tooltips = (
            (
                self.file_list,
                "Conversion queue. Select a file to preview it; files are processed one at a time.",
            ),
            (
                self.preview,
                "Live source preview. In Crop or Fit modes, drag the image to reposition it.",
            ),
            (
                self.gif_radio,
                "Create an animated GIF with infinite looping.",
            ),
            (
                self.mp4_radio,
                "Create a high-quality H.264 MP4. Looping is controlled by the player or platform.",
            ),
            (
                self.size_radio,
                "Keep encoder quality fixed and adjust image dimensions to stay under the file-size limit.",
            ),
            (
                self.max_mb,
                "Maximum output size in decimal MB. 1 MB = 1,000,000 bytes.",
            ),
            (
                self.res_radio,
                "Use exact output dimensions. Polymorph will not upscale beyond the source.",
            ),
            (
                self.width_spin,
                "Output width in pixels. Height follows the active framed aspect ratio.",
            ),
            (
                self.height_spin,
                "Output height in pixels. Width follows the active framed aspect ratio.",
            ),
            (
                self.motion_preserve_radio,
                "Keep every source frame and the original frame rate. Best motion smoothness.",
            ),
            (
                self.motion_favor_radio,
                "Trade some original source frames for a larger GIF only when Polymorph measures a worthwhile resolution gain. No synthetic frames are created.",
            ),
            (
                self.frame_mode,
                "Original keeps the full source. Crop fills a ratio by trimming edges. Fit keeps all content and adds padding.",
            ),
            (
                self.ratio_combo,
                "Target aspect ratio used by Crop to ratio and Fit to ratio.",
            ),
            (
                self.center_btn,
                "Reset Crop or Fit positioning to the center.",
            ),
            (
                self.color_btn,
                "Choose the padding color used by Fit to ratio.",
            ),
            (
                self.output_path,
                "Converted files are saved in this folder.",
            ),
            (
                self.convert_btn,
                "Start converting the queued files with the selected settings.",
            ),
        )
        for widget, text in tooltips:
            widget.setToolTip(text)

        button_tooltips = {
            "Add Files": "Add one or more animated WebP files to the conversion queue.",
            "Remove Selected": "Remove the selected item from the queue. The source file is not deleted.",
            "Cancel": "Stop the current conversion.",
        }
        for button in self.findChildren(QPushButton):
            tooltip = button_tooltips.get(button.text())
            if tooltip:
                button.setToolTip(tooltip)

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
