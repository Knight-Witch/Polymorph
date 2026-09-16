from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QAbstractItemView, QDialog, QDialogButtonBox, QInputDialog, QLabel,
    QListWidget, QListWidgetItem, QMessageBox, QTreeWidget, QTreeWidgetItem, QVBoxLayout,
)


class V7UIDialogMixin:
    def set_geometry_pulse_enabled(self, checked: bool) -> None:
        if self._syncing:
            return
        self.loader.editor.geometry_pulse_enabled = checked
        self.loader.update()
        self._history_commit("pulse:enabled", force=True)

    def open_pulse_order_dialog(self) -> None:
        dialog = QDialog(self)
        dialog.setWindowTitle("Geometry Pulse Order")
        dialog.resize(430, 560)
        layout = QVBoxLayout(dialog)
        note = QLabel("Drag pulse-enabled geometry into the order it should fire. Top fires first. Geometry not currently included in the pulse array is omitted.")
        note.setWordWrap(True)
        layout.addWidget(note)
        pulse_list = QListWidget()
        pulse_list.setDragDropMode(QAbstractItemView.DragDropMode.InternalMove)
        pulse_list.setDefaultDropAction(Qt.DropAction.MoveAction)
        active = [
            element_id for element_id in self.loader.editor.pulse_order
            if element_id in self.loader.editor.elements
            and self.loader.editor.elements[element_id].pulse
            and self.loader.editor.supports(element_id, "pulse")
        ]
        for element_id, state in self.loader.editor.elements.items():
            if state.pulse and self.loader.editor.supports(element_id, "pulse") and element_id not in active:
                active.append(element_id)
        for element_id in active:
            item = QListWidgetItem(self.loader.editor.get(element_id).label)
            item.setData(Qt.ItemDataRole.UserRole, element_id)
            pulse_list.addItem(item)
        layout.addWidget(pulse_list, 1)
        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Save | QDialogButtonBox.StandardButton.Cancel)
        buttons.accepted.connect(dialog.accept)
        buttons.rejected.connect(dialog.reject)
        layout.addWidget(buttons)
        if dialog.exec() != QDialog.DialogCode.Accepted:
            return
        reordered = [str(pulse_list.item(index).data(Qt.ItemDataRole.UserRole)) for index in range(pulse_list.count())]
        remainder = [element_id for element_id in self.loader.editor.pulse_order if element_id not in reordered]
        self.loader.editor.pulse_order = reordered + remainder
        self.loader.update()
        self._history_commit("pulse:order", force=True)

    def open_group_hierarchy_dialog(self) -> None:
        dialog = QDialog(self)
        dialog.setWindowTitle("Group Hierarchy")
        dialog.resize(500, 620)
        layout = QVBoxLayout(dialog)
        note = QLabel(
            "Drag layers between expandable groups. Drop a layer on a group to link it there; "
            "drop it under Ungrouped to disconnect it. Group names are editable in this window."
        )
        note.setWordWrap(True)
        layout.addWidget(note)
        tree = QTreeWidget()
        tree.setHeaderLabels(["Group / layer"])
        tree.setDragDropMode(QAbstractItemView.DragDropMode.InternalMove)
        tree.setDefaultDropAction(Qt.DropAction.MoveAction)
        tree.setDragEnabled(True)
        tree.setAcceptDrops(True)
        tree.setDropIndicatorShown(True)
        groups = [value for value in self.loader.editor.link_groups() if value != "None"]
        group_items: dict[str, QTreeWidgetItem] = {}
        ungrouped = QTreeWidgetItem(["Ungrouped"])
        ungrouped.setData(0, Qt.ItemDataRole.UserRole, "__ungrouped__")
        ungrouped.setFlags((ungrouped.flags() | Qt.ItemFlag.ItemIsDropEnabled) & ~Qt.ItemFlag.ItemIsDragEnabled)
        tree.addTopLevelItem(ungrouped)
        for group in groups:
            item = QTreeWidgetItem([group])
            item.setData(0, Qt.ItemDataRole.UserRole, "__group__")
            item.setFlags((item.flags() | Qt.ItemFlag.ItemIsEditable | Qt.ItemFlag.ItemIsDropEnabled) & ~Qt.ItemFlag.ItemIsDragEnabled)
            tree.addTopLevelItem(item)
            group_items[group] = item
        for element_id in self.loader.editor.layer_order:
            if element_id not in self.loader.editor.elements:
                continue
            state = self.loader.editor.get(element_id)
            child = QTreeWidgetItem([state.label])
            child.setData(0, Qt.ItemDataRole.UserRole, element_id)
            child.setFlags((child.flags() | Qt.ItemFlag.ItemIsDragEnabled | Qt.ItemFlag.ItemIsSelectable) & ~Qt.ItemFlag.ItemIsDropEnabled)
            parent = group_items.get(state.link_group, ungrouped)
            parent.addChild(child)
        tree.expandAll()
        layout.addWidget(tree, 1)
        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Save | QDialogButtonBox.StandardButton.Cancel)
        buttons.accepted.connect(dialog.accept)
        buttons.rejected.connect(dialog.reject)
        layout.addWidget(buttons)
        if dialog.exec() != QDialog.DialogCode.Accepted:
            return
        assignments: dict[str, str] = {}
        for top_index in range(tree.topLevelItemCount()):
            top = tree.topLevelItem(top_index)
            marker = str(top.data(0, Qt.ItemDataRole.UserRole) or "")
            group_name = "None" if marker == "__ungrouped__" else top.text(0).strip() or "None"
            for child_index in range(top.childCount()):
                child = top.child(child_index)
                element_id = str(child.data(0, Qt.ItemDataRole.UserRole) or "")
                if element_id in self.loader.editor.elements:
                    assignments[element_id] = group_name
        for top_index in range(tree.topLevelItemCount()):
            top = tree.topLevelItem(top_index)
            element_id = str(top.data(0, Qt.ItemDataRole.UserRole) or "")
            if element_id in self.loader.editor.elements:
                assignments[element_id] = "None"
        for element_id, group_name in assignments.items():
            self.loader.editor.get(element_id).link_group = group_name
        self.refresh_groups()
        self.refresh_editor()
        self.loader.update()
        self._history_commit("groups:hierarchy", force=True)

    def rename_selected_layer(self) -> None:
        element_id = self.current_element_id()
        state = self.current_state()
        if not element_id or state is None:
            return
        name, ok = QInputDialog.getText(self, "Rename layer", "Layer name:", text=state.label)
        if not ok or not name.strip() or name.strip() == state.label:
            return
        self.loader.editor.rename_element(element_id, name.strip())
        self.refresh_elements(element_id)
        self.refresh_editor()
        self.loader.update()
        self._history_commit("layers:rename", force=True)

    def rename_selected_group(self) -> None:
        state = self.current_state()
        if state is None or state.link_group == "None":
            QMessageBox.information(self, "Rename group", "The selected layer is not currently in a link group.")
            return
        old_name = state.link_group
        name, ok = QInputDialog.getText(self, "Rename group", "Group name:", text=old_name)
        if not ok or not name.strip() or name.strip() == old_name:
            return
        self.loader.editor.rename_group(old_name, name.strip())
        self.refresh_groups()
        self.refresh_editor()
        self._history_commit("groups:rename", force=True)

    def layer_order_changed(self, *_args) -> None:
        super().layer_order_changed(*_args)
        self._history_commit("layers:order")

    def _apply_v7_tooltips(self) -> None:
        tips = {
            self.span: "Moves the selected layer inward/outward without changing the size of the individual marks.",
            self.scale: "Scales the selected marks themselves rather than the overall radius/span.",
            self.base_rotation: "Manual starting angle; independent from animation direction and speed.",
            self.spin: "Negative values rotate counterclockwise, positive values clockwise; 0 is static.",
            self.opaque_alpha: "How strongly this mask hides layers behind it. 0% is transparent; 100% fully opaque.",
            self.loader_tail_length: "Circumference occupied by a Gradient Tail loading ring.",
            self.loader_tail_fade: "How gradual the loading tail fades from its bright head.",
            self.loader_tail_balance: "Bias the loading gradient toward its head or tail.",
            self.tracer_length: "Length of each tracer/comet trail.",
            self.tracer_fade: "Softness of the tracer gradient.",
            self.tracer_balance: "Bias tracer brightness toward the front/head or rear/tail.",
            self.rune_speed: "How quickly glyphs transition. 0 stops glyph changes.",
            self.rune_random: "Left synchronizes rune timing; right makes each rune independent.",
            self.fade_bright: "How long each rune holds at full brightness before fading.",
            self.fade_dark: "How long the rune position stays dark before the next glyph appears.",
            self.radial_length: "Length of the radial rune-glimmer sweep.",
            self.radial_balance: "Bias radial glimmer toward its leading head or trailing tail.",
            self.twinkle_random: "Left correlates neighbors; right makes rune twinkles independent.",
        }
        for widget, text in tips.items():
            widget.setToolTip(text)
