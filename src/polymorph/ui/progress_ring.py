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


class StatusActivityRing(QWidget):
    """Footer indicator: idle, animated activity, successful or failed."""
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setObjectName("StatusActivityRing")
        self.setFixedSize(45, 45)
        self.state = "idle"
        self._angle = 0
        self._timer = QTimer(self)
        self._timer.setInterval(40)
        self._timer.timeout.connect(self._tick)
        self.setToolTip("Ready")

    def set_active(self, active: bool) -> None:
        self.set_result("active" if active else "idle")

    def set_result(self, state: str) -> None:
        if state not in ("idle", "active", "success", "error"):
            raise ValueError("Invalid footer activity state")
        self.state = state
        if state == "active":
            self._angle = 0
            self._timer.start()
        else:
            self._timer.stop()
        captions = {"idle": "Ready", "active": "Converting",
                    "success": "Conversion completed", "error": "Conversion failed"}
        self.setToolTip(captions[state])
        self.setAccessibleName(captions[state])
        self.update()

    def _tick(self) -> None:
        if self.state == "active":
            self._angle = (self._angle + 13) % 360
            self.update()

    def paintEvent(self, _event) -> None:
        from PySide6.QtCore import QPointF, QRectF
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing, True)
        side = min(self.width(), self.height())
        weight = max(2.5, side * 0.12)
        circle = QRectF(self.rect()).adjusted(weight, weight, -weight, -weight)
        pen_style = Qt.PenStyle.SolidLine
        cap = Qt.PenCapStyle.RoundCap
        p.setBrush(Qt.BrushStyle.NoBrush)
        p.setPen(QPen(QColor("#362127"), weight, pen_style, cap))
        p.drawEllipse(circle)
        if self.state == "active":
            p.setPen(QPen(QColor("#d51f2d"), weight, pen_style, cap))
            p.drawArc(circle, round((90 - self._angle) * 16), -260 * 16)
        elif self.state in ("success", "error"):
            good = self.state == "success"
            p.setPen(QPen(QColor("#cda85f" if good else "#d51f2d"), weight, pen_style, cap))
            p.drawEllipse(circle)
            p.setPen(QPen(QColor("#f0d8a4" if good else "#e68187"),
                          max(2.0, weight * 0.58), pen_style, cap))
            cx, cy, delta = self.width() / 2, self.height() / 2, side * .12
            if good:
                p.drawLine(QPointF(cx-delta*1.4, cy), QPointF(cx-delta*.25, cy+delta))
                p.drawLine(QPointF(cx-delta*.25, cy+delta), QPointF(cx+delta*1.7, cy-delta*1.5))
            else:
                p.drawLine(QPointF(cx-delta, cy-delta), QPointF(cx+delta, cy+delta))
                p.drawLine(QPointF(cx+delta, cy-delta), QPointF(cx-delta, cy+delta))
        p.end()
