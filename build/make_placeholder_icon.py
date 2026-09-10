from __future__ import annotations

from pathlib import Path
from PIL import Image, ImageDraw

out = Path(__file__).with_name("polymorph_placeholder.ico")
size = 256
img = Image.new("RGBA", (size, size), (23, 25, 29, 255))
d = ImageDraw.Draw(img)

# Deliberately generic development mark. This is not intended to become the final emblem.
for inset, width in ((20, 8), (46, 4), (72, 3)):
    d.ellipse((inset, inset, size - inset, size - inset), outline=(235, 238, 242, 230), width=width)

d.line((128, 60, 128, 196), fill=(235, 238, 242, 220), width=5)
d.line((60, 128, 196, 128), fill=(235, 238, 242, 220), width=5)
d.polygon([(128, 78), (162, 128), (128, 178), (94, 128)], outline=(235, 238, 242, 230))

img.save(out, format="ICO", sizes=[(16,16),(24,24),(32,32),(48,48),(64,64),(128,128),(256,256)])
print(out)
