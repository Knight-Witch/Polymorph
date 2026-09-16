from __future__ import annotations

import argparse
from copy import deepcopy
import json
import sys
from pathlib import Path

from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QColor
from PySide6.QtWidgets import (
    QAbstractItemView,
    QApplication,
    QCheckBox,
    QColorDialog,
    QComboBox,
    QDoubleSpinBox,
    QFileDialog,
    QFrame,
    QHBoxLayout,
    QInputDialog,
    QLabel,
    QListWidget,
    QListWidgetItem,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QScrollArea,
    QSlider,
    QVBoxLayout,
    QWidget,
)

from .motion_button import ArcaneButton
from .motion_editor import MotionEditorState
from .motion_effects import load_runic_font
from .motion_loader import ArcaneLoader
from .motion_stage import Stage
from .ui.fonts import load_brand_fonts


class NoWheelSlider(QSlider):
    def wheelEvent(self, event) -> None:  # noqa: N802
        event.ignore()


class NoWheelSpinBox(QDoubleSpinBox):
    def wheelEvent(self, event) -> None:  # noqa: N802
        event.ignore()


class NoWheelCombo(QComboBox):
    def wheelEvent(self, event) -> None:  # noqa: N802
        event.ignore()


class NumericControl(QWidget):
    def __init__(
        self,
        label: str,
        minimum: float,
        maximum: float,
        value: float,
        callback,
        reset_callback,
        *,
        step: float = 1.0,
        decimals: int = 0,
        suffix: str = "",
        parent=None,
    ) -> None:
        super().__init__(parent)
        self.minimum = minimum
        self.maximum = maximum
        self.step = step
        self.callback = callback
        self.reset_callback = reset_callback
        self._syncing = False
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(3)
        top = QHBoxLayout()
        top.addWidget(QLabel(label))
        top.addStretch()
        self.spin = NoWheelSpinBox()
        self.spin.setRange(minimum, maximum)
        self.spin.setSingleStep(step)
        self.spin.setDecimals(decimals)
        self.spin.setSuffix(suffix)
        self.spin.setKeyboardTracking(False)
        self.spin.setFixedWidth(108)
        self.reset = QPushButton("↺")
        self.reset.setToolTip("Reset to last saved checkpoint")
        self.reset.setFixedWidth(30)
        top.addWidget(self.spin)
        top.addWidget(self.reset)
        layout.addLayout(top)
        self.slider = NoWheelSlider(Qt.Orientation.Horizontal)
        steps = max(1, round((maximum - minimum) / step))
        self.slider.setRange(0, steps)
        layout.addWidget(self.slider)
        self.spin.valueChanged.connect(self._from_spin)
        self.slider.valueChanged.connect(self._from_slider)
        self.reset.clicked.connect(self._reset)
        self.set_value(value, emit=False)

    def _to_slider(self, value: float) -> int:
        return round((value - self.minimum) / self.step)

    def _from_slider(self, raw: int) -> None:
        if self._syncing:
            return
        value = self.minimum + raw * self.step
        self._syncing = True
        self.spin.setValue(value)
        self._syncing = False
        self.callback(value)

    def _from_spin(self, value: float) -> None:
        if self._syncing:
            return
        self._syncing = True
        self.slider.setValue(self._to_slider(value))
        self._syncing = False
        self.callback(float(value))

    def _reset(self) -> None:
        value = self.reset_callback()
        if value is not None:
            self.set_value(float(value), emit=True)

    def set_value(self, value: float, *, emit: bool = False) -> None:
        value = max(self.minimum, min(self.maximum, value))
        self._syncing = True
        self.spin.setValue(value)
        self.slider.setValue(self._to_slider(value))
        self._syncing = False
        if emit:
            self.callback(value)

    def setEnabled(self, enabled: bool) -> None:  # noqa: N802
        super().setEnabled(enabled)
        self.spin.setEnabled(enabled)
        self.slider.setEnabled(enabled)
        self.reset.setEnabled(enabled)


