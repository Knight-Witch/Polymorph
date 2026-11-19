from __future__ import annotations

import copy
import threading
import traceback
from pathlib import Path

from PySide6.QtCore import QSettings, QSize, QThread, QTimer, Qt, QUrl, Signal, Slot
from PySide6.QtGui import QColor, QDesktopServices, QDragEnterEvent, QDropEvent, QIcon
from PySide6.QtWidgets import (
    QApplication,
    QButtonGroup,
    QCheckBox,
    QColorDialog,
    QComboBox,
    QDoubleSpinBox,
    QFileDialog,
    QFrame,
    QHBoxLayout,
    QLabel,
    QListWidget,
    QListWidgetItem,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QProgressBar,
    QRadioButton,
    QSpinBox,
    QSplitter,
    QToolButton,
    QVBoxLayout,
    QWidget,
)

from ..constants import (
    APP_NAME,
    APP_ORG,
    APP_VERSION,
    DEFAULT_MAX_MB,
    DISCORD_URL,
    KOFI_URL,
    PATREON_URL,
    RATIO_PRESETS,
    REPO_URL,
    SUPPORTED_INPUT_EXTENSIONS,
    default_output_dir,
)
from ..converter import ConversionCancelled, Converter
from ..conversion_log import ConversionLog, latest_log
from ..geometry import native_geometry
from ..models import ConversionSettings, FramingMode, FramingSettings, OutputFormat, SizingMode
from ..resources import asset_path
from ..static_image import is_still_image
from ..tools import find_toolchain
from ..update_service import download_and_verify_installer, download_and_stage_public_delta, fetch_latest_for_channel, is_newer, launch_installer
from ..delta_update import launch_staged_update
from .whats_new import show_whats_new_once
from .dialogs import AspectGuideDialog
from .conversion_log_dialog import ConversionLogDialog
from .preview import AnimatedPreview
from .progress_ring import ArcaneProgress
from .resolution_linker import ResolutionLinker
from .styles import BASE_STYLESHEET


class ConversionWorker(QThread):
    progressChanged = Signal(float, str)
    fileStarted = Signal(str)
    fileFinished = Signal(str, str, str)
    failed = Signal(str, str, str)

    def __init__(self, converter: Converter, files: list[Path], settings: ConversionSettings, parent=None) -> None:
        super().__init__(parent)
        self.converter = converter
        self.files = files
        self.settings = settings

    def run(self) -> None:
        for path in self.files:
            if self.isInterruptionRequested():
                break
            self.fileStarted.emit(str(path))
            try:
                result = self.converter.convert(path, copy.deepcopy(self.settings), self._progress)
                summary = f"{result.width}×{result.height} • {result.size_bytes / (1024*1024):.1f} MB"
                self.fileFinished.emit(str(path), summary, str(result.output))
            except ConversionCancelled:
                self.failed.emit(str(path), "Cancelled", "")
                break
            except Exception as exc:
                self.failed.emit(str(path), str(exc) or type(exc).__name__, traceback.format_exc())

    def _progress(self, fraction: float, label: str) -> None:
        self.progressChanged.emit(fraction, label)

    def stop(self) -> None:
        self.requestInterruption()
        self.converter.cancel()


