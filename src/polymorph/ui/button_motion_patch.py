from __future__ import annotations

from math import cos, pi, sin

from PySide6.QtCore import QEasingCurve, QPointF, QRectF, Qt, QVariantAnimation
from PySide6.QtGui import (
    QColor,
    QFont,
    QImage,
    QLinearGradient,
    QPainter,
    QPainterPath,
    QPen,
    QPixmap,
    QRadialGradient,
)

from . import brand_widgets as _brand
from . import visual_patch as _visual


_INSTALLED = False


def _smoothstep(value: float) -> float:
    value = max(0.0, min(1.0, float(value)))
    return value * value * (3.0 - 2.0 * value)


def _loop_envelope(phase: float, fade: float = 0.08) -> float:
    """Fade only around a wrapped positional reset; rotation itself remains continuous."""
    phase = phase % 1.0
    if phase < fade:
        return _smoothstep(phase / fade)
    if phase > 1.0 - fade:
        return _smoothstep((1.0 - phase) / fade)
    return 1.0


def _alpha_bounds_center(source: QPixmap) -> QPointF:
    """Find the visible canonical-mark center instead of assuming the square pixmap center."""
    if source.isNull():
        return QPointF()
    image = source.toImage().convertToFormat(QImage.Format.Format_ARGB32)
    if image.isNull():
        return QPointF()

    left = image.width()
    top = image.height()
    right = -1
    bottom = -1
    for y in range(image.height()):
        for x in range(image.width()):
            if image.pixelColor(x, y).alpha() > 8:
                left = min(left, x)
                top = min(top, y)
                right = max(right, x)
                bottom = max(bottom, y)

    if right < left or bottom < top:
        return QPointF(image.width() / 2.0, image.height() / 2.0)
    return QPointF((left + right) / 2.0, (top + bottom) / 2.0)


def _outward_pulse_emblem(
    source: QPixmap,
    phase: float,
    center_px: QPointF,
) -> QPixmap:
    """Center -> edge travel, edge shine, fade, then restart from the center."""
    if source.isNull():
        return source

    image = source.toImage()
    if image.isNull():
        return source

    phase = max(0.0, min(1.0, float(phase)))
    if phase < 0.72:
        travel = _smoothstep(phase / 0.72)
        ring = 0.14 + 0.70 * travel
        intensity = 1.0
        width = 0.075 + 0.025 * travel
    elif phase < 0.88:
        edge = _smoothstep((phase - 0.72) / 0.16)
        ring = 0.84 + 0.035 * edge
        intensity = 1.0
        width = 0.10 + 0.035 * sin(pi * edge)
    else:
        fade = _smoothstep((phase - 0.88) / 0.12)
        ring = 0.875
        intensity = 1.0 - fade
        width = 0.10

    if intensity <= 0.001:
        transparent = QPixmap(source.size())
        transparent.fill(Qt.GlobalColor.transparent)
        transparent.setDevicePixelRatio(source.devicePixelRatio())
        return transparent

    radius_px = max(image.width(), image.height()) * 0.53
    mask = QRadialGradient(center_px, radius_px)

    p0 = max(0.0, ring - width * 1.7)
    p1 = max(p0 + 0.001, ring - width)
    p2 = max(p1 + 0.001, ring)
    p3 = min(0.999, max(p2 + 0.001, ring + width))
    p4 = min(1.0, max(p3 + 0.001, ring + width * 1.7))

    center_alpha = round(105 * intensity * max(0.0, 1.0 - ring / 0.24))
    mask.setColorAt(0.0, QColor(255, 255, 255, center_alpha))
    mask.setColorAt(p0, QColor(255, 255, 255, 0))
    mask.setColorAt(p1, QColor(255, 255, 255, round(110 * intensity)))
    mask.setColorAt(p2, QColor(255, 255, 255, round(255 * intensity)))
    mask.setColorAt(p3, QColor(255, 255, 255, round(110 * intensity)))
    mask.setColorAt(p4, QColor(255, 255, 255, 0))
    mask.setColorAt(1.0, QColor(255, 255, 255, 0))

    painter = QPainter(image)
    painter.setCompositionMode(QPainter.CompositionMode.CompositionMode_DestinationIn)
    painter.fillRect(image.rect(), mask)
    painter.end()

    pixmap = QPixmap.fromImage(image)
    pixmap.setDevicePixelRatio(source.devicePixelRatio())
    return pixmap


