from __future__ import annotations

from pathlib import Path

from PySide6.QtCore import QPoint, QRect, QRectF, Qt, Signal
from PySide6.QtGui import QColor, QMovie, QPainter, QPen, QPixmap
from PySide6.QtWidgets import QWidget

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

        source = QRectF(self._pixmap.rect())
        target_ratio = self._framing.ratio if self._framing.mode is not FramingMode.ORIGINAL else None
        display_rect = self._fit_rect(inner, target_ratio or (source.width() / source.height()))

        if self._framing.mode is FramingMode.CROP and target_ratio:
            crop = self._crop_rect(source, target_ratio)
            painter.drawPixmap(display_rect, self._pixmap, crop)
        elif self._framing.mode is FramingMode.FIT and target_ratio:
            painter.fillRect(display_rect, QColor(self._framing.background))
            content_rect = self._content_rect_for_fit(display_rect, source.width() / source.height())
            content_rect = self._offset_fit_rect(content_rect, display_rect)
            painter.drawPixmap(content_rect, self._pixmap, source)
        else:
            painter.drawPixmap(display_rect, self._pixmap, source)

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

    def _crop_rect(self, source: QRectF, ratio: float) -> QRectF:
        sr = source.width() / source.height()
        if sr > ratio:
            h = source.height()
            w = h * ratio
            extra = source.width() - w
            x = ((self._framing.offset_x + 1) / 2) * extra
            return QRectF(x, 0, w, h)
        w = source.width()
        h = w / ratio
        extra = source.height() - h
        y = ((self._framing.offset_y + 1) / 2) * extra
        return QRectF(0, y, w, h)

    @staticmethod
    def _content_rect_for_fit(canvas: QRectF, source_ratio: float) -> QRectF:
        if canvas.width() / canvas.height() > source_ratio:
            h = canvas.height()
            w = h * source_ratio
        else:
            w = canvas.width()
            h = w / source_ratio
        return QRectF(canvas.x() + (canvas.width() - w) / 2, canvas.y() + (canvas.height() - h) / 2, w, h)

    def _offset_fit_rect(self, content: QRectF, canvas: QRectF) -> QRectF:
        max_x = max(0.0, canvas.width() - content.width())
        max_y = max(0.0, canvas.height() - content.height())
        x = canvas.x() + ((self._framing.offset_x + 1) / 2) * max_x
        y = canvas.y() + ((self._framing.offset_y + 1) / 2) * max_y
        return QRectF(x, y, content.width(), content.height())

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
