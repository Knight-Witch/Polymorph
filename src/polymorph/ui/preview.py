from __future__ import annotations

from pathlib import Path

from PySide6.QtCore import QPoint, QRect, QRectF, Qt, Signal
from PySide6.QtGui import QColor, QMovie, QPainter, QPen, QPixmap
from PySide6.QtWidgets import QWidget

from ..geometry import clamp_framing_zoom, content_placement
from ..models import FramingMode, FramingSettings


class AnimatedPreview(QWidget):
    framingChanged = Signal(float, float)
    zoomChanged = Signal(float)

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
        source_ratio = source.width() / source.height()
        target_ratio = (
            self._framing.ratio
            if self._framing.mode is not FramingMode.ORIGINAL and self._framing.ratio
            else source_ratio
        )
        canvas = self._fit_rect(inner, target_ratio)

        if self._framing.mode is FramingMode.FIT and self._framing.ratio:
            painter.fillRect(canvas, QColor(self._framing.background))

        if self._framing.mode is FramingMode.ORIGINAL or not self._framing.ratio:
            content = canvas
        else:
            placement = content_placement(
                source.width(),
                source.height(),
                canvas.width(),
                canvas.height(),
                self._framing,
            )
            content = QRectF(
                canvas.x() + placement.x,
                canvas.y() + placement.y,
                placement.width,
                placement.height,
            )

        # Draw the entire source at an aspect-preserving size and clip it to the
        # framing canvas. This mirrors the encoder's cover/contain placement model
        # and cannot stretch the source to the target ratio.
        painter.save()
        painter.setClipRect(canvas)
        painter.drawPixmap(content, self._pixmap, source)
        painter.restore()

        self._draw_border(painter, canvas.toRect())

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

    def _preview_sizes(self) -> tuple[float, float, float, float] | None:
        if self._pixmap.isNull() or self._framing.mode is FramingMode.ORIGINAL or not self._framing.ratio:
            return None
        inner = self.rect().adjusted(18, 18, -18, -18)
        canvas = self._fit_rect(inner, self._framing.ratio)
        placement = content_placement(
            self._pixmap.width(),
            self._pixmap.height(),
            canvas.width(),
            canvas.height(),
            self._framing,
        )
        return canvas.width(), canvas.height(), placement.width, placement.height

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
        sizes = self._preview_sizes()
        if sizes is None:
            return
        canvas_w, canvas_h, content_w, content_h = sizes

        # Make the visible media follow the pointer. Contained content moves in the
        # same direction as the drag; overflowing/cropped content uses the inverse
        # normalized offset because revealing the far edge moves the image left/up.
        direction_x = 1.0 if content_w <= canvas_w else -1.0
        direction_y = 1.0 if content_h <= canvas_h else -1.0
        nx = max(
            -1.0,
            min(1.0, ox + direction_x * delta.x() / max(80.0, canvas_w / 3.0)),
        )
        ny = max(
            -1.0,
            min(1.0, oy + direction_y * delta.y() / max(80.0, canvas_h / 3.0)),
        )
        self._framing.offset_x = nx
        self._framing.offset_y = ny
        self.framingChanged.emit(nx, ny)
        self.update()

    def mouseReleaseEvent(self, _event) -> None:
        self._drag_origin = None
        self.unsetCursor()

    def wheelEvent(self, event) -> None:
        if self._framing.mode is FramingMode.ORIGINAL:
            return super().wheelEvent(event)
        steps = event.angleDelta().y() / 120.0
        if not steps:
            return
        zoom = clamp_framing_zoom(self._framing.zoom + steps * 0.10)
        if abs(zoom - self._framing.zoom) > 1e-9:
            self._framing.zoom = zoom
            self.zoomChanged.emit(zoom)
            self.update()
        event.accept()
