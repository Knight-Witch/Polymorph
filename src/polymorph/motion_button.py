from __future__ import annotations

from PySide6.QtCore import QPointF, QRectF, Qt
from PySide6.QtGui import QColor, QFont, QLinearGradient, QPainter, QPainterPath, QPen, QRadialGradient, QTransform
from PySide6.QtWidgets import QPushButton

from .motion_effects import CRIMSON, ELDER_FUTHARK, GOLD, IVORY, Clock, RunePainter, alpha, comet, glow_ellipse, polar
from .ui.brand_widgets import tracked_font

class ArcaneButton(QPushButton):
    def __init__(self, rune_family: str, parent=None) -> None:
        super().__init__(parent)
        self.setText("")
        self.setMinimumWidth(430)
        self.setFixedHeight(98)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.clock = Clock(self)
        self.runes = RunePainter(rune_family)
        self.hover = 0.0
        self.forced: str | None = None
        self.glow = 1.0
        self.speed = 1.0
        self.trace_speed = 1.0
        self.debug = False
        self.cast_at: float | None = None
        self.clicked.connect(self.cast)

    def cast(self) -> None:
        self.cast_at = self.clock.t
        self.update()

    def set_debug(self, on: bool) -> None:
        self.debug = on
        self.setFixedHeight(260 if on else 98)
        self.update()

    def burst(self) -> float:
        if self.cast_at is None:
            return 0.0
        age = self.clock.t - self.cast_at
        if age < 0:
            age += 100000
        if age >= 0.9:
            self.cast_at = None
            return 0.0
        return (1.0 - age / 0.9) ** 2

    def target(self) -> float:
        if self.forced in ("hover", "pressed"):
            return 1.0
        if self.forced == "rest":
            return 0.0
        return 1.0 if self.underMouse() else 0.0

    def mechanism(self, painter: QPainter, rect: QRectF, clip: bool) -> None:
        if clip:
            path = QPainterPath(); path.addRoundedRect(rect, 5, 5); painter.setClipPath(path)
        center = QPointF(rect.center().x() - rect.width() * 0.16, rect.center().y())
        radius = rect.height() * 1.16
        burst = self.burst(); active = min(1.35, 0.16 + self.hover * 0.84 + burst * 0.55)
        angle = self.clock.t * 15.0 * self.speed * (0.22 + self.hover * 0.78) + burst * 78.0
        for factor, opacity in ((1.0,0.34),(0.76,0.46),(0.51,0.28)):
            glow_ellipse(painter, center, radius * factor, GOLD, intensity=active * opacity * self.glow, core_width=0.7, spread=0.62)
        for i in range(12):
            degrees = angle + i * 30.0
            self.runes.draw(painter, ELDER_FUTHARK[i % len(ELDER_FUTHARK)], polar(center, radius * 0.76, degrees), 10.5, degrees + 90, color=GOLD, intensity=active * self.glow * 0.72, spread=0.45)
        if self.hover > 0.08:
            degrees = (self.clock.t * 72.0 * self.trace_speed) % 360.0
            head = polar(center, radius * 0.76, degrees); tail = polar(center, radius * 0.76, degrees - 25.0)
            comet(painter, tail, head, GOLD, intensity=self.hover * self.glow, spread=0.65)
        if clip:
            painter.setClipping(False)

    def text(self, painter: QPainter, rect: QRectF) -> None:
        text_rect = QRectF(rect.left() + 60, rect.top() + 15, rect.width() - 120, 42)
        path = QPainterPath(); path.addText(QPointF(0, 0), QFont(tracked_font(17, 5.1)), "POLYMORPH")
        bounds = path.boundingRect(); x = text_rect.center().x() - bounds.width() / 2 - bounds.left(); y = text_rect.center().y() + bounds.height() / 2 - bounds.bottom()
        transform = QTransform(); transform.translate(x, y); path = transform.map(path)
        painter.setPen(Qt.PenStyle.NoPen); painter.setBrush(IVORY); painter.drawPath(path)
        if self.hover > 0.03:
            sweep = ((self.clock.t * 0.22 * self.trace_speed) % 1.35) - 0.16
            cx = text_rect.left() + text_rect.width() * sweep; width = max(28, text_rect.width() * 0.11)
            gradient = QLinearGradient(cx - width, 0, cx + width, 0)
            gradient.setColorAt(0,QColor(255,255,255,0)); gradient.setColorAt(0.45,alpha(GOLD,115*self.hover*self.glow)); gradient.setColorAt(0.5,alpha(IVORY,255*self.hover*self.glow)); gradient.setColorAt(0.55,alpha(GOLD,115*self.hover*self.glow)); gradient.setColorAt(1,QColor(255,255,255,0))
            painter.save(); painter.setClipPath(path); painter.fillRect(text_rect.adjusted(-30,-12,30,12), gradient); painter.restore()

    def paintEvent(self, _event) -> None:
        target = self.target(); self.hover += (target - self.hover) * (0.11 if target > self.hover else 0.075)
        painter = QPainter(self); painter.setRenderHint(QPainter.RenderHint.Antialiasing, True); painter.setRenderHint(QPainter.RenderHint.TextAntialiasing, True)
        rect = QRectF(30,(self.height()-98)/2,max(1,self.width()-60),98) if self.debug else QRectF(self.rect()).adjusted(1,1,-1,-1)
        if self.debug:
            painter.save(); painter.setOpacity(0.38); self.mechanism(painter, rect, False); painter.restore()
        pressed = self.isDown() or self.forced == "pressed"; active = max(self.hover, 0.35 if pressed else 0.0, self.burst())
        path = QPainterPath(); path.addRoundedRect(rect,5,5); painter.setClipPath(path)
        gradient = QLinearGradient(rect.left(),rect.top(),rect.right(),rect.bottom()); gradient.setColorAt(0,QColor("#180609")); gradient.setColorAt(0.45,QColor("#78131d") if pressed else QColor("#621019")); gradient.setColorAt(1,QColor("#120507")); painter.fillPath(path,gradient)
        wake = QRadialGradient(QPointF(rect.center().x()-rect.width()*0.18,rect.center().y()),rect.width()*0.62); wake.setColorAt(0,alpha(CRIMSON,50+80*active)); wake.setColorAt(0.46,alpha(GOLD,7+17*active)); wake.setColorAt(1,QColor(0,0,0,0)); painter.fillPath(path,wake)
        painter.setClipping(False); self.mechanism(painter,rect,True)
        painter.setPen(QPen(alpha(GOLD,115+75*active),1)); painter.setBrush(Qt.BrushStyle.NoBrush); painter.drawRoundedRect(rect,5,5); self.text(painter,rect)
        painter.setPen(alpha(GOLD,160)); painter.setFont(tracked_font(7,2.3)); painter.drawText(QRectF(rect.left(),rect.center().y()+18,rect.width(),22),Qt.AlignmentFlag.AlignHCenter|Qt.AlignmentFlag.AlignTop,"CONVERT MEDIA")
        if self.debug:
            painter.setPen(QPen(QColor("#68c7ff"),1,Qt.PenStyle.DashLine)); painter.drawRoundedRect(rect,5,5)
