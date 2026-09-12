from __future__ import annotations

import sys
from pathlib import Path

from PySide6.QtCore import QDir, QProcess, QSize, Qt, QUrl
from PySide6.QtGui import (
    QColor,
    QDesktopServices,
    QFont,
    QIcon,
    QImageReader,
    QPainter,
    QPen,
    QPixmap,
)
from PySide6.QtWidgets import (
    QAbstractItemView,
    QAbstractSpinBox,
    QButtonGroup,
    QFrame,
    QHBoxLayout,
    QLabel,
    QListWidgetItem,
    QMenu,
    QPushButton,
    QRadioButton,
    QScrollArea,
    QSizePolicy,
    QSplitter,
    QStyle,
    QToolButton,
    QVBoxLayout,
    QWidget,
)

from ..constants import APP_VERSION, DISCORD_URL, KOFI_URL, PATREON_URL, REPO_URL
from ..resources import asset_path


class CardIcon(QWidget):
    """Small line icon used in branded card headers."""

    def __init__(self, kind: str, parent=None) -> None:
        super().__init__(parent)
        self.kind = kind
        self.setFixedSize(18, 18)

    def paintEvent(self, _event) -> None:
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing, True)
        pen = QPen(QColor("#d0ad6d"), 1.35, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin)
        painter.setPen(pen)
        painter.setBrush(Qt.NoBrush)
        r = self.rect().adjusted(2, 2, -2, -2)
        cx = r.center().x()
        cy = r.center().y()

        if self.kind == "output":
            painter.drawEllipse(r.left(), cy - 4, 7, 8)
            painter.drawEllipse(r.right() - 7, cy - 4, 7, 8)
            painter.drawLine(cx - 2, cy - 3, cx + 2, cy + 3)
            painter.drawLine(cx - 2, cy + 3, cx + 2, cy - 3)
        elif self.kind == "sizing":
            painter.drawLine(r.left(), r.top() + 4, r.left(), r.top())
            painter.drawLine(r.left(), r.top(), r.left() + 4, r.top())
            painter.drawLine(r.right() - 4, r.top(), r.right(), r.top())
            painter.drawLine(r.right(), r.top(), r.right(), r.top() + 4)
            painter.drawLine(r.left(), r.bottom() - 4, r.left(), r.bottom())
            painter.drawLine(r.left(), r.bottom(), r.left() + 4, r.bottom())
            painter.drawLine(r.right() - 4, r.bottom(), r.right(), r.bottom())
            painter.drawLine(r.right(), r.bottom(), r.right(), r.bottom() - 4)
        elif self.kind == "priority":
            p1 = r.topLeft() + self._pt(6, 1)
            p2 = r.topLeft() + self._pt(12, 4)
            p3 = r.topLeft() + self._pt(6, 7)
            p4 = r.topLeft() + self._pt(0, 4)
            painter.drawLine(p1, p2)
            painter.drawLine(p2, p3)
            painter.drawLine(p3, p4)
            painter.drawLine(p4, p1)
            painter.drawLine(r.left(), cy + 1, cx, r.bottom() - 1)
            painter.drawLine(cx, r.bottom() - 1, r.right(), cy + 1)
        elif self.kind == "framing":
            painter.drawLine(r.left(), r.top() + 3, r.left(), r.bottom() - 2)
            painter.drawLine(r.left(), r.top() + 3, r.right() - 2, r.top() + 3)
            painter.drawLine(r.right() - 3, r.top() + 1, r.right() - 3, r.bottom())
            painter.drawLine(r.left() + 2, r.bottom() - 3, r.right() - 3, r.bottom() - 3)
        elif self.kind == "ratio":
            painter.drawRoundedRect(r.adjusted(0, 2, 0, -2), 2, 2)
            painter.drawLine(cx, r.top() + 4, cx, r.bottom() - 4)
        elif self.kind == "zoom":
            painter.drawEllipse(r.left() + 1, r.top() + 1, 9, 9)
            painter.drawLine(r.left() + 9, r.top() + 9, r.right(), r.bottom())
        elif self.kind == "folder":
            path_top = r.top() + 4
            painter.drawLine(r.left(), path_top + 2, r.left() + 3, path_top + 2)
            painter.drawLine(r.left() + 3, path_top + 2, r.left() + 5, r.top() + 2)
            painter.drawLine(r.left() + 5, r.top() + 2, r.left() + 9, r.top() + 2)
            painter.drawLine(r.left() + 9, r.top() + 2, r.left() + 11, path_top + 2)
            painter.drawRoundedRect(r.adjusted(0, 6, 0, -1), 2, 2)
        elif self.kind == "files":
            painter.drawRoundedRect(r.adjusted(1, 0, -3, -2), 1.5, 1.5)
            painter.drawRoundedRect(r.adjusted(3, 3, -1, 0), 1.5, 1.5)
        else:
            painter.drawEllipse(r)

    @staticmethod
    def _pt(x: int, y: int):
        from PySide6.QtCore import QPoint
        return QPoint(x, y)