class MainWindow(QMainWindow):
    updateCheckCompleted = Signal(object, bool)
    updateDownloadCompleted = Signal(object, object)

    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle(f"{APP_NAME} {APP_VERSION}")
        self.resize(1080, 720)
        self.setMinimumSize(900, 620)
        self.setAcceptDrops(True)
        self.settings_store = QSettings(APP_ORG, APP_NAME)
        self.files: list[Path] = []
        self.media_cache = {}
        self._still_mode: bool | None = None
        self._animated_ratio = "16:9"
        self.framing = FramingSettings()
        self.worker: ConversionWorker | None = None
        self._saved_files = 0
        self._failed_files = 0
        self._batch_failures: list[tuple[str, str]] = []
        self._conversion_log: ConversionLog | None = None
        self._conversion_log_dialog: ConversionLogDialog | None = None
        self.converter: Converter | None = None

        try:
            self.converter = Converter(find_toolchain())
        except FileNotFoundError:
            self.converter = None

        self.setStyleSheet(BASE_STYLESHEET)
        self._build_ui()
        self.updateCheckCompleted.connect(self._handle_release)
        self.updateDownloadCompleted.connect(self._handle_downloaded_update)
        self._sync_enabled_state()
        QTimer.singleShot(1600, self._auto_check_updates)

    def _build_ui(self) -> None:
        root = QWidget()
        outer = QVBoxLayout(root)
        outer.setContentsMargins(18, 18, 18, 10)
        outer.setSpacing(12)

        header = QHBoxLayout()
        title_box = QVBoxLayout()
        title = QLabel("POLYMORPH")
        title.setObjectName("Title")
        subtitle = QLabel("Media Transmutation Utility")
        subtitle.setObjectName("Muted")
        title_box.addWidget(title)
        title_box.addWidget(subtitle)
        header.addLayout(title_box)
        header.addStretch(1)
        add_button = QPushButton("Add Files")
        add_button.clicked.connect(self._choose_files)
        header.addWidget(add_button)
        outer.addLayout(header)

        splitter = QSplitter(Qt.Horizontal)
        splitter.setChildrenCollapsible(False)

        left = self._card()
        left_layout = QVBoxLayout(left)
        left_layout.setContentsMargins(12, 12, 12, 12)
        left_layout.addWidget(QLabel("Files"))
        self.file_list = QListWidget()
        self.file_list.currentRowChanged.connect(self._selection_changed)
        left_layout.addWidget(self.file_list, 1)
        remove_btn = QPushButton("Remove Selected")
        remove_btn.clicked.connect(self._remove_selected)
        left_layout.addWidget(remove_btn)
        splitter.addWidget(left)

        preview_card = self._card()
        preview_layout = QVBoxLayout(preview_card)
        preview_layout.setContentsMargins(10, 10, 10, 10)
        self.preview = AnimatedPreview()
        self.preview.framingChanged.connect(self._preview_offset_changed)
        preview_layout.addWidget(self.preview, 1)
        self.dimensions_label = QLabel("No file selected")
        self.dimensions_label.setAlignment(Qt.AlignCenter)
        self.dimensions_label.setObjectName("Muted")
        preview_layout.addWidget(self.dimensions_label)
        splitter.addWidget(preview_card)

        controls = self._card()
        controls_layout = QVBoxLayout(controls)
        controls_layout.setContentsMargins(14, 14, 14, 14)
        controls_layout.setSpacing(12)
        controls_layout.addWidget(self._section("Output"))
        format_row = QHBoxLayout()
        self.gif_radio = QRadioButton("GIF")
        self.mp4_radio = QRadioButton("MP4")
        self.webp_radio = QRadioButton("WebP")
        self.png_radio = QRadioButton("PNG")
        self.webp_lossless = QCheckBox("Lossless WebP")
        self.webp_lossless.setToolTip("Preserve exact pixels (potentially very large files).")
        self.webp_quality = QComboBox()
        self.webp_quality.setObjectName("AnimatedWebpQuality")
        for title, quality in (
            ("65 Compact", 65), ("75 Balanced", 75),
            ("85 High", 85), ("95 Maximum", 95),
        ):
            self.webp_quality.addItem(title, quality)
        self.webp_quality.setCurrentIndex(self.webp_quality.findData(75))
        self.webp_quality.setToolTip(
            "Animated WebP only. Higher quality substantially increases file size. "
            "When Limit MB is enabled, quality may decrease to meet the limit."
        )
        self.webp_limit_mb = QCheckBox("Limit MB")
        self.webp_limit_mb.setChecked(True)
        self.webp_limit_mb.setObjectName("AnimatedWebpLimit")
        self.webp_limit_mb.setToolTip(
            "Also enforce the MB value in Sizing when using Set resolution. "
            "Keep the exact resolution and full frame timing; reduce WebP quality "
            "if required. If the limit cannot be met, report an error instead "
            "of silently making an oversized file."
        )
        self.webp_lossless.toggled.connect(self._sync_enabled_state)
        self.webp_limit_mb.toggled.connect(self._sync_enabled_state)
        self.gif_radio.setChecked(True)
        format_group = QButtonGroup(self)
        for radio in (self.gif_radio, self.mp4_radio, self.webp_radio, self.png_radio):
            format_group.addButton(radio)
            radio.toggled.connect(self._sync_enabled_state)
            format_row.addWidget(radio)
        format_row.addStretch(1)
        controls_layout.addLayout(format_row)
        webp_options = QHBoxLayout()
        webp_options.setContentsMargins(0, 0, 0, 0)
        webp_options.setSpacing(7)
        webp_options.addWidget(self.webp_lossless)
        webp_options.addWidget(self.webp_quality)
        webp_options.addWidget(self.webp_limit_mb)
        controls_layout.addLayout(webp_options)
        self.webp_radio.hide()
        self.png_radio.hide()
        self.webp_lossless.hide()
        self.webp_quality.hide()
        self.webp_limit_mb.hide()

        controls_layout.addWidget(self._section("Sizing"))
        self.size_radio = QRadioButton("Fit under file size")
        self.res_radio = QRadioButton("Set resolution")
        self.native_radio = QRadioButton("Original resolution")
        self.size_radio.setChecked(True)
        size_group = QButtonGroup(self)
        for radio in (self.size_radio, self.res_radio, self.native_radio):
            size_group.addButton(radio)
            radio.toggled.connect(self._sync_enabled_state)
        controls_layout.addWidget(self.size_radio)
        size_row = QHBoxLayout()
        self.max_mb = QDoubleSpinBox()
        self.max_mb.setRange(1, 5000)
        self.max_mb.setDecimals(1)
        self.max_mb.setValue(DEFAULT_MAX_MB)
        self.max_mb.setSuffix(" MB")
        size_row.addSpacing(22)
        size_row.addWidget(self.max_mb)
        controls_layout.addLayout(size_row)
        controls_layout.addWidget(self.res_radio)
        res_row = QHBoxLayout()
        res_row.addSpacing(22)
        self.width_spin = QSpinBox()
        self.height_spin = QSpinBox()
        for spin in (self.width_spin, self.height_spin):
            spin.setRange(2, 32768)
            spin.setSingleStep(2)
        self.width_spin.setValue(700)
        self.height_spin.setValue(700)
        self.resolution_linker = ResolutionLinker(self.width_spin, self.height_spin, self)
        res_row.addWidget(self.width_spin)
        res_row.addWidget(QLabel("×"))
        res_row.addWidget(self.height_spin)
        controls_layout.addLayout(res_row)
        controls_layout.addWidget(self.native_radio)
        self.native_radio.hide()

        controls_layout.addWidget(self._section("Framing"))
        self.frame_mode = QComboBox()
        self.frame_mode.addItem("Original", FramingMode.ORIGINAL)
        self.frame_mode.addItem("Crop to ratio", FramingMode.CROP)
        self.frame_mode.addItem("Fit to ratio", FramingMode.FIT)
        self.frame_mode.currentIndexChanged.connect(self._framing_changed)
        controls_layout.addWidget(self.frame_mode)

        ratio_row = QHBoxLayout()
        self.ratio_combo = QComboBox()
        for label, ratio in RATIO_PRESETS:
            if ratio is not None:
                self.ratio_combo.addItem(label, ratio)
        self.ratio_combo.setCurrentText("16:9")
        self.ratio_combo.currentIndexChanged.connect(self._framing_changed)
        ratio_row.addWidget(self.ratio_combo, 1)
        guide = QToolButton()
        guide.setText("ⓘ")
        guide.setToolTip("Open aspect ratio guide")
        guide.clicked.connect(self._show_aspect_guide)
        ratio_row.addWidget(guide)
        controls_layout.addLayout(ratio_row)

        frame_actions = QHBoxLayout()
        self.center_btn = QPushButton("Center")
        self.center_btn.clicked.connect(self._center_framing)
        self.color_btn = QPushButton("Background")
        self.color_btn.clicked.connect(self._choose_background)
        frame_actions.addWidget(self.center_btn)
        frame_actions.addWidget(self.color_btn)
        controls_layout.addLayout(frame_actions)

        controls_layout.addWidget(self._section("Output folder"))
        out_row = QHBoxLayout()
        self.output_path = QLabel(str(default_output_dir()))
        self.output_path.setObjectName("Muted")
        self.output_path.setWordWrap(True)
        out_row.addWidget(self.output_path, 1)
        choose_out = QToolButton()
        choose_out.setText("…")
        choose_out.setToolTip("Choose output folder")
        choose_out.clicked.connect(self._choose_output_folder)
        out_row.addWidget(choose_out)
        controls_layout.addLayout(out_row)

        controls_layout.addStretch(1)
        self.convert_btn = QPushButton("POLYMORPH")
        self.convert_btn.setObjectName("Primary")
        self.convert_btn.clicked.connect(self._start_conversion)
        controls_layout.addWidget(self.convert_btn)
        splitter.addWidget(controls)
        splitter.setSizes([220, 560, 300])
        outer.addWidget(splitter, 1)

        progress_card = self._card()
        progress_layout = QHBoxLayout(progress_card)
        progress_layout.setContentsMargins(12, 8, 12, 8)
        self.arcane_progress = ArcaneProgress()
        self.arcane_progress.setVisible(False)
        progress_layout.addWidget(self.arcane_progress)
        status_box = QVBoxLayout()
        self.status_label = QLabel("Ready")
        self.status_label.setObjectName("Muted")
        self.progress = QProgressBar()
        self.progress.setRange(0, 100)
        self.progress.setValue(0)
        status_box.addWidget(self.status_label)
        status_box.addWidget(self.progress)
        progress_layout.addLayout(status_box, 1)
        self.cancel_btn = QPushButton("Cancel")
        self.cancel_btn.setVisible(False)
        self.cancel_btn.clicked.connect(self._cancel_conversion)
        progress_layout.addWidget(self.cancel_btn)
        outer.addWidget(progress_card)

        footer = QHBoxLayout()
        version = QLabel(f"Polymorph v{APP_VERSION}")
        version.setObjectName("Muted")
        footer.addWidget(version)
        footer.addStretch(1)
        footer.addWidget(self._footer_button("update.svg", "Check for updates", self._manual_check_updates))
        whats_new_button = QToolButton()
        whats_new_button.setObjectName("WhatsNewFooter")
        whats_new_button.setText("What's New")
        whats_new_button.setToolTip("View the latest feature announcement and support links")
        whats_new_button.setAccessibleName("View What's New")
        whats_new_button.clicked.connect(self.view_whats_new)
        footer.addWidget(whats_new_button)
        self.whats_new_button = whats_new_button
        self.log_button = QToolButton()
        self.log_button.setObjectName("ConversionLogFooter")
        self.log_button.setText("View Log")
        self.log_button.setToolTip("Open the locally saved per-file conversion errors")
        self.log_button.clicked.connect(self.view_conversion_log)
        footer.addWidget(self.log_button)
        footer.addWidget(self._footer_button("github.svg", "View source on GitHub", lambda: self._open_url(REPO_URL)))
        footer.addWidget(self._footer_button("kofi.svg", "Support me on Ko-fi", lambda: self._open_url(KOFI_URL), bool(KOFI_URL)))
        footer.addWidget(self._footer_button("patreon.svg", "Support me on Patreon", lambda: self._open_url(PATREON_URL), bool(PATREON_URL)))
        footer.addWidget(self._footer_button("discord.svg", "Join the Discord", lambda: self._open_url(DISCORD_URL), bool(DISCORD_URL)))
        outer.addLayout(footer)

        self.setCentralWidget(root)

    @staticmethod
    def _card() -> QFrame:
        frame = QFrame()
        frame.setObjectName("Card")
        return frame

    @staticmethod
    def _section(text: str) -> QLabel:
        label = QLabel(text)
        label.setObjectName("Section")
        return label

    def _footer_button(self, icon_name: str, tooltip: str, slot, enabled: bool = True) -> QToolButton:
        button = QToolButton()
        button.setObjectName("FooterIcon")
        button.setIcon(QIcon(str(asset_path(icon_name))))
        button.setIconSize(QSize(17, 17))
        button.setToolTip(tooltip)
        button.setAccessibleName(tooltip)
        button.setFixedSize(32, 30)
        button.setEnabled(enabled)
        button.clicked.connect(slot)
        return button

    def dragEnterEvent(self, event: QDragEnterEvent) -> None:
        if event.mimeData().hasUrls() and any(
            Path(u.toLocalFile()).suffix.lower() in SUPPORTED_INPUT_EXTENSIONS
            for u in event.mimeData().urls()
        ):
            event.acceptProposedAction()

    def dropEvent(self, event: QDropEvent) -> None:
        self._add_files([Path(u.toLocalFile()) for u in event.mimeData().urls()])
        event.acceptProposedAction()

    def _choose_files(self) -> None:
        paths, _ = QFileDialog.getOpenFileNames(
            self, "Add animated WebP files", str(Path.home()), "Animated WebP (*.webp)"
        )
        self._add_files([Path(p) for p in paths])

    def _add_files(self, paths: list[Path]) -> None:
        mixed = False
        for path in paths:
            path = path.resolve()
            if (path.suffix.lower() not in SUPPORTED_INPUT_EXTENSIONS
                    or not path.is_file() or path in self.files):
                continue
            if self.files and is_still_image(path) != is_still_image(self.files[0]):
                mixed = True
                continue
            self.files.append(path)
            self.file_list.addItem(QListWidgetItem(path.name))
        if self.files and self.file_list.currentRow() < 0:
            self.file_list.setCurrentRow(0)
        self._sync_enabled_state()
        if mixed:
            self.status_label.setText("Add still images and animations in separate batches.")

    def _remove_selected(self) -> None:
        row = self.file_list.currentRow()
        if row < 0:
            return
        self.file_list.takeItem(row)
        self.files.pop(row)
        if not self.files:
            self.preview.set_source(None)
            self.dimensions_label.setText("No file selected")
            self._set_media_mode(None)
        self._sync_enabled_state()

    def _selection_changed(self, row: int) -> None:
        if row < 0 or row >= len(self.files):
            return
        path = self.files[row]
        self._set_media_mode(is_still_image(path))
        self.preview.set_source(path)
        self._update_probe_label(path)

    def _set_media_mode(self, still: bool | None) -> None:
        if self._still_mode is still:
            return
        was_static = self._still_mode is True
        self._still_mode = still
        static = still is True
        for radio in (self.gif_radio, self.mp4_radio):
            radio.setVisible(not static)
        self.webp_radio.setVisible(still is not None)
        self.png_radio.setVisible(static)
        self.native_radio.setVisible(static)
        if static:
            self._animated_ratio = self.ratio_combo.currentText()
            self.ratio_combo.setCurrentText("1:1")
            self.webp_radio.setChecked(True)
            self.webp_lossless.setChecked(True)
            self.native_radio.setChecked(True)
            self.max_mb.setValue(20.0)
        else:
            if was_static:
                self.ratio_combo.setCurrentText(self._animated_ratio)
            self.gif_radio.setChecked(True)
            self.webp_lossless.setChecked(False)
            self.size_radio.setChecked(True)
            self.max_mb.setValue(DEFAULT_MAX_MB)
        for widget in getattr(self, "_brand_animated_format_notes", ()):
            widget.setVisible(not static)
        for widget in getattr(self, "_brand_still_format_notes", ()):
            widget.setVisible(static)
        if hasattr(self, "_brand_webp_animation_note"):
            self._brand_webp_animation_note.setVisible(not static and still is False)
        if hasattr(self, "_brand_priority_card"):
            self._brand_priority_card.setVisible(not static)
        for widget in getattr(self, "_brand_playback_controls", ()):
            widget.setVisible(not static)
        self._sync_enabled_state()

    def _update_probe_label(self, path: Path) -> None:
        if not self.converter:
            self.dimensions_label.setText(
                "Preview loaded • conversion components not installed in this dev environment"
            )
            return
        try:
            info = self.media_cache.get(path) or self.converter.probe(path)
            self.media_cache[path] = info
            native = native_geometry(info, self.framing)
            self.dimensions_label.setText(
                (f"Source {info.width}×{info.height} • still image • "
                 f"framed max {native.width}×{native.height}" if info.is_still
                 else f"Source {info.width}×{info.height} • {info.frame_count} frames • "
                 f"framed max {native.width}×{native.height}")
            )
            self.resolution_linker.set_native(native.width, native.height)
        except Exception as exc:
            self.dimensions_label.setText(str(exc))

    def _framing_changed(self) -> None:
        self.framing.mode = self.frame_mode.currentData()
        self.framing.ratio = (
            self.ratio_combo.currentData()
            if self.framing.mode is not FramingMode.ORIGINAL
            else None
        )
        self.preview.set_framing(self.framing)
        self._sync_enabled_state()
        row = self.file_list.currentRow()
        if 0 <= row < len(self.files):
            self._update_probe_label(self.files[row])

    def _preview_offset_changed(self, x: float, y: float) -> None:
        self.framing.offset_x = x
        self.framing.offset_y = y

    def _center_framing(self) -> None:
        self.framing.offset_x = 0.0
        self.framing.offset_y = 0.0
        self.preview.set_framing(self.framing)

    def _choose_background(self) -> None:
        chosen = QColorDialog.getColor(
            QColor(self.framing.background), self, "Fit background color"
        )
        if chosen.isValid():
            self.framing.background = chosen.name()
            self.preview.set_framing(self.framing)

    def _show_aspect_guide(self) -> None:
        AspectGuideDialog(self).exec()

    def _choose_output_folder(self) -> None:
        folder = QFileDialog.getExistingDirectory(
            self, "Choose output folder", self.output_path.text()
        )
        if folder:
            self.output_path.setText(folder)

    def _open_output_folder(self) -> None:
        folder = Path(self.output_path.text())
        if not folder.is_dir():
            QMessageBox.warning(self, "Output folder unavailable", f"Folder does not exist: {folder}")
            return
        QDesktopServices.openUrl(QUrl.fromLocalFile(str(folder.resolve())))

    def _sync_enabled_state(self) -> None:
        busy = self.worker is not None and self.worker.isRunning()
        fixed_webp_cap = (
            self._still_mode is False
            and self.webp_radio.isChecked()
            and self.webp_limit_mb.isChecked()
        )
        self.max_mb.setEnabled((self.size_radio.isChecked() or fixed_webp_cap) and not busy)
        self.max_mb.setToolTip(
            "Maximum animated WebP output size; enabled by Limit MB even "
            "when Set resolution is selected."
            if fixed_webp_cap else "Maximum output size in Fit under file size mode."
        )
        self.width_spin.setEnabled(self.res_radio.isChecked() and not busy)
        self.height_spin.setEnabled(self.res_radio.isChecked() and not busy)
        self.native_radio.setEnabled(not busy)
        show_webp = self._still_mode is not None and self.webp_radio.isChecked()
        show_animated_webp = self._still_mode is False and self.webp_radio.isChecked()
        self.webp_lossless.setVisible(show_webp)
        self.webp_lossless.setEnabled(not busy)
        self.webp_quality.setVisible(show_animated_webp and not self.webp_lossless.isChecked())
        self.webp_quality.setEnabled(not busy)
        self.webp_limit_mb.setVisible(show_animated_webp)
        self.webp_limit_mb.setEnabled(not busy)
        framing_enabled = self.frame_mode.currentData() is not FramingMode.ORIGINAL
        self.ratio_combo.setEnabled(framing_enabled and not busy)
        self.center_btn.setEnabled(framing_enabled and not busy)
        self.color_btn.setEnabled(
            self.frame_mode.currentData() is FramingMode.FIT and not busy
        )
        self.convert_btn.setEnabled(
            bool(self.files) and not busy and self.converter is not None
        )
        if self.converter is None and not busy:
            self.status_label.setText(
                "Conversion components not found — use the packaged Windows build or "
                "install FFmpeg/ffprobe/gifski for development"
            )

    def _make_settings(self) -> ConversionSettings:
        return ConversionSettings(
            output_format=(
                OutputFormat.WEBP if self.webp_radio.isChecked() else
                OutputFormat.PNG if self.png_radio.isChecked() else
                OutputFormat.GIF if self.gif_radio.isChecked() else OutputFormat.MP4
            ),
            sizing_mode=(
                SizingMode.NATIVE if self.native_radio.isChecked() else
                SizingMode.FILE_SIZE if self.size_radio.isChecked() else SizingMode.RESOLUTION
            ),
            max_mb=self.max_mb.value(),
            requested_width=self.width_spin.value() if self.res_radio.isChecked() else None,
            requested_height=self.height_spin.value() if self.res_radio.isChecked() else None,
            output_dir=Path(self.output_path.text()),
            framing=copy.deepcopy(self.framing),
            webp_lossless=self.webp_lossless.isChecked(),
            webp_quality=int(self.webp_quality.currentData()),
            webp_limit_enabled=self.webp_limit_mb.isChecked(),
        )

    def _start_conversion(self) -> None:
        if not self.converter or not self.files:
            return
        self._saved_files = 0
        self._failed_files = 0
        self._batch_failures = []
        settings = self._make_settings()
        self._conversion_log = ConversionLog(list(self.files), settings, APP_VERSION)
        self.worker = ConversionWorker(
            self.converter, list(self.files), settings, self
        )
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
        self.worker.start()
        self._sync_enabled_state()

    @Slot(float, str)
    def _progress_changed(self, fraction: float, label: str) -> None:
        percent = int(round(fraction * 100))
        self.progress.setValue(percent)
        self.arcane_progress.set_progress(fraction)
        self.status_label.setText(f"{label}… {percent}%")
        if self._conversion_log:
            self._conversion_log.progress(fraction, label)

    def _file_started(self, path: str) -> None:
        self.status_label.setText(f"Polymorphing {Path(path).name}…")
        if self._conversion_log:
            self._conversion_log.started(path)

    def _file_finished(self, path: str, summary: str, output: str) -> None:
        self._saved_files += 1
        if self._conversion_log:
            self._conversion_log.saved(path, output, summary)
        saved = Path(output)
        self.status_label.setText(f"Saved {saved.name} • {summary}")
        self.status_label.setToolTip(str(saved))
        if hasattr(self, "_brand_status_detail"):
            self._brand_status_detail.setText(f"Output: {saved}")
            self._brand_status_detail.setToolTip(str(saved))

    def _file_failed(self, path: str, reason: str, trace: str = "") -> None:
        self._failed_files += 1
        self._batch_failures.append((path, reason))
        if self._conversion_log:
            self._conversion_log.failed(path, reason, trace)
        self.status_label.setText(f"Failed {Path(path).name}: {reason}")
        self.status_label.setToolTip(reason)
        if hasattr(self, "_brand_status_detail"):
            self._brand_status_detail.setText(f"Reason: {reason}")
            self._brand_status_detail.setToolTip(reason)

    def _conversion_finished(self) -> None:
        self.arcane_progress.set_active(False)
        if hasattr(self, "status_ring"):
            self.status_ring.set_result(
                "error" if self._failed_files else "success" if self._saved_files else "idle"
            )
        self.arcane_progress.setVisible(False)
        self.cancel_btn.setVisible(False)
        self.progress.setValue(100 if self._saved_files and not self._failed_files else 0)
        if self.status_label.text().startswith(("Encoding", "Optimizing", "Polymorphing")):
            self.status_label.setText("Conversion ended without an output.")
        if self._failed_files:
            errors = "\n".join(f"{Path(path).name}: {reason}" for path, reason in self._batch_failures)
            summary = (
                f"Partial success: {self._saved_files} saved, {self._failed_files} failed."
                if self._saved_files else f"Conversion failed: {self._failed_files} file(s)."
            )
            self.status_label.setText(summary + " Click View Log for details.")
            self.status_label.setToolTip(errors)
            first_path, first_reason = self._batch_failures[0]
            if hasattr(self, "_brand_status_detail"):
                self._brand_status_detail.setText(
                    f"First failure: {Path(first_path).name}: {first_reason}"
                )
                self._brand_status_detail.setToolTip(errors)
            self.log_button.setToolTip(f"View details for {self._failed_files} failed file(s)")
        if self._conversion_log:
            self._conversion_log.finished(self._saved_files, self._failed_files)
        worker = self.worker
        self.worker = None
        if worker:
            worker.deleteLater()
        self._sync_enabled_state()

    def _cancel_conversion(self) -> None:
        if self.worker:
            self.status_label.setText("Cancelling…")
            self.worker.stop()

    def closeEvent(self, event) -> None:
        # Closing the app while FFmpeg is running used to leave expensive
        # orphaned encoders behind (observed on Windows with animated WebP).
        worker = self.worker
        if worker is not None and worker.isRunning():
            worker.stop()
            if not worker.wait(5000):
                self.status_label.setText("Stopping active conversion before exit…")
                event.ignore()
                return
        super().closeEvent(event)

    def view_conversion_log(self) -> None:
        if self._conversion_log is not None:
            log = self._conversion_log
            content = log.text
            path = log.path if log.write_error is None else None
        else:
            path, content = latest_log()
        if self._conversion_log_dialog is not None:
            self._conversion_log_dialog.close()
        dialog = ConversionLogDialog(content, path, self)
        self._conversion_log_dialog = dialog
        dialog.show()
        dialog.raise_()

    def show_whats_new_if_needed(self):
        return show_whats_new_once(self)

    def view_whats_new(self):
        return show_whats_new_once(self, force=True)

    def _manual_check_updates(self) -> None:
        self._check_updates(manual=True)

    def _auto_check_updates(self) -> None:
        self._check_updates(manual=False)

    def _check_updates(self, manual: bool) -> None:
        def task() -> None:
            release = fetch_latest_for_channel()
            self.updateCheckCompleted.emit(release, manual)

        threading.Thread(target=task, daemon=True).start()

    def _handle_release(self, release, manual: bool) -> None:
        if not release:
            if manual:
                QMessageBox.information(
                    self, "Updates",
                    "No Polymorph release information is available yet."
                )
            return
        if not is_newer(release.version):
            if manual:
                QMessageBox.information(
                    self, "Updates", f"Polymorph v{APP_VERSION} is up to date."
                )
            return
        skipped = self.settings_store.value("updates/skipped_version", "", str)
        if not manual and skipped == release.version:
            return

        box = QMessageBox(self)
        box.setWindowTitle("Update available")
        box.setText(f"Update available! Polymorph v{release.version}")
        box.setInformativeText(f"You are currently using v{APP_VERSION}.")
        update_btn = box.addButton("Update", QMessageBox.AcceptRole)
        skip_btn = box.addButton("Skip This Version", QMessageBox.DestructiveRole)
        box.addButton(QMessageBox.Close)
        box.exec()
        if box.clickedButton() is skip_btn:
            self.settings_store.setValue("updates/skipped_version", release.version)
        elif box.clickedButton() is update_btn:
            self._install_update(release)

    def _install_update(self, release) -> None:
        self.status_label.setText(f"Downloading Polymorph v{release.version} update…")

        def task() -> None:
            try:
                if release.kind == "stable_delta":
                    import sys
                    stage = download_and_stage_public_delta(release, Path(sys.executable).parent)
                    self.updateDownloadCompleted.emit(("delta", str(stage)), None)
                else:
                    installer = download_and_verify_installer(release)
                    self.updateDownloadCompleted.emit(installer, None)
            except Exception as exc:
                self.updateDownloadCompleted.emit(None, str(exc))

        threading.Thread(target=task, daemon=True).start()

    @Slot(object, object)
    def _handle_downloaded_update(self, installer, error) -> None:
        if error:
            QMessageBox.warning(self, "Update failed", str(error))
            return
        if isinstance(installer, tuple) and installer[0] == "delta":
            import sys
            try:
                launch_staged_update(Path(installer[1]), Path(sys.executable).parent)
            except Exception as exc:
                QMessageBox.warning(self, "Update failed", str(exc))
                return
            QApplication.quit()
        else:
            self._launch_verified_update(Path(installer))

    def _launch_verified_update(self, installer: Path) -> None:
        try:
            launch_installer(installer)
        except Exception as exc:
            QMessageBox.warning(self, "Update failed", str(exc))
            return
        QApplication.quit()

    @staticmethod
    def _open_url(url: str) -> None:
        if url:
            QDesktopServices.openUrl(QUrl(url))