class MotionLab(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Polymorph Motion Lab — Scene Builder")
        self.resize(1540, 980)
        self.rune_family = load_runic_font()
        self._syncing = False
        self._switching_study = False

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
        subtitle = QLabel("ELDER FUTHARK / LIVE SCENE BUILDER")
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
        panel_shell.setFixedWidth(510)
        shell_layout = QVBoxLayout(panel_shell)
        shell_layout.setContentsMargins(0, 0, 0, 0)
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setFrameShape(QFrame.Shape.NoFrame)
        panel = QWidget()
        self.panel_layout = QVBoxLayout(panel)
        self.panel_layout.setContentsMargins(15, 15, 15, 15)
        self.panel_layout.setSpacing(10)
        self.scroll.setWidget(panel)
        shell_layout.addWidget(self.scroll)
        outer.addWidget(panel_shell)

        self._build_stage_section()
        self._build_global_section()
        self._build_sparkle_section()
        self._build_layer_section()
        self._build_element_section()
        self._build_rune_section()
        self._build_button_section()
        self.panel_layout.addStretch()

        self._apply_style()
        self.hold = 0
        self.timer = QTimer(self)
        self.timer.setInterval(34)
        self.timer.timeout.connect(self.loop)
        self.timer.start()

        self.studies = self._initial_studies()
        self._populate_study_combo(selected=1)
        self._checkpoint = self.capture_workspace()
        self.refresh_everything()

    def _section_label(self, text: str) -> QLabel:
        label = QLabel(text)
        label.setObjectName("Section")
        return label

    def _initial_studies(self) -> list[dict]:
        studies = []
        for index, name in enumerate(ArcaneLoader.VARIANTS):
            editor = MotionEditorState()
            studies.append({
                "name": name,
                "variant": index,
                "editor": editor.export(),
                "global": {"master_brightness": 1.0, "master_glow_spread": 1.0, "tracer_travel_speed": 1.0},
            })
        return studies

    def _build_stage_section(self) -> None:
        self.panel_layout.addWidget(self._section_label("STAGE / PRESETS"))
        self.bg = NoWheelCombo()
        self.bg.addItems(Stage.NAMES)
        self.bg.setCurrentIndex(1)
        self.bg.currentIndexChanged.connect(self.background)
        self._combo_row("Background", self.bg)

        study_row = QHBoxLayout()
        self.study_combo = NoWheelCombo()
        self.study_combo.currentIndexChanged.connect(self.switch_study)
        self.new_study = QPushButton("+ New Study")
        self.new_study.clicked.connect(self.add_study)
        self.rename_study = QPushButton("Rename")
        self.rename_study.clicked.connect(self.rename_current_study)
        study_row.addWidget(self.study_combo, 1)
        study_row.addWidget(self.new_study)
        study_row.addWidget(self.rename_study)
        self.panel_layout.addWidget(QLabel("Study"))
        self.panel_layout.addLayout(study_row)

        self.progress = NumericControl("Progress", 0, 100, 62, lambda v: self.loader.set_progress(v / 100.0), lambda: 62, suffix="%")
        self.panel_layout.addWidget(self.progress)
        self.auto = QCheckBox("Auto loop 0–100% + completion")
        self.auto.setChecked(True)
        self.panel_layout.addWidget(self.auto)

        preset_row = QHBoxLayout()
        load_button = QPushButton("Load preset…")
        load_button.clicked.connect(self.load_preset)
        export_button = QPushButton("Export preset…")
        export_button.clicked.connect(self.export_motion_spec)
        preset_row.addWidget(load_button)
        preset_row.addWidget(export_button)
        self.panel_layout.addLayout(preset_row)

        save_row = QHBoxLayout()
        checkpoint = QPushButton("Save progress checkpoint")
        checkpoint.clicked.connect(self.save_checkpoint)
        revert = QPushButton("Revert all to checkpoint")
        revert.clicked.connect(self.revert_checkpoint)
        save_row.addWidget(checkpoint)
        save_row.addWidget(revert)
        self.panel_layout.addLayout(save_row)
        self.status = QLabel("")
        self.status.setObjectName("Note")
        self.status.setWordWrap(True)
        self.panel_layout.addWidget(self.status)

    def _build_global_section(self) -> None:
        self.panel_layout.addWidget(self._section_label("GLOBAL LIGHT / GEOMETRY PULSE"))
        self.master_glow = self._numeric("Master brightness", 0, 300, 100, self.set_master_glow, lambda: self._checkpoint_global("master_brightness") * 100, suffix="%")
        self.master_spread = self._numeric("Master glow spread", 10, 400, 100, self.set_master_spread, lambda: self._checkpoint_global("master_glow_spread") * 100, suffix="%")
        self.trace_speed = self._numeric("Tracer travel speed", 0, 2000, 100, self.set_trace_speed, lambda: self._checkpoint_global("tracer_travel_speed") * 100, suffix="%")
        self.pulse_speed = self._numeric("Geometry pulse speed", 0, 2000, 100, self.set_pulse_speed, lambda: self._checkpoint_editor_root("pulse", "speed") * 100, suffix="%")
        self.pulse_trail = self._numeric("Geometry pulse trail / hold", 0, 100, 46, self.set_pulse_trail, lambda: self._checkpoint_editor_root("pulse", "trail") * 100, suffix="%")
        self.pulse_end = self._numeric("Geometry pulse dark-end length", 0, 90, 16, self.set_pulse_end, lambda: self._checkpoint_editor_root("pulse", "end_dark") * 100, suffix="%")
        note = QLabel("Pulse membership is intentionally available only on linework / geometry. Rune elements use the rune glimmer/transition system below.")
        note.setObjectName("Note")
        note.setWordWrap(True)
        self.panel_layout.addWidget(note)

    def _build_sparkle_section(self) -> None:
        self.panel_layout.addWidget(self._section_label("BACKGROUND SPARKLE PARTICLES"))
        self.sparkle_enabled, self.sparkle_enabled_reset = self._checkbox_row("Enabled", True, self.set_sparkle_enabled, lambda: bool(self._checkpoint_sparkle("enabled")))
        self.sparkle_spread = self._numeric("Particle spread", 0, 220, 92, lambda v: self.set_sparkle("spread", v / 100), lambda: self._checkpoint_sparkle("spread") * 100, suffix="%")
        self.sparkle_fade = self._numeric("Outer fade softness", 0, 100, 62, lambda v: self.set_sparkle("fade", v / 100), lambda: self._checkpoint_sparkle("fade") * 100, suffix="%")
        self.sparkle_density = self._numeric("Density", 0, 100, 34, lambda v: self.set_sparkle("density", v / 100), lambda: self._checkpoint_sparkle("density") * 100, suffix="%")
        self.sparkle_speed = self._numeric("Sparkle speed", 0, 2000, 100, lambda v: self.set_sparkle("speed", v / 100), lambda: self._checkpoint_sparkle("speed") * 100, suffix="%")
        self.sparkle_brightness = self._numeric("Max particle brightness", 0, 200, 52, lambda v: self.set_sparkle("max_brightness", v / 100), lambda: self._checkpoint_sparkle("max_brightness") * 100, suffix="%")
        self.sparkle_colors = []
        for index in range(1, 4):
            self.sparkle_colors.append(self._color_row(f"Colour {index}", lambda i=index: self.pick_sparkle_color(i), lambda i=index: self.reset_sparkle_color(i)))

    def _build_layer_section(self) -> None:
        self.panel_layout.addWidget(self._section_label("LAYER ORDER — BOTTOM → TOP"))
        self.layers = QListWidget()
        self.layers.setDragDropMode(QAbstractItemView.DragDropMode.InternalMove)
        self.layers.setDefaultDropAction(Qt.DropAction.MoveAction)
        self.layers.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.layers.setMinimumHeight(190)
        self.layers.model().rowsMoved.connect(self.layer_order_changed)
        self.layers.itemSelectionChanged.connect(self.layer_selected)
        self.panel_layout.addWidget(self.layers)

    def _build_element_section(self) -> None:
        self.panel_layout.addWidget(self._section_label("ELEMENT EDITOR"))
        self.element = NoWheelCombo()
        self.element.currentIndexChanged.connect(self.refresh_editor)
        self.panel_layout.addWidget(self.element)
        actions = QHBoxLayout()
        duplicate = QPushButton("Duplicate")
        duplicate.clicked.connect(lambda: self.duplicate_element(False))
        duplicate_group = QPushButton("Duplicate + group")
        duplicate_group.clicked.connect(lambda: self.duplicate_element(True))
        remove = QPushButton("Remove")
        remove.clicked.connect(self.remove_element)
        actions.addWidget(duplicate)
        actions.addWidget(duplicate_group)
        actions.addWidget(remove)
        self.panel_layout.addLayout(actions)

        group_actions = QHBoxLayout()
        clear_group = QPushButton("Clear selected group")
        clear_group.clicked.connect(self.clear_selected_group)
        clear_all = QPushButton("Clear all groups")
        clear_all.clicked.connect(self.clear_all_groups)
        group_actions.addWidget(clear_group)
        group_actions.addWidget(clear_all)
        self.panel_layout.addLayout(group_actions)

        self.span = self._numeric("Expand / contract span", 10, 300, 100, lambda v: self.set_element("spread", v / 100), lambda: self._checkpoint_element("spread") * 100, suffix="%")
        self.scale = self._numeric("Element scale", 10, 400, 100, lambda v: self.set_element("scale", v / 100), lambda: self._checkpoint_element("scale") * 100, suffix="%")
        self.base_rotation = self._numeric("Base rotation", -360, 360, 0, lambda v: self.set_element("base_rotation", v), lambda: self._checkpoint_element("base_rotation"), step=0.1, decimals=1, suffix="°")
        self.main_color = self._color_row("Element colour", self.pick_element_color, lambda: self.reset_element_color("color"))

        self.link_group = NoWheelCombo()
        self.link_group.setEditable(True)
        self.link_group.currentTextChanged.connect(self.set_link_group)
        self.link_reset = self._combo_reset_row("Link group", self.link_group, lambda: self.reset_element_combo("link_group"))

        self.element_brightness = self._numeric("Element brightness", 0, 300, 100, lambda v: self.set_element("brightness", v / 100), lambda: self._checkpoint_element("brightness") * 100, suffix="%")
        self.element_glow = self._numeric("Element glow spread", 0, 400, 100, lambda v: self.set_element("glow_spread", v / 100), lambda: self._checkpoint_element("glow_spread") * 100, suffix="%")
        self.spin = self._numeric("Rotation direction / speed", -2000, 2000, 0, lambda v: self.set_element("spin", v / 100), lambda: self._checkpoint_element("spin") * 100, suffix="%")
        self.static, self.static_reset = self._checkbox_row("Static — disable rotational motion", True, lambda v: self.set_element("static", v), lambda: bool(self._checkpoint_element("static")))
        self.pulse, self.pulse_reset = self._checkbox_row("Include in geometry pulse array", False, lambda v: self.set_element("pulse", v), lambda: bool(self._checkpoint_element("pulse")))

    def _build_rune_section(self) -> None:
        self.panel_layout.addWidget(self._section_label("RUNES — TRANSITIONS / GLIMMER"))
        self.rune_speed = self._numeric("Transition speed", 0, 2000, 0, lambda v: self.set_rune("rune_speed", v / 100), lambda: self._checkpoint_element("rune_speed") * 100, suffix="%")
        self.rune_random = self._numeric("Transition timing randomizer", 0, 100, 72, lambda v: self.set_rune("rune_timing_randomness", v / 100), lambda: self._checkpoint_element("rune_timing_randomness") * 100, suffix="%")
        self.transition_type = NoWheelCombo()
        self.transition_type.addItems(["Fade", "Snap"])
        self.transition_type.currentTextChanged.connect(lambda text: self.set_rune("rune_transition_type", text))
        self._combo_reset_row("Transition type", self.transition_type, lambda: self.reset_element_combo("rune_transition_type"))
        self.fade_bright = self._numeric("Fade bright — hold", 0, 5, 0.70, lambda v: self.set_rune("rune_bright_hold", v), lambda: self._checkpoint_element("rune_bright_hold"), step=0.05, decimals=2, suffix=" s")
        self.fade_dark = self._numeric("Fade dark — hold", 0, 5, 0.14, lambda v: self.set_rune("rune_dark_hold", v), lambda: self._checkpoint_element("rune_dark_hold"), step=0.05, decimals=2, suffix=" s")

        self.panel_layout.addWidget(self._section_label("RUNE GLIMMER RANGE"))
        self.dim_brightness = self._numeric("Dim rune — min brightness", 0, 200, 0, lambda v: self.set_rune("rune_min_brightness", v / 100), lambda: self._checkpoint_element("rune_min_brightness") * 100, suffix="%")
        self.dim_color = self._color_row("Dim rune colour", lambda: self.pick_rune_color("rune_dim_color"), lambda: self.reset_element_color("rune_dim_color"))
        self.bright_brightness = self._numeric("Bright rune — max brightness", 0, 300, 100, lambda v: self.set_rune("rune_max_brightness", v / 100), lambda: self._checkpoint_element("rune_max_brightness") * 100, suffix="%")
        self.bright_color = self._color_row("Bright rune colour", lambda: self.pick_rune_color("rune_bright_color"), lambda: self.reset_element_color("rune_bright_color"))

        self.panel_layout.addWidget(self._section_label("SPECIAL GLIMMER — ACTIVE WHEN TRANSITION SPEED = 0"))
        self.glimmer_type = NoWheelCombo()
        self.glimmer_type.addItems(["None", "Radial", "Twinkle", "Pulse"])
        self.glimmer_type.currentTextChanged.connect(self.set_glimmer_type)
        self._combo_reset_row("Glimmer type", self.glimmer_type, lambda: self.reset_element_combo("glimmer_type"))
        self.radial_speed = self._numeric("Radial speed", 0, 2000, 100, lambda v: self.set_rune("radial_speed", v / 100), lambda: self._checkpoint_element("radial_speed") * 100, suffix="%")
        self.radial_length = self._numeric("Radial length", 1, 100, 28, lambda v: self.set_rune("radial_length", v / 100), lambda: self._checkpoint_element("radial_length") * 100, suffix="%")
        self.radial_fade = self._numeric("Radial fade span", 1, 100, 55, lambda v: self.set_rune("radial_fade_span", v / 100), lambda: self._checkpoint_element("radial_fade_span") * 100, suffix="%")
        self.radial_balance = self._numeric("Radial balance", -100, 100, 0, lambda v: self.set_rune("radial_balance", v / 100), lambda: self._checkpoint_element("radial_balance") * 100, suffix="%")
        self.radial_direction = NoWheelCombo()
        self.radial_direction.addItems(["Counterclockwise", "Clockwise"])
        self.radial_direction.currentIndexChanged.connect(lambda i: self.set_rune("radial_direction", -1 if i == 0 else 1))
        self._combo_reset_row("Radial direction", self.radial_direction, self.reset_radial_direction)
        self.twinkle_speed = self._numeric("Twinkle speed", 0, 2000, 100, lambda v: self.set_rune("twinkle_speed", v / 100), lambda: self._checkpoint_element("twinkle_speed") * 100, suffix="%")
        self.twinkle_random = self._numeric("Twinkle randomness", 0, 100, 80, lambda v: self.set_rune("twinkle_randomness", v / 100), lambda: self._checkpoint_element("twinkle_randomness") * 100, suffix="%")
        self.rune_pulse_speed = self._numeric("Rune pulse speed", 0, 2000, 100, lambda v: self.set_rune("rune_pulse_speed", v / 100), lambda: self._checkpoint_element("rune_pulse_speed") * 100, suffix="%")
        self.rune_pulse_fade = self._numeric("Rune pulse fade span", 1, 100, 55, lambda v: self.set_rune("rune_pulse_fade_span", v / 100), lambda: self._checkpoint_element("rune_pulse_fade_span") * 100, suffix="%")
        self.rune_pulse_balance = self._numeric("Rune pulse balance", -100, 100, 0, lambda v: self.set_rune("rune_pulse_balance", v / 100), lambda: self._checkpoint_element("rune_pulse_balance") * 100, suffix="%")

    def _build_button_section(self) -> None:
        self.panel_layout.addWidget(self._section_label("BUTTON PREVIEW"))
        states = QHBoxLayout()
        for label, state in (("Rest", "rest"), ("Hover", "hover"), ("Pressed", "pressed"), ("Live", None)):
            button = QPushButton(label)
            button.clicked.connect(lambda _=False, selected=state: setattr(self.button, "forced", selected))
            states.addWidget(button)
        self.panel_layout.addLayout(states)
        debug = QCheckBox("Reveal full button mechanism")
        debug.toggled.connect(self.button.set_debug)
        self.panel_layout.addWidget(debug)
        background_button = QPushButton("Load custom background…")
        background_button.clicked.connect(self.choose_background)
        self.panel_layout.addWidget(background_button)
        emblem_button = QPushButton("Load alternate emblem SVG…")
        emblem_button.clicked.connect(self.choose_emblem)
        self.panel_layout.addWidget(emblem_button)
        self.emblem_status = QLabel("Emblem: bundled Knight Witch SVG" if self.loader.emblem else "Emblem: bundled SVG unavailable")
        self.emblem_status.setObjectName("Note")
        self.panel_layout.addWidget(self.emblem_status)

    def _numeric(self, label, minimum, maximum, value, callback, reset_callback, *, step=1.0, decimals=0, suffix="") -> NumericControl:
        control = NumericControl(label, minimum, maximum, value, callback, reset_callback, step=step, decimals=decimals, suffix=suffix)
        self.panel_layout.addWidget(control)
        return control

    def _combo_row(self, label: str, combo: QComboBox) -> None:
        row = QHBoxLayout()
        row.addWidget(QLabel(label))
        row.addStretch()
        row.addWidget(combo, 1)
        self.panel_layout.addLayout(row)

    def _combo_reset_row(self, label: str, combo: QComboBox, resetter) -> QPushButton:
        row = QHBoxLayout()
        row.addWidget(QLabel(label))
        row.addStretch()
        row.addWidget(combo, 1)
        reset = QPushButton("↺")
        reset.setFixedWidth(30)
        reset.setToolTip("Reset to last saved checkpoint")
        reset.clicked.connect(resetter)
        row.addWidget(reset)
        self.panel_layout.addLayout(row)
        return reset

    def _checkbox_row(self, label: str, checked: bool, callback, resetter):
        row = QHBoxLayout()
        box = QCheckBox(label)
        box.setChecked(checked)
        box.toggled.connect(callback)
        reset = QPushButton("↺")
        reset.setFixedWidth(30)
        reset.setToolTip("Reset to last saved checkpoint")
        reset.clicked.connect(lambda: self._reset_checkbox(box, resetter, callback))
        row.addWidget(box, 1)
        row.addWidget(reset)
        self.panel_layout.addLayout(row)
        return box, reset

    def _reset_checkbox(self, box: QCheckBox, resetter, callback) -> None:
        value = bool(resetter())
        box.blockSignals(True)
        box.setChecked(value)
        box.blockSignals(False)
        callback(value)

    def _color_row(self, label: str, picker, resetter):
        row = QHBoxLayout()
        row.addWidget(QLabel(label))
        row.addStretch()
        button = QPushButton("#FFFFFF")
        button.clicked.connect(picker)
        reset = QPushButton("↺")
        reset.setFixedWidth(30)
        reset.clicked.connect(resetter)
        row.addWidget(button)
        row.addWidget(reset)
        self.panel_layout.addLayout(row)
        return button

    def _apply_style(self) -> None:
        self.setStyleSheet(
            "QMainWindow,QWidget{background:#040506;color:#eee8de;font-family:Inter,'Segoe UI';font-size:9.5pt} "
            "QLabel#LabTitle{font-size:18pt;letter-spacing:4px;background:transparent} "
            "QLabel#LabSubtitle{font-size:8pt;letter-spacing:2px;color:#aa9d87;background:transparent} "
            "QLabel#Section{font-size:8.5pt;font-weight:700;letter-spacing:1.5px;color:#d9c397;background:transparent;padding-top:7px} "
            "QFrame#Panel{background:#0b0d10;border:1px solid #34302a;border-radius:5px} "
            "QScrollArea{background:#0b0d10;border:none} QScrollArea>QWidget>QWidget{background:#0b0d10} "
            "QLabel#Note{color:#8e8b86;background:transparent;font-size:8.2pt} "
            "QComboBox,QPushButton,QDoubleSpinBox,QListWidget{background:#111318;border:1px solid #4d463d;border-radius:4px;padding:5px 7px} "
            "QPushButton:hover,QComboBox:hover,QDoubleSpinBox:hover{border-color:#cbb17e;background:#171a1f} "
            "QPushButton:disabled,QComboBox:disabled,QDoubleSpinBox:disabled{color:#555;background:#0b0c0f;border-color:#25272b} "
            "QSlider::groove:horizontal{height:4px;background:#17191d;border-radius:2px} "
            "QSlider::sub-page:horizontal{background:#b4212c;border-radius:2px} "
            "QSlider::handle:horizontal{width:12px;margin:-5px 0;border-radius:6px;background:#e7d5ae} "
            "QSlider:disabled::handle:horizontal{background:#4a4a4a} QCheckBox:disabled{color:#555}"
        )

    def _populate_study_combo(self, selected: int = 0) -> None:
        self._switching_study = True
        self.study_combo.clear()
        for study in self.studies:
            self.study_combo.addItem(study["name"])
        self.study_combo.setCurrentIndex(max(0, min(selected, len(self.studies) - 1)))
        self._switching_study = False
        self.apply_study(self.study_combo.currentIndex())
        self._last_study_index = self.study_combo.currentIndex()

    def _save_current_study(self) -> None:
        index = self.study_combo.currentIndex()
        if index < 0 or index >= len(self.studies):
            return
        record = self.studies[index]
        record["variant"] = self.loader.variant
        record["editor"] = deepcopy(self.loader.editor.export())
        record["global"] = {
            "master_brightness": self.loader.glow,
            "master_glow_spread": self.loader.glow_spread,
            "tracer_travel_speed": self.loader.trace_speed,
        }

    def apply_study(self, index: int) -> None:
        if index < 0 or index >= len(self.studies):
            return
        record = self.studies[index]
        self.loader.variant = int(record.get("variant", 1))
        editor = MotionEditorState()
        editor.load(deepcopy(record["editor"]))
        self.loader.editor = editor
        global_state = record.get("global", {})
        self.loader.glow = float(global_state.get("master_brightness", 1.0))
        self.loader.glow_spread = float(global_state.get("master_glow_spread", 1.0))
        self.loader.trace_speed = float(global_state.get("tracer_travel_speed", 1.0))
        self.button.trace_speed = self.loader.trace_speed
        self.refresh_everything()
        self.loader.update()

    def switch_study(self, index: int) -> None:
        if self._switching_study:
            return
        previous = getattr(self, "_last_study_index", None)
        if previous is not None and 0 <= previous < len(self.studies):
            current_index = self.study_combo.currentIndex()
            self.study_combo.blockSignals(True)
            self.study_combo.setCurrentIndex(previous)
            self._save_current_study()
            self.study_combo.setCurrentIndex(current_index)
            self.study_combo.blockSignals(False)
        self.apply_study(index)
        self._last_study_index = index

    def add_study(self) -> None:
        self._save_current_study()
        name, ok = QInputDialog.getText(self, "New study", "Study name:", text=f"{self.study_combo.currentText()} Copy")
        if not ok or not name.strip():
            return
        name = self._unique_study_name(name.strip())
        clone = deepcopy(self.studies[self.study_combo.currentIndex()])
        clone["name"] = name
        self.studies.append(clone)
        self._populate_study_combo(len(self.studies) - 1)
        self.save_checkpoint()

    def rename_current_study(self) -> None:
        self._save_current_study()
        index = self.study_combo.currentIndex()
        if index < 0:
            return
        name, ok = QInputDialog.getText(self, "Rename study", "Study name:", text=self.studies[index]["name"])
        if not ok or not name.strip():
            return
        self.studies[index]["name"] = self._unique_study_name(name.strip(), ignore=index)
        self._populate_study_combo(index)

    def _unique_study_name(self, name: str, ignore: int | None = None) -> str:
        names = {study["name"] for i, study in enumerate(self.studies) if i != ignore}
        if name not in names:
            return name
        index = 2
        while f"{name} {index}" in names:
            index += 1
        return f"{name} {index}"

    def capture_workspace(self) -> dict:
        self._save_current_study()
        return {
            "format": "polymorph-motion-workspace",
            "version": 2,
            "selected_study": self.study_combo.currentIndex(),
            "studies": deepcopy(self.studies),
        }

    def save_checkpoint(self) -> None:
        self._checkpoint = self.capture_workspace()
        self.status.setText("Progress checkpoint saved. Field reset buttons now return to this point.")

    def revert_checkpoint(self) -> None:
        self.load_workspace(deepcopy(self._checkpoint), checkpoint=False)
        self.status.setText("Reverted to the saved progress checkpoint.")

    def load_workspace(self, payload: dict, *, checkpoint: bool = True) -> None:
        if payload.get("format") == "polymorph-motion-workspace":
            studies = payload.get("studies", [])
            if not studies:
                raise ValueError("Workspace contains no studies")
            self.studies = deepcopy(studies)
            selected = int(payload.get("selected_study", 0))
            self._populate_study_combo(selected)
        else:
            editor = MotionEditorState()
            editor.load(payload)
            index = self.study_combo.currentIndex()
            if index < 0:
                index = 0
            record = self.studies[index]
            record["editor"] = editor.export()
            study_info = payload.get("study", {})
            if isinstance(study_info, dict):
                record["variant"] = int(study_info.get("index", record.get("variant", 1)))
                if study_info.get("name"):
                    record["name"] = str(study_info["name"])
            global_state = payload.get("global", {})
            if isinstance(global_state, dict):
                record["global"] = {
                    "master_brightness": float(global_state.get("master_brightness", 1.0)),
                    "master_glow_spread": float(global_state.get("master_glow_spread", 1.0)),
                    "tracer_travel_speed": float(global_state.get("tracer_travel_speed", 1.0)),
                }
            self._populate_study_combo(index)
        if checkpoint:
            self._checkpoint = self.capture_workspace()

    def load_preset(self) -> None:
        path, _ = QFileDialog.getOpenFileName(self, "Load Polymorph motion preset", "", "JSON files (*.json)")
        if not path:
            return
        try:
            payload = json.loads(Path(path).read_text(encoding="utf-8"))
            self.load_workspace(payload)
        except Exception as exc:
            QMessageBox.critical(self, "Preset load failed", str(exc))
            return
        self.status.setText(f"Loaded {Path(path).name}. Existing values were preserved where the old preset format had them.")

    def export_motion_spec(self) -> None:
        path, _ = QFileDialog.getSaveFileName(self, "Export Polymorph motion workspace", str(Path.home() / "polymorph-motion-workspace.json"), "JSON files (*.json)")
        if not path:
            return
        payload = self.capture_workspace()
        Path(path).write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
        self.status.setText(f"Saved exact workspace: {Path(path).name}")

    def current_element_id(self) -> str:
        return str(self.element.currentData() or "")

    def current_state(self):
        element_id = self.current_element_id()
        return self.loader.editor.get(element_id) if element_id in self.loader.editor.elements else None

    def refresh_everything(self) -> None:
        self._syncing = True
        self.master_glow.set_value(self.loader.glow * 100)
        self.master_spread.set_value(self.loader.glow_spread * 100)
        self.trace_speed.set_value(self.loader.trace_speed * 100)
        self.pulse_speed.set_value(self.loader.editor.pulse_speed * 100)
        self.pulse_trail.set_value(self.loader.editor.pulse_trail * 100)
        self.pulse_end.set_value(self.loader.editor.pulse_end_dark * 100)
        self.refresh_sparkles()
        self.refresh_elements()
        self._syncing = False
        self.refresh_editor()

    def refresh_elements(self, select_id: str | None = None) -> None:
        current = select_id or self.current_element_id()
        self.element.blockSignals(True)
        self.element.clear()
        for element_id, state in self.loader.editor.elements.items():
            self.element.addItem(state.label, element_id)
        target_index = self.element.findData(current)
        self.element.setCurrentIndex(target_index if target_index >= 0 else 0)
        self.element.blockSignals(False)
        self.refresh_groups()
        self.refresh_layers(current)

    def refresh_groups(self) -> None:
        current = self.link_group.currentText() if hasattr(self, "link_group") else "None"
        self.link_group.blockSignals(True)
        self.link_group.clear()
        self.link_group.addItems(self.loader.editor.link_groups())
        self.link_group.setCurrentText(current)
        self.link_group.blockSignals(False)

    def refresh_layers(self, select_id: str | None = None) -> None:
        self.layers.blockSignals(True)
        self.layers.clear()
        for element_id in self.loader.editor.layer_order:
            if element_id not in self.loader.editor.elements:
                continue
            item = QListWidgetItem(self.loader.editor.get(element_id).label)
            item.setData(Qt.ItemDataRole.UserRole, element_id)
            self.layers.addItem(item)
            if element_id == select_id:
                item.setSelected(True)
        self.layers.blockSignals(False)

    def layer_order_changed(self, *_args) -> None:
        if self._syncing:
            return
        self.loader.editor.layer_order = [str(self.layers.item(index).data(Qt.ItemDataRole.UserRole)) for index in range(self.layers.count())]
        self.loader.update()

    def layer_selected(self) -> None:
        items = self.layers.selectedItems()
        if not items:
            return
        element_id = str(items[0].data(Qt.ItemDataRole.UserRole))
        index = self.element.findData(element_id)
        if index >= 0:
            self.element.setCurrentIndex(index)

    def refresh_editor(self) -> None:
        state = self.current_state()
        if state is None:
            return
        element_id = self.current_element_id()
        editor = self.loader.editor
        self._syncing = True
        self.span.set_value(state.spread * 100)
        self.scale.set_value(state.scale * 100)
        self.base_rotation.set_value(state.base_rotation)
        self.element_brightness.set_value(state.brightness * 100)
        self.element_glow.set_value(state.glow_spread * 100)
        self.spin.set_value(state.spin * 100)
        self._set_checkbox(self.static, state.static)
        self._set_checkbox(self.pulse, state.pulse)
        self.link_group.setCurrentText(state.link_group)
        self._set_color_button(self.main_color, QColor(state.color))

        self.rune_speed.set_value(state.rune_speed * 100)
        self.rune_random.set_value(state.rune_timing_randomness * 100)
        self.transition_type.setCurrentText(state.rune_transition_type)
        self.fade_bright.set_value(state.rune_bright_hold)
        self.fade_dark.set_value(state.rune_dark_hold)
        self.dim_brightness.set_value(state.rune_min_brightness * 100)
        self.bright_brightness.set_value(state.rune_max_brightness * 100)
        self._set_color_button(self.dim_color, QColor(state.rune_dim_color))
        self._set_color_button(self.bright_color, QColor(state.rune_bright_color))
        self.glimmer_type.setCurrentText(state.glimmer_type)
        self.radial_speed.set_value(state.radial_speed * 100)
        self.radial_length.set_value(state.radial_length * 100)
        self.radial_fade.set_value(state.radial_fade_span * 100)
        self.radial_balance.set_value(state.radial_balance * 100)
        self.radial_direction.setCurrentIndex(1 if state.radial_direction >= 0 else 0)
        self.twinkle_speed.set_value(state.twinkle_speed * 100)
        self.twinkle_random.set_value(state.twinkle_randomness * 100)
        self.rune_pulse_speed.set_value(state.rune_pulse_speed * 100)
        self.rune_pulse_fade.set_value(state.rune_pulse_fade_span * 100)
        self.rune_pulse_balance.set_value(state.rune_pulse_balance * 100)

        self.span.setEnabled(editor.supports(element_id, "spread"))
        self.scale.setEnabled(editor.supports(element_id, "scale"))
        self.base_rotation.setEnabled(editor.supports(element_id, "rotation"))
        self.element_brightness.setEnabled(editor.supports(element_id, "brightness"))
        self.element_glow.setEnabled(editor.supports(element_id, "glow"))
        self.main_color.setEnabled(editor.supports(element_id, "color"))
        self.link_group.setEnabled(editor.supports(element_id, "link"))
        self.static.setEnabled(editor.supports(element_id, "static"))
        self.static_reset.setEnabled(editor.supports(element_id, "static"))
        self.spin.setEnabled(editor.supports(element_id, "spin") and not state.static)
        self.pulse.setEnabled(editor.supports(element_id, "pulse"))
        self.pulse_reset.setEnabled(editor.supports(element_id, "pulse"))
        rune_enabled = editor.supports(element_id, "rune_transition")
        for control in self._rune_controls():
            control.setEnabled(rune_enabled)
        special = rune_enabled and state.rune_speed <= 0.001
        self.glimmer_type.setEnabled(special)
        self._set_special_glimmer_enabled(state.glimmer_type if special else "None", special)
        self._syncing = False

    def _rune_controls(self):
        return [
            self.rune_speed, self.rune_random, self.transition_type, self.fade_bright, self.fade_dark,
            self.dim_brightness, self.dim_color, self.bright_brightness, self.bright_color,
            self.glimmer_type, self.radial_speed, self.radial_length, self.radial_fade, self.radial_balance,
            self.radial_direction, self.twinkle_speed, self.twinkle_random,
            self.rune_pulse_speed, self.rune_pulse_fade, self.rune_pulse_balance,
        ]

    def _set_special_glimmer_enabled(self, mode: str, special: bool = True) -> None:
        radial = special and mode == "Radial"
        twinkle = special and mode == "Twinkle"
        pulse = special and mode == "Pulse"
        for control in (self.radial_speed, self.radial_length, self.radial_fade, self.radial_balance, self.radial_direction):
            control.setEnabled(radial)
        for control in (self.twinkle_speed, self.twinkle_random):
            control.setEnabled(twinkle)
        for control in (self.rune_pulse_speed, self.rune_pulse_fade, self.rune_pulse_balance):
            control.setEnabled(pulse)

    def refresh_sparkles(self) -> None:
        state = self.loader.editor.sparkles
        self._set_checkbox(self.sparkle_enabled, state.enabled)
        self.sparkle_spread.set_value(state.spread * 100)
        self.sparkle_fade.set_value(state.fade * 100)
        self.sparkle_density.set_value(state.density * 100)
        self.sparkle_speed.set_value(state.speed * 100)
        self.sparkle_brightness.set_value(state.max_brightness * 100)
        for button, value in zip(self.sparkle_colors, (state.color_1, state.color_2, state.color_3)):
            self._set_color_button(button, QColor(value))

    def _set_checkbox(self, box: QCheckBox, checked: bool) -> None:
        box.blockSignals(True)
        box.setChecked(checked)
        box.blockSignals(False)

    def set_element(self, field: str, value) -> None:
        if self._syncing or not self.current_element_id():
            return
        self.loader.editor.set_value(self.current_element_id(), field, value)
        if field in {"link_group", "spread", "scale", "base_rotation", "brightness", "glow_spread"}:
            self.refresh_groups()
        self.loader.update()
        if field in {"static", "rune_speed"}:
            self.refresh_editor()

    def set_rune(self, field: str, value) -> None:
        self.set_element(field, value)

    def set_glimmer_type(self, text: str) -> None:
        self.set_rune("glimmer_type", text)
        if not self._syncing:
            self._set_special_glimmer_enabled(text, self.current_state() is not None and self.current_state().rune_speed <= 0.001)

    def set_link_group(self, text: str) -> None:
        if not self._syncing and self.current_element_id():
            self.loader.editor.set_value(self.current_element_id(), "link_group", text.strip() or "None")
            self.refresh_groups()

    def duplicate_element(self, with_group: bool) -> None:
        element_id = self.current_element_id()
        if not element_id:
            return
        new_id = self.loader.editor.duplicate_element_with_group(element_id) if with_group else self.loader.editor.duplicate_element(element_id)
        self.refresh_elements(new_id)
        self.refresh_editor()
        self.loader.update()

    def remove_element(self) -> None:
        element_id = self.current_element_id()
        if not element_id:
            return
        self.loader.editor.remove_element(element_id)
        self.refresh_elements()
        self.refresh_editor()
        self.loader.update()

    def clear_selected_group(self) -> None:
        state = self.current_state()
        if state is None:
            return
        self.loader.editor.clear_group(state.link_group)
        self.refresh_groups()
        self.refresh_editor()

    def clear_all_groups(self) -> None:
        self.loader.editor.clear_all_groups()
        self.refresh_groups()
        self.refresh_editor()

    def pick_element_color(self) -> None:
        state = self.current_state()
        if state is None:
            return
        color = QColorDialog.getColor(QColor(state.color), self, f"Element colour — {state.label}")
        if color.isValid():
            self.set_element("color", color.name())
            self._set_color_button(self.main_color, color)
            self._set_color_button(self.bright_color, color)

    def pick_rune_color(self, field: str) -> None:
        state = self.current_state()
        if state is None:
            return
        current = QColor(getattr(state, field))
        color = QColorDialog.getColor(current, self, field.replace("_", " ").title())
        if color.isValid():
            self.set_rune(field, color.name())
            self._set_color_button(self.dim_color if field == "rune_dim_color" else self.bright_color, color)

    def pick_sparkle_color(self, index: int) -> None:
        field = f"color_{index}"
        state = self.loader.editor.sparkles
        color = QColorDialog.getColor(QColor(getattr(state, field)), self, f"Sparkle colour {index}")
        if color.isValid():
            setattr(state, field, color.name())
            self._set_color_button(self.sparkle_colors[index - 1], color)
            self.loader.update()

    def _set_color_button(self, button: QPushButton, color: QColor) -> None:
        button.setText(color.name().upper())
        text_color = "#111111" if color.lightness() > 150 else "#f5e8c8"
        button.setStyleSheet(f"QPushButton{{background:{color.name()};color:{text_color};border:1px solid #6b6255;border-radius:4px;padding:6px 12px}}")

    def set_master_glow(self, value: float) -> None:
        if not self._syncing:
            self.loader.glow = value / 100.0
            self.loader.update()

    def set_master_spread(self, value: float) -> None:
        if not self._syncing:
            self.loader.glow_spread = value / 100.0
            self.loader.update()

    def set_trace_speed(self, value: float) -> None:
        if not self._syncing:
            self.loader.trace_speed = value / 100.0
            self.button.trace_speed = value / 100.0
            self.loader.update()

    def set_pulse_speed(self, value: float) -> None:
        if not self._syncing:
            self.loader.editor.pulse_speed = value / 100.0
            self.loader.update()

    def set_pulse_trail(self, value: float) -> None:
        if not self._syncing:
            self.loader.editor.pulse_trail = value / 100.0
            self.loader.update()

    def set_pulse_end(self, value: float) -> None:
        if not self._syncing:
            self.loader.editor.pulse_end_dark = value / 100.0
            self.loader.update()

    def set_sparkle_enabled(self, checked: bool) -> None:
        if not self._syncing:
            self.loader.editor.sparkles.enabled = checked
            self.loader.update()

    def set_sparkle(self, field: str, value: float) -> None:
        if not self._syncing:
            setattr(self.loader.editor.sparkles, field, value)
            self.loader.update()

    def _checkpoint_record(self) -> dict | None:
        name = self.study_combo.currentText()
        for study in self._checkpoint.get("studies", []):
            if study.get("name") == name:
                return study
        return None

    def _checkpoint_element(self, field: str):
        record = self._checkpoint_record()
        state = self.current_state()
        if record and self.current_element_id() in record.get("editor", {}).get("elements", {}):
            return record["editor"]["elements"][self.current_element_id()].get(field, getattr(state, field))
        return getattr(state, field) if state is not None else 0

    def _checkpoint_global(self, field: str):
        record = self._checkpoint_record()
        if record:
            return record.get("global", {}).get(field, 1.0)
        return 1.0

    def _checkpoint_editor_root(self, section: str, field: str):
        record = self._checkpoint_record()
        if record:
            return record.get("editor", {}).get(section, {}).get(field, 0.0)
        return 0.0

    def _checkpoint_sparkle(self, field: str):
        record = self._checkpoint_record()
        current = getattr(self.loader.editor.sparkles, field)
        if record:
            return record.get("editor", {}).get("sparkles", {}).get(field, current)
        return current

    def reset_element_color(self, field: str) -> None:
        value = str(self._checkpoint_element(field))
        self.set_rune(field, value) if field.startswith("rune_") else self.set_element(field, value)
        button = self.main_color if field == "color" else self.dim_color if field == "rune_dim_color" else self.bright_color
        self._set_color_button(button, QColor(value))

    def reset_sparkle_color(self, index: int) -> None:
        field = f"color_{index}"
        value = str(self._checkpoint_sparkle(field))
        setattr(self.loader.editor.sparkles, field, value)
        self._set_color_button(self.sparkle_colors[index - 1], QColor(value))
        self.loader.update()

    def reset_element_combo(self, field: str) -> None:
        value = self._checkpoint_element(field)
        if field == "link_group":
            self.link_group.setCurrentText(str(value))
            self.set_link_group(str(value))
        elif field == "rune_transition_type":
            self.transition_type.setCurrentText(str(value))
            self.set_rune(field, str(value))
        elif field == "glimmer_type":
            self.glimmer_type.setCurrentText(str(value))
            self.set_glimmer_type(str(value))

    def reset_radial_direction(self) -> None:
        value = int(self._checkpoint_element("radial_direction"))
        self.radial_direction.setCurrentIndex(1 if value >= 0 else 0)
        self.set_rune("radial_direction", value)

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
        if path and self.loader.load_emblem(path):
            self.emblem_status.setText(f"Emblem override: {Path(path).name}")

    def loop(self) -> None:
        if not self.auto.isChecked():
            return
        value = self.progress.spin.value()
        if value >= 100:
            self.hold += 1
            if self.hold >= 62:
                self.hold = 0
                self.progress.set_value(0, emit=True)
        else:
            self.progress.set_value(value + 1, emit=True)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--smoke-test", action="store_true")
    args = parser.parse_args(argv)
    app = QApplication(sys.argv[:1])
    load_brand_fonts(app)
    window = MotionLab()
    window.show()
    if args.smoke_test:
        window.loader.set_progress(1.0)
        window.loader.editor.set_value("triangle", "static", True)
        window.loader.editor.set_value("hex_a", "spin", -4.0)
        window.loader.editor.set_value("middle_runes", "rune_speed", 0.0)
        window.loader.editor.set_value("middle_runes", "glimmer_type", "Radial")
        window.button.forced = "hover"
        QTimer.singleShot(260, app.quit)
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
