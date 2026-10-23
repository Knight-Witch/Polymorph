"""One-time release announcement with optional community support links."""
from __future__ import annotations

from PySide6.QtCore import Qt, QUrl, QSize
from PySide6.QtGui import QIcon, QDesktopServices
from PySide6.QtWidgets import QDialog, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QFrame

from ..constants import KOFI_URL
from ..resources import asset_path

PAYPAL_URL = "https://www.paypal.com/paypalme/knightwitch"
FEATURE_ID = "static-and-animated-webp-0.2.0"


def _support_button(label: str, logo: str, url: str, name: str) -> QPushButton:
    button = QPushButton(label)
    button.setObjectName(name)
    button.setFixedSize(150, 43)
    button.setIcon(QIcon(str(asset_path(logo))))
    button.setIconSize(QSize(32, 31))
    button.clicked.connect(lambda: QDesktopServices.openUrl(QUrl(url)))
    button.setToolTip(f"Open {label} to support Knight Witch")
    return button


class WhatsNewDialog(QDialog):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setObjectName("PolymorphWhatsNew")
        self.setWindowTitle("What's New in Polymorph")
        self.setModal(False)
        self.setMinimumWidth(470)
        self.setMaximumWidth(590)
        self.setStyleSheet(
            "QDialog{background:#101011;color:#eae0d0;border:1px solid #8a6535}"
            "QLabel{color:#eae0d0;font-size:12px;}"
            "QPushButton{background:#521318;color:#f0dcb2;border:1px solid #b68b55;"
            "padding:5px 11px;border-radius:4px}"
            "QPushButton:hover{background:#731c24;border-color:#d2ac70}"
        )
        layout = QVBoxLayout(self)
        layout.setContentsMargins(25, 19, 25, 18)
        layout.setSpacing(9)

        heading = QLabel("Polymorph now converts static image files!")
        heading.setObjectName("WhatsNewHeading")
        heading.setStyleSheet("font-size:17px;font-weight:bold;color:#d9b578;")
        heading.setWordWrap(True)
        layout.addWidget(heading)
        for title, detail in (
            ("PNG to WebP", "Share images more easily on platforms with smaller file-size limits."),
            ("WebP to PNG", "Export a PNG for places that don't recognize WebP."),
            ("PNG to PNG", "Shrink a PNG to a chosen maximum size, such as 16 MB down to 10 MB."),
            ("GIF / video to animated WebP", "Create high-quality looping WebP animations for sharing."),
        ):
            line = QLabel(f"<b>{title}</b> — {detail}")
            line.setTextFormat(Qt.TextFormat.RichText)
            line.setWordWrap(True)
            layout.addWidget(line)

        note = QLabel("All conversions run locally on your computer.")
        note.setStyleSheet("color:#ada59a")
        layout.addWidget(note)
        divider = QFrame()
        divider.setFrameShape(QFrame.Shape.HLine)
        divider.setStyleSheet("background:#694b32;max-height:1px")
        layout.addWidget(divider)

        support = QLabel(
            "I cover growing costs of the Hero Forge script ecosystem out of pocket "
            "&amp; spend most of my free time working on tools for the community I love. "
            "If you like what I do &amp; want to help keep it alive, you can support me below. "
            "Your support goes a <b>long</b> way to enable more &amp; more tools, stability, "
            "&amp; maintenance. Thank you so much for helping make it all possible!"
        )
        support.setObjectName("WhatsNewSupportMessage")
        support.setTextFormat(Qt.TextFormat.RichText)
        support.setWordWrap(True)
        support.setStyleSheet("line-height:1.25;color:#e1d6c7")
        layout.addWidget(support)
        signature = QLabel("— Knight Witch")
        signature.setStyleSheet("color:#d9b578;font-style:italic")
        layout.addWidget(signature, alignment=Qt.AlignmentFlag.AlignRight)

        buttons = QHBoxLayout()
        buttons.setSpacing(12)
        buttons.addStretch(1)
        buttons.addWidget(_support_button("Ko-fi", "donation/kofi.webp", KOFI_URL, "SupportKofi"))
        buttons.addWidget(_support_button("PayPal", "donation/paypal.png", PAYPAL_URL, "SupportPaypal"))
        buttons.addStretch(1)
        layout.addLayout(buttons)

        close = QPushButton("Got it")
        close.setObjectName("WhatsNewDismiss")
        close.clicked.connect(self.accept)
        layout.addWidget(close, alignment=Qt.AlignmentFlag.AlignRight)


def show_whats_new_once(window):
    key = "announcements/" + FEATURE_ID
    if window.settings_store.value(key, False, type=bool):
        return None
    dialog = WhatsNewDialog(window)
    dialog.finished.connect(lambda _code: window.settings_store.setValue(key, True))
    window._whats_new_dialog = dialog
    dialog.open()
    return dialog
