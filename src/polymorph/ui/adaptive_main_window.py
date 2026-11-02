from __future__ import annotations

import copy
import traceback
from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QAbstractItemView,
    QButtonGroup,
    QCheckBox,
    QComboBox,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QRadioButton,
    QSpinBox,
    QWidget,
    QSlider,
    QVBoxLayout,
)

from ..adaptive_converter import AdaptiveConverter
from ..batch_queue import BatchJob, build_jobs, resolve_shared_resolution
from ..constants import APP_VERSION
from ..conversion_log import ConversionLog
from ..geometry import native_geometry
from ..converter import ConversionCancelled
from ..models import ConversionSettings, FramingMode, GifMotionMode, OutputFormat, SizingMode
from ..size_units import bytes_to_mb
from ..tools import find_toolchain
from .main_window import ConversionWorker, MainWindow as BaseMainWindow


class AdaptiveConversionWorker(ConversionWorker):
    """Run one immutable settings snapshot per file; report full failures."""

    def __init__(self, converter, jobs: list[BatchJob], parent=None):
        super().__init__(converter, [j.source for j in jobs], jobs[0].settings, parent)
        self.jobs = jobs
        self._job_index = 0

    def _progress(self, fraction: float, label: str) -> None:
        total = max(1, len(self.jobs))
        self.progressChanged.emit(
            (self._job_index + max(0.0, min(1.0, fraction))) / total,
            f"[{self._job_index + 1}/{total}] {label}",
        )

    def run(self) -> None:
        for self._job_index, job in enumerate(self.jobs):
            if self.isInterruptionRequested():
                break
            path = job.source
            self.fileStarted.emit(str(path))
            try:
                result = self.converter.convert(
                    path, copy.deepcopy(job.settings), self._progress
                )
                summary = (
                    f"{result.width}×{result.height} • "
                    f"{bytes_to_mb(result.size_bytes):.1f} MB"
                )
                if result.duration_s > 0 and result.frames > 0:
                    fps = result.frames / result.duration_s
                    summary += f" • {fps:.2f}".rstrip("0").rstrip(".") + " FPS"
                self.fileFinished.emit(str(path), summary, str(result.output))
            except ConversionCancelled:
                self.failed.emit(str(path), "Cancelled", "")
                break
            except Exception as exc:
                self.failed.emit(
                    str(path), str(exc) or type(exc).__name__, traceback.format_exc()
                )


