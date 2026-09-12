from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QButtonGroup,
    QFrame,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QRadioButton,
    QScrollArea,
    QSplitter,
    QToolButton,
    QVBoxLayout,
    QWidget,
)

from ..constants import (
    APP_VERSION,
    DISCORD_URL,
    KOFI_URL,
    PATREON_URL,
    REPO_URL,
)


def _card(title: str, object_name: str = "ControlCard") -> tuple[QFrame, QVBoxLayout]:
    frame = QFrame()
    frame.setObjectName(object_name)
    layout = QVBoxLayout(frame)
    layout.setContentsMargins(14, 12, 14, 13)
    layout.setSpacing(9)

    heading = QLabel(title)
    heading.setObjectName("CardHeading")
    layout.addWidget(heading)
    return frame, layout


def _subtext(text: str) -> QLabel:
    label = QLabel(text)
    label.setObjectName("SecondaryText")
    label.setWordWrap(True)
    return label


def rebuild_brand_layout(window) -> None:
    """Re-compose the validated controls into the branded two-column UI.

    This function intentionally reuses the existing functional widgets instead
    of replacing conversion/framing controls with look-alike copies. All engine
    wiring stays on the already-tested MainWindow objects.
    """
    root = QWidget()
    root.setObjectName("AppRoot")
    outer = QVBoxLayout(root)
    outer.setContentsMargins(20, 16, 20, 10)
    outer.setSpacing(12)

    # Header -----------------------------------------------------------------
    header = QHBoxLayout()
    header.setSpacing(12)

    brand = QVBoxLayout()
    brand.setSpacing(1)

    title_row = QHBoxLayout()
    title_row.setSpacing(10)
    title = QLabel("POLYMORPH")
    title.setObjectName("BrandTitle")
    version = QLabel(f"v{APP_VERSION}")
    version.setObjectName("HeaderVersion")
    title_row.addWidget(title)
    title_row.addWidget(version, 0, Qt.AlignBottom)
    title_row.addStretch(1)

    subtitle = QLabel("MEDIA CONVERSION MAGIC — BY KNIGHT WITCH™")
    subtitle.setObjectName("BrandSubtitle")

    brand.addLayout(title_row)
    brand.addWidget(subtitle)
    header.addLayout(brand, 1)
    outer.addLayout(header)

    # Main split --------------------------------------------------------------
    splitter = QSplitter(Qt.Horizontal)
    splitter.setObjectName("BrandMainSplitter")
    splitter.setChildrenCollapsible(False)
    splitter.setHandleWidth(6)

    workspace = QWidget()
    workspace.setObjectName("Workspace")
    workspace_layout = QVBoxLayout(workspace)
    workspace_layout.setContentsMargins(0, 0, 0, 0)
    workspace_layout.setSpacing(10)

    # File queue card.
    files_card, files_layout = _card("FILES", "FileCard")
    files_header = QHBoxLayout()
    files_header.setSpacing(7)
    files_count = QLabel()
    files_count.setObjectName("FileCount")
    files_header.addWidget(files_count)
    files_header.addStretch(1)

    add_btn = QPushButton("+ Add Files")
    add_btn.setObjectName("HeaderAction")
    add_btn.setToolTip("Add one or more animated WebP files to the conversion queue.")
    add_btn.clicked.connect(window._choose_files)

    remove_btn = QPushButton("Remove")
    remove_btn.setObjectName("QuietAction")
    remove_btn.setToolTip("Remove the selected item from the queue. The source file is not deleted.")
    remove_btn.clicked.connect(window._remove_selected)

    clear_btn = QPushButton("Clear")
    clear_btn.setObjectName("QuietAction")
    clear_btn.setToolTip("Remove every item from the queue. Source files are not deleted.")

    def clear_queue() -> None:
        window.file_list.clear()
        window.files.clear()
        window.media_cache.clear()
        window.preview.set_source(None)
        window.dimensions_label.setText("No file selected")
        window._sync_enabled_state()

    clear_btn.clicked.connect(clear_queue)

    files_header.addWidget(add_btn)
    files_header.addWidget(remove_btn)
    files_header.addWidget(clear_btn)
    files_layout.addLayout(files_header)

    window.file_list.setParent(files_card)
    window.file_list.setMinimumHeight(76)
    window.file_list.setMaximumHeight(132)
    files_layout.addWidget(window.file_list)

    def update_file_count(*_args) -> None:
        count = window.file_list.count()
        files_count.setText(f"{count} file" if count == 1 else f"{count} files")

    model = window.file_list.model()
    model.rowsInserted.connect(update_file_count)
    model.rowsRemoved.connect(update_file_count)
    model.modelReset.connect(update_file_count)
    update_file_count()
    workspace_layout.addWidget(files_card)

    # Preview card.
    preview_card, preview_layout = _card("PREVIEW", "PreviewCard")
    window.preview.setParent(preview_card)
    window.preview.setMinimumHeight(360)
    preview_layout.addWidget(window.preview, 1)

    window.dimensions_label.setParent(preview_card)
    window.dimensions_label.setObjectName("PreviewMeta")
    preview_layout.addWidget(window.dimensions_label)
    workspace_layout.addWidget(preview_card, 1)

    splitter.addWidget(workspace)
    splitter.setStretchFactor(0, 1)

    # Right rail --------------------------------------------------------------
    rail_scroll = QScrollArea()
    rail_scroll.setObjectName("ControlRail")
    rail_scroll.setWidgetResizable(True)
    rail_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
    rail_scroll.setFrameShape(QFrame.NoFrame)
    rail_scroll.setMinimumWidth(350)
    rail_scroll.setMaximumWidth(430)

    rail = QWidget()
    rail.setObjectName("ControlRailContent")
    rail_layout = QVBoxLayout(rail)
    rail_layout.setContentsMargins(3, 0, 3, 0)
    rail_layout.setSpacing(9)

    # OUTPUT FORMAT
    card, layout = _card("OUTPUT FORMAT")
    format_row = QHBoxLayout()
    format_row.setSpacing(18)
    window.gif_radio.setParent(card)
    window.mp4_radio.setParent(card)
    format_row.addWidget(window.gif_radio)
    format_row.addWidget(window.mp4_radio)
    format_row.addStretch(1)
    layout.addLayout(format_row)
    layout.addWidget(_subtext("GIF for looping animation; MP4 for smaller broadly compatible video."))
    rail_layout.addWidget(card)

    # SIZING
    card, layout = _card("SIZING")
    size_row = QHBoxLayout()
    size_row.setSpacing(9)
    window.size_radio.setParent(card)
    window.max_mb.setParent(card)
    window.max_mb.setMinimumWidth(112)
    size_row.addWidget(window.size_radio, 1)
    size_row.addWidget(window.max_mb)
    layout.addLayout(size_row)

    resolution_row = QHBoxLayout()
    resolution_row.setSpacing(7)
    window.res_radio.setParent(card)
    window.width_spin.setParent(card)
    window.height_spin.setParent(card)
    resolution_row.addWidget(window.res_radio, 1)
    resolution_row.addWidget(window.width_spin)
    times = QLabel("×")
    times.setObjectName("TimesLabel")
    resolution_row.addWidget(times)
    resolution_row.addWidget(window.height_spin)
    layout.addLayout(resolution_row)
    rail_layout.addWidget(card)

    # GIF PRIORITY
    card, layout = _card("GIF PRIORITY")
    window.motion_preserve_radio.setParent(card)
    window.motion_favor_radio.setParent(card)
    layout.addWidget(window.motion_preserve_radio)
    preserve_note = _subtext("Keeps every source frame for the smoothest motion.")
    preserve_note.setContentsMargins(23, 0, 0, 0)
    layout.addWidget(preserve_note)
    layout.addWidget(window.motion_favor_radio)
    favor_note = _subtext("Uses measured frame savings only when they buy a meaningfully larger GIF.")
    favor_note.setContentsMargins(23, 0, 0, 0)
    layout.addWidget(favor_note)
    rail_layout.addWidget(card)

    # FRAMING — expose the existing combo as real radio choices.
    card, layout = _card("FRAMING")
    window.frame_mode.setParent(card)
    window.frame_mode.hide()

    frame_radios = QHBoxLayout()
    frame_radios.setSpacing(12)
    original_radio = window._brand_original_radio = QRadioButton("Original")
    crop_radio = window._brand_crop_radio = QRadioButton("Crop")
    fit_radio = window._brand_fit_radio = QRadioButton("Fit")
    frame_group = window._brand_frame_group = QButtonGroup(window)
    for radio in (original_radio, crop_radio, fit_radio):
        frame_group.addButton(radio)
        frame_radios.addWidget(radio)
    frame_radios.addStretch(1)
    layout.addLayout(frame_radios)

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
    rail_layout.addWidget(card)

    # ASPECT RATIO / CROP ADJUSTMENTS
    card, layout = _card("ASPECT RATIO")
    ratio_row = QHBoxLayout()
    ratio_row.setSpacing(7)
    window.ratio_combo.setParent(card)
    ratio_row.addWidget(window.ratio_combo, 1)

    guide_btn = QToolButton()
    guide_btn.setText("ⓘ")
    guide_btn.setObjectName("InfoButton")
    guide_btn.setToolTip("Open aspect ratio guide")
    guide_btn.clicked.connect(window._show_aspect_guide)
    ratio_row.addWidget(guide_btn)
    layout.addLayout(ratio_row)

    window.crop_zoom_label.setParent(card)
    window.crop_zoom_slider.setParent(card)
    zoom_row = QHBoxLayout()
    zoom_row.setSpacing(8)
    zoom_row.addWidget(window.crop_zoom_label)
    zoom_row.addWidget(window.crop_zoom_slider, 1)
    layout.addLayout(zoom_row)

    window.center_btn.setParent(card)
    window.color_btn.setParent(card)
    action_row = QHBoxLayout()
    action_row.setSpacing(7)
    action_row.addWidget(window.center_btn)
    action_row.addWidget(window.color_btn)
    layout.addLayout(action_row)
    rail_layout.addWidget(card)

    # OUTPUT FOLDER
    card, layout = _card("OUTPUT FOLDER")
    output_row = QHBoxLayout()
    output_row.setSpacing(7)
    window.output_path.setParent(card)
    window.output_path.setObjectName("PathText")
    output_row.addWidget(window.output_path, 1)

    browse_btn = QToolButton()
    browse_btn.setText("…")
    browse_btn.setObjectName("BrowseButton")
    browse_btn.setToolTip("Choose output folder")
    browse_btn.clicked.connect(window._choose_output_folder)
    output_row.addWidget(browse_btn)
    layout.addLayout(output_row)
    rail_layout.addWidget(card)

    rail_layout.addStretch(1)

    window.convert_btn.setParent(rail)
    window.convert_btn.setText("Cast Polymorph")
    window.convert_btn.setAccessibleName("Cast Polymorph")
    rail_layout.addWidget(window.convert_btn)

    rail_scroll.setWidget(rail)
    splitter.addWidget(rail_scroll)
    splitter.setStretchFactor(1, 0)
    splitter.setSizes([840, 390])
    outer.addWidget(splitter, 1)

    # Status/progress strip ---------------------------------------------------
    status_card = QFrame()
    status_card.setObjectName("StatusCard")
    status_layout = QHBoxLayout(status_card)
    status_layout.setContentsMargins(12, 8, 12, 8)
    status_layout.setSpacing(10)

    window.arcane_progress.setParent(status_card)
    status_layout.addWidget(window.arcane_progress)

    status_box = QVBoxLayout()
    status_box.setSpacing(4)
    window.status_label.setParent(status_card)
    window.status_label.setObjectName("StatusLabel")
    window.progress.setParent(status_card)
    window.progress.setTextVisible(False)
    status_box.addWidget(window.status_label)
    status_box.addWidget(window.progress)
    status_layout.addLayout(status_box, 1)

    window.cancel_btn.setParent(status_card)
    status_layout.addWidget(window.cancel_btn)
    outer.addWidget(status_card)

    # Footer -----------------------------------------------------------------
    footer = QHBoxLayout()
    footer.setSpacing(4)

    footer_version = QLabel(f"Polymorph v{APP_VERSION}")
    footer_version.setObjectName("FooterVersion")
    footer.addWidget(footer_version)
    footer.addStretch(1)

    footer.addWidget(window._footer_button("update.svg", "Check for updates", window._manual_check_updates))
    footer.addWidget(window._footer_button("github.svg", "View source on GitHub", lambda: window._open_url(REPO_URL)))
    footer.addWidget(window._footer_button("kofi.svg", "Support me on Ko-fi", lambda: window._open_url(KOFI_URL), bool(KOFI_URL)))
    footer.addWidget(window._footer_button("patreon.svg", "Support me on Patreon", lambda: window._open_url(PATREON_URL), bool(PATREON_URL)))
    footer.addWidget(window._footer_button("discord.svg", "Join the Discord", lambda: window._open_url(DISCORD_URL), bool(DISCORD_URL)))
    outer.addLayout(footer)

    # Make sure live logic continues to own all functional widgets before the
    # obsolete three-column root is released.
    window.setCentralWidget(root)
    window.setProperty("polymorphLayout", "two-column-v1")
