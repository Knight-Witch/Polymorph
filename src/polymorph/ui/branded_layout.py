from __future__ import annotations

import sys
from pathlib import Path

from PySide6.QtCore import QDir, QProcess, QSize, Qt, QUrl
from PySide6.QtGui import QColor, QDesktopServices, QIcon, QImageReader, QPixmap
from PySide6.QtWidgets import (
    QAbstractItemView,
    QAbstractSpinBox,
    QButtonGroup,
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QListWidgetItem,
    QMenu,
    QPushButton,
    QRadioButton,
    QSizePolicy,
    QSlider,
    QSplitter,
    QToolButton,
    QVBoxLayout,
    QWidget,
)

from ..constants import APP_VERSION, DISCORD_URL, KOFI_URL, PATREON_URL, REPO_URL
from ..resources import asset_path
from .brand_widgets import (
    BrandSigil,
    PolymorphButton,
    ScaleRegistry,
    TexturedFrame,
    TintIconLabel,
    tinted_icon_pixmap,
)


class QueueRow(TexturedFrame):
    def __init__(self, window, path: Path, select_callback, parent=None) -> None:
        super().__init__("queue", parent)
        self.window = window
        self.path = path
        self._select_callback = select_callback
        self.setObjectName("QueueRow")
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self._scale = 1.0

        self.row = QHBoxLayout(self)
        self.row.setContentsMargins(7, 5, 7, 5)
        self.row.setSpacing(9)

        self.thumb = QLabel()
        self.thumb.setObjectName("QueueThumb")
        self.thumb.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.row.addWidget(self.thumb)

        text_box = QVBoxLayout()
        text_box.setSpacing(1)
        self.name_label = QLabel(path.name)
        self.name_label.setObjectName("QueueFileName")
        self.name_label.setToolTip(str(path))
        self.meta_label = QLabel(self._metadata_text())
        self.meta_label.setObjectName("QueueMeta")
        text_box.addWidget(self.name_label)
        text_box.addWidget(self.meta_label)
        self.row.addLayout(text_box, 1)

        self.menu_btn = QToolButton()
        self.menu_btn.setObjectName("QueueMenuButton")
        self.menu_btn.setText("⋯")
        self.menu_btn.setToolTip("File actions")
        self.menu_btn.clicked.connect(self._show_menu)
        self.row.addWidget(self.menu_btn)
        self.apply_scale(1.0)

    def apply_scale(self, scale: float) -> None:
        self._scale = scale
        self.row.setContentsMargins(
            round(7 * scale), round(5 * scale), round(7 * scale), round(5 * scale)
        )
        self.row.setSpacing(max(4, round(9 * scale)))
        width = max(54, round(78 * scale))
        height = max(34, round(46 * scale))
        self.thumb.setFixedSize(width, height)
        self.menu_btn.setFixedWidth(max(24, round(30 * scale)))
        self.setMinimumHeight(max(44, round(58 * scale)))
        self._load_thumbnail()

    def set_selected(self, selected: bool) -> None:
        self.setProperty("selected", selected)
        self.update()

    def mousePressEvent(self, event) -> None:
        self._select_callback()
        super().mousePressEvent(event)

    def _load_thumbnail(self) -> None:
        reader = QImageReader(str(self.path))
        reader.setAutoTransform(True)
        image = reader.read()
        if image.isNull():
            self.thumb.setText("WEBP")
            return
        pixmap = QPixmap.fromImage(image)
        pixmap = pixmap.scaled(
            self.thumb.size(),
            Qt.AspectRatioMode.KeepAspectRatioByExpanding,
            Qt.TransformationMode.SmoothTransformation,
        )
        x = max(0, (pixmap.width() - self.thumb.width()) // 2)
        y = max(0, (pixmap.height() - self.thumb.height()) // 2)
        self.thumb.setPixmap(pixmap.copy(x, y, self.thumb.width(), self.thumb.height()))

    def _metadata_text(self) -> str:
        try:
            size = self.path.stat().st_size
            size_text = f"{size / 1_000_000:.1f} MB" if size >= 1_000_000 else f"{size / 1000:.0f} KB"
        except OSError:
            size_text = "Unknown size"
        try:
            info = self.window.media_cache.get(self.path)
            if info is None and self.window.converter is not None:
                info = self.window.converter.probe(self.path)
                self.window.media_cache[self.path] = info
            if info is not None:
                return f"{size_text}   |   {info.width} × {info.height}   |   {info.duration_s:.1f}s"
        except Exception:
            pass
        return size_text

    def _show_menu(self) -> None:
        menu = QMenu(self)
        open_action = menu.addAction("Open")
        reveal_action = menu.addAction("Open file location")
        menu.addSeparator()
        remove_action = menu.addAction("Remove from queue")
        chosen = menu.exec(self.mapToGlobal(self.rect().bottomRight()))
        if chosen is open_action:
            QDesktopServices.openUrl(QUrl.fromLocalFile(str(self.path)))
        elif chosen is reveal_action:
            if sys.platform == "win32":
                QProcess.startDetached(
                    "explorer.exe",
                    ["/select,", QDir.toNativeSeparators(str(self.path))],
                )
            else:
                QDesktopServices.openUrl(QUrl.fromLocalFile(str(self.path.parent)))
        elif chosen is remove_action:
            self._remove_this()

    def _remove_this(self) -> None:
        try:
            index = self.window.files.index(self.path)
        except ValueError:
            return
        self.window.file_list.setCurrentRow(index)
        self.window._remove_selected()


def _line(vertical: bool = False) -> QFrame:
    line = QFrame()
    line.setObjectName("VerticalSeparator" if vertical else "CardSeparator")
    line.setFrameShape(QFrame.Shape.VLine if vertical else QFrame.Shape.HLine)
    return line


def _header_icon(icon_name: str | None, symbol: str | None = None):
    if icon_name:
        return TintIconLabel(icon_name, 15)
    label = QLabel(symbol or "•")
    label.setStyleSheet("color:#d0ad6d; background:transparent;")
    label.setAlignment(Qt.AlignmentFlag.AlignCenter)
    label.setFixedWidth(15)
    return label


def _card(
    registry: ScaleRegistry,
    title: str,
    icon_name: str | None = None,
    *,
    symbol: str | None = None,
    separator: bool = True,
    object_name: str = "ControlCard",
    tone: str = "control",
):
    frame = TexturedFrame(tone)
    frame.setObjectName(object_name)
    layout = QVBoxLayout(frame)
    registry.layout(layout, (10, 7, 10, 8), 5)

    header = QHBoxLayout()
    registry.layout(header, (0, 0, 0, 0), 6)
    icon = _header_icon(icon_name, symbol)
    header.addWidget(icon)
    heading = QLabel(title)
    heading.setObjectName("CardHeading")
    header.addWidget(heading)
    header.addStretch(1)
    layout.addLayout(header)
    if separator:
        layout.addWidget(_line())
    return frame, layout, header, icon


def _subtext(text: str) -> QLabel:
    label = QLabel(text)
    label.setObjectName("SecondaryText")
    label.setWordWrap(True)
    return label


def _format_time(seconds: float) -> str:
    seconds = max(0.0, float(seconds))
    minutes = int(seconds // 60)
    remainder = seconds - minutes * 60
    return f"{minutes}:{remainder:04.1f}"


def _footer_link(window, icon_name: str, text: str, tooltip: str, slot, enabled: bool = True):
    button = QToolButton()
    button.setObjectName("FooterLink")
    button.setIcon(QIcon(str(asset_path(icon_name))))
    button.setIconSize(QSize(14, 14))
    button.setText(text)
    button.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextBesideIcon)
    button.setToolTip(tooltip)
    button.setEnabled(enabled)
    button.clicked.connect(slot)
    return button


def rebuild_brand_layout(window) -> None:
    registry = ScaleRegistry()
    window._brand_scale_registry = registry

    root = QWidget()
    root.setObjectName("AppRoot")
    outer = QVBoxLayout(root)
    registry.layout(outer, (15, 11, 15, 7), 7)

    # Header -----------------------------------------------------------------
    header = QHBoxLayout()
    registry.layout(header, (0, 0, 0, 0), 10)
    sigil = BrandSigil(40)
    registry.callback(sigil.apply_scale)
    header.addWidget(sigil, 0, Qt.AlignmentFlag.AlignTop)

    brand = QVBoxLayout()
    registry.layout(brand, (0, 0, 0, 0), 0)
    title = QLabel("POLYMORPH")
    title.setObjectName("BrandTitle")
    subtitle = QLabel("Media conversion magic — by Knight Witch™")
    subtitle.setObjectName("BrandSubtitle")
    brand.addWidget(title)
    brand.addWidget(subtitle)
    header.addLayout(brand, 1)
    outer.addLayout(header)

    splitter = QSplitter(Qt.Orientation.Horizontal)
    splitter.setObjectName("BrandMainSplitter")
    splitter.setChildrenCollapsible(False)
    splitter.setHandleWidth(5)

    # LEFT WORKSPACE ----------------------------------------------------------
    workspace = QWidget()
    workspace.setObjectName("Workspace")
    workspace_layout = QVBoxLayout(workspace)
    registry.layout(workspace_layout, (0, 0, 0, 0), 7)

    files_card, files_layout, files_header, files_icon = _card(
        registry,
        "FILES",
        "folder.png",
        separator=False,
        object_name="FileCard",
        tone="control",
    )
    registry.callback(files_icon.refresh)
    files_count = QLabel("0 files")
    files_count.setObjectName("FileCount")
    files_header.addWidget(files_count)
    files_header.addStretch(1)

    add_btn = QPushButton("+ Add Files")
    add_btn.setObjectName("HeaderAction")
    add_btn.setToolTip("Add one or more animated WebP files to the conversion queue.")
    add_btn.clicked.connect(window._choose_files)
    files_header.addWidget(add_btn)

    trash_btn = QToolButton()
    trash_btn.setObjectName("HeaderTrash")
    trash_btn.setIcon(QIcon(tinted_icon_pixmap("trash.png", 16, QColor("#aaa39a"))))
    trash_btn.setIconSize(QSize(16, 16))
    trash_btn.setToolTip("Remove selected file from the queue.")
    trash_btn.clicked.connect(window._remove_selected)
    registry.size(trash_btn, 26, 25)
    files_header.addWidget(trash_btn)
    files_header.addWidget(_line(True))

    clear_btn = QPushButton("Clear All")
    clear_btn.setObjectName("ClearAllLink")
    clear_btn.setToolTip("Remove every item from the queue. Source files are not deleted.")
    files_header.addWidget(clear_btn)

    def clear_queue() -> None:
        window.file_list.clear()
        window.files.clear()
        window.media_cache.clear()
        window.preview.set_source(None)
        window.dimensions_label.setText("No file selected")
        window._sync_enabled_state()

    clear_btn.clicked.connect(clear_queue)

    window.file_list.setParent(files_card)
    window.file_list.setObjectName("QueueList")
    window.file_list.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
    window.file_list.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
    window.file_list.setVerticalScrollMode(QAbstractItemView.ScrollMode.ScrollPerPixel)
    window.file_list.setSpacing(3)
    files_layout.addWidget(window.file_list)

    status_detail = QLabel()
    status_detail.setObjectName("StatusDetail")
    window._brand_status_detail = status_detail

    def queue_rows():
        result = []
        for row in range(window.file_list.count()):
            item = window.file_list.item(row)
            widget = window.file_list.itemWidget(item)
            if isinstance(widget, QueueRow):
                result.append(widget)
        return result

    window._brand_queue_rows = queue_rows

    def update_selection(*_args) -> None:
        current = window.file_list.currentRow()
        for row, widget in enumerate(queue_rows()):
            widget.set_selected(row == current)
        trash_btn.setEnabled(current >= 0)

    def sync_preview_timing(row: int) -> None:
        if row < 0 or row >= len(window.files):
            window.preview.set_timing(0, 0.0, [])
            return
        path = window.files[row]
        try:
            info = window.media_cache.get(path)
            if info is None and window.converter is not None:
                info = window.converter.probe(path)
                window.media_cache[path] = info
            if info is not None:
                window.preview.set_timing(info.frame_count, info.duration_s, info.frame_durations_ms)
        except Exception:
            pass

    def decorate_queue_rows(*_args) -> None:
        for row in range(window.file_list.count()):
            item = window.file_list.item(row)
            if window.file_list.itemWidget(item) is not None or row >= len(window.files):
                continue
            path = window.files[row]
            widget = QueueRow(
                window,
                path,
                select_callback=lambda p=path: window.file_list.setCurrentRow(
                    window.files.index(p) if p in window.files else -1
                ),
            )
            widget.apply_scale(float(window.property("brandScale") or 1.0))
            item.setSizeHint(QSize(100, widget.minimumHeight()))
            window.file_list.setItemWidget(item, widget)
        update_selection()

    def update_file_count(*_args) -> None:
        count = window.file_list.count()
        files_count.setText(f"{count} file" if count == 1 else f"{count} files")
        scale = float(window.property("brandScale") or 1.0)
        row_height = max(44, round(61 * scale))
        target = max(round(58 * scale), min(round(125 * scale), count * row_height + round(7 * scale)))
        window.file_list.setFixedHeight(target)
        if count == 0:
            status_detail.setText("No files imported. Add media to begin.")
        elif count == 1:
            status_detail.setText("1 file imported. Choose your settings and begin.")
        else:
            status_detail.setText(f"{count} files imported. Choose your settings and begin.")
        if window.worker is None or not window.worker.isRunning():
            window.status_label.setText("Ready")

    registry.callback(lambda _scale: update_file_count())
    model = window.file_list.model()
    model.rowsInserted.connect(decorate_queue_rows)
    model.rowsInserted.connect(update_file_count)
    model.rowsRemoved.connect(update_file_count)
    model.modelReset.connect(update_file_count)
    window.file_list.currentRowChanged.connect(update_selection)
    window.file_list.currentRowChanged.connect(sync_preview_timing)
    decorate_queue_rows()
    update_file_count()
    workspace_layout.addWidget(files_card)

    # Preview: no redundant title/header. ------------------------------------
    preview_card = TexturedFrame("preview")
    preview_card.setObjectName("PreviewCard")
    preview_layout = QVBoxLayout(preview_card)
    registry.layout(preview_layout, (9, 8, 9, 7), 5)

    window.preview.setParent(preview_card)
    window.preview.setObjectName("MediaPreview")
    window.preview.setMinimumHeight(305)
    registry.min_height(window.preview, 305)
    preview_layout.addWidget(window.preview, 1)

    playback = QHBoxLayout()
    registry.layout(playback, (4, 0, 4, 0), 7)
    play_btn = QToolButton()
    play_btn.setObjectName("PlaybackButton")
    play_btn.setText("❚❚")
    play_btn.setToolTip("Play or pause the preview")
    play_btn.clicked.connect(window.preview.toggle_playback)
    registry.size(play_btn, 28, 24)
    playback.addWidget(play_btn)

    timeline = QSlider(Qt.Orientation.Horizontal)
    timeline.setObjectName("PlaybackTimeline")
    timeline.setRange(0, 1000)
    timeline.setValue(0)
    timeline.setToolTip("Preview timeline")
    timeline.sliderMoved.connect(lambda value: window.preview.seek_fraction(value / 1000.0))
    playback.addWidget(timeline, 1)

    time_label = QLabel("0:00.0 / 0:00.0")
    time_label.setObjectName("PlaybackTime")
    playback.addWidget(time_label)
    preview_layout.addLayout(playback)

    meta_separator = _line(False)
    meta_separator.setObjectName("PreviewMetaSeparator")
    preview_layout.addWidget(meta_separator)

    window.dimensions_label.setParent(preview_card)
    window.dimensions_label.setObjectName("PreviewMeta")
    window.dimensions_label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
    preview_layout.addWidget(window.dimensions_label)

    def update_playback(index: int, total: int, current_s: float, total_s: float, playing: bool) -> None:
        play_btn.setText("❚❚" if playing else "▶")
        if total > 1 and not timeline.isSliderDown():
            timeline.blockSignals(True)
            timeline.setValue(round(index / (total - 1) * 1000))
            timeline.blockSignals(False)
        elif total <= 1 and not timeline.isSliderDown():
            timeline.setValue(0)
        time_label.setText(f"{_format_time(current_s)} / {_format_time(total_s)}")

    window.preview.playbackChanged.connect(update_playback)
    workspace_layout.addWidget(preview_card, 1)
    splitter.addWidget(workspace)
    splitter.setStretchFactor(0, 1)

    # RIGHT RAIL --------------------------------------------------------------
    rail = QWidget()
    rail.setObjectName("ControlRailContent")
    rail.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Expanding)
    rail_layout = QVBoxLayout(rail)
    registry.layout(rail_layout, (0, 0, 0, 0), 6)
    registry.width(rail, 404)

    # Output format.
    card, layout, _, icon = _card(registry, "OUTPUT FORMAT", symbol="∞", separator=True)
    format_grid = QGridLayout()
    registry.layout(format_grid, (0, 0, 0, 0), 2)
    window.gif_radio.setParent(card)
    window.mp4_radio.setParent(card)
    format_grid.addWidget(window.gif_radio, 0, 0)
    format_grid.addWidget(window.mp4_radio, 0, 1)
    gif_note = _subtext("Best for animations")
    mp4_note = _subtext("Smaller files, wider support")
    gif_note.setContentsMargins(19, 0, 0, 0)
    mp4_note.setContentsMargins(19, 0, 0, 0)
    format_grid.addWidget(gif_note, 1, 0)
    format_grid.addWidget(mp4_note, 1, 1)
    format_grid.setColumnStretch(0, 1)
    format_grid.setColumnStretch(1, 1)
    layout.addLayout(format_grid)
    rail_layout.addWidget(card)

    # Sizing.
    card, layout, _, resize_icon = _card(registry, "SIZING", "resize.png", separator=True)
    registry.callback(resize_icon.refresh)
    for spin in (window.max_mb, window.width_spin, window.height_spin):
        spin.setParent(card)
        spin.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)
        spin.setAlignment(Qt.AlignmentFlag.AlignCenter)
    window.size_radio.setParent(card)
    window.res_radio.setParent(card)
    window.max_mb.setSuffix("")
    registry.width(window.max_mb, 83)
    registry.width(window.width_spin, 78)
    registry.width(window.height_spin, 78)

    sizing_grid = QGridLayout()
    registry.layout(sizing_grid, (0, 0, 0, 0), 5)
    sizing_grid.addWidget(window.size_radio, 0, 0)
    sizing_grid.addWidget(window.max_mb, 0, 1)
    mb = QLabel("MB")
    mb.setObjectName("UnitLabel")
    sizing_grid.addWidget(mb, 0, 2)
    sizing_grid.addWidget(window.res_radio, 1, 0)
    sizing_grid.addWidget(window.width_spin, 1, 1)
    times = QLabel("×")
    times.setObjectName("TimesLabel")
    sizing_grid.addWidget(times, 1, 2, Qt.AlignmentFlag.AlignCenter)
    sizing_grid.addWidget(window.height_spin, 1, 3)
    sizing_grid.setColumnStretch(0, 1)
    layout.addLayout(sizing_grid)
    rail_layout.addWidget(card)

    # GIF priority.
    card, layout, _, priority_icon = _card(registry, "GIF PRIORITY", "priority.png", separator=True)
    registry.callback(priority_icon.refresh)
    window.motion_preserve_radio.setParent(card)
    window.motion_favor_radio.setParent(card)
    layout.addWidget(window.motion_preserve_radio)
    preserve_note = _subtext("Smoother animation, larger file size")
    preserve_note.setContentsMargins(19, 0, 0, 0)
    layout.addWidget(preserve_note)
    layout.addWidget(window.motion_favor_radio)
    favor_note = _subtext("Sharper detail, fewer frames")
    favor_note.setContentsMargins(19, 0, 0, 0)
    layout.addWidget(favor_note)
    rail_layout.addWidget(card)

    # Framing + aspect ratio.
    pair = QHBoxLayout()
    registry.layout(pair, (0, 0, 0, 0), 6)
    frame_card, frame_layout, _, crop_icon = _card(registry, "FRAMING", "crop.png", separator=True)
    registry.callback(crop_icon.refresh)
    aspect_card, aspect_layout, _, ratio_icon = _card(registry, "ASPECT RATIO", "aspect-ratio.png", separator=True)
    registry.callback(ratio_icon.refresh)

    window.frame_mode.setParent(frame_card)
    window.frame_mode.hide()
    frame_radios = QHBoxLayout()
    registry.layout(frame_radios, (0, 0, 0, 0), 6)
    original_radio = window._brand_original_radio = QRadioButton("Original")
    crop_radio = window._brand_crop_radio = QRadioButton("Crop")
    fit_radio = window._brand_fit_radio = QRadioButton("Fit")
    frame_group = window._brand_frame_group = QButtonGroup(window)
    for radio in (original_radio, crop_radio, fit_radio):
        frame_group.addButton(radio)
        frame_radios.addWidget(radio)
    frame_layout.addLayout(frame_radios)

    def set_frame_index(index: int) -> None:
        if window.frame_mode.currentIndex() != index:
            window.frame_mode.setCurrentIndex(index)

    original_radio.toggled.connect(lambda checked: checked and set_frame_index(0))
    crop_radio.toggled.connect(lambda checked: checked and set_frame_index(1))
    fit_radio.toggled.connect(lambda checked: checked and set_frame_index(2))

    def sync_frame_radios(*_args) -> None:
        idx = window.frame_mode.currentIndex()
        for radio, target in ((original_radio, 0), (crop_radio, 1), (fit_radio, 2)):
            radio.blockSignals(True)
            radio.setChecked(idx == target)
            radio.blockSignals(False)

    window.frame_mode.currentIndexChanged.connect(sync_frame_radios)
    sync_frame_radios()

    window.ratio_combo.setParent(aspect_card)
    guide_btn = QToolButton()
    guide_btn.setObjectName("InfoButton")
    guide_btn.setText("ⓘ")
    guide_btn.setToolTip("Open aspect ratio guide")
    guide_btn.clicked.connect(window._show_aspect_guide)
    registry.width(guide_btn, 25)
    aspect_row = QHBoxLayout()
    registry.layout(aspect_row, (0, 0, 0, 0), 4)
    aspect_row.addWidget(window.ratio_combo, 1)
    aspect_row.addWidget(guide_btn)
    aspect_layout.addLayout(aspect_row)

    # Keep background color/center engine widgets alive but intentionally hidden in branded v1.
    window.color_btn.setParent(root)
    window.color_btn.hide()
    window.center_btn.setParent(root)
    window.center_btn.hide()

    pair.addWidget(frame_card, 1)
    pair.addWidget(aspect_card, 1)
    rail_layout.addLayout(pair)

    # Crop zoom: intentionally no divider.
    zoom_card, zoom_layout, _, zoom_icon = _card(
        registry, "CROP ZOOM", "crop.png", separator=False
    )
    registry.callback(zoom_icon.refresh)
    window.crop_zoom_label.setParent(zoom_card)
    window.crop_zoom_label.hide()
    window.crop_zoom_slider.setParent(zoom_card)
    window.crop_zoom_slider.setObjectName("CropZoomSlider")
    zoom_value = QLabel(f"{window.crop_zoom_slider.value()}%")
    zoom_value.setObjectName("ZoomValue")
    window.crop_zoom_slider.valueChanged.connect(lambda value: zoom_value.setText(f"{value}%"))
    zoom_row = QHBoxLayout()
    registry.layout(zoom_row, (0, 0, 0, 0), 8)
    zoom_row.addWidget(window.crop_zoom_slider, 1)
    zoom_row.addWidget(zoom_value)
    zoom_layout.addLayout(zoom_row)
    rail_layout.addWidget(zoom_card)

    # Output folder: intentionally no divider.
    out_card, out_layout, _, folder_icon = _card(
        registry, "OUTPUT FOLDER", "folder.png", separator=False
    )
    registry.callback(folder_icon.refresh)
    window.output_path.setParent(out_card)
    window.output_path.setObjectName("PathText")
    output_row = QHBoxLayout()
    registry.layout(output_row, (0, 0, 0, 0), 6)
    output_row.addWidget(window.output_path, 1)
    browse_btn = QPushButton("Browse…")
    browse_btn.setObjectName("BrowseButton")
    browse_btn.setToolTip("Choose output folder")
    browse_btn.clicked.connect(window._choose_output_folder)
    registry.width(browse_btn, 67)
    output_row.addWidget(browse_btn)
    out_layout.addLayout(output_row)
    rail_layout.addWidget(out_card)

    # Replace the old action with a properly centered custom POLYMORPH button.
    old_convert = window.convert_btn
    old_convert.setParent(None)
    old_convert.deleteLater()
    window.convert_btn = PolymorphButton()
    window.convert_btn.setToolTip("Start converting the queued files with the selected settings.")
    window.convert_btn.clicked.connect(window._start_conversion)
    rail_layout.addWidget(window.convert_btn)
    rail_layout.addStretch(1)

    splitter.addWidget(rail)
    splitter.setStretchFactor(1, 0)
    splitter.setSizes([840, 404])
    outer.addWidget(splitter, 1)

    # STATUS + LINKS ----------------------------------------------------------
    footer_panel = TexturedFrame("status")
    footer_panel.setObjectName("StatusCard")
    footer_layout = QVBoxLayout(footer_panel)
    registry.layout(footer_layout, (11, 6, 11, 6), 5)

    top_row = QHBoxLayout()
    registry.layout(top_row, (0, 0, 0, 0), 7)

    # Simple ring indicator.
    ring = QLabel("◯")
    ring.setStyleSheet("color:#c72831; background:transparent; font-weight:700;")
    registry.width(ring, 24)
    top_row.addWidget(ring)

    status_box = QVBoxLayout()
    registry.layout(status_box, (0, 0, 0, 0), 0)
    window.status_label.setParent(footer_panel)
    window.status_label.setObjectName("StatusLabel")
    status_box.addWidget(window.status_label)
    status_box.addWidget(status_detail)
    top_row.addLayout(status_box, 1)

    # Suppress the old large placeholder until the actual loader pass.
    window.arcane_progress.setParent(footer_panel)
    window.arcane_progress.setFixedSize(0, 0)
    window.arcane_progress.hide()

    window.progress.setParent(footer_panel)
    window.progress.setObjectName("InlineProgress")
    window.progress.setTextVisible(False)
    window.progress.setVisible(False)
    registry.width(window.progress, 150)

    def sync_progress_visibility(value: int) -> None:
        active = 0 < value < 100
        window.progress.setVisible(active)
        if active:
            status_detail.setText("Polymorph is working. Your output is being prepared.")
        elif value >= 100:
            update_file_count()

    window.progress.valueChanged.connect(sync_progress_visibility)
    top_row.addWidget(window.progress)
    window.cancel_btn.setParent(footer_panel)
    top_row.addWidget(window.cancel_btn)
    top_row.addWidget(_line(True))

    update_button = QToolButton()
    update_button.setObjectName("FooterLink")
    update_button.setIcon(QIcon(tinted_icon_pixmap("update.png", 14, QColor("#c8c2b9"))))
    update_button.setIconSize(QSize(14, 14))
    update_button.setText("Check for Updates")
    update_button.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextBesideIcon)
    update_button.setToolTip("Check for updates")
    update_button.clicked.connect(window._manual_check_updates)

    links = [
        update_button,
        _footer_link(window, "github.svg", "GitHub", "View source on GitHub", lambda: window._open_url(REPO_URL)),
        _footer_link(window, "kofi.svg", "Ko-fi", "Support me on Ko-fi", lambda: window._open_url(KOFI_URL), bool(KOFI_URL)),
        _footer_link(window, "patreon.svg", "Patreon", "Support me on Patreon", lambda: window._open_url(PATREON_URL), bool(PATREON_URL)),
        _footer_link(window, "discord.svg", "Discord", "Join the Discord", lambda: window._open_url(DISCORD_URL), bool(DISCORD_URL)),
    ]
    for index, link in enumerate(links):
        if index:
            top_row.addWidget(_line(True))
        top_row.addWidget(link)
    footer_layout.addLayout(top_row)

    footer_sep = _line(False)
    footer_sep.setObjectName("FooterSeparator")
    footer_layout.addWidget(footer_sep)

    meta_row = QHBoxLayout()
    registry.layout(meta_row, (0, 0, 0, 0), 4)
    version = QLabel(f"Polymorph v{APP_VERSION}")
    version.setObjectName("FooterMeta")
    creator = QLabel("Polymorph 2026, Knight Witch™")
    creator.setObjectName("FooterMeta")
    meta_row.addWidget(version)
    meta_row.addStretch(1)
    meta_row.addWidget(creator)
    footer_layout.addLayout(meta_row)
    outer.addWidget(footer_panel)

    # Responsive bits that depend on current scale/content.
    def apply_runtime_scale(scale: float) -> None:
        splitter.setHandleWidth(max(3, round(5 * scale)))
        trash_btn.setIconSize(QSize(max(12, round(16 * scale)), max(12, round(16 * scale))))
        trash_btn.setIcon(QIcon(tinted_icon_pixmap("trash.png", max(12, round(16 * scale)), QColor("#aaa39a"))))
        update_button.setIconSize(QSize(max(11, round(14 * scale)), max(11, round(14 * scale))))
        update_button.setIcon(QIcon(tinted_icon_pixmap("update.png", max(11, round(14 * scale)), QColor("#c8c2b9"))))
        update_file_count()
        for row in queue_rows():
            row.apply_scale(scale)
            item = window.file_list.item(window.files.index(row.path)) if row.path in window.files else None
            if item is not None:
                item.setSizeHint(QSize(100, row.minimumHeight()))

    registry.callback(apply_runtime_scale)

    window.setCentralWidget(root)
    window.setProperty("polymorphLayout", "concept-match-v2")
    window._sync_enabled_state()
