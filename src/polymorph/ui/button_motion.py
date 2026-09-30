from __future__ import annotations

from math import cos, pi, sin

from PySide6.QtCore import QPointF, QRectF, Qt
from PySide6.QtGui import (
    QColor,
    QImage,
    QLinearGradient,
    QPainter,
    QPainterPath,
    QPen,
    QPixmap,
    QRadialGradient,
)

from . import brand_widgets as _brand
from . import button_motion_patch as _motion
from . import visual_patch as _visual


_INSTALLED = False


def _outward_pulse_emblem(source: QPixmap, phase: float) -> QPixmap:
    """Soft center bloom -> outward travel -> edge shine -> full fade -> restart."""
    if source.isNull():
        return source

    image = source.toImage().convertToFormat(QImage.Format.Format_ARGB32)
    if image.isNull():
        return source

    source_dpr = max(1.0, float(source.devicePixelRatio()))
    image.setDevicePixelRatio(1.0)
    center = QPointF(image.width() / 2.0, image.height() / 2.0)
    radius = max(image.width(), image.height()) * 0.53

    phase = max(0.0, min(1.0, float(phase)))
    if phase < 0.14:
        bloom = _motion._smoothstep(phase / 0.14)
        ring = 0.025 + 0.085 * bloom
        intensity = bloom
        width = 0.13 - 0.025 * bloom
        center_alpha = round(220 * bloom)
        edge_boost = 1.0
    elif phase < 0.70:
        travel = _motion._smoothstep((phase - 0.14) / 0.56)
        ring = 0.11 + 0.70 * travel
        intensity = 1.0
        width = 0.085 + 0.020 * travel
        center_alpha = round(100 * max(0.0, 1.0 - travel * 2.2))
        edge_boost = 1.0
    elif phase < 0.86:
        shine = _motion._smoothstep((phase - 0.70) / 0.16)
        ring = 0.81 + 0.065 * shine
        intensity = 1.0
        width = 0.105 + 0.035 * sin(pi * shine)
        center_alpha = 0
        edge_boost = 1.18
    else:
        fade = _motion._smoothstep((phase - 0.86) / 0.14)
        ring = 0.875
        intensity = 1.0 - fade
        width = 0.11
        center_alpha = 0
        edge_boost = 1.0

    if intensity <= 0.001:
        transparent = QPixmap(source.size())
        transparent.fill(Qt.GlobalColor.transparent)
        transparent.setDevicePixelRatio(source_dpr)
        return transparent

    mask = QRadialGradient(center, radius)
    p0 = max(0.0, ring - width * 1.7)
    p1 = max(p0 + 0.001, ring - width)
    p2 = max(p1 + 0.001, ring)
    p3 = min(0.999, max(p2 + 0.001, ring + width))
    p4 = min(1.0, max(p3 + 0.001, ring + width * 1.7))

    peak = min(255, round(255 * intensity * edge_boost))
    shoulder = min(210, round(118 * intensity * edge_boost))

    mask.setColorAt(0.0, QColor(255, 255, 255, center_alpha))
    mask.setColorAt(p0, QColor(255, 255, 255, 0))
    mask.setColorAt(p1, QColor(255, 255, 255, shoulder))
    mask.setColorAt(p2, QColor(255, 255, 255, peak))
    mask.setColorAt(p3, QColor(255, 255, 255, shoulder))
    mask.setColorAt(p4, QColor(255, 255, 255, 0))
    mask.setColorAt(1.0, QColor(255, 255, 255, 0))

    painter = QPainter(image)
    painter.setCompositionMode(QPainter.CompositionMode.CompositionMode_DestinationIn)
    painter.fillRect(image.rect(), mask)
    painter.end()

    pixmap = QPixmap.fromImage(image)
    pixmap.setDevicePixelRatio(source_dpr)
    return pixmap


