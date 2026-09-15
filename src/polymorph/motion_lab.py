from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QColor
from PySide6.QtWidgets import (
    QApplication,
    QCheckBox,
    QColorDialog,
    QComboBox,
    QFileDialog,
    QFormLayout,
    QFrame,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QPushButton,
    QScrollArea,
    QSlider,
    QVBoxLayout,
    QWidget,
)

from .motion_button import ArcaneButton
from .motion_effects import load_runic_font
from .motion_loader import ArcaneLoader
from .motion_stage import Stage
from .ui.fonts import load_brand_fonts


class MotionLab(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Polymorph Motion Lab — Element Editor")
        self.resize(1450, 950)
        self.rune_family = load_runic_font()
        self._syncing_editor = False

        root = QWidget()
        self.setCentralWidget(root)
        outer = QHBoxLayout(root)
        outer.setContentsMargins(18, 18, 18, 18)
        outer.setSpacing(18)

        self.stage = Stage()
        stage_layout = QVBoxLayout(self.stage)
        stage_layout.setContentsMargins(34, 22, 34, 26)

        title = QLabel("POLYMORPH MOTION LAB")
        title.setObjectName("LabTitle")
        title.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        stage_layout.addWidget(title)

        subtitle = QLabel("ELDER FUTHARK / LIVE ELEMENT EDITOR")
        subtitle.setObjectName("LabSubtitle")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        stage_layout.addWidget(subtitle)

        self.loader = ArcaneLoader(self.rune_family)
        self.loader.variant = 1
        row = QHBoxLayout()
        row.addStretch()
        row.addWidget(self.loader)
        row.addStretch()
        stage_layout.addLayout(row, 1)

        self.button = ArcaneButton(self.rune_family)
        row = QHBoxLayout()
        row.addStretch()
        row.addWidget(self.button)
        row.addStretch()
        stage_layout.addLayout(row)
        stage_layout.addStretch()
        outer.addWidget(self.stage, 1)

        panel_shell = QFrame()
        panel_shell.setObjectName("Panel")
        panel_shell.setFixedWidth(430)
        shell_layout = QVBoxLayout(panel_shell)
        shell_layout.setContentsMargins(0, 0, 0, 0)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        panel = QWidget()
        panel_layout = QVBoxLayout(panel)
        panel_layout.setContentsMargins(15, 15, 15, 15)
        panel_layout.setSpacing(9)
        scroll.setWidget(panel)
        shell_layout.addWidget(scroll)
        outer.addWidget(panel_shell)

        panel_layout.addWidget(self._section_label("STAGE"))
        form = QFormLayout()
        self.bg = QComboBox()
        self.bg.addItems(Stage.NAMES)
        self.bg.setCurrentIndex(1)
        self.bg.currentIndexChanged.connect(self.background)
        form.addRow("Background", self.bg)

        self.variant = QComboBox()
        self.variant.addItems(ArcaneLoader.VARIANTS)
        self.variant.setCurrentIndex(1)
        self.variant.currentIndexChanged.connect(self.set_variant)
        form.addRow("Study", self.variant)

        self.progress = QSlider(Qt.Orientation.Horizontal)
        self.progress.setRange(0, 100)
        self.progress.setValue(62)
        self.progress.valueChanged.connect(lambda value: self.loader.set_progress(value / 100.0))
        form.addRow("Progress", self.progress)

        self.auto = QCheckBox("Auto loop 0–100% + completion")
        self.auto.setChecked(True)
        form.addRow("", self.auto)
        panel_layout.addLayout(form)

        panel_layout.addWidget(self._section_label("GLOBAL LIGHT / PULSE"))
        self.master_glow = self._add_value_slider(panel_layout, "Master brightness", 20, 180, 100, self.set_master_glow, suffix="%")
        self.master_spread = self._add_value_slider(panel_layout, "Master glow spread", 35, 200, 100, self.set_master_spread, suffix="%")
        self.trace_speed = self._add_value_slider(panel_layout, "Tracer travel speed", 10, 260, 100, self.set_trace_speed, suffix="%")
        self.pulse_speed = self._add_value_slider(panel_layout, "Pulse speed", 10, 250, 100, self.set_pulse_speed, suffix="%")
        self.pulse_trail = self._add_value_slider(panel_layout, "Pulse trail / hold", 5, 95, 46, self.set_pulse_trail, suffix="%")
        self.pulse_end = self._add_value_slider(panel_layout, "Pulse dark-end length", 0, 80, 16, self.set_pulse_end, suffix="%")

        panel_layout.addWidget(self._section_label("ELEMENT EDITOR"))
        self.element = QComboBox()
        for element_id, state in self.loader.editor.elements.items():
            self.element.addItem(state.label, element_id)
        self.element.currentIndexChanged.connect(self.refresh_editor)
        panel_layout.addWidget(self.element)

        self.span = self._add_value_slider(panel_layout, "Expand / contract span", 25, 175, 100, self.set_span, suffix="%")
        self.scale = self._add_value_slider(panel_layout, "Element scale", 25, 220, 100, self.set_scale, suffix="%")
        self.base_rotation = self._add_value_slider(panel_layout, "Base rotation", -180, 180, 0, self.set_base_rotation, suffix="°")

        color_row = QHBoxLayout()
        self.color_button = QPushButton("#FFFFFF")
        self.color_button.clicked.connect(self.pick_color)
        color_row.addWidget(QLabel("Colour"))
        color_row.addStretch()
        color_row.addWidget(self.color_button)
        panel_layout.addLayout(color_row)

        self.link_group = QComboBox()
        self.link_group.addItems(self.loader.editor.LINK_GROUPS)
        self.link_group.currentTextChanged.connect(self.set_link_group)
        link_form = QFormLayout()
        link_form.addRow("Link group", self.link_group)
        panel_layout.addLayout(link_form)

        self.element_brightness = self._add_value_slider(panel_layout, "Element brightness", 0, 220, 100, self.set_element_brightness, suffix="%")
        self.element_glow = self._add_value_slider(panel_layout, "Element glow spread", 10, 250, 100, self.set_element_glow, suffix="%")

        panel_layout.addWidget(self._section_label("ELEMENT ANIMATION"))
        self.spin = self._add_value_slider(
            panel_layout,
            "Rotation direction / speed",
            -200,
            200,
            0,
            self.set_spin,
            formatter=self.format_spin,
        )
        self.static = QCheckBox("Static — disable rotational motion")
        self.static.toggled.connect(self.set_static)
        panel_layout.addWidget(self.static)

        self.pulse = QCheckBox("Include in pulse array")
        self.pulse.toggled.connect(self.set_pulse)
        panel_layout.addWidget(self.pulse)

        self.rune_speed = self._add_value_slider(panel_layout, "Rune transition speed", 0, 250, 0, self.set_rune_speed, suffix="%")

        self.editor_note = QLabel(
            "Controls that do not apply to the selected element are disabled. "
            "Linked elements share span, scale, base rotation, brightness and glow changes."
        )
        self.editor_note.setObjectName("Note")
        self.editor_note.setWordWrap(True)
        panel_layout.addWidget(self.editor_note)

        export_button = QPushButton("Export motion spec…")
        export_button.clicked.connect(self.export_motion_spec)
        panel_layout.addWidget(export_button)
        self.export_status = QLabel("")
        self.export_status.setObjectName("Note")
        self.export_status.setWordWrap(True)
        panel_layout.addWidget(self.export_status)

        panel_layout.addWidget(self._section_label("BUTTON PREVIEW"))
        states = QHBoxLayout()
        for label, state in (("Rest", "rest"), ("Hover", "hover"), ("Pressed", "pressed"), ("Live", None)):
            button = QPushButton(label)
            button.clicked.connect(lambda _=False, selected=state: setattr(self.button, "forced", selected))
            states.addWidget(button)
        panel_layout.addLayout(states)

        debug = QCheckBox("Reveal full button mechanism")
        debug.toggled.connect(self.button.set_debug)
        panel_layout.addWidget(debug)

        background_button = QPushButton("Load custom background…")
        background_button.clicked.connect(self.choose_background)
        panel_layout.addWidget(background_button)

        emblem_button = QPushButton("Load alternate emblem SVG…")
        emblem_button.clicked.connect(self.choose_emblem)
        panel_layout.addWidget(emblem_button)

        self.emblem_status = QLabel("Emblem: bundled Knight Witch SVG" if self.loader.emblem else "Emblem: bundled SVG unavailable")
        self.emblem_status.setObjectName("Note")
        self.emblem_status.setWordWrap(True)
        panel_layout.addWidget(self.emblem_status)
        panel_layout.addStretch()

        self.setStyleSheet(
            "QMainWindow,QWidget{background:#040506;color:#eee8de;font-family:Inter,'Segoe UI';font-size:9.5pt} "
            "QLabel#LabTitle{font-size:18pt;letter-spacing:4px;background:transparent} "
            "QLabel#LabSubtitle{font-size:8pt;letter-spacing:2px;color:#aa9d87;background:transparent} "
            "QLabel#Section{font-size:8.5pt;font-weight:700;letter-spacing:1.5px;color:#d9c397;background:transparent;padding-top:6px} "
            "QFrame#Panel{background:#0b0d10;border:1px solid #34302a;border-radius:5px} "
            "QScrollArea{background:#0b0d10;border:none} QScrollArea>QWidget>QWidget{background:#0b0d10} "
            "QLabel#Note{color:#8e8b86;background:transparent;font-size:8.2pt} "
            "QComboBox,QPushButton{background:#111318;border:1px solid #4d463d;border-radius:4px;padding:6px 8px} "
            "QPushButton:hover,QComboBox:hover{border-color:#cbb17e;background:#171a1f} "
            "QPushButton:disabled,QComboBox:disabled{color:#555;background:#0b0c0f;border-color:#25272b} "
            "QSlider::groove:horizontal{height:4px;background:#17191d;border-radius:2px} "
            "QSlider::sub-page:horizontal{background:#b4212c;border-radius:2px} "
            "QSlider::handle:horizontal{width:12px;margin:-5px 0;border-radius:6px;background:#e7d5ae} "
            "QSlider:disabled::handle:horizontal{background:#4a4a4a} QCheckBox:disabled{color:#555}"
        )

        self.hold = 0
        self.timer = QTimer(self)
        self.timer.setInterval(34)
        self.timer.timeout.connect(self.loop)
        self.timer.start()
        self.refresh_editor()

    def _section_label(self, text: str) -> QLabel:
        label = QLabel(text)
        label.setObjectName("Section")
        return label

    def _add_value_slider(self, layout: QVBoxLayout, label: str, minimum: int, maximum: int, value: int, callback, *, suffix: str = "", formatter=None) -> QSlider:
        row = QHBoxLayout()
        text = QLabel(label)
        value_label = QLabel("")
        value_label.setMinimumWidth(74)
        value_label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        row.addWidget(text)
        row.addStretch()
        row.addWidget(value_label)
        layout.addLayout(row)
        slider = QSlider(Qt.Orientation.Horizontal)
        slider.setRange(minimum, maximum)
        slider.setValue(value)
        slider._value_label = value_label  # type: ignore[attr-defined]
        slider._suffix = suffix  # type: ignore[attr-defined]
        slider._formatter = formatter  # type: ignore[attr-defined]
        slider.valueChanged.connect(callback)
        slider.valueChanged.connect(lambda raw, s=slider: self._update_slider_label(s, raw))
        self._update_slider_label(slider, value)
        layout.addWidget(slider)
        return slider

    def _update_slider_label(self, slider: QSlider, value: int) -> None:
        formatter = getattr(slider, "_formatter", None)
        text = formatter(value) if formatter else f"{value}{getattr(slider, '_suffix', '')}"
        slider._value_label.setText(text)  # type: ignore[attr-defined]

    def format_spin(self, value: int) -> str:
        if value == 0:
            return "STATIC"
        direction = "CW" if value > 0 else "CCW"
        return f"{direction} {abs(value) / 100.0:.2f}×"

    def current_element_id(self) -> str:
        return str(self.element.currentData())

    def current_state(self):
        return self.loader.editor.get(self.current_element_id())

    def _set_slider_safely(self, slider: QSlider, value: int) -> None:
        slider.blockSignals(True)
        slider.setValue(value)
        self._update_slider_label(slider, value)
        slider.blockSignals(False)

    def refresh_editor(self) -> None:
        element_id = self.current_element_id()
        if not element_id:
            return
        state = self.loader.editor.get(element_id)
        editor = self.loader.editor
        self._syncing_editor = True
        self._set_slider_safely(self.span, round(state.spread * 100))
        self._set_slider_safely(self.scale, round(state.scale * 100))
        self._set_slider_safely(self.base_rotation, round(state.base_rotation))
        self._set_slider_safely(self.element_brightness, round(state.brightness * 100))
        self._set_slider_safely(self.element_glow, round(state.glow_spread * 100))
        self._set_slider_safely(self.spin, round(state.spin * 100))
        self._set_slider_safely(self.rune_speed, round(state.rune_speed * 100))

        self.static.blockSignals(True)
        self.static.setChecked(state.static)
        self.static.blockSignals(False)
        self.pulse.blockSignals(True)
        self.pulse.setChecked(state.pulse)
        self.pulse.blockSignals(False)
        self.link_group.blockSignals(True)
        self.link_group.setCurrentText(state.link_group)
        self.link_group.blockSignals(False)

        self.span.setEnabled(editor.supports(element_id, "spread"))
        self.scale.setEnabled(editor.supports(element_id, "scale"))
        self.base_rotation.setEnabled(editor.supports(element_id, "rotation"))
        self.element_brightness.setEnabled(editor.supports(element_id, "brightness"))
        self.element_glow.setEnabled(editor.supports(element_id, "glow"))
        self.static.setEnabled(editor.supports(element_id, "static"))
        self.spin.setEnabled(editor.supports(element_id, "spin") and not state.static)
        self.pulse.setEnabled(editor.supports(element_id, "pulse"))
        self.rune_speed.setEnabled(editor.supports(element_id, "rune_speed"))
        self.link_group.setEnabled(editor.supports(element_id, "link"))
        self.color_button.setEnabled(editor.supports(element_id, "color"))
        self._set_color_button(QColor(state.color))
        self._syncing_editor = False

    def _set_color_button(self, color: QColor) -> None:
        self.color_button.setText(color.name().upper())
        text_color = "#111111" if color.lightness() > 150 else "#f5e8c8"
        self.color_button.setStyleSheet(f"QPushButton{{background:{color.name()};color:{text_color};border:1px solid #6b6255;border-radius:4px;padding:6px 12px}}")

    def _set_element_field(self, field: str, value) -> None:
        if self._syncing_editor:
            return
        self.loader.editor.set_value(self.current_element_id(), field, value)
        self.loader.update()

    def set_span(self, value: int) -> None:
        self._set_element_field("spread", value / 100.0)

    def set_scale(self, value: int) -> None:
        self._set_element_field("scale", value / 100.0)

    def set_base_rotation(self, value: int) -> None:
        self._set_element_field("base_rotation", float(value))

    def set_element_brightness(self, value: int) -> None:
        self._set_element_field("brightness", value / 100.0)

    def set_element_glow(self, value: int) -> None:
        self._set_element_field("glow_spread", value / 100.0)

    def set_spin(self, value: int) -> None:
        self._set_element_field("spin", value / 100.0)

    def set_static(self, checked: bool) -> None:
        self._set_element_field("static", checked)
        self.spin.setEnabled(self.loader.editor.supports(self.current_element_id(), "spin") and not checked)

    def set_pulse(self, checked: bool) -> None:
        self._set_element_field("pulse", checked)

    def set_rune_speed(self, value: int) -> None:
        self._set_element_field("rune_speed", value / 100.0)

    def set_link_group(self, text: str) -> None:
        self._set_element_field("link_group", text)

    def pick_color(self) -> None:
        element_id = self.current_element_id()
        current = self.loader.editor.color(element_id)
        color = QColorDialog.getColor(current, self, f"Colour — {self.current_state().label}")
        if not color.isValid():
            return
        self.loader.editor.set_value(element_id, "color", color.name())
        self._set_color_button(color)
        self.loader.update()

    def set_variant(self, value: int) -> None:
        self.loader.variant = value
        self.loader.update()

    def set_master_glow(self, value: int) -> None:
        self.loader.glow = value / 100.0
        self.loader.update()

    def set_master_spread(self, value: int) -> None:
        self.loader.glow_spread = value / 100.0
        self.loader.update()

    def set_trace_speed(self, value: int) -> None:
        self.loader.trace_speed = value / 100.0
        self.button.trace_speed = value / 100.0
        self.loader.update()

    def set_pulse_speed(self, value: int) -> None:
        self.loader.editor.pulse_speed = value / 100.0
        self.loader.update()

    def set_pulse_trail(self, value: int) -> None:
        self.loader.editor.pulse_trail = value / 100.0
        self.loader.update()

    def set_pulse_end(self, value: int) -> None:
        self.loader.editor.pulse_end_dark = value / 100.0
        self.loader.update()

    def export_motion_spec(self) -> None:
        path, _ = QFileDialog.getSaveFileName(
            self,
            "Export Polymorph motion spec",
            str(Path.home() / "polymorph-motion-spec.json"),
            "JSON files (*.json)",
        )
        if not path:
            return
        payload = self.loader.editor.export()
        payload["study"] = {"index": self.loader.variant, "name": ArcaneLoader.VARIANTS[self.loader.variant]}
        payload["global"] = {
            "master_brightness": self.loader.glow,
            "master_glow_spread": self.loader.glow_spread,
            "tracer_travel_speed": self.loader.trace_speed,
        }
        Path(path).write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
        self.export_status.setText(f"Saved exact motion setup: {Path(path).name}")

    def loop(self) -> None:
        if not self.auto.isChecked():
            return
        if self.progress.value() >= 100:
            self.hold += 1
            if self.hold >= 62:
                self.hold = 0
                self.progress.setValue(0)
        else:
            self.progress.setValue(self.progress.value() + 1)

    def background(self, index: int) -> None:
        if index == 5 and self.stage.custom.isNull():
            self.choose_background()
        else:
            self.stage.index = index
            self.stage.update()

    def choose_background(self) -> None:
        path, _ = QFileDialog.getOpenFileName(self, "Choose preview background", "", "Images (*.png *.jpg *.jpeg *.webp *.bmp)")
        if path and self.stage.load(path):
            self.bg.blockSignals(True)
            self.bg.setCurrentIndex(5)
            self.bg.blockSignals(False)

    def choose_emblem(self) -> None:
        path, _ = QFileDialog.getOpenFileName(self, "Choose emblem SVG", "", "SVG files (*.svg)")
        if not path:
            return
        if self.loader.load_emblem(path):
            self.emblem_status.setText(f"Emblem override: {Path(path).name}")
        else:
            self.emblem_status.setText("Emblem override failed to load.")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--smoke-test", action="store_true")
    args = parser.parse_args(argv)

    app = QApplication(sys.argv[:1])
    load_brand_fonts(app)
    window = MotionLab()
    window.show()

    if args.smoke_test:
        window.loader.variant = 1
        window.loader.set_progress(1.0)
        window.loader.editor.set_value("triangle", "static", True)
        window.loader.editor.set_value("hex_a", "spread", 1.05)
        window.loader.editor.set_value("middle_runes", "rune_speed", 0.5)
        window.button.forced = "hover"
        QTimer.singleShot(220, app.quit)

    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
