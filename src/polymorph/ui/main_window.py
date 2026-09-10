from __future__ import annotations

import copy
import threading
from pathlib import Path

from PySide6.QtCore import QSettings, QThread, QTimer, Qt, Signal, Slot
from PySide6.QtGui import QColor, QDesktopServices, QDragEnterEvent, QDropEvent
from PySide6.QtCore import QUrl
from PySide6.QtWidgets import (
    QApplication,
    QButtonGroup,
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
from ..geometry import native_geometry
from ..models import ConversionSettings, FramingMode, FramingSettings, OutputFormat, SizingMode
from ..tools import find_toolchain
from ..update_service import download_and_verify_installer, fetch_latest_release, is_newer, launch_installer
from .dialogs import AspectGuideDialog
from .preview import AnimatedPreview
from .progress_ring import ArcaneProgress
from .styles import BASE_STYLESHEET


class ConversionWorker(QThread):
    progressChanged = Signal(float, str)
    fileStarted = Signal(str)
    fileFinished = Signal(str, str)
    failed = Signal(str, str)

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
                self.fileFinished.emit(str(path), summary)
            except ConversionCancelled:
                self.failed.emit(str(path), "Cancelled")
                break
            except Exception as exc:
                self.failed.emit(str(path), str(exc))

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
        self.framing = FramingSettings()
        self.worker: ConversionWorker | None = None
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
        self.gif_radio.setChecked(True)
        format_group = QButtonGroup(self)
        format_group.addButton(self.gif_radio)
        format_group.addButton(self.mp4_radio)
        format_row.addWidget(self.gif_radio)
        format_row.addWidget(self.mp4_radio)
        format_row.addStretch(1)
        controls_layout.addLayout(format_row)

        controls_layout.addWidget(self._section("Sizing"))
        self.size_radio = QRadioButton("Fit under file size")
        self.res_radio = QRadioButton("Set resolution")
        self.size_radio.setChecked(True)
        size_group = QButtonGroup(self)
        size_group.addButton(self.size_radio)
        size_group.addButton(self.res_radio)
        self.size_radio.toggled.connect(self._sync_enabled_state)
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
        res_row.addWidget(self.width_spin)
        res_row.addWidget(QLabel("×"))
        res_row.addWidget(self.height_spin)
        controls_layout.addLayout(res_row)

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
        footer.addWidget(self._footer_button("↻", "Check for updates", self._manual_check_updates))
        footer.addWidget(self._footer_button("⌂", "View source on GitHub", lambda: self._open_url(REPO_URL)))
        footer.addWidget(self._footer_button("K", "Support me on Ko-fi", lambda: self._open_url(KOFI_URL), bool(KOFI_URL)))
        footer.addWidget(self._footer_button("P", "Support me on Patreon", lambda: self._open_url(PATREON_URL), bool(PATREON_URL)))
        footer.addWidget(self._footer_button("D", "Join the Discord", lambda: self._open_url(DISCORD_URL), bool(DISCORD_URL)))
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

    def _footer_button(self, text: str, tooltip: str, slot, enabled: bool = True) -> QToolButton:
        button = QToolButton()
        button.setText(text)
        button.setToolTip(tooltip)
        button.setAccessibleName(tooltip)
        button.setFixedSize(32, 30)
        button.setEnabled(enabled)
        button.clicked.connect(slot)
        return button

    def dragEnterEvent(self, event: QDragEnterEvent) -> None:
        if event.mimeData().hasUrls() and any(Path(u.toLocalFile()).suffix.lower() in SUPPORTED_INPUT_EXTENSIONS for u in event.mimeData().urls()):
            event.acceptProposedAction()

    def dropEvent(self, event: QDropEvent) -> None:
        self._add_files([Path(u.toLocalFile()) for u in event.mimeData().urls()])
        event.acceptProposedAction()

    def _choose_files(self) -> None:
        paths, _ = QFileDialog.getOpenFileNames(self, "Add animated WebP files", str(Path.home()), "Animated WebP (*.webp)")
        self._add_files([Path(p) for p in paths])

    def _add_files(self, paths: list[Path]) -> None:
        for path in paths:
            path = path.resolve()
            if path.suffix.lower() not in SUPPORTED_INPUT_EXTENSIONS or not path.is_file() or path in self.files:
                continue
            self.files.append(path)
            self.file_list.addItem(QListWidgetItem(path.name))
        if self.files and self.file_list.currentRow() < 0:
            self.file_list.setCurrentRow(0)
        self._sync_enabled_state()

    def _remove_selected(self) -> None:
        row = self.file_list.currentRow()
        if row < 0:
            return
        self.file_list.takeItem(row)
        self.files.pop(row)
        if not self.files:
            self.preview.set_source(None)
            self.dimensions_label.setText("No file selected")
        self._sync_enabled_state()

    def _selection_changed(self, row: int) -> None:
        if row < 0 or row >= len(self.files):
            return
        path = self.files[row]
        self.preview.set_source(path)
        self._update_probe_label(path)

    def _update_probe_label(self, path: Path) -> None:
        if not self.converter:
            self.dimensions_label.setText("Preview loaded • conversion components not installed in this dev environment")
            return
        try:
            info = self.media_cache.get(path) or self.converter.probe(path)
            self.media_cache[path] = info
            native = native_geometry(info, self.framing)
            self.dimensions_label.setText(f"Source {info.width}×{info.height} • {info.frame_count} frames • framed max {native.width}×{native.height}")
            self.width_spin.setMaximum(native.width)
            self.height_spin.setMaximum(native.height)
        except Exception as exc:
            self.dimensions_label.setText(str(exc))

    def _framing_changed(self) -> None:
        self.framing.mode = self.frame_mode.currentData()
        self.framing.ratio = self.ratio_combo.currentData() if self.framing.mode is not FramingMode.ORIGINAL else None
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
        chosen = QColorDialog.getColor(QColor(self.framing.background), self, "Fit background color")
        if chosen.isValid():
            self.framing.background = chosen.name()
            self.preview.set_framing(self.framing)

    def _show_aspect_guide(self) -> None:
        AspectGuideDialog(self).exec()

    def _choose_output_folder(self) -> None:
        folder = QFileDialog.getExistingDirectory(self, "Choose output folder", self.output_path.text())
        if folder:
            self.output_path.setText(folder)

    def _sync_enabled_state(self) -> None:
        busy = self.worker is not None and self.worker.isRunning()
        self.max_mb.setEnabled(self.size_radio.isChecked() and not busy)
        self.width_spin.setEnabled(self.res_radio.isChecked() and not busy)
        self.height_spin.setEnabled(self.res_radio.isChecked() and not busy)
        framing_enabled = self.frame_mode.currentData() is not FramingMode.ORIGINAL
        self.ratio_combo.setEnabled(framing_enabled and not busy)
        self.center_btn.setEnabled(framing_enabled and not busy)
        self.color_btn.setEnabled(self.frame_mode.currentData() is FramingMode.FIT and not busy)
        self.convert_btn.setEnabled(bool(self.files) and not busy and self.converter is not None)
        if self.converter is None and not busy:
            self.status_label.setText("Conversion components not found — use the packaged Windows build or install FFmpeg/ffprobe/gifski for development")

    def _make_settings(self) -> ConversionSettings:
        return ConversionSettings(
            output_format=OutputFormat.GIF if self.gif_radio.isChecked() else OutputFormat.MP4,
            sizing_mode=SizingMode.FILE_SIZE if self.size_radio.isChecked() else SizingMode.RESOLUTION,
            max_mb=self.max_mb.value(),
            requested_width=self.width_spin.value() if self.res_radio.isChecked() else None,
            requested_height=self.height_spin.value() if self.res_radio.isChecked() else None,
            output_dir=Path(self.output_path.text()),
            framing=copy.deepcopy(self.framing),
        )

    def _start_conversion(self) -> None:
        if not self.converter or not self.files:
            return
        self.worker = ConversionWorker(self.converter, list(self.files), self._make_settings(), self)
        self.worker.progressChanged.connect(self._progress_changed)
        self.worker.fileStarted.connect(lambda p: self.status_label.setText(f"Polymorphing {Path(p).name}…"))
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

    @Slot(float, str)
    def _progress_changed(self, fraction: float, label: str) -> None:
        percent = int(round(fraction * 100))
        self.progress.setValue(percent)
        self.arcane_progress.set_progress(fraction)
        self.status_label.setText(f"{label}… {percent}%")

    def _file_finished(self, path: str, summary: str) -> None:
        self.status_label.setText(f"Finished {Path(path).name} • {summary}")

    def _file_failed(self, path: str, reason: str) -> None:
        self.status_label.setText(f"{Path(path).name}: {reason}")

    def _conversion_finished(self) -> None:
        self.arcane_progress.set_active(False)
        self.arcane_progress.setVisible(False)
        self.cancel_btn.setVisible(False)
        self.progress.setValue(100 if self.files else 0)
        if self.status_label.text().startswith(("Encoding", "Optimizing", "Polymorphing")):
            self.status_label.setText("Complete")
        worker = self.worker
        self.worker = None
        if worker:
            worker.deleteLater()
        self._sync_enabled_state()

    def _cancel_conversion(self) -> None:
        if self.worker:
            self.status_label.setText("Cancelling…")
            self.worker.stop()

    def _manual_check_updates(self) -> None:
        self._check_updates(manual=True)

    def _auto_check_updates(self) -> None:
        self._check_updates(manual=False)

    def _check_updates(self, manual: bool) -> None:
        def task() -> None:
            release = fetch_latest_release()
            self.updateCheckCompleted.emit(release, manual)
        threading.Thread(target=task, daemon=True).start()

    def _handle_release(self, release, manual: bool) -> None:
        if not release:
            if manual:
                QMessageBox.information(self, "Updates", "No Polymorph release information is available yet.")
            return
        if not is_newer(release.version):
            if manual:
                QMessageBox.information(self, "Updates", f"Polymorph v{APP_VERSION} is up to date.")
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
