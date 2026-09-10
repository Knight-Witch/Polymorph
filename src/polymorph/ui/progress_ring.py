from __future__ import annotations

from PySide6.QtCore import QTimer, Qt
from PySide6.QtGui import QColor, QPainter, QPen
from PySide6.QtWidgets import QWidget


class ArcaneProgress(QWidget):
    """Lightweight development placeholder for the future Polymorph sigil animation."""

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setFixedSize(110, 110)
        self._progress = 0.0
        self._angle = 0.0
        self._active = False
        self._timer = QTimer(self)
        self._timer.setInterval(33)
        self._timer.timeout.connect(self._tick)

    def set_progress(self, value: float) -> None:
        self._progress = max(0.0, min(1.0, value))
        self.update()

    def set_active(self, active: bool) -> None:
        self._active = active
        if active and not self._timer.isActive():
            self._timer.start()
        elif not active:
            self._timer.stop()
        self.update()

    def _tick(self) -> None:
        self._angle = (self._angle + 2.5) % 360
        self.update()

    def paintEvent(self, _event) -> None:
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing, True)
        center = self.rect().center()
        outer = self.rect().adjusted(8, 8, -8, -8)

        p.setPen(QPen(QColor(255, 255, 255, 26), 4))
        p.drawArc(outer, 0, 360 * 16)
        p.setPen(QPen(QColor(230, 234, 239, 220), 4, Qt.SolidLine, Qt.RoundCap))
        p.drawArc(outer, 90 * 16, int(-360 * 16 * self._progress))

        p.save()
        p.translate(center)
        p.rotate(self._angle if self._active else 0)
        p.setPen(QPen(QColor(210, 216, 224, 145), 1.5))
        p.drawEllipse(-27, -27, 54, 54)
        p.drawLine(-22, 0, 22, 0)
        p.drawLine(0, -22, 0, 22)
        p.rotate(-2 * self._angle if self._active else 0)
        p.drawRect(-15, -15, 30, 30)
        p.restore()