class PolymorphButton(_motion.AnimatedPolymorphButton):
    """Final production treatment for the Polymorph conversion action."""

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self._polish_cache_key: tuple[int, int, int] | None = None
        self._foreground_mark = QPixmap()

    def _ensure_foreground_cache(self) -> None:
        key = (self.width(), self.height(), round(self._scale * 1000))
        if key == self._polish_cache_key:
            return
        self._polish_cache_key = key
        foreground_size = max(62, round(self.height() * 1.42))
        self._foreground_mark = _visual._polymorph_mark_pixmap(
            foreground_size,
            QColor("#f0cf88"),
            QColor("#8a2e3d"),
            mid_color=QColor("#c47b58"),
        )

    def _repaint_hover_interior(
        self,
        painter: QPainter,
        rect: QRectF,
        radius: float,
        hover: float,
    ) -> None:
        """Replace the inherited idle ghost with the animated hover surface."""
        if hover <= 0.001:
            return

        interior = rect.adjusted(1.35, 1.35, -1.35, -1.35)
        interior_path = QPainterPath()
        interior_path.addRoundedRect(
            interior,
            max(1.5, radius - 1.2),
            max(1.5, radius - 1.2),
        )

        painter.save()
        painter.setOpacity(hover)

        base = QLinearGradient(
            rect.left(), rect.center().y(), rect.right(), rect.center().y()
        )
        base.setColorAt(0.0, QColor("#35090f"))
        base.setColorAt(0.5, QColor("#9e1d2a"))
        base.setColorAt(1.0, QColor("#35090f"))
        painter.fillPath(interior_path, base)

        bronze = QLinearGradient(rect.left(), rect.top(), rect.left(), rect.bottom())
        bronze.setColorAt(0.0, QColor(235, 190, 108, 34))
        bronze.setColorAt(0.34, QColor(211, 151, 75, 10))
        bronze.setColorAt(0.58, QColor(255, 255, 255, 0))
        bronze.setColorAt(1.0, QColor(0, 0, 0, 72))
        painter.fillPath(interior_path, bronze)
        painter.restore()

        if not self._foreground_mark.isNull():
            dpr = self._foreground_mark.devicePixelRatio()
            logical = self._foreground_mark.width() / dpr
            mark_x = rect.left() + max(8.0, 12.0 * self._scale)
            mark_y = rect.center().y() - logical / 2.0
            painter.save()
            painter.setOpacity(0.430 * hover)
            painter.drawPixmap(round(mark_x), round(mark_y), self._foreground_mark)
            painter.restore()

    def paintEvent(self, event) -> None:
        super().paintEvent(event)

        enabled = self.isEnabled()
        if (
            not enabled
            and self._click_flash <= 0.001
            and self._press_progress <= 0.001
            and self._hover_progress <= 0.001
        ):
            return

        self._ensure_motion_cache()
        self._ensure_foreground_cache()

        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing, True)
        painter.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform, True)

        rect = QRectF(self.rect()).adjusted(0.5, 0.5, -0.5, -0.5)
        radius = max(3.0, 4.5 * self._scale)
        path = QPainterPath()
        path.addRoundedRect(rect, radius, radius)
        painter.setClipPath(path)

        hover = max(0.0, min(1.0, self._hover_progress)) if enabled else 0.0
        master = self._ambient_progress % 1.0

        if hover > 0.001:
            self._repaint_hover_interior(painter, rect, radius, hover)

            glaze = QLinearGradient(rect.left(), rect.top(), rect.left(), rect.bottom())
            glaze.setColorAt(0.0, QColor(255, 239, 204, round(25 * hover)))
            glaze.setColorAt(0.24, QColor(255, 223, 165, round(10 * hover)))
            glaze.setColorAt(0.58, QColor(255, 255, 255, 0))
            glaze.setColorAt(1.0, QColor(0, 0, 0, 0))
            painter.fillPath(path, glaze)

            phase_a = (master * 3.0) % 1.0
            travel_a = _motion._smoothstep(phase_a)
            envelope_a = _motion._loop_envelope(phase_a, 0.08)
            self._draw_rotated_pixmap(
                painter,
                self._ghost_mark_a,
                QPointF(
                    rect.left() + rect.width() * (0.50 + 0.30 * travel_a),
                    rect.center().y() - 3.0 * self._scale * sin(pi * phase_a),
                ),
                360.0 * phase_a,
                0.90 + 0.30 * travel_a,
                0.145 * hover * envelope_a,
            )

            phase_b = (master * 2.0 + 0.31) % 1.0
            angle_b = 2.0 * pi * phase_b
            anchor_b = QPointF(
                rect.left() + rect.width() * 0.27,
                rect.center().y() + 5.0 * self._scale,
            )
            self._draw_rotated_pixmap(
                painter,
                self._ghost_mark_b,
                QPointF(
                    anchor_b.x() + 7.0 * self._scale * cos(angle_b),
                    anchor_b.y() + 4.0 * self._scale * sin(angle_b),
                ),
                28.0 - 360.0 * phase_b,
                0.94 + 0.035 * (0.5 + 0.5 * sin(angle_b)),
                0.105 * hover,
            )

            self._draw_magic_flecks(painter, rect, hover, master)

            pulse_phase = (master * 6.0) % 1.0
            pulse = _outward_pulse_emblem(self._foreground_glow, pulse_phase)
            if not pulse.isNull():
                dpr = pulse.devicePixelRatio()
                logical = pulse.width() / dpr
                mark_x = rect.left() + max(8.0, 12.0 * self._scale)
                mark_y = rect.center().y() - logical / 2.0
                painter.save()
                painter.setOpacity(0.34 * hover)
                painter.drawPixmap(round(mark_x), round(mark_y), pulse)
                painter.restore()

        sheen = self._sheen_progress
        if hover > 0.001 and -0.40 <= sheen <= 1.40:
            center_x = rect.left() + rect.width() * sheen
            band = max(48.0, rect.width() * 0.18)
            sweep = QLinearGradient(
                QPointF(center_x - band, rect.bottom()),
                QPointF(center_x + band, rect.top()),
            )
            peak = round(66 * hover)
            warm = round(28 * hover)
            sweep.setColorAt(0.0, QColor(255, 255, 255, 0))
            sweep.setColorAt(0.34, QColor(255, 246, 226, 0))
            sweep.setColorAt(0.50, QColor(255, 250, 238, peak))
            sweep.setColorAt(0.61, QColor(238, 194, 117, warm))
            sweep.setColorAt(1.0, QColor(255, 255, 255, 0))
            painter.fillPath(path, sweep)

        press = max(0.0, min(1.0, self._press_progress))
        if press > 0.001:
            pressed = QLinearGradient(rect.left(), rect.top(), rect.left(), rect.bottom())
            pressed.setColorAt(0.0, QColor(0, 0, 0, round(34 * press)))
            pressed.setColorAt(0.52, QColor(0, 0, 0, round(12 * press)))
            pressed.setColorAt(1.0, QColor(246, 190, 92, round(14 * press)))
            painter.fillPath(path, pressed)

            inset = rect.adjusted(
                1.4 * press,
                1.8 * press,
                -1.4 * press,
                -1.0 * press,
            )
            painter.setClipping(False)
            painter.setPen(QPen(QColor(245, 198, 111, round(72 * press)), 1.0))
            painter.setBrush(Qt.BrushStyle.NoBrush)
            painter.drawRoundedRect(
                inset,
                max(2.0, radius - 1.0),
                max(2.0, radius - 1.0),
            )
            painter.setClipPath(path)

        flash = max(0.0, min(1.0, self._click_flash))
        if flash > 0.001:
            flash_phase = 1.0 - flash
            radius_px = max(
                self.height() * 0.55,
                self.width() * (0.10 + 0.35 * flash_phase),
            )
            click_pulse = QRadialGradient(self._click_origin, radius_px)
            click_pulse.setColorAt(
                0.0, QColor(255, 222, 153, round(58 * flash))
            )
            click_pulse.setColorAt(
                0.28, QColor(231, 171, 78, round(28 * flash))
            )
            click_pulse.setColorAt(1.0, QColor(220, 148, 54, 0))
            painter.fillPath(path, click_pulse)

            painter.setClipping(False)
            painter.setPen(QPen(QColor(246, 202, 118, round(105 * flash)), 1.2))
            painter.setBrush(Qt.BrushStyle.NoBrush)
            painter.drawRoundedRect(rect, radius, radius)
            painter.setClipPath(path)

        painter.setClipping(False)
        self._redraw_text(painter, rect, enabled)
        painter.end()


def install_button_motion() -> None:
    global _INSTALLED
    if _INSTALLED:
        return
    _INSTALLED = True
    _brand.PolymorphButton = PolymorphButton
