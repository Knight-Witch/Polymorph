from __future__ import annotations

from pathlib import Path

from PIL import Image
from PySide6.QtCore import QRectF, Qt
from PySide6.QtGui import QColor, QImage, QLinearGradient, QPainter, QPainterPath, QPen, QRadialGradient
from PySide6.QtSvg import QSvgRenderer


ROOT = Path(__file__).resolve().parent.parent
SOURCE = ROOT / "src" / "polymorph" / "assets" / "polymorph_mark.svg"
OUT = Path(__file__).with_name("polymorph.ico")
MASTER = Path(__file__).with_name("polymorph_icon_master.png")
SIZE = 1024

canvas = QImage(SIZE, SIZE, QImage.Format.Format_ARGB32_Premultiplied)
canvas.fill(Qt.GlobalColor.transparent)
painter = QPainter(canvas)
painter.setRenderHint(QPainter.RenderHint.Antialiasing, True)
painter.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform, True)

outer = QRectF(20, 20, SIZE - 40, SIZE - 40)
radius = 188.0
tile = QPainterPath()
tile.addRoundedRect(outer, radius, radius)
painter.setClipPath(tile)

background = QLinearGradient(outer.topLeft(), outer.bottomRight())
background.setColorAt(0.0, QColor("#111a24"))
background.setColorAt(0.52, QColor("#07090d"))
background.setColorAt(1.0, QColor("#17090f"))
painter.fillPath(tile, background)

halo = QRadialGradient(outer.center(), SIZE * 0.52)
halo.setColorAt(0.0, QColor(113, 27, 45, 82))
halo.setColorAt(0.46, QColor(44, 25, 39, 28))
halo.setColorAt(1.0, QColor(0, 0, 0, 0))
painter.fillPath(tile, halo)
painter.setClipping(False)

painter.setPen(QPen(QColor(226, 211, 180, 118), 4.0))
painter.setBrush(Qt.BrushStyle.NoBrush)
painter.drawRoundedRect(outer, radius, radius)
painter.setPen(QPen(QColor(255, 244, 224, 34), 2.0))
painter.drawRoundedRect(outer.adjusted(8, 8, -8, -8), radius - 8, radius - 8)

renderer = QSvgRenderer(str(SOURCE))
if not renderer.isValid():
    raise RuntimeError(f"Invalid Polymorph SVG: {SOURCE}")

mask = QImage(SIZE, SIZE, QImage.Format.Format_ARGB32_Premultiplied)
mask.fill(Qt.GlobalColor.transparent)
mask_painter = QPainter(mask)
mask_painter.setRenderHint(QPainter.RenderHint.Antialiasing, True)
mark_box = QRectF(132, 144, SIZE - 264, SIZE - 288)
renderer.render(mask_painter, mark_box)
mask_painter.end()

mark = QImage(SIZE, SIZE, QImage.Format.Format_ARGB32_Premultiplied)
mark.fill(Qt.GlobalColor.transparent)
mark_painter = QPainter(mark)
mark_gradient = QLinearGradient(mark_box.topLeft(), mark_box.bottomRight())
mark_gradient.setColorAt(0.0, QColor("#fffaf1"))
mark_gradient.setColorAt(0.48, QColor("#dfcda8"))
mark_gradient.setColorAt(0.78, QColor("#c28b68"))
mark_gradient.setColorAt(1.0, QColor("#9b3b4c"))
mark_painter.fillRect(mark.rect(), mark_gradient)
mark_painter.setCompositionMode(QPainter.CompositionMode.CompositionMode_DestinationIn)
mark_painter.drawImage(0, 0, mask)
mark_painter.end()

painter.setOpacity(0.16)
painter.drawImage(0, 8, mark)
painter.setOpacity(0.98)
painter.drawImage(0, 0, mark)
painter.end()

if not canvas.save(str(MASTER), "PNG"):
    raise RuntimeError(f"Could not write icon master: {MASTER}")

with Image.open(MASTER) as image:
    image.save(
        OUT,
        format="ICO",
        sizes=[(16, 16), (24, 24), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)],
    )

MASTER.unlink(missing_ok=True)
print(OUT)
