from __future__ import annotations

from pathlib import Path

from PySide6.QtCore import QPoint, QRect, QRectF, Qt, Signal
from PySide6.QtGui import QColor, QFont, QMovie, QPainter, QPen, QPixmap
from PySide6.QtWidgets import QWidget

from ..geometry import native_geometry_for_size
from ..models import FramingMode, FramingSettings


class AnimatedPreview(QWidget):
    framingChanged = Signal(float, float)
    playbackChanged = Signal(int, int, float, float, bool)

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setMinimumSize(420, 320)
        self.setAcceptDrops(False)
        self._movie: QMovie | None = None
        self._pixmap = QPixmap()
        self._framing = FramingSettings()
        self._drag_origin: QPoint | None = None
        self._drag_start_offsets = (0.0, 0.0)
        self._empty_text = "Drop animated WebP files here"
        self._frame_count = 0
        self._duration_ms = 0
        self._frame_durations_ms: list[int] = []
        self._frame_offsets_ms: list[int] = []
        self._current_frame = 0

    def set_source(self, path: Path | None) -> None:
        if self._movie:
            self._movie.stop()
            self._movie.deleteLater()
            self._movie = None
        self._pixmap = QPixmap()
        self._current_frame = 0
        if path:
            movie = QMovie(str(path))
            # CacheAll proved capable of stalling the frozen/offscreen Qt path.
            # CacheNone was already stable in production preview builds and still
            # supports frame seeking for animated WebP without retaining the full
            # loop in memory.
            movie.setCacheMode(QMovie.CacheMode.CacheNone)
            movie.frameChanged.connect(self._on_frame)
            self._movie = movie
            movie.start()
        else:
            self._frame_count = 0
            self._duration_ms = 0
            self._frame_durations_ms = []
            self._frame_offsets_ms = []
            self._emit_playback()
        self.update()

    def set_timing(
        self,
        frame_count: int,
        duration_s: float,
        frame_durations_ms: list[int] | None = None,
    ) -> None:
        self._frame_count = max(0, int(frame_count))
        self._duration_ms = max(0, int(round(float(duration_s) * 1000.0)))
        durations = [max(1, int(value)) for value in (frame_durations_ms or [])]
        if self._frame_count and len(durations) != self._frame_count:
            average = max(1, round(self._duration_ms / self._frame_count)) if self._duration_ms else 40
            durations = [average] * self._frame_count
        self._frame_durations_ms = durations
        offsets: list[int] = []
        elapsed = 0
        for delay in durations:
            offsets.append(elapsed)
            elapsed += delay
        self._frame_offsets_ms = offsets
        if not self._duration_ms and elapsed:
            self._duration_ms = elapsed
        self._emit_playback()
        self.update()

    def set_framing(self, framing: FramingSettings) -> None:
        self._framing = framing
        self.update()

    def toggle_playback(self) -> None:
        movie = self._movie
        if movie is None or not movie.isValid():
            return
        if movie.state() == QMovie.MovieState.Running:
            movie.setPaused(True)
        elif movie.state() == QMovie.MovieState.Paused:
            movie.setPaused(False)
        else:
            movie.start()
        self._emit_playback()

    def seek_frame(self, frame_index: int) -> bool:
        movie = self._movie
        if movie is None or not movie.isValid():
            return False
        total = self.total_frames()
        if total <= 0:
            return False
        target = max(0, min(total - 1, int(frame_index)))

        # Scrubbing should be deterministic. Pause the movie before jumping so
        # the playback timer cannot advance concurrently with the requested seek.
        if movie.state() == QMovie.MovieState.Running:
            movie.setPaused(True)
        ok = movie.jumpToFrame(target)
        if ok:
            self._current_frame = target
            self._pixmap = movie.currentPixmap()
            self._emit_playback()
            self.update()
        return bool(ok)

    def seek_fraction(self, fraction: float) -> bool:
        total = self.total_frames()
        if total <= 1:
            return False
        fraction = max(0.0, min(1.0, float(fraction)))
        return self.seek_frame(round(fraction * (total - 1)))

    def total_frames(self) -> int:
        if self._frame_count > 0:
            return self._frame_count
        if self._movie is not None:
            count = self._movie.frameCount()
            if count > 0:
                return count
        return 0

    def duration_seconds(self) -> float:
        return self._duration_ms / 1000.0

    def current_seconds(self) -> float:
        if self._frame_offsets_ms and 0 <= self._current_frame < len(self._frame_offsets_ms):
            return self._frame_offsets_ms[self._current_frame] / 1000.0
        total = self.total_frames()
        if total > 1 and self._duration_ms > 0:
            return (self._current_frame / (total - 1)) * self.duration_seconds()
        return 0.0

    def is_playing(self) -> bool:
        return self._movie is not None and self._movie.state() == QMovie.MovieState.Running

    def _on_frame(self, index: int) -> None:
        if self._movie:
            self._current_frame = max(0, index)
            self._pixmap = self._movie.currentPixmap()
            self._emit_playback()
            self.update()

    def _emit_playback(self) -> None:
        self.playbackChanged.emit(
            self._current_frame,
            self.total_frames(),
            self.current_seconds(),
            self.duration_seconds(),
            self.is_playing(),
        )

    def paintEvent(self, _event) -> None:
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform, True)
        painter.fillRect(self.rect(), QColor("#090a0b"))

        inner = self.rect().adjusted(10, 9, -10, -9)
        if self._pixmap.isNull():
            painter.setPen(QColor("#77736c"))
            painter.drawText(inner, Qt.AlignmentFlag.AlignCenter, self._empty_text)
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
        self._draw_frame_readout(painter, display_rect)

    def _draw_frame_readout(self, painter: QPainter, display_rect: QRectF) -> None:
        total = self.total_frames()
        if total <= 0:
            return
        current = min(total, self._current_frame + 1)
        text = f"FRAME   {current} / {total}"
        painter.save()
        painter.setPen(QColor(221, 215, 205, 180))
        font = painter.font()
        font.setPointSizeF(8.0)
        font.setLetterSpacing(QFont.SpacingType.AbsoluteSpacing, 0.8)
        painter.setFont(font)
        x = display_rect.left() + 10
        y = display_rect.bottom() - 10
        metrics = painter.fontMetrics()
        box = QRectF(x - 5, y - metrics.height() + 2, metrics.horizontalAdvance(text) + 10, metrics.height() + 4)
        painter.fillRect(box, QColor(0, 0, 0, 92))
        painter.drawText(QRectF(x, y - metrics.height(), box.width(), metrics.height() + 2), Qt.AlignmentFlag.AlignVCenter, text)
        painter.restore()

    @staticmethod
    def _fit_rect(bounds: QRect, ratio: float) -> QRectF:
        bw, bh = bounds.width(), bounds.height()
        if bh <= 0 or ratio <= 0:
            return QRectF(bounds)
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
        painter.setPen(QPen(QColor(206, 171, 105, 72), 1.0))
        painter.drawRoundedRect(rect, 1.5, 1.5)

    def mousePressEvent(self, event) -> None:
        if event.button() == Qt.MouseButton.LeftButton and self._framing.mode is not FramingMode.ORIGINAL:
            self._drag_origin = event.position().toPoint()
            self._drag_start_offsets = (self._framing.offset_x, self._framing.offset_y)
            self.setCursor(Qt.CursorShape.ClosedHandCursor)

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
