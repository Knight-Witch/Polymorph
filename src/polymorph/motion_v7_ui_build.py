from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtGui import QColor
from PySide6.QtWidgets import QColorDialog, QHBoxLayout, QLabel, QPushButton

from . import motion_lab as base_lab


class V7UIBuildMixin:
    def _section_label(self, text: str) -> QLabel:
        label = super()._section_label(text)
        label.setToolTip(text.replace(" / ", " — "))
        return label

    def _color_row(self, label: str, picker, resetter):
        row = QHBoxLayout()
        caption = QLabel(label)
        caption.setToolTip(f"Choose {label.lower()}; Ø clears it to fully transparent.")
        row.addWidget(caption)
        row.addStretch()
        button = QPushButton("#FFFFFF")
        button.clicked.connect(picker)
        clear = QPushButton("Ø")
        clear.setFixedWidth(30)
        clear.setToolTip("Clear this color to full transparency")
        if label == "Element colour":
            clear.clicked.connect(lambda: self.clear_element_color("color"))
        elif label == "Dim rune colour":
            clear.clicked.connect(lambda: self.clear_element_color("rune_dim_color"))
        elif label == "Bright rune colour":
            clear.clicked.connect(lambda: self.clear_element_color("rune_bright_color"))
        elif label.startswith("Colour "):
            try:
                index = int(label.rsplit(" ", 1)[1])
            except ValueError:
                index = 1
            clear.clicked.connect(lambda _=False, i=index: self.clear_sparkle_color(i))
        reset = QPushButton("↺")
        reset.setFixedWidth(30)
        reset.setToolTip("Reset to last saved checkpoint")
        reset.clicked.connect(resetter)
        row.addWidget(button)
        row.addWidget(clear)
        row.addWidget(reset)
        self.panel_layout.addLayout(row)
        return button

    def _build_stage_section(self) -> None:
        super()._build_stage_section()
        row = QHBoxLayout()
        self.undo_button = QPushButton("Undo")
        self.undo_button.setToolTip("Undo the last edit (Ctrl+Z)")
        self.undo_button.clicked.connect(self.undo)
        self.redo_button = QPushButton("Redo")
        self.redo_button.setToolTip("Redo the last undone edit (Ctrl+Y / Ctrl+Shift+Z)")
        self.redo_button.clicked.connect(self.redo)
        row.addWidget(self.undo_button)
        row.addWidget(self.redo_button)
        self.panel_layout.addLayout(row)

    def _build_global_section(self) -> None:
        super()._build_global_section()
        self.geometry_pulse_enabled, self.geometry_pulse_enabled_reset = self._checkbox_row(
            "Geometry pulse enabled",
            True,
            self.set_geometry_pulse_enabled,
            lambda: bool(self._checkpoint_editor_root("pulse", "enabled")),
        )
        self.geometry_pulse_enabled.setToolTip("Suspend/resume the geometry pulse without changing its membership or order.")
        pulse_order = QPushButton("Geometry pulse order…")
        pulse_order.setToolTip("Open a drag/drop editor for the order in which pulse-enabled geometry fires.")
        pulse_order.clicked.connect(self.open_pulse_order_dialog)
        self.panel_layout.addWidget(pulse_order)

    def _build_layer_section(self) -> None:
        super()._build_layer_section()
        self.layers.setToolTip("Bottom → top render order. Click to edit, drag to reorder, double-click to rename.")
        self.layers.itemDoubleClicked.connect(lambda _item: self.rename_selected_layer())

    def _build_element_section(self) -> None:
        super()._build_element_section()
        self.element.hide()
        actions = QHBoxLayout()
        rename_layer = QPushButton("Rename layer")
        rename_layer.clicked.connect(self.rename_selected_layer)
        rename_group = QPushButton("Rename group")
        rename_group.clicked.connect(self.rename_selected_group)
        group_hierarchy = QPushButton("Group hierarchy…")
        group_hierarchy.setToolTip("Open an expandable drag/drop view of link groups and their member layers.")
        group_hierarchy.clicked.connect(self.open_group_hierarchy_dialog)
        actions.addWidget(rename_layer)
        actions.addWidget(rename_group)
        actions.addWidget(group_hierarchy)
        self.panel_layout.addLayout(actions)

        self.panel_layout.addWidget(self._section_label("SELECTED LAYER — SPECIAL"))
        self.element_enabled, self.element_enabled_reset = self._checkbox_row(
            "Layer enabled / visible",
            True,
            lambda value: self.set_element("enabled", value),
            lambda: bool(self._checkpoint_element("enabled")),
        )
        self.opaque_alpha = self._numeric(
            "Opaque fill opacity", 0, 100, 100,
            lambda value: self.set_element("opaque_fill_alpha", value / 100.0),
            lambda: float(self._checkpoint_element("opaque_fill_alpha")) * 100.0,
            suffix="%",
        )
        self.loader_ring_type = base_lab.NoWheelCombo()
        self.loader_ring_type.addItems(["Static Ring", "Progress Arc", "Gradient Tail"])
        self.loader_ring_type.currentTextChanged.connect(lambda text: self.set_element("loader_ring_type", text))
        self._combo_reset_row("Loading ring type", self.loader_ring_type, lambda: self.reset_v7_combo("loader_ring_type"))
        self.loader_tail_length = self._numeric(
            "Loading tail length", 1, 100, 28,
            lambda value: self.set_element("loader_tail_length", value / 100.0),
            lambda: float(self._checkpoint_element("loader_tail_length")) * 100.0,
            suffix="%",
        )
        self.loader_tail_fade = self._numeric(
            "Loading tail fade span", 1, 100, 60,
            lambda value: self.set_element("loader_tail_fade_span", value / 100.0),
            lambda: float(self._checkpoint_element("loader_tail_fade_span")) * 100.0,
            suffix="%",
        )
        self.loader_tail_balance = self._numeric(
            "Loading tail balance", -100, 100, 0,
            lambda value: self.set_element("loader_tail_balance", value / 100.0),
            lambda: float(self._checkpoint_element("loader_tail_balance")) * 100.0,
            suffix="%",
        )
        self.tracer_length = self._numeric(
            "Tracer length", 1, 140, 60,
            lambda value: self.set_element("tracer_length", value / 100.0),
            lambda: float(self._checkpoint_element("tracer_length")) * 100.0,
            suffix="%",
        )
        self.tracer_fade = self._numeric(
            "Tracer gradient fade", 1, 100, 60,
            lambda value: self.set_element("tracer_fade_span", value / 100.0),
            lambda: float(self._checkpoint_element("tracer_fade_span")) * 100.0,
            suffix="%",
        )
        self.tracer_balance = self._numeric(
            "Tracer front / back balance", -100, 100, 0,
            lambda value: self.set_element("tracer_balance", value / 100.0),
            lambda: float(self._checkpoint_element("tracer_balance")) * 100.0,
            suffix="%",
        )

    def _build_rune_section(self) -> None:
        super()._build_rune_section()
        self.panel_layout.addWidget(self._section_label("RUNE EFFECT ENABLES / STYLE"))
        self.rune_transition_enabled, self.rune_transition_enabled_reset = self._checkbox_row(
            "Rune transitions enabled",
            True,
            lambda value: self.set_rune("rune_transition_enabled", value),
            lambda: bool(self._checkpoint_element("rune_transition_enabled")),
        )
        self.rune_glimmer_enabled, self.rune_glimmer_enabled_reset = self._checkbox_row(
            "Rune glimmer enabled",
            True,
            lambda value: self.set_rune("rune_glimmer_enabled", value),
            lambda: bool(self._checkpoint_element("rune_glimmer_enabled")),
        )
        self.rune_render_mode = base_lab.NoWheelCombo()
        self.rune_render_mode.addItems(["Outline", "Solid"])
        self.rune_render_mode.currentTextChanged.connect(lambda text: self.set_rune("rune_render_mode", text))
        self._combo_reset_row("Rune render", self.rune_render_mode, lambda: self.reset_v7_combo("rune_render_mode"))
        self.rune_weight = base_lab.NoWheelCombo()
        self.rune_weight.addItems(["Thin", "Regular", "Bold"])
        self.rune_weight.currentTextChanged.connect(lambda text: self.set_rune("rune_weight", text))
        self._combo_reset_row("Rune weight", self.rune_weight, lambda: self.reset_v7_combo("rune_weight"))

    def _apply_style(self) -> None:
        super()._apply_style()
        self.setStyleSheet(self.styleSheet() + (
            " QLabel#Section{font-size:8.6pt;font-weight:750;letter-spacing:1.5px;"
            "color:#f0d9aa;background:#111318;border:1px solid #2f343d;"
            "border-radius:4px;padding:8px 10px;margin-top:8px}"
        ))

    def current_element_id(self) -> str:
        items = self.layers.selectedItems() if hasattr(self, "layers") else []
        if items:
            return str(items[0].data(Qt.ItemDataRole.UserRole) or "")
        return super().current_element_id()

    def refresh_everything(self) -> None:
        super().refresh_everything()
        if hasattr(self, "geometry_pulse_enabled"):
            self._set_checkbox(self.geometry_pulse_enabled, bool(self.loader.editor.geometry_pulse_enabled))

    def refresh_editor(self) -> None:
        super().refresh_editor()
        state = self.current_state()
        if state is None or not hasattr(self, "element_enabled"):
            return
        element_id = self.current_element_id()
        editor = self.loader.editor
        self._syncing = True
        self._set_checkbox(self.element_enabled, bool(getattr(state, "enabled", True)))
        self.opaque_alpha.set_value(float(getattr(state, "opaque_fill_alpha", 1.0)) * 100.0)
        self.loader_ring_type.setCurrentText(str(getattr(state, "loader_ring_type", "Progress Arc")))
        self.loader_tail_length.set_value(float(getattr(state, "loader_tail_length", 0.28)) * 100.0)
        self.loader_tail_fade.set_value(float(getattr(state, "loader_tail_fade_span", 0.60)) * 100.0)
        self.loader_tail_balance.set_value(float(getattr(state, "loader_tail_balance", 0.0)) * 100.0)
        self.tracer_length.set_value(float(getattr(state, "tracer_length", 0.60)) * 100.0)
        self.tracer_fade.set_value(float(getattr(state, "tracer_fade_span", 0.60)) * 100.0)
        self.tracer_balance.set_value(float(getattr(state, "tracer_balance", 0.0)) * 100.0)
        self._set_checkbox(self.rune_transition_enabled, bool(getattr(state, "rune_transition_enabled", True)))
        self._set_checkbox(self.rune_glimmer_enabled, bool(getattr(state, "rune_glimmer_enabled", True)))
        self.rune_render_mode.setCurrentText(str(getattr(state, "rune_render_mode", "Outline")))
        self.rune_weight.setCurrentText(str(getattr(state, "rune_weight", "Regular")))

        mask_capable = editor.supports(element_id, "opaque")
        self.opaque_alpha.setVisible(mask_capable)
        self.opaque_alpha.setEnabled(mask_capable)

        loader_capable = editor.supports(element_id, "loader_effect")
        self.loader_ring_type.setVisible(loader_capable)
        gradient = loader_capable and str(getattr(state, "loader_ring_type", "Progress Arc")) == "Gradient Tail"
        for control in (self.loader_tail_length, self.loader_tail_fade, self.loader_tail_balance):
            control.setVisible(gradient)
            control.setEnabled(gradient)

        tracer_capable = editor.supports(element_id, "tracer_effect")
        for control in (self.tracer_length, self.tracer_fade, self.tracer_balance):
            control.setVisible(tracer_capable)
            control.setEnabled(tracer_capable)

        rune_capable = editor.supports(element_id, "rune_transition")
        for control in (self.rune_transition_enabled, self.rune_transition_enabled_reset, self.rune_glimmer_enabled, self.rune_glimmer_enabled_reset, self.rune_render_mode, self.rune_weight):
            control.setVisible(rune_capable)
            control.setEnabled(rune_capable)
        transition_on = rune_capable and bool(getattr(state, "rune_transition_enabled", True))
        glimmer_on = rune_capable and bool(getattr(state, "rune_glimmer_enabled", True))
        self.rune_speed.setEnabled(transition_on)
        self.rune_random.setEnabled(transition_on)
        self.transition_type.setEnabled(transition_on)
        fade_controls = transition_on and state.rune_speed > 0.001 and str(state.rune_transition_type) == "Fade"
        self.fade_bright.setVisible(fade_controls)
        self.fade_dark.setVisible(fade_controls)

        special = glimmer_on and (not transition_on or state.rune_speed <= 0.001)
        self.glimmer_type.setEnabled(special)
        mode = state.glimmer_type if special else "None"
        radial = special and mode == "Radial"
        twinkle = special and mode == "Twinkle"
        pulse = special and mode == "Pulse"
        for control in (self.radial_speed, self.radial_length, self.radial_fade, self.radial_balance, self.radial_direction):
            control.setVisible(radial)
            control.setEnabled(radial)
        for control in (self.twinkle_speed, self.twinkle_random):
            control.setVisible(twinkle)
            control.setEnabled(twinkle)
        for control in (self.rune_pulse_speed, self.rune_pulse_fade, self.rune_pulse_balance):
            control.setVisible(pulse)
            control.setEnabled(pulse)
        self._syncing = False

    def _checkpoint_editor_root(self, section: str, field: str):
        if section == "pulse" and field == "enabled":
            record = self._checkpoint_record()
            if record:
                return record.get("editor", {}).get("pulse", {}).get("enabled", True)
            return True
        return super()._checkpoint_editor_root(section, field)

    def reset_v7_combo(self, field: str) -> None:
        value = str(self._checkpoint_element(field))
        if field == "loader_ring_type":
            self.loader_ring_type.setCurrentText(value)
        elif field == "rune_render_mode":
            self.rune_render_mode.setCurrentText(value)
        elif field == "rune_weight":
            self.rune_weight.setCurrentText(value)
        self.set_element(field, value)

    def _set_color_button(self, button: QPushButton, color: QColor) -> None:
        if not color.isValid() or color.alpha() == 0:
            button.setText("CLEAR")
            button.setStyleSheet("QPushButton{background:#0f1217;color:#8b8f98;border:1px dashed #4f5663;border-radius:4px;padding:6px 12px}")
            return
        name = color.name(QColor.NameFormat.HexArgb).upper() if color.alpha() < 255 else color.name().upper()
        button.setText(name)
        text_color = "#111111" if color.lightness() > 150 else "#f5e8c8"
        background = color.name(QColor.NameFormat.HexArgb) if color.alpha() < 255 else color.name()
        button.setStyleSheet(f"QPushButton{{background:{background};color:{text_color};border:1px solid #6b6255;border-radius:4px;padding:6px 12px}}")

    def pick_element_color(self) -> None:
        state = self.current_state()
        if state is None:
            return
        current = QColor(state.color) if state.color else QColor("#ffffff")
        color = QColorDialog.getColor(current, self, f"Element colour — {state.label}", QColorDialog.ColorDialogOption.ShowAlphaChannel)
        if color.isValid():
            value = color.name(QColor.NameFormat.HexArgb) if color.alpha() < 255 else color.name()
            self.set_element("color", value)
            self._set_color_button(self.main_color, color)
            self._set_color_button(self.bright_color, color)

    def pick_rune_color(self, field: str) -> None:
        state = self.current_state()
        if state is None:
            return
        raw = str(getattr(state, field))
        current = QColor(raw) if raw else QColor("#ffffff")
        color = QColorDialog.getColor(current, self, field.replace("_", " ").title(), QColorDialog.ColorDialogOption.ShowAlphaChannel)
        if color.isValid():
            value = color.name(QColor.NameFormat.HexArgb) if color.alpha() < 255 else color.name()
            self.set_rune(field, value)
            self._set_color_button(self.dim_color if field == "rune_dim_color" else self.bright_color, color)

    def pick_sparkle_color(self, index: int) -> None:
        field = f"color_{index}"
        state = self.loader.editor.sparkles
        raw = str(getattr(state, field))
        current = QColor(raw) if raw else QColor("#ffffff")
        color = QColorDialog.getColor(current, self, f"Sparkle colour {index}", QColorDialog.ColorDialogOption.ShowAlphaChannel)
        if color.isValid():
            setattr(state, field, color.name(QColor.NameFormat.HexArgb) if color.alpha() < 255 else color.name())
            self._set_color_button(self.sparkle_colors[index - 1], color)
            self.loader.update()
            self._history_commit(f"sparkles:color_{index}", force=True)

    def clear_element_color(self, field: str) -> None:
        if field.startswith("rune_"):
            self.set_rune(field, "#00000000")
        else:
            self.set_element(field, "#00000000")
        button = self.main_color if field == "color" else self.dim_color if field == "rune_dim_color" else self.bright_color
        self._set_color_button(button, QColor(0, 0, 0, 0))

    def clear_sparkle_color(self, index: int) -> None:
        field = f"color_{index}"
        setattr(self.loader.editor.sparkles, field, "#00000000")
        self._set_color_button(self.sparkle_colors[index - 1], QColor(0, 0, 0, 0))
        self.loader.update()
        self._history_commit(f"sparkles:{field}", force=True)
