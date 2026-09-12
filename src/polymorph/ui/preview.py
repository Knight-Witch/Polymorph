from __future__ import annotations

from pathlib import Path

from PySide6.QtCore import QPoint, QRect, QRectF, Qt, Signal
from PySide6.QtGui import QColor, QMovie, QPainter, QPen, QPixmap
from PySide6.QtWidgets import QWidget

from ..geometry import native_geometry_for_size
from ..models import FramingMode, FramingSettings


class AnimatedPreview(QWidget):
    framingChanged = Signal(float, float)

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setMinimumSize(420, 420)
        self.setAcceptDrops(False)
        self._movie: QMovie | None = None
        self._pixmap = QPixmap()
        self._framing = FramingSettings()
        self._drag_origin: QPoint | None = None
        self._drag_start_offsets = (0.0, 0.0)
        self._empty_text = "Drop animated WebP files here"

    def set_source(self, path: Path | None) -> None:
        if self._movie:
            self._movie.stop()
            self._movie.deleteLater()
            self._movie = None
        self._pixmap = QPixmap()
        if path:
            movie = QMovie(str(path))
            movie.setCacheMode(QMovie.CacheNone)
            movie.frameChanged.connect(self._on_frame)
            self._movie = movie
            movie.start()
        self.update()

    def set_framing(self, framing: FramingSettings) -> None:
        self._framing = framing
        self.update()

    def _on_frame(self, _index: int) -> None:
        if self._movie:
            self._pixmap = self._movie.currentPixmap()
            self.update()

    def paintEvent(self, _event) -> None:
        painter = QPainter(self)
        painter.setRenderHint(QPainter.SmoothPixmapTransform, True)
        painter.fillRect(self.rect(), QColor("#111317"))

        inner = self.rect().adjusted(18, 18, -18, -18)
        if self._pixmap.isNull():
            painter.setPen(QColor("#7f8792"))
            painter.drawText(inner, Qt.AlignCenter, self._empty_text)
            self._draw_border(painter, inner)
            return

        source_width = self._pixmap.width()
        source_height = self._pixmap.height()
        geometry = native_geometry_for_size(source_width, source_height, self._framing)
        display_rect = self._fit_rect(inner, geometry.width / geometry.height)

        if self._framing.mode is FramingMode.CROP and geometry.crop_width and geometry.crop_height:
            source_rect = QRectF(
                geometry.crop_x,
                geometry.crop_y,
                geometry.crop_width,
                geometry.crop_height,
            )
            painter.drawPixmap(display_rect, self._pixmap, source_rect)
        elif self._framing.mode is FramingMode.FIT and self._framing.ratio:
            painter.fillRect(display_rect, QColor(self._framing.background))
            content_width = geometry.content_width or source_width
            content_height = geometry.content_height or source_height
            content_rect = QRectF(
                display_rect.x() + display_rect.width() * geometry.pad_x / geometry.width,
                display_rect.y() + display_rect.height() * geometry.pad_y / geometry.height,
                display_rect.width() * content_width / geometry.width,
                display_rect.height() * content_height / geometry.height,
            )
            painter.drawPixmap(content_rect, self._pixmap, QRectF(self._pixmap.rect()))
        else:
            painter.drawPixmap(display_rect, self._pixmap, QRectF(self._pixmap.rect()))

        self._draw_border(painter, display_rect.toRect())

    @staticmethod
    def _fit_rect(bounds: QRect, ratio: float) -> QRectF:
        bw, bh = bounds.width(), bounds.height()
        if bw / bh > ratio:
            h = bh
            w = h * ratio
        else:
            w = bw
            h = w / ratio
        x = bounds.x() + (bw - w) / 2
        y = bounds.y() + (bh - h) / 2
        return QRectF(x, y, w, h)

    @staticmethod
    def _draw_border(painter: QPainter, rect: QRect) -> None:
        painter.setPen(QPen(QColor(255, 255, 255, 28), 1))
        painter.drawRoundedRect(rect, 10, 10)

    def mousePressEvent(self, event) -> None:
        if event.button() == Qt.LeftButton and self._framing.mode is not FramingMode.ORIGINAL:
            self._drag_origin = event.position().toPoint()
            self._drag_start_offsets = (self._framing.offset_x, self._framing.offset_y)
            self.setCursor(Qt.ClosedHandCursor)

    def mouseMoveEvent(self, event) -> None:
        if not self._drag_origin:
            return
        delta = event.position().toPoint() - self._drag_origin
        ox, oy = self._drag_start_offsets
        direction = -1.0 if self._framing.mode is FramingMode.CROP else 1.0
        nx = max(-1.0, min(1.0, ox + direction * delta.x() / max(80, self.width() / 3)))
        ny = max(-1.0, min(1.0, oy + direction * delta.y() / max(80, self.height() / 3)))
        self._framing.offset_x = nx
        self._framing.offset_y = ny
        self.framingChanged.emit(nx, ny)
        self.update()

    def mouseReleaseEvent(self, _event) -> None:
        self._drag_origin = None
        self.unsetCursor()