class BrandSigil(QWidget):
    """Small static header/status sigil. The real loader remains a later feature."""

    def __init__(self, size: int = 38, parent=None) -> None:
        super().__init__(parent)
        self.setFixedSize(size, size)

    def paintEvent(self, _event) -> None:
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing, True)
        rect = self.rect().adjusted(3, 3, -3, -3)
        painter.setPen(QPen(QColor("#b99658"), 1.2))
        painter.drawEllipse(rect)
        inner = rect.adjusted(6, 6, -6, -6)
        painter.setPen(QPen(QColor("#d3b574"), 1.15))
        painter.drawEllipse(inner)
        a = inner.topLeft() + CardIcon._pt(inner.width() // 2, 1)
        b = inner.bottomLeft() + CardIcon._pt(2, -2)
        c = inner.bottomRight() + CardIcon._pt(-2, -2)
        painter.drawLine(a, b)
        painter.drawLine(b, c)
        painter.drawLine(c, a)


class ReadyRing(QWidget):
    """Compact idle/working status glyph for the bottom status strip."""

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setFixedSize(32, 32)

    def paintEvent(self, _event) -> None:
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing, True)
        r = self.rect().adjusted(5, 5, -5, -5)
        painter.setPen(QPen(QColor(255, 255, 255, 28), 3.0))
        painter.drawArc(r, 0, 360 * 16)
        painter.setPen(QPen(QColor("#ba2029"), 3.0, Qt.SolidLine, Qt.RoundCap))
        painter.drawArc(r, 35 * 16, 285 * 16)


