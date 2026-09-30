from __future__ import annotations

from PySide6.QtWidgets import QDialog, QDialogButtonBox, QLabel, QTableWidget, QTableWidgetItem, QVBoxLayout

from ..constants import ASPECT_RATIO_GUIDE


class AspectGuideDialog(QDialog):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setWindowTitle("Aspect Ratio Guide")
        self.resize(560, 330)
        layout = QVBoxLayout(self)
        intro = QLabel("Common aspect-ratio references. Platform requirements and recommendations can change; these are general guidelines, not guarantees.")
        intro.setWordWrap(True)
        layout.addWidget(intro)
        table = QTableWidget(len(ASPECT_RATIO_GUIDE), 2)
        table.setHorizontalHeaderLabels(["Ratio", "Common use"])
        table.verticalHeader().setVisible(False)
        table.setEditTriggers(QTableWidget.NoEditTriggers)
        for row, (ratio, use) in enumerate(ASPECT_RATIO_GUIDE):
            table.setItem(row, 0, QTableWidgetItem(ratio))
            table.setItem(row, 1, QTableWidgetItem(use))
        table.horizontalHeader().setStretchLastSection(True)
        layout.addWidget(table)
        buttons = QDialogButtonBox(QDialogButtonBox.Close)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)