class MainWindow(BaseMainWindow):
    """Production UI extension for adaptive GIF priority and Crop Zoom controls."""

    def __init__(self) -> None:
        super().__init__()
        if self.converter is not None:
            self.converter = AdaptiveConverter(find_toolchain())
        self._install_gif_priority_controls()
        self._install_crop_zoom_control()
        self._apply_layout_polish()
        self._install_hover_tooltips()
        self._install_batch_controls()
        self.frame_mode.currentIndexChanged.connect(self._sync_crop_zoom_state)
        self._sync_crop_zoom_state()
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

    def _install_crop_zoom_control(self) -> None:
        layout = self.convert_btn.parentWidget().layout()
        framing_index = -1
        for index in range(layout.count()):
            widget = layout.itemAt(index).widget()
            if isinstance(widget, QLabel) and widget.text() == "Framing":
                framing_index = index
                break
        if framing_index < 0:
            return

        self.crop_zoom_label = QLabel("Zoom 100%")
        self.crop_zoom_label.setObjectName("Muted")
        self.crop_zoom_slider = QSlider(Qt.Horizontal)
        self.crop_zoom_slider.setRange(100, 300)
        self.crop_zoom_slider.setSingleStep(5)
        self.crop_zoom_slider.setPageStep(25)
        self.crop_zoom_slider.setValue(100)
        self.crop_zoom_slider.valueChanged.connect(self._crop_zoom_changed)

        row = QHBoxLayout()
        row.setContentsMargins(0, 0, 0, 0)
        row.setSpacing(8)
        row.addWidget(self.crop_zoom_label)
        row.addWidget(self.crop_zoom_slider, 1)
        layout.insertLayout(framing_index + 3, row)

    def _framing_changed(self) -> None:
        """Normalize Qt item data back into a real FramingMode before use."""
        self.framing.mode = FramingMode(self.frame_mode.currentData())
        self.framing.ratio = (
            self.ratio_combo.currentData()
            if self.framing.mode != FramingMode.ORIGINAL
            else None
        )
        self.preview.set_framing(self.framing)
        self._sync_enabled_state()
        row = self.file_list.currentRow()
        if 0 <= row < len(self.files):
            self._update_probe_label(self.files[row])

    def _crop_zoom_changed(self, value: int) -> None:
        if not hasattr(self, "crop_zoom_label"):
            return
        self.crop_zoom_label.setText(f"Zoom {value}%")
        self.framing.zoom = max(1.0, value / 100.0)
        self.preview.set_framing(self.framing)
        row = self.file_list.currentRow()
        if 0 <= row < len(self.files):
            self._update_probe_label(self.files[row])

    def _sync_crop_zoom_state(self) -> None:
        if not hasattr(self, "crop_zoom_slider"):
            return
        busy = self.worker is not None and self.worker.isRunning()
        try:
            mode = FramingMode(self.frame_mode.currentData())
        except (TypeError, ValueError):
            mode = FramingMode.ORIGINAL
        crop = mode == FramingMode.CROP
        self.crop_zoom_slider.setEnabled(crop and not busy)
        self.crop_zoom_label.setEnabled(crop and not busy)

    def _apply_layout_polish(self) -> None:
        self.resize(1080, 820)
        self.setMinimumSize(900, 700)
        controls_layout = self.convert_btn.parentWidget().layout()
        controls_layout.setSpacing(9)

    def _install_hover_tooltips(self) -> None:
        tooltips = (
            (
                self.file_list,
                "Conversion queue. Select a file to preview it; files are processed one at a time.",
            ),
            (
                self.preview,
                "Live output framing preview. In Crop or Fit modes, drag the media to reposition it.",
            ),
            (
                self.gif_radio,
                "Create an animated GIF with infinite looping.",
            ),
            (
                self.mp4_radio,
                "Create a high-quality H.264 MP4. Looping is controlled by the player or platform.",
            ),
            (self.webp_radio, "Create static WebP from images, or animated WebP from GIF/video with source timing and alpha preservation."),
            (self.png_radio, "Create lossless PNG images at the selected pixel dimensions."),
            (self.native_radio, "Keep exactly the original image pixel dimensions."),
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
                "Original keeps the source unchanged. Crop trims to the chosen ratio without stretching. Fit expands the frame with padding while preserving the source aspect ratio.",
            ),
            (
                self.ratio_combo,
                "Target aspect ratio used by Crop to ratio and Fit to ratio.",
            ),
            (
                self.crop_zoom_slider,
                "Crop only: zoom into the source from 100% to 300%. Drag the preview to choose which area stays visible.",
            ),
            (
                self.center_btn,
                "Center the media within the current Crop or Fit frame.",
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
            "Add Files": "Add static images, GIFs, animated WebP, or MP4 media to the queue.",
            "Remove Selected": "Remove the selected item from the queue. The source file is not deleted.",
            "Cancel": "Stop the current conversion.",
        }
        for button in self.findChildren(QPushButton):
            tooltip = button_tooltips.get(button.text())
            if tooltip:
                button.setToolTip(tooltip)

    def _install_batch_controls(self) -> None:
        """Keep queue scope and shared/per-file switches outside the tight rail."""
        self._batch_restoring = False
        self._batch_active_path: Path | None = None
        self._batch_profiles: dict[Path, ConversionSettings] = {}
        self._batch_profile_axes: dict[Path, str] = {}
        self._batch_shared_settings = copy.deepcopy(self._make_settings())
        self._batch_last_shared = True
        self._batch_media_kind: bool | None = None
        self._batch_axis = "width"
        self.file_list.setSelectionMode(QAbstractItemView.SelectionMode.ExtendedSelection)

        self.batch_panel = QWidget()
        self.batch_panel.setObjectName("BatchQueueControls")
        row = QHBoxLayout(self.batch_panel)
        row.setContentsMargins(0, 0, 0, 0)
        row.setSpacing(7)
        self.batch_apply_all = QCheckBox("Apply settings to all")
        self.batch_apply_all.setObjectName("BatchApplyAll")
        self.batch_apply_all.setChecked(True)
        self.batch_apply_all.setToolTip(
            "Checked: shared output and framing. Unchecked: each file remembers its own settings."
        )
        row.addWidget(self.batch_apply_all)
        row.addStretch(1)
        self.batch_scope = QComboBox()
        self.batch_scope.setObjectName("BatchScope")
        self.batch_scope.addItems(("Queue: All", "Queue: Selected"))
        self.batch_scope.setToolTip("All queued files or only the selected rows (Ctrl/Shift-click).")
        row.addWidget(self.batch_scope)

        self.batch_dimension_panel = QWidget()
        self.batch_dimension_panel.setObjectName("BatchDimensionControls")
        dimension_row = QHBoxLayout(self.batch_dimension_panel)
        dimension_row.setContentsMargins(0, 0, 0, 0)
        dimension_row.setSpacing(5)
        self.batch_dimension_axis = QComboBox()
        self.batch_dimension_axis.setObjectName("BatchDimensionAxis")
        self.batch_dimension_axis.addItem("Match width", "width")
        self.batch_dimension_axis.addItem("Match height", "height")
        self.batch_dimension_axis.setToolTip(
            "Match only this dimension; the other is calculated per source. Never upscale."
        )
        dimension_row.addWidget(self.batch_dimension_axis)
        self.batch_dimension_pixels = QSpinBox()
        self.batch_dimension_pixels.setObjectName("BatchDimensionPixels")
        self.batch_dimension_pixels.setRange(2, 32768)
        self.batch_dimension_pixels.setKeyboardTracking(False)
        self.batch_dimension_pixels.setValue(1200)
        self.batch_dimension_pixels.setSuffix(" px")
        dimension_row.addWidget(self.batch_dimension_pixels)
        dimension_row.addStretch(1)

        parent_layout = self.file_list.parentWidget().layout()
        idx = parent_layout.indexOf(self.file_list)
        parent_layout.insertWidget(idx + 1, self.batch_panel)
        parent_layout.insertWidget(idx + 2, self.batch_dimension_panel)
        self.batch_apply_all.toggled.connect(self._toggle_batch_mode)
        self.batch_dimension_axis.currentIndexChanged.connect(self._batch_dimension_changed)
        self.batch_dimension_pixels.valueChanged.connect(self._batch_dimension_changed)
        self.size_radio.toggled.connect(self._sync_batch_controls)
        self.res_radio.toggled.connect(self._sync_batch_controls)
        self.width_spin.valueChanged.connect(lambda _v: self._note_resolution_axis("width"))
        self.height_spin.valueChanged.connect(lambda _v: self._note_resolution_axis("height"))
        self._sync_batch_controls()

    def _note_resolution_axis(self, axis: str) -> None:
        if self._batch_restoring or self.resolution_linker._syncing:
            return
        if self._batch_active_path is not None:
            self._batch_profile_axes[self._batch_active_path] = axis
        # A direct edit in shared mode also selects the common axis/amount,
        # so the main sizing fields remain fully functional.
        if self.batch_apply_all.isChecked() and self.res_radio.isChecked():
            self._batch_axis = axis
            widget = self.width_spin if axis == "width" else self.height_spin
            self.batch_dimension_axis.blockSignals(True)
            self.batch_dimension_pixels.blockSignals(True)
            try:
                self.batch_dimension_axis.setCurrentIndex(0 if axis == "width" else 1)
                self.batch_dimension_pixels.setValue(widget.value())
            finally:
                self.batch_dimension_axis.blockSignals(False)
                self.batch_dimension_pixels.blockSignals(False)

    def _capture_batch_editor(self, shared: bool | None = None) -> None:
        if self._batch_restoring or self._batch_active_path is None:
            return
        settings = copy.deepcopy(self._make_settings())
        if shared if shared is not None else self.batch_apply_all.isChecked():
            self._batch_shared_settings = settings
        else:
            self._batch_profiles[self._batch_active_path] = settings

    def _profile_for(self, path: Path) -> ConversionSettings:
        if not self.converter:
            return copy.deepcopy(self._batch_shared_settings)
        info = self.media_cache.get(path) or self.converter.probe(path)
        self.media_cache[path] = info
        return resolve_shared_resolution(
            self._batch_shared_settings, info, self._batch_axis,
            self.batch_dimension_pixels.value()
        )

    def _load_batch_editor(self, path: Path) -> None:
        if not self.converter:
            return
        self._batch_restoring = True
        try:
            if self.batch_apply_all.isChecked():
                settings = self._profile_for(path)
                axis = self._batch_axis
            else:
                if path not in self._batch_profiles:
                    self._batch_profiles[path] = self._profile_for(path)
                settings = copy.deepcopy(self._batch_profiles[path])
                axis = self._batch_profile_axes.get(path, "width")
            choices = {
                OutputFormat.GIF: self.gif_radio,
                OutputFormat.MP4: self.mp4_radio,
                OutputFormat.WEBP: self.webp_radio,
                OutputFormat.PNG: self.png_radio,
            }
            choices[settings.output_format].setChecked(True)
            modes = {
                SizingMode.FILE_SIZE: self.size_radio,
                SizingMode.RESOLUTION: self.res_radio,
                SizingMode.NATIVE: self.native_radio,
            }
            modes[settings.sizing_mode].setChecked(True)
            self.max_mb.setValue(settings.max_mb)
            self.webp_lossless.setChecked(settings.webp_lossless)
            self.motion_favor_radio.setChecked(
                settings.gif_motion_mode is GifMotionMode.FAVOR_RESOLUTION
            )
            self.motion_preserve_radio.setChecked(
                settings.gif_motion_mode is GifMotionMode.PRESERVE
            )
            self.framing = copy.deepcopy(settings.framing)
            for i in range(self.frame_mode.count()):
                if self.frame_mode.itemData(i) == self.framing.mode:
                    self.frame_mode.setCurrentIndex(i)
                    break
            if self.framing.ratio is not None:
                for i in range(self.ratio_combo.count()):
                    if self.ratio_combo.itemData(i) == self.framing.ratio:
                        self.ratio_combo.setCurrentIndex(i)
                        break
            self.crop_zoom_slider.setValue(round(self.framing.zoom * 100))
            self.preview.set_framing(self.framing)
            self._update_probe_label(path)
            if settings.sizing_mode is SizingMode.RESOLUTION:
                value = settings.requested_width if axis == "width" else settings.requested_height
                if value is not None:
                    (self.width_spin if axis == "width" else self.height_spin).setValue(value)
        finally:
            self._batch_restoring = False
        self._sync_enabled_state()

    def _selection_changed(self, row: int) -> None:
        if hasattr(self, "_batch_profiles"):
            self._capture_batch_editor()
        if row < 0 or row >= len(self.files):
            if hasattr(self, "_batch_active_path"):
                self._batch_active_path = None
            return
        # Native-resolution updates caused by changing files must not
        # overwrite the requested shared axis/target with intermediate values.
        if hasattr(self, "_batch_restoring"):
            self._batch_restoring = True
        try:
            super()._selection_changed(row)
        finally:
            if hasattr(self, "_batch_restoring"):
                self._batch_restoring = False
        if hasattr(self, "_batch_profiles"):
            # Static files and videos have different safe initial defaults.
            # Preserve old per-file profiles, but reset the shared template when
            # the queue changes media class after being cleared.
            if self._batch_media_kind is None or self._batch_media_kind != self._still_mode:
                self._batch_shared_settings = copy.deepcopy(self._make_settings())
                self._batch_media_kind = self._still_mode
            self._batch_active_path = self.files[row]
            self._load_batch_editor(self._batch_active_path)

    def _toggle_batch_mode(self, enabled: bool) -> None:
        self._capture_batch_editor(shared=self._batch_last_shared)
        if not enabled:
            for path in self.files:
                self._batch_profiles.setdefault(path, self._profile_for(path))
        else:
            if self._batch_active_path is not None:
                self._batch_shared_settings = copy.deepcopy(
                    self._batch_profiles.get(self._batch_active_path, self._batch_shared_settings)
                )
                self._batch_axis = self._batch_profile_axes.get(self._batch_active_path, "width")
                target = (self._batch_shared_settings.requested_width
                          if self._batch_axis == "width"
                          else self._batch_shared_settings.requested_height)
                if target is not None:
                    self.batch_dimension_axis.blockSignals(True)
                    self.batch_dimension_pixels.blockSignals(True)
                    try:
                        self.batch_dimension_axis.setCurrentIndex(0 if self._batch_axis == "width" else 1)
                        self.batch_dimension_pixels.setValue(target)
                    finally:
                        self.batch_dimension_axis.blockSignals(False)
                        self.batch_dimension_pixels.blockSignals(False)
        self._batch_last_shared = enabled
        if self._batch_active_path is not None:
            self._load_batch_editor(self._batch_active_path)
        self._sync_batch_controls()

    def _batch_dimension_changed(self, *_args) -> None:
        if self._batch_restoring:
            return
        self._capture_batch_editor(shared=True)
        self._batch_axis = self.batch_dimension_axis.currentData()
        if (self.batch_apply_all.isChecked() and self.res_radio.isChecked()
                and self._batch_active_path is not None):
            self._load_batch_editor(self._batch_active_path)

    def _sync_batch_controls(self, *_args) -> None:
        if not hasattr(self, "batch_dimension_panel"):
            return
        busy = self.worker is not None and self.worker.isRunning()
        show = self.batch_apply_all.isChecked() and self.res_radio.isChecked()
        self.batch_dimension_panel.setVisible(show)
        for widget in (self.batch_panel, self.batch_dimension_axis, self.batch_dimension_pixels):
            widget.setEnabled(not busy)

    def _remove_selected(self) -> None:
        if self.worker is not None and self.worker.isRunning():
            return
        self._capture_batch_editor()
        rows = sorted({self.file_list.row(item) for item in self.file_list.selectedItems()}, reverse=True)
        if not rows and self.file_list.currentRow() >= 0:
            rows = [self.file_list.currentRow()]
        self._batch_restoring = True
        try:
            for row in rows:
                if 0 <= row < len(self.files):
                    path = self.files.pop(row)
                    self.file_list.takeItem(row)
                    self._batch_profiles.pop(path, None)
                    self._batch_profile_axes.pop(path, None)
                    self.media_cache.pop(path, None)
        finally:
            self._batch_restoring = False
        self._batch_active_path = None
        if not self.files:
            self.preview.set_source(None)
            self.dimensions_label.setText("No file selected")
            self._set_media_mode(None)
        elif self.file_list.currentRow() < 0:
            self.file_list.setCurrentRow(0)
        else:
            self._selection_changed(self.file_list.currentRow())
        self._sync_enabled_state()

    def _clear_queue(self) -> None:
        if self.worker is not None and self.worker.isRunning():
            return
        self.file_list.clear()
        self.files.clear()
        self.media_cache.clear()
        self._batch_profiles.clear()
        self._batch_profile_axes.clear()
        self._batch_active_path = None
        self._set_media_mode(None)
        self.preview.set_source(None)
        self.dimensions_label.setText("No file selected")
        self._sync_enabled_state()

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
        if hasattr(self, "_brand_priority_card") and self._still_mode is False:
            self._brand_priority_card.setVisible(self.gif_radio.isChecked())
        self._sync_crop_zoom_state()
        self._sync_batch_controls()

    def _make_settings(self):
        settings = super()._make_settings()
        settings.framing.mode = FramingMode(settings.framing.mode)
        settings.gif_motion_mode = (
            GifMotionMode.FAVOR_RESOLUTION
            if self.motion_favor_radio.isChecked()
            else GifMotionMode.PRESERVE
        )
        return settings

    def _start_conversion(self) -> None:
        if not self.converter or not self.files:
            return
        self._capture_batch_editor()
        selected = {self.file_list.row(item) for item in self.file_list.selectedItems()}
        if self.batch_scope.currentIndex() == 1:
            paths = [path for i, path in enumerate(self.files) if i in selected]
            if not paths:
                self.status_label.setText("Select one or more queued files to convert.")
                return
        else:
            paths = list(self.files)
        try:
            jobs = build_jobs(
                paths, self._batch_profiles, self._batch_shared_settings,
                self.batch_apply_all.isChecked(), self._batch_axis,
                self.batch_dimension_pixels.value(), self.converter.probe,
            )
            # Output directory is intentionally a shared queue destination.
            # Preserve per-file framing, mode and bitrate targets.
            for job in jobs:
                job.settings.output_dir = Path(self.output_path.text())
        except Exception as exc:
            self.status_label.setText(f"Queue configuration failed: {exc}")
            return
        self._saved_files = 0
        self._failed_files = 0
        self._batch_failures = []
        self._conversion_log = ConversionLog(paths, jobs[0].settings, APP_VERSION)
        for job in jobs:
            self._conversion_log.planned(str(job.source), job.settings)
        self.worker = AdaptiveConversionWorker(self.converter, jobs, self)
        self.worker.progressChanged.connect(self._progress_changed)
        self.worker.fileStarted.connect(self._file_started)
        self.worker.fileFinished.connect(self._file_finished)
        self.worker.failed.connect(self._file_failed)
        self.worker.finished.connect(self._conversion_finished)
        self.progress.setValue(0)
        self.arcane_progress.set_progress(0)
        self.arcane_progress.setVisible(True)
        self.arcane_progress.set_active(True)
        if hasattr(self, "status_ring"):
            self.status_ring.set_active(True)
        self.cancel_btn.setVisible(True)
        self.status_label.setText(f"Queue started: {len(jobs)} file(s).")
        self.worker.start()
        self._sync_enabled_state()

    def _conversion_finished(self) -> None:
        total = len(self.worker.jobs) if isinstance(self.worker, AdaptiveConversionWorker) else 0
        super()._conversion_finished()
        if total > 1 and not self._failed_files:
            self.status_label.setText(f"Queue complete: {self._saved_files}/{total} saved.")
            if hasattr(self, "_brand_status_detail"):
                self._brand_status_detail.setText(f"Output folder: {self.output_path.text()}")
