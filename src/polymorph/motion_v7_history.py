from __future__ import annotations

from copy import deepcopy

from PySide6.QtGui import QKeySequence, QShortcut


class V7HistoryMixin:
    def set_element(self, field: str, value) -> None:
        if self._syncing or not self.current_element_id():
            return
        element_id = self.current_element_id()
        super().set_element(field, value)
        self._history_commit(f"element:{element_id}:{field}")
        if field in {"loader_ring_type", "rune_transition_enabled", "rune_glimmer_enabled", "rune_render_mode", "rune_weight", "rune_speed", "rune_transition_type"}:
            self.refresh_editor()

    def set_link_group(self, text: str) -> None:
        if self._syncing or not self.current_element_id():
            return
        element_id = self.current_element_id()
        super().set_link_group(text)
        self._history_commit(f"element:{element_id}:link_group", force=True)

    def duplicate_element(self, with_group: bool) -> None:
        super().duplicate_element(with_group)
        self._history_commit("elements:duplicate", force=True)

    def remove_element(self) -> None:
        super().remove_element()
        self._history_commit("elements:remove", force=True)

    def clear_selected_group(self) -> None:
        super().clear_selected_group()
        self._history_commit("groups:clear-selected", force=True)

    def clear_all_groups(self) -> None:
        super().clear_all_groups()
        self._history_commit("groups:clear-all", force=True)

    def set_master_glow(self, value: float) -> None:
        super().set_master_glow(value)
        self._history_commit("global:master-brightness")

    def set_master_spread(self, value: float) -> None:
        super().set_master_spread(value)
        self._history_commit("global:master-spread")

    def set_trace_speed(self, value: float) -> None:
        super().set_trace_speed(value)
        self._history_commit("global:trace-speed")

    def set_pulse_speed(self, value: float) -> None:
        super().set_pulse_speed(value)
        self._history_commit("pulse:speed")

    def set_pulse_trail(self, value: float) -> None:
        super().set_pulse_trail(value)
        self._history_commit("pulse:trail")

    def set_pulse_end(self, value: float) -> None:
        super().set_pulse_end(value)
        self._history_commit("pulse:end")

    def set_sparkle_enabled(self, checked: bool) -> None:
        super().set_sparkle_enabled(checked)
        self._history_commit("sparkles:enabled", force=True)

    def set_sparkle(self, field: str, value: float) -> None:
        super().set_sparkle(field, value)
        self._history_commit(f"sparkles:{field}")

    def add_study(self) -> None:
        before = self.capture_workspace()
        super().add_study()
        if self.capture_workspace() != before:
            self._history_commit("studies:add", force=True)

    def rename_current_study(self) -> None:
        before = self.capture_workspace()
        super().rename_current_study()
        if self.capture_workspace() != before:
            self._history_commit("studies:rename", force=True)

    def revert_checkpoint(self) -> None:
        before = self.capture_workspace()
        self._history_suspended = True
        try:
            super().revert_checkpoint()
        finally:
            self._history_suspended = False
        after = self.capture_workspace()
        if before != after:
            self._undo_stack.append(deepcopy(before))
            self._redo_stack.clear()
            self._history_current = deepcopy(after)
            self._update_history_buttons()

    def load_preset(self) -> None:
        super().load_preset()
        self._reset_history_baseline()

    def loop(self) -> None:
        if not self.auto.isChecked():
            return
        value = self.progress.spin.value()
        self.progress.set_value(0 if value >= 99 else value + 1, emit=True)

    def _install_history_shortcuts(self) -> None:
        self._undo_shortcut = QShortcut(QKeySequence.StandardKey.Undo, self)
        self._undo_shortcut.activated.connect(self.undo)
        self._redo_shortcut = QShortcut(QKeySequence.StandardKey.Redo, self)
        self._redo_shortcut.activated.connect(self.redo)
        self._redo_shift_shortcut = QShortcut(QKeySequence("Ctrl+Shift+Z"), self)
        self._redo_shift_shortcut.activated.connect(self.redo)

    def _clear_history_merge(self) -> None:
        self._history_merge_key = None

    def _history_commit(self, key: str, *, force: bool = False) -> None:
        if self._history_suspended or self._syncing or self._switching_study or self._history_current is None:
            return
        current = self.capture_workspace()
        if current == self._history_current:
            return
        merge = bool(
            not force
            and self._history_merge_key == key
            and self._history_merge_timer is not None
            and self._history_merge_timer.isActive()
        )
        if not merge:
            self._undo_stack.append(deepcopy(self._history_current))
            if len(self._undo_stack) > 200:
                self._undo_stack.pop(0)
            self._redo_stack.clear()
        self._history_current = deepcopy(current)
        self._history_merge_key = None if force else key
        if self._history_merge_timer is not None:
            if force:
                self._history_merge_timer.stop()
            else:
                self._history_merge_timer.start(450)
        self._update_history_buttons()

    def _update_history_buttons(self) -> None:
        if hasattr(self, "undo_button"):
            self.undo_button.setEnabled(bool(self._undo_stack))
        if hasattr(self, "redo_button"):
            self.redo_button.setEnabled(bool(self._redo_stack))

    def undo(self) -> None:
        if not self._undo_stack:
            return
        current = self.capture_workspace()
        target = self._undo_stack.pop()
        self._redo_stack.append(deepcopy(current))
        self._history_suspended = True
        try:
            self.load_workspace(deepcopy(target), checkpoint=False)
        finally:
            self._history_suspended = False
        self._history_current = deepcopy(target)
        self._clear_history_merge()
        self._update_history_buttons()
        self.status.setText("Undo")

    def redo(self) -> None:
        if not self._redo_stack:
            return
        current = self.capture_workspace()
        target = self._redo_stack.pop()
        self._undo_stack.append(deepcopy(current))
        self._history_suspended = True
        try:
            self.load_workspace(deepcopy(target), checkpoint=False)
        finally:
            self._history_suspended = False
        self._history_current = deepcopy(target)
        self._clear_history_merge()
        self._update_history_buttons()
        self.status.setText("Redo")

    def _reset_history_baseline(self) -> None:
        self._undo_stack.clear()
        self._redo_stack.clear()
        self._history_current = self.capture_workspace()
        self._clear_history_merge()
        self._update_history_buttons()