class QueueRow(QFrame):
    def __init__(self, window, path: Path, select_callback, parent=None) -> None:
        super().__init__(parent)
        self.window = window
        self.path = path
        self._select_callback = select_callback
        self.setObjectName("QueueRow")
        self.setCursor(Qt.PointingHandCursor)

        row = QHBoxLayout(self)
        row.setContentsMargins(7, 5, 7, 5)
        row.setSpacing(9)

        self.thumb = QLabel()
        self.thumb.setObjectName("QueueThumb")
        self.thumb.setAlignment(Qt.AlignCenter)
        self.thumb.setFixedSize(78, 46)
        self._load_thumbnail()
        row.addWidget(self.thumb)

        text_box = QVBoxLayout()
        text_box.setSpacing(1)
        name = QLabel(path.name)
        name.setObjectName("QueueFileName")
        name.setToolTip(str(path))
        meta = QLabel(self._metadata_text())
        meta.setObjectName("QueueMeta")
        text_box.addWidget(name)
        text_box.addWidget(meta)
        row.addLayout(text_box, 1)

        menu_btn = QToolButton()
        menu_btn.setObjectName("QueueMenuButton")
        menu_btn.setText("⋯")
        menu_btn.setToolTip("File actions")
        menu_btn.clicked.connect(self._show_menu)
        row.addWidget(menu_btn)

    def set_selected(self, selected: bool) -> None:
        self.setProperty("selected", selected)
        self.style().unpolish(self)
        self.style().polish(self)
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
            Qt.KeepAspectRatioByExpanding,
            Qt.SmoothTransformation,
        )
        x = max(0, (pixmap.width() - self.thumb.width()) // 2)
        y = max(0, (pixmap.height() - self.thumb.height()) // 2)
        self.thumb.setPixmap(pixmap.copy(x, y, self.thumb.width(), self.thumb.height()))

    def _metadata_text(self) -> str:
        try:
            size = self.path.stat().st_size
            if size >= 1_000_000:
                size_text = f"{size / 1_000_000:.1f} MB"
            else:
                size_text = f"{size / 1000:.0f} KB"
        except OSError:
            size_text = "Unknown size"

        try:
            info = self.window.media_cache.get(self.path)
            if info is None and self.window.converter is not None:
                info = self.window.converter.probe(self.path)
                self.window.media_cache[self.path] = info
            if info is not None:
                duration = f"{info.duration_s:.1f}s"
                return f"{size_text}   |   {info.width} × {info.height}   |   {duration}"
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


def _card(
    title: str,
    icon_kind: str,
    object_name: str = "ControlCard",
) -> tuple[QFrame, QVBoxLayout, QHBoxLayout]:
    frame = QFrame()
    frame.setObjectName(object_name)
    layout = QVBoxLayout(frame)
    layout.setContentsMargins(11, 8, 11, 9)
    layout.setSpacing(6)

    header = QHBoxLayout()
    header.setContentsMargins(0, 0, 0, 0)
    header.setSpacing(7)
    header.addWidget(CardIcon(icon_kind))

    heading = QLabel(title)
    heading.setObjectName("CardHeading")
    header.addWidget(heading)
    header.addStretch(1)
    layout.addLayout(header)

    separator = QFrame()
    separator.setObjectName("CardSeparator")
    separator.setFrameShape(QFrame.HLine)
    layout.addWidget(separator)
    return frame, layout, header


def _subtext(text: str) -> QLabel:
    label = QLabel(text)
    label.setObjectName("SecondaryText")
    label.setWordWrap(True)
    return label


def _vertical_separator() -> QFrame:
    line = QFrame()
    line.setObjectName("VerticalSeparator")
    line.setFrameShape(QFrame.VLine)
    line.setFixedHeight(22)
    return line


def _make_cast_icon() -> QIcon:
    pixmap = QPixmap(52, 52)
    pixmap.fill(Qt.transparent)
    painter = QPainter(pixmap)
    painter.setRenderHint(QPainter.Antialiasing, True)
    painter.setPen(QPen(QColor("#d3b574"), 1.5))
    painter.drawEllipse(5, 5, 42, 42)
    painter.drawEllipse(10, 10, 32, 32)
    painter.drawLine(26, 13, 15, 36)
    painter.drawLine(15, 36, 38, 36)
    painter.drawLine(38, 36, 26, 13)
    painter.end()
    return QIcon(pixmap)


def _footer_link(window, icon_name: str, text: str, tooltip: str, slot, enabled: bool = True):
    button = QToolButton()
    button.setObjectName("FooterLink")
    button.setIcon(QIcon(str(asset_path(icon_name))))
    button.setIconSize(QSize(14, 14))
    button.setText(text)
    button.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
    button.setToolTip(tooltip)
    button.setEnabled(enabled)
    button.clicked.connect(slot)
    return button


def rebuild_brand_layout(window) -> None:
    """Re-compose validated controls to closely match the approved concept mockup."""
    root = QWidget()
    root.setObjectName("AppRoot")
    outer = QVBoxLayout(root)
    outer.setContentsMargins(16, 13, 16, 8)
    outer.setSpacing(8)

    # Header -----------------------------------------------------------------
    header = QHBoxLayout()
    header.setContentsMargins(0, 0, 0, 0)
    header.setSpacing(10)
    header.addWidget(BrandSigil(42), 0, Qt.AlignTop)

    brand = QVBoxLayout()
    brand.setSpacing(0)

    title_row = QHBoxLayout()
    title_row.setSpacing(9)
    title = QLabel("POLYMORPH")
    title.setObjectName("BrandTitle")
    title_font = QFont("Cinzel")
    title_font.setPointSizeF(25.0)
    title_font.setWeight(QFont.Weight.DemiBold)
    title_font.setLetterSpacing(QFont.AbsoluteSpacing, 3.2)
    title.setFont(title_font)

    version = QLabel(f"v{APP_VERSION}")
    version.setObjectName("HeaderVersion")
    title_row.addWidget(title)
    title_row.addWidget(version, 0, Qt.AlignBottom)
    title_row.addStretch(1)

    subtitle = QLabel("MEDIA CONVERSION MAGIC — BY KNIGHT WITCH™")
    subtitle.setObjectName("BrandSubtitle")
    subtitle_font = QFont("Inter")
    subtitle_font.setPointSizeF(8.7)
    subtitle_font.setWeight(QFont.Weight.DemiBold)
    subtitle_font.setLetterSpacing(QFont.AbsoluteSpacing, 1.8)
    subtitle.setFont(subtitle_font)

    brand.addLayout(title_row)
    brand.addWidget(subtitle)
    header.addLayout(brand, 1)
    outer.addLayout(header)

    # Main split --------------------------------------------------------------
    splitter = QSplitter(Qt.Horizontal)
    splitter.setObjectName("BrandMainSplitter")
    splitter.setChildrenCollapsible(False)
    splitter.setHandleWidth(5)

    workspace = QWidget()
    workspace.setObjectName("Workspace")
    workspace_layout = QVBoxLayout(workspace)
    workspace_layout.setContentsMargins(0, 0, 0, 0)
    workspace_layout.setSpacing(8)

    # FILES panel: count/actions share the title row like the concept.
    files_card, files_layout, files_header = _card("FILES", "files", "FileCard")
    files_count = QLabel()
    files_count.setObjectName("FileCount")
    files_header.insertWidget(files_header.count() - 1, files_count)

    add_btn = QPushButton("+ Add Files")
    add_btn.setObjectName("HeaderAction")
    add_btn.setToolTip("Add one or more animated WebP files to the conversion queue.")
    add_btn.clicked.connect(window._choose_files)

    trash_btn = QToolButton()
    trash_btn.setObjectName("HeaderTrash")
    trash_btn.setIcon(window.style().standardIcon(QStyle.StandardPixmap.SP_TrashIcon))
    trash_btn.setIconSize(QSize(14, 14))
    trash_btn.setToolTip("Remove selected file from the queue.")
    trash_btn.clicked.connect(window._remove_selected)

    clear_btn = QPushButton("Clear All")
    clear_btn.setObjectName("ClearAllLink")
    clear_btn.setToolTip("Remove every item from the queue. Source files are not deleted.")

    def clear_queue() -> None:
        window.file_list.clear()
        window.files.clear()
        window.media_cache.clear()
        window.preview.set_source(None)
        window.dimensions_label.setText("No file selected")
        window._sync_enabled_state()

    clear_btn.clicked.connect(clear_queue)

    insert_at = files_header.count() - 1
    files_header.insertWidget(insert_at, add_btn)
    insert_at += 1
    files_header.insertWidget(insert_at, trash_btn)
    insert_at += 1
    files_header.insertWidget(insert_at, _vertical_separator())
    insert_at += 1
    files_header.insertWidget(insert_at, clear_btn)

    window.file_list.setParent(files_card)
    window.file_list.setObjectName("QueueList")
    window.file_list.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
    window.file_list.setVerticalScrollMode(QAbstractItemView.ScrollMode.ScrollPerPixel)
    window.file_list.setSpacing(3)
    files_layout.addWidget(window.file_list)

    status_detail = QLabel()
    status_detail.setObjectName("StatusDetail")
    window._brand_status_detail = status_detail

    def decorate_queue_rows(*_args) -> None:
        for row in range(window.file_list.count()):
            item = window.file_list.item(row)
            if window.file_list.itemWidget(item) is not None:
                continue
            if row >= len(window.files):
                continue
            path = window.files[row]
            widget = QueueRow(
                window,
                path,
                select_callback=lambda p=path: window.file_list.setCurrentRow(
                    window.files.index(p) if p in window.files else -1
                ),
            )
            item.setSizeHint(QSize(100, 58))
            window.file_list.setItemWidget(item, widget)
        update_selection()

    def update_selection(*_args) -> None:
        current = window.file_list.currentRow()
        for row in range(window.file_list.count()):
            item = window.file_list.item(row)
            widget = window.file_list.itemWidget(item)
            if isinstance(widget, QueueRow):
                widget.set_selected(row == current)
        trash_btn.setEnabled(current >= 0)

    def update_file_count(*_args) -> None:
        count = window.file_list.count()
        files_count.setText(f"{count} file" if count == 1 else f"{count} files")
        # Two media rows are visible without bloating the whole workspace.
        target_height = max(68, min(132, count * 61 + 8))
        window.file_list.setFixedHeight(target_height)
        if count == 0:
            status_detail.setText("No files imported. Add media to begin.")
        elif count == 1:
            status_detail.setText("1 file imported. Choose your settings and begin.")
        else:
            status_detail.setText(f"{count} files imported. Choose your settings and begin.")
        if window.worker is None or not window.worker.isRunning():
            window.status_label.setText("Ready")

    model = window.file_list.model()
    model.rowsInserted.connect(decorate_queue_rows)
    model.rowsInserted.connect(update_file_count)
    model.rowsRemoved.connect(update_file_count)
    model.modelReset.connect(update_file_count)
    window.file_list.currentRowChanged.connect(update_selection)
    decorate_queue_rows()
    update_file_count()
    workspace_layout.addWidget(files_card)

    # PREVIEW panel.
    preview_card, preview_layout, _ = _card("PREVIEW", "framing", "PreviewCard")
    window.preview.setParent(preview_card)
    window.preview.setMinimumHeight(360)
    preview_layout.addWidget(window.preview, 1)

    window.dimensions_label.setParent(preview_card)
    window.dimensions_label.setObjectName("PreviewMeta")
    preview_layout.addWidget(window.dimensions_label)
    workspace_layout.addWidget(preview_card, 1)

    splitter.addWidget(workspace)
    splitter.setStretchFactor(0, 1)

    # Right settings rail -----------------------------------------------------
    rail_scroll = QScrollArea()
    rail_scroll.setObjectName("ControlRail")
    rail_scroll.setWidgetResizable(True)
    rail_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
    rail_scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
    rail_scroll.setFrameShape(QFrame.NoFrame)
    rail_scroll.setFixedWidth(410)
    rail_scroll.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)

    rail = QWidget()
    rail.setObjectName("ControlRailContent")
    rail.setMinimumWidth(0)
    rail_layout = QVBoxLayout(rail)
    rail_layout.setContentsMargins(2, 0, 2, 0)
    rail_layout.setSpacing(7)

    # OUTPUT FORMAT
    card, layout, _ = _card("OUTPUT FORMAT", "output")
    format_row = QHBoxLayout()
    format_row.setSpacing(18)

    gif_col = QVBoxLayout()
    gif_col.setSpacing(0)
    window.gif_radio.setParent(card)
    gif_col.addWidget(window.gif_radio)
    gif_note = _subtext("Best for animations")
    gif_note.setContentsMargins(23, 0, 0, 0)
    gif_col.addWidget(gif_note)

    mp4_col = QVBoxLayout()
    mp4_col.setSpacing(0)
    window.mp4_radio.setParent(card)
    mp4_col.addWidget(window.mp4_radio)
    mp4_note = _subtext("Smaller files, wider support")
    mp4_note.setContentsMargins(23, 0, 0, 0)
    mp4_col.addWidget(mp4_note)

    format_row.addLayout(gif_col, 1)
    format_row.addLayout(mp4_col, 1)
    layout.addLayout(format_row)
    rail_layout.addWidget(card)

    # SIZING
    card, layout, _ = _card("SIZING", "sizing")
    window.size_radio.setParent(card)
    window.res_radio.setParent(card)
    window.max_mb.setParent(card)
    window.width_spin.setParent(card)
    window.height_spin.setParent(card)

    for spin in (window.max_mb, window.width_spin, window.height_spin):
        spin.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)
        spin.setAlignment(Qt.AlignCenter)
    window.max_mb.setSuffix("")
    window.max_mb.setFixedWidth(84)
    window.width_spin.setFixedWidth(78)
    window.height_spin.setFixedWidth(78)

    size_row = QHBoxLayout()
    size_row.setSpacing(8)
    size_row.addWidget(window.size_radio, 1)
    size_row.addWidget(window.max_mb)
    mb = QLabel("MB")
    mb.setObjectName("UnitLabel")
    size_row.addWidget(mb)
    layout.addLayout(size_row)

    resolution_row = QHBoxLayout()
    resolution_row.setSpacing(7)
    resolution_row.addWidget(window.res_radio, 1)
    resolution_row.addWidget(window.width_spin)
    times = QLabel("×")
    times.setObjectName("TimesLabel")
    resolution_row.addWidget(times)
    resolution_row.addWidget(window.height_spin)
    layout.addLayout(resolution_row)
    rail_layout.addWidget(card)

    # GIF PRIORITY
    card, layout, _ = _card("GIF PRIORITY", "priority")
    window.motion_preserve_radio.setParent(card)
    window.motion_favor_radio.setParent(card)

    preserve_row = QVBoxLayout()
    preserve_row.setSpacing(0)
    preserve_row.addWidget(window.motion_preserve_radio)
    preserve_note = _subtext("Smoother animation, larger file size")
    preserve_note.setContentsMargins(23, 0, 0, 0)
    preserve_row.addWidget(preserve_note)
    layout.addLayout(preserve_row)

    favor_row = QVBoxLayout()
    favor_row.setSpacing(0)
    favor_row.addWidget(window.motion_favor_radio)
    favor_note = _subtext("Sharper detail, fewer frames")
    favor_note.setContentsMargins(23, 0, 0, 0)
    favor_row.addWidget(favor_note)
    layout.addLayout(favor_row)
    rail_layout.addWidget(card)

    # FRAMING + ASPECT RATIO share a row like the concept.
    pair = QHBoxLayout()
    pair.setSpacing(6)

    frame_card, frame_layout, _ = _card("FRAMING", "framing")
    window.frame_mode.setParent(frame_card)
    window.frame_mode.hide()

    frame_radios = QHBoxLayout()
    frame_radios.setSpacing(8)
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

    aspect_card, aspect_layout, _ = _card("ASPECT RATIO", "ratio")
    window.ratio_combo.setParent(aspect_card)
    guide_btn = QToolButton()
    guide_btn.setText("ⓘ")
    guide_btn.setObjectName("InfoButton")
    guide_btn.setToolTip("Open aspect ratio guide")
    guide_btn.clicked.connect(window._show_aspect_guide)
    aspect_row = QHBoxLayout()
    aspect_row.setSpacing(5)
    aspect_row.addWidget(window.ratio_combo, 1)
    aspect_row.addWidget(guide_btn)
    aspect_layout.addLayout(aspect_row)

    # Keep Fit background as an unobtrusive Fit-only utility rather than a
    # dedicated mockup card.
    window.color_btn.setParent(frame_card)
    window.color_btn.setObjectName("FitColorButton")
    window.color_btn.setText("Fill")
    window.color_btn.setMaximumWidth(44)
    frame_layout.addWidget(window.color_btn, 0, Qt.AlignRight)

    def sync_frame_radios(*_args) -> None:
        idx = window.frame_mode.currentIndex()
        for radio, target in ((original_radio, 0), (crop_radio, 1), (fit_radio, 2)):
            radio.blockSignals(True)
            radio.setChecked(idx == target)
            radio.blockSignals(False)
        window.color_btn.setVisible(idx == 2)

    window.frame_mode.currentIndexChanged.connect(sync_frame_radios)
    sync_frame_radios()

    pair.addWidget(frame_card, 1)
    pair.addWidget(aspect_card, 1)
    rail_layout.addLayout(pair)

    # CROP ZOOM
    zoom_card, zoom_layout, _ = _card("CROP ZOOM", "zoom")
    window.crop_zoom_label.setParent(zoom_card)
    window.crop_zoom_label.hide()
    window.crop_zoom_slider.setParent(zoom_card)
    window.center_btn.setParent(zoom_card)
    window.center_btn.setObjectName("TinyAction")
    window.center_btn.setText("↺")
    window.center_btn.setToolTip("Center the current Crop or Fit framing.")
    window.center_btn.setFixedWidth(32)

    zoom_value = QLabel(f"{window.crop_zoom_slider.value()}%")
    zoom_value.setObjectName("ZoomValue")
    window.crop_zoom_slider.valueChanged.connect(lambda value: zoom_value.setText(f"{value}%"))

    zoom_row = QHBoxLayout()
    zoom_row.setSpacing(8)
    zoom_row.addWidget(window.crop_zoom_slider, 1)
    zoom_row.addWidget(zoom_value)
    zoom_row.addWidget(window.center_btn)
    zoom_layout.addLayout(zoom_row)
    rail_layout.addWidget(zoom_card)

    # OUTPUT FOLDER
    card, layout, _ = _card("OUTPUT FOLDER", "folder")
    output_row = QHBoxLayout()
    output_row.setSpacing(7)
    window.output_path.setParent(card)
    window.output_path.setObjectName("PathText")
    output_row.addWidget(window.output_path, 1)

    browse_btn = QPushButton("Browse…")
    browse_btn.setObjectName("BrowseButton")
    browse_btn.setToolTip("Choose output folder")
    browse_btn.clicked.connect(window._choose_output_folder)
    output_row.addWidget(browse_btn)
    layout.addLayout(output_row)
    rail_layout.addWidget(card)

    # CAST POLYMORPH
    window.convert_btn.setParent(rail)
    window.convert_btn.setText("")
    window.convert_btn.setIcon(QIcon())
    window.convert_btn.setAccessibleName("Cast Polymorph")
    cast_layout = QHBoxLayout(window.convert_btn)
    cast_layout.setContentsMargins(14, 5, 14, 5)
    cast_layout.setSpacing(10)
    left_dash = QLabel("—")
    left_dash.setObjectName("CastDash")
    right_dash = QLabel("—")
    right_dash.setObjectName("CastDash")
    cast_layout.addWidget(left_dash)
    cast_layout.addWidget(BrandSigil(42))
    cast_words = QVBoxLayout()
    cast_words.setSpacing(0)
    cast_title = QLabel("CAST POLYMORPH")
    cast_title.setObjectName("CastTitle")
    cast_subtitle = QLabel("CONVERT MEDIA")
    cast_subtitle.setObjectName("CastSubtitle")
    cast_words.addWidget(cast_title)
    cast_words.addWidget(cast_subtitle)
    cast_layout.addLayout(cast_words, 1)
    cast_layout.addWidget(right_dash)
    rail_layout.addWidget(window.convert_btn)
    rail_layout.addStretch(1)

    rail_scroll.setWidget(rail)
    splitter.addWidget(rail_scroll)
    splitter.setStretchFactor(1, 0)
    splitter.setSizes([830, 410])
    outer.addWidget(splitter, 1)

    # Status/progress strip ---------------------------------------------------
    status_card = QFrame()
    status_card.setObjectName("StatusCard")
    status_layout = QHBoxLayout(status_card)
    status_layout.setContentsMargins(11, 6, 11, 6)
    status_layout.setSpacing(9)

    status_layout.addWidget(ReadyRing())

    status_box = QVBoxLayout()
    status_box.setSpacing(0)
    window.status_label.setParent(status_card)
    window.status_label.setObjectName("StatusLabel")
    status_box.addWidget(window.status_label)
    status_box.addWidget(status_detail)
    status_layout.addLayout(status_box, 1)

    window.arcane_progress.setParent(status_card)
    # Existing development placeholder is suppressed in this compact strip;
    # the real magic-circle/D20 working animation is a later dedicated pass.
    window.arcane_progress.setFixedSize(0, 0)
    window.arcane_progress.hide()

    window.progress.setParent(status_card)
    window.progress.setObjectName("InlineProgress")
    window.progress.setTextVisible(False)
    window.progress.setFixedWidth(180)
    window.progress.setVisible(False)

    def sync_progress_visibility(value: int) -> None:
        active = 0 < value < 100
        window.progress.setVisible(active)
        if active:
            status_detail.setText("Casting Polymorph. Your output is being prepared.")
        elif value >= 100:
            count = window.file_list.count()
            if count == 1:
                status_detail.setText("1 file imported. Choose your settings and begin.")
            else:
                status_detail.setText(f"{count} files imported. Choose your settings and begin.")

    window.progress.valueChanged.connect(sync_progress_visibility)
    status_layout.addWidget(window.progress)

    window.cancel_btn.setParent(status_card)
    status_layout.addWidget(window.cancel_btn)
    outer.addWidget(status_card)

    # Footer -----------------------------------------------------------------
    footer = QHBoxLayout()
    footer.setContentsMargins(0, 0, 0, 0)
    footer.setSpacing(5)

    footer_version = QLabel(f"Polymorph v{APP_VERSION}")
    footer_version.setObjectName("FooterVersion")
    footer.addWidget(footer_version)
    footer.addStretch(1)

    links = [
        _footer_link(
            window,
            "update.svg",
            "Check for Updates",
            "Check for updates",
            window._manual_check_updates,
        ),
        _footer_link(
            window,
            "github.svg",
            "GitHub",
            "View source on GitHub",
            lambda: window._open_url(REPO_URL),
        ),
        _footer_link(
            window,
            "kofi.svg",
            "Ko-fi",
            "Support me on Ko-fi",
            lambda: window._open_url(KOFI_URL),
            bool(KOFI_URL),
        ),
        _footer_link(
            window,
            "patreon.svg",
            "Patreon",
            "Support me on Patreon",
            lambda: window._open_url(PATREON_URL),
            bool(PATREON_URL),
        ),
        _footer_link(
            window,
            "discord.svg",
            "Discord",
            "Join the Discord",
            lambda: window._open_url(DISCORD_URL),
            bool(DISCORD_URL),
        ),
    ]
    for index, link in enumerate(links):
        if index:
            footer.addWidget(_vertical_separator())
        footer.addWidget(link)
    outer.addLayout(footer)

    window.setCentralWidget(root)
    window.setProperty("polymorphLayout", "concept-match-v1")