class AnimatedPolymorphButton(_visual.RefinedPolymorphButton):
    """Long-form arcane hover ambience plus the accepted tactile click motion."""

    _FLECKS = (
        (0.03, 0.74, 0.34, -0.20, 2.8, 0.00),
        (0.18, 0.20, 0.38, 0.08, 1.7, 0.14),
        (0.43, 0.84, -0.24, -0.23, 2.2, 0.29),
        (0.62, 0.12, 0.27, 0.20, 1.5, 0.43),
        (0.88, 0.64, -0.36, -0.11, 2.6, 0.59),
        (1.04, 0.27, -0.40, 0.15, 1.8, 0.76),
        (0.31, 0.55, 0.20, -0.29, 1.3, 0.90),
        (0.73, 0.91, 0.18, -0.31, 1.6, 0.47),
    )
    _LIGHT_FLECKS = (
        (0.08, 0.38, 0.30, -0.16, 1.4, 0.04),
        (0.27, 0.88, -0.15, -0.36, 1.2, 0.22),
        (0.48, 0.16, 0.24, 0.17, 1.0, 0.39),
        (0.69, 0.70, -0.30, -0.14, 1.5, 0.56),
        (0.94, 0.31, -0.34, 0.18, 1.1, 0.71),
        (0.56, 0.95, 0.16, -0.35, 0.9, 0.87),
    )

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setAttribute(Qt.WidgetAttribute.WA_Hover, True)

        self._hover_progress = 0.0
        self._sheen_progress = -0.35
        self._press_progress = 0.0
        self._click_flash = 0.0
        self._click_origin = QPointF()
        self._ambient_progress = 0.0

        self._motion_cache_key: tuple[int, int, int] | None = None
        self._ghost_mark_a = QPixmap()
        self._ghost_mark_b = QPixmap()
        self._foreground_glow = QPixmap()
        self._foreground_center_px = QPointF()

        self._hover_anim = QVariantAnimation(self)
        self._hover_anim.setDuration(190)
        self._hover_anim.setEasingCurve(QEasingCurve.Type.OutCubic)
        self._hover_anim.valueChanged.connect(self._on_hover_value)

        self._sheen_anim = QVariantAnimation(self)
        self._sheen_anim.setDuration(1300)
        self._sheen_anim.setEasingCurve(QEasingCurve.Type.InOutCubic)
        self._sheen_anim.valueChanged.connect(self._on_sheen_value)

        # Long common clock. Integer subdivisions make each sub-loop join cleanly:
        # ghost A = 18 s, ghost B = 27 s, foreground pulse = 6 s.
        self._ambient_anim = QVariantAnimation(self)
        self._ambient_anim.setDuration(54000)
        self._ambient_anim.setStartValue(0.0)
        self._ambient_anim.setEndValue(1.0)
        self._ambient_anim.setLoopCount(-1)
        self._ambient_anim.setEasingCurve(QEasingCurve.Type.Linear)
        self._ambient_anim.valueChanged.connect(self._on_ambient_value)

        self._press_anim = QVariantAnimation(self)
        self._press_anim.setEasingCurve(QEasingCurve.Type.OutCubic)
        self._press_anim.valueChanged.connect(self._on_press_value)

        self._flash_anim = QVariantAnimation(self)
        self._flash_anim.setDuration(230)
        self._flash_anim.setEasingCurve(QEasingCurve.Type.OutCubic)
        self._flash_anim.valueChanged.connect(self._on_flash_value)

    def _on_hover_value(self, value) -> None:
        self._hover_progress = float(value)
        self.update()

    def _on_sheen_value(self, value) -> None:
        self._sheen_progress = float(value)
        self.update()

    def _on_ambient_value(self, value) -> None:
        self._ambient_progress = float(value)
        self.update()

    def _on_press_value(self, value) -> None:
        self._press_progress = float(value)
        self.update()

    def _on_flash_value(self, value) -> None:
        self._click_flash = float(value)
        self.update()

    def _animate_hover(self, target: float) -> None:
        self._hover_anim.stop()
        self._hover_anim.setStartValue(self._hover_progress)
        self._hover_anim.setEndValue(target)
        self._hover_anim.setDuration(190 if target > self._hover_progress else 145)
        self._hover_anim.start()

    def _start_sheen(self) -> None:
        self._sheen_anim.stop()
        self._sheen_progress = -0.35
        self._sheen_anim.setStartValue(-0.35)
        self._sheen_anim.setEndValue(1.35)
        self._sheen_anim.start()

    def _start_ambient(self) -> None:
        self._ambient_anim.stop()
        self._ambient_progress = 0.0
        self._ambient_anim.start()

    def _animate_press(self, target: float) -> None:
        self._press_anim.stop()
        self._press_anim.setStartValue(self._press_progress)
        self._press_anim.setEndValue(target)
        self._press_anim.setDuration(72 if target > self._press_progress else 125)
        self._press_anim.start()

    def _start_click_flash(self) -> None:
        self._flash_anim.stop()
        self._click_flash = 1.0
        self._flash_anim.setStartValue(1.0)
        self._flash_anim.setEndValue(0.0)
        self._flash_anim.start()

    def _ensure_motion_cache(self) -> None:
        key = (self.width(), self.height(), round(self._scale * 1000))
        if key == self._motion_cache_key:
            return
        self._motion_cache_key = key

        ghost_a_size = max(156, round(self.height() * 2.68))
        ghost_b_size = max(108, round(self.height() * 1.78))
        foreground_size = max(62, round(self.height() * 1.42))

        self._ghost_mark_a = _visual._polymorph_mark_pixmap(
            ghost_a_size,
            QColor("#ddb36f"),
            QColor("#54141d"),
            mid_color=QColor("#91483b"),
        )
        self._ghost_mark_b = _visual._polymorph_mark_pixmap(
            ghost_b_size,
            QColor("#c99c5b"),
            QColor("#3b0c13"),
            mid_color=QColor("#714034"),
        )
        self._foreground_glow = _visual._polymorph_mark_pixmap(
            foreground_size,
            QColor("#fff7d9"),
            QColor("#dc843a"),
            mid_color=QColor("#f4cc7f"),
        )
        self._foreground_center_px = _alpha_bounds_center(self._foreground_glow)

    @staticmethod
    def _draw_rotated_pixmap(
        painter: QPainter,
        pixmap: QPixmap,
        center: QPointF,
        rotation: float,
        scale: float,
        opacity: float,
    ) -> None:
        if pixmap.isNull() or opacity <= 0.001:
            return
        dpr = pixmap.devicePixelRatio()
        width = pixmap.width() / dpr
        height = pixmap.height() / dpr
        painter.save()
        painter.setOpacity(opacity)
        painter.translate(center)
        painter.rotate(rotation)
        painter.scale(scale, scale)
        painter.drawPixmap(round(-width / 2.0), round(-height / 2.0), pixmap)
        painter.restore()

    def _draw_fleck_layer(
        self,
        painter: QPainter,
        rect: QRectF,
        hover: float,
        phase: float,
        specs,
        *,
        pale: bool,
    ) -> None:
        for x0, y0, dx, dy, base_radius, offset in specs:
            progress = (phase + offset) % 1.0
            fade = sin(pi * progress) ** 2
            if fade <= 0.01:
                continue

            center = QPointF(
                rect.left() + rect.width() * (x0 + dx * progress),
                rect.top() + rect.height() * (y0 + dy * progress),
            )
            core = max(0.9, base_radius * self._scale)
            glow_radius = core * (2.8 if pale else 2.5)
            alpha = round((62 if pale else 78) * hover * fade)

            fleck = QRadialGradient(center, glow_radius)
            if pale:
                fleck.setColorAt(0.0, QColor(255, 255, 246, alpha))
                fleck.setColorAt(0.24, QColor(255, 239, 201, round(alpha * 0.72)))
                fleck.setColorAt(0.67, QColor(235, 205, 151, round(alpha * 0.18)))
                fleck.setColorAt(1.0, QColor(235, 205, 151, 0))
                core_color = QColor(255, 255, 247, round(alpha * 0.82))
            else:
                fleck.setColorAt(0.0, QColor(255, 243, 208, alpha))
                fleck.setColorAt(0.25, QColor(238, 190, 104, round(alpha * 0.72)))
                fleck.setColorAt(0.65, QColor(205, 111, 71, round(alpha * 0.24)))
                fleck.setColorAt(1.0, QColor(205, 111, 71, 0))
                core_color = QColor(255, 244, 216, round(alpha * 0.72))

            painter.setBrush(fleck)
            painter.drawEllipse(center, glow_radius, glow_radius)
            painter.setBrush(core_color)
            painter.drawEllipse(center, core * 0.34, core * 0.34)

    def _draw_magic_flecks(
        self,
        painter: QPainter,
        rect: QRectF,
        hover: float,
        master_phase: float,
    ) -> None:
        if hover <= 0.001:
            return

        painter.save()
        painter.setPen(Qt.PenStyle.NoPen)
        warm_phase = (master_phase * 10.0) % 1.0
        pale_phase = (master_phase * 7.0 + 0.19) % 1.0
        self._draw_fleck_layer(
            painter, rect, hover, warm_phase, self._FLECKS, pale=False
        )
        self._draw_fleck_layer(
            painter, rect, hover, pale_phase, self._LIGHT_FLECKS, pale=True
        )
        painter.restore()

    def _redraw_text(self, painter: QPainter, rect: QRectF, enabled: bool) -> None:
        title_rect = QRectF(rect).translated(0, -7 * self._scale)
        subtitle_rect = QRectF(rect).translated(0, 14 * self._scale)

        painter.setPen(QColor("#e8bf6e") if enabled else QColor("#776a58"))
        painter.setFont(
            _brand.tracked_font(
                max(9.8, 13.1 * self._scale),
                max(2.2, 4.6 * self._scale),
                bold=False,
            )
        )
        painter.drawText(title_rect, Qt.AlignmentFlag.AlignCenter, "POLYMORPH")

        subtitle_font = QFont("Inter")
        subtitle_font.setPointSizeF(max(5.4, 6.3 * self._scale))
        subtitle_font.setWeight(QFont.Weight.Medium)
        subtitle_font.setLetterSpacing(
            QFont.SpacingType.AbsoluteSpacing,
            max(0.9, 1.55 * self._scale),
        )
        painter.setFont(subtitle_font)
        painter.setPen(QColor("#c99652") if enabled else QColor("#675848"))
        painter.drawText(subtitle_rect, Qt.AlignmentFlag.AlignCenter, "CONVERT MEDIA")

    def enterEvent(self, event) -> None:
        super().enterEvent(event)
        if not self.isEnabled():
            return
        self._animate_hover(1.0)
        self._start_sheen()
        self._start_ambient()

    def leaveEvent(self, event) -> None:
        super().leaveEvent(event)
        self._animate_hover(0.0)
        self._ambient_anim.stop()
        if not self.isDown():
            self._animate_press(0.0)

    def mousePressEvent(self, event) -> None:
        if self.isEnabled() and event.button() == Qt.MouseButton.LeftButton:
            self._click_origin = event.position()
            self._animate_press(1.0)
        super().mousePressEvent(event)

    def mouseReleaseEvent(self, event) -> None:
        clicked_inside = (
            self.isEnabled()
            and event.button() == Qt.MouseButton.LeftButton
            and self.isDown()
            and self.rect().contains(event.position().toPoint())
        )
        self._animate_press(0.0)
        if clicked_inside:
            self._click_origin = event.position()
            self._start_click_flash()
        super().mouseReleaseEvent(event)

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
            glaze = QLinearGradient(rect.left(), rect.top(), rect.left(), rect.bottom())
            glaze.setColorAt(0.0, QColor(255, 239, 204, round(25 * hover)))
            glaze.setColorAt(0.24, QColor(255, 223, 165, round(10 * hover)))
            glaze.setColorAt(0.58, QColor(255, 255, 255, 0))
            glaze.setColorAt(1.0, QColor(0, 0, 0, 0))
            painter.fillPath(path, glaze)

            # Softly suppress the static stable release center-right ghost while hovered so
            # the two animated geometry layers read as motion, not as a third static emblem.
            veil_center = QPointF(
                rect.left() + rect.width() * 0.70,
                rect.center().y(),
            )
            veil = QRadialGradient(
                veil_center,
                max(rect.width() * 0.27, rect.height() * 1.5),
            )
            veil.setColorAt(0.0, QColor(35, 7, 11, round(72 * hover)))
            veil.setColorAt(0.55, QColor(35, 7, 11, round(38 * hover)))
            veil.setColorAt(1.0, QColor(35, 7, 11, 0))
            painter.fillPath(path, veil)

            # Main ghost: one-way clockwise 360° turn every 18 seconds.
            # It begins near the middle, drifts right and grows as if moving closer.
            phase_a = (master * 3.0) % 1.0
            travel_a = _smoothstep(phase_a)
            envelope_a = _loop_envelope(phase_a, 0.08)
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

            # Secondary ghost: clearly smaller, separately anchored, and slower
            # counter-clockwise rotation. Its orbit is periodic and never reverses.
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

            # Six-second one-way pulse: true center -> outer geometry -> edge shine
            # -> fade completely -> restart at center. There is no reverse pass.
            pulse_phase = (master * 9.0) % 1.0
            pulse = _outward_pulse_emblem(
                self._foreground_glow,
                pulse_phase,
                self._foreground_center_px,
            )
            if not pulse.isNull():
                dpr = pulse.devicePixelRatio()
                logical = pulse.width() / dpr
                mark_x = rect.left() + max(8.0, 12.0 * self._scale)
                mark_y = rect.center().y() - logical / 2.0
                if pulse_phase < 0.72:
                    pulse_opacity = 0.30
                elif pulse_phase < 0.88:
                    pulse_opacity = 0.38
                else:
                    pulse_opacity = 0.38 * (1.0 - _smoothstep((pulse_phase - 0.88) / 0.12))
                painter.save()
                painter.setOpacity(pulse_opacity * hover)
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

        # stable release click/press response is intentionally unchanged.
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
            click_pulse.setColorAt(0.0, QColor(255, 222, 153, round(58 * flash)))
            click_pulse.setColorAt(0.28, QColor(231, 171, 78, round(28 * flash)))
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


def install_button_motion_patch() -> None:
    global _INSTALLED
    if _INSTALLED:
        return
    _INSTALLED = True
    _brand.PolymorphButton = AnimatedPolymorphButton
