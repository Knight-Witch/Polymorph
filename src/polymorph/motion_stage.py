from __future__ import annotations

from PySide6.QtCore import QRectF, Qt
from PySide6.QtGui import QColor, QLinearGradient, QPainter, QPen, QPixmap
from PySide6.QtWidgets import QWidget

class Stage(QWidget):
    NAMES = ("Black", "Polymorph Gradient", "Obsidian Grain", "Slate Texture", "Busy Test", "Custom Image")

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.index = 1
        self.custom = QPixmap()
        self.setMinimumSize(820, 720)

    def load(self, path: str) -> bool:
        self.custom = QPixmap(path)
        self.index = 5
        self.update()
        return not self.custom.isNull()

    def paintEvent(self, _event) -> None:
        painter = QPainter(self); rect = QRectF(self.rect()); index = self.index
        if index == 0:
            painter.fillRect(rect, QColor("#000")); return
        if index == 5 and not self.custom.isNull():
            image = self.custom.scaled(self.size(), Qt.AspectRatioMode.KeepAspectRatioByExpanding, Qt.TransformationMode.SmoothTransformation)
            x = (image.width() - self.width()) // 2; y = (image.height() - self.height()) // 2
            painter.drawPixmap(0, 0, image, x, y, self.width(), self.height()); return
        gradient = QLinearGradient(rect.topLeft(), rect.bottomRight())
        colors = {1:("#050608","#0b0d11","#030405"),2:("#090a0c","#111318","#050607"),3:("#292d34","#171b21","#0d0f13"),4:("#23111b","#102332","#0b0d10")}[index]
        gradient.setColorAt(0,QColor(colors[0])); gradient.setColorAt(0.5,QColor(colors[1])); gradient.setColorAt(1,QColor(colors[2])); painter.fillRect(rect,gradient)
        if index in (2,3,4):
            state = 0xC0FFEE
            for n in range(640 if index == 4 else 390):
                state = (1664525*state+1013904223+n)&0xFFFFFFFF; x = state % max(1,self.width()); state = (1664525*state+1013904223)&0xFFFFFFFF; y = state % max(1,self.height())
                painter.setPen(QColor(255,245,228,15 if index == 4 else 8)); painter.drawPoint(int(x),int(y))
        if index == 4:
            painter.setPen(QPen(QColor(255,255,255,16),1))
            for x in range(-self.height(), self.width(), 46): painter.drawLine(x,0,x+self.height(),self.height())
