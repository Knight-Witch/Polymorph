"""Readable conversion log with copy and local folder access."""
from __future__ import annotations

from pathlib import Path

from PySide6.QtCore import QUrl
from PySide6.QtGui import QDesktopServices
from PySide6.QtWidgets import (
    QApplication, QDialog, QHBoxLayout, QLabel, QMessageBox,
    QPlainTextEdit, QPushButton, QVBoxLayout,
)

from ..conversion_log import logs_directory


class ConversionLogDialog(QDialog):
    def __init__(self, content: str, path: Path | None, parent=None) -> None:
        super().__init__(parent)
        self.setObjectName("ConversionLogDialog")
        self.setWindowTitle("Polymorph — Conversion Log")
        self.resize(820, 540)
        self.setMinimumSize(560, 360)
        self.setStyleSheet(
            "QDialog {background:#101011;color:#eae0d0}"
            "QLabel {color:#ded0bd}"
            "QPlainTextEdit {background:#08090a;color:#f1e9df;"
            "border:1px solid #725638;font-family:Consolas,monospace;font-size:11px}"
            "QPushButton {background:#521318;color:#f0dcb2;border:1px solid #b68b55;"
            "padding:6px 11px;border-radius:4px}"
            "QPushButton:hover {background:#731c24;border-color:#d2ac70}"
        )
        layout = QVBoxLayout(self)
        location = QLabel(f"File: {path}" if path is not None else "Log available in memory only")
        location.setObjectName("ConversionLogPath")
        location.setWordWrap(True)
        layout.addWidget(location)
        privacy = QLabel("Stored locally; includes filenames, paths and error details. Nothing is uploaded.")
        layout.addWidget(privacy)
        self.viewer = QPlainTextEdit()
        self.viewer.setObjectName("ConversionLogText")
        self.viewer.setReadOnly(True)
        self.viewer.setPlainText(content)
        layout.addWidget(self.viewer, 1)

        actions = QHBoxLayout()
        copy_button = QPushButton("Copy Log")
        copy_button.setObjectName("CopyConversionLog")
        copy_button.clicked.connect(lambda: QApplication.clipboard().setText(self.viewer.toPlainText()))
        actions.addWidget(copy_button)
        folder_button = QPushButton("Open Logs Folder")
        folder_button.setObjectName("OpenConversionLogFolder")
        folder_button.clicked.connect(self._open_folder)
        actions.addWidget(folder_button)
        actions.addStretch(1)
        close = QPushButton("Close")
        close.clicked.connect(self.close)
        actions.addWidget(close)
        layout.addLayout(actions)

    def _open_folder(self) -> None:
        directory = logs_directory()
        if not directory.is_dir():
            QMessageBox.warning(self, "Logs folder unavailable", f"No log folder exists at:\n{directory}")
        elif not QDesktopServices.openUrl(QUrl.fromLocalFile(str(directory))):
            QMessageBox.warning(self, "Could not open logs", f"Open this folder manually:\n{directory}")
