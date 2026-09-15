from __future__ import annotations

import argparse
import sys
from pathlib import Path

from PySide6.QtCore import Qt, QTimer
from PySide6.QtWidgets import QApplication, QCheckBox, QComboBox, QFileDialog, QFormLayout, QFrame, QHBoxLayout, QLabel, QMainWindow, QPushButton, QSlider, QVBoxLayout, QWidget

from .motion_button import ArcaneButton
from .motion_effects import load_runic_font
from .motion_loader import ArcaneLoader
from .motion_stage import Stage
from .ui.fonts import load_brand_fonts

class MotionLab(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Polymorph Motion Lab — Elder Futhark Transmutation")
        self.resize(1320, 930)
        self.rune_family = load_runic_font()
        root = QWidget(); self.setCentralWidget(root); outer = QHBoxLayout(root); outer.setContentsMargins(18,18,18,18); outer.setSpacing(18)
        self.stage = Stage(); stage_layout = QVBoxLayout(self.stage); stage_layout.setContentsMargins(34,22,34,26)
        title = QLabel("POLYMORPH MOTION LAB"); title.setObjectName("LabTitle"); title.setAlignment(Qt.AlignmentFlag.AlignHCenter); stage_layout.addWidget(title)
        subtitle = QLabel("ELDER FUTHARK / TRANSMUTATION STUDY"); subtitle.setObjectName("LabSubtitle"); subtitle.setAlignment(Qt.AlignmentFlag.AlignHCenter); stage_layout.addWidget(subtitle)
        self.loader = ArcaneLoader(self.rune_family); row = QHBoxLayout(); row.addStretch(); row.addWidget(self.loader); row.addStretch(); stage_layout.addLayout(row,1)
        self.button = ArcaneButton(self.rune_family); row = QHBoxLayout(); row.addStretch(); row.addWidget(self.button); row.addStretch(); stage_layout.addLayout(row); stage_layout.addStretch(); outer.addWidget(self.stage,1)
        panel = QFrame(); panel.setObjectName("Panel"); panel.setFixedWidth(350); panel_layout = QVBoxLayout(panel); panel_layout.setContentsMargins(15,15,15,15); panel_layout.setSpacing(7)
        form = QFormLayout(); self.bg = QComboBox(); self.bg.addItems(Stage.NAMES); self.bg.setCurrentIndex(1); self.bg.currentIndexChanged.connect(self.background); form.addRow("Background",self.bg)
        self.variant = QComboBox(); self.variant.addItems(ArcaneLoader.VARIANTS); self.variant.setCurrentIndex(0); self.variant.currentIndexChanged.connect(lambda value:setattr(self.loader,"variant",value)); form.addRow("Study",self.variant)
        self.progress = QSlider(Qt.Orientation.Horizontal); self.progress.setRange(0,100); self.progress.setValue(62); self.progress.valueChanged.connect(lambda value:self.loader.set_progress(value/100.0)); form.addRow("Progress",self.progress)
        self.auto = QCheckBox("Auto loop 0–100% + completion"); self.auto.setChecked(True); form.addRow("",self.auto); panel_layout.addLayout(form)
        self._add_slider(panel_layout,"Master glow",20,180,100,self.loader,"glow")
        self._add_slider(panel_layout,"Glow spread",35,185,100,self.loader,"glow_spread")
        self._add_slider(panel_layout,"Outer rune ring — CW",10,220,100,self.loader,"outer_rune_speed")
        self._add_slider(panel_layout,"Inner rune ring — CCW",10,220,100,self.loader,"inner_rune_speed")
        self._add_slider(panel_layout,"Partial rune arcs — CCW",10,220,100,self.loader,"partial_speed")
        self._add_slider(panel_layout,"Triangle + rune spheres — CW",10,220,100,self.loader,"triangle_speed")
        self._add_slider(panel_layout,"Twin hexagons — CCW",10,220,100,self.loader,"hex_speed")
        trace_slider = self._add_slider(panel_layout,"Comet tracer speed",10,260,100,self.loader,"trace_speed"); trace_slider.valueChanged.connect(lambda value:setattr(self.button,"trace_speed",value/100.0))
        self._add_slider(panel_layout,"Cascade / flicker pace",20,220,100,self.loader,"flicker_speed")
        self._add_slider(panel_layout,"Button glow",20,180,100,self.button,"glow")
        self._add_slider(panel_layout,"Button rune rotation",10,240,100,self.button,"speed")
        background_button = QPushButton("Load custom background…"); background_button.clicked.connect(self.choose_background); panel_layout.addWidget(background_button)
        emblem_button = QPushButton("Load alternate emblem SVG…"); emblem_button.clicked.connect(self.choose_emblem); panel_layout.addWidget(emblem_button)
        self.emblem_status = QLabel("Emblem: bundled Knight Witch SVG" if self.loader.emblem else "Emblem: bundled SVG unavailable"); self.emblem_status.setObjectName("Note"); self.emblem_status.setWordWrap(True); panel_layout.addWidget(self.emblem_status)
        panel_layout.addWidget(QLabel("BUTTON STATE")); states = QHBoxLayout()
        for label,state in (("Rest","rest"),("Hover","hover"),("Pressed","pressed"),("Live",None)):
            button = QPushButton(label); button.clicked.connect(lambda _=False,selected=state:setattr(self.button,"forced",selected)); states.addWidget(button)
        panel_layout.addLayout(states); debug = QCheckBox("Reveal full button mechanism"); debug.toggled.connect(self.button.set_debug); panel_layout.addWidget(debug)
        note = QLabel("Rune glyphs are Elder Futhark. The two outermost rings are real progress indicators moving in opposite directions. At 100%, they pulse while the inner ritual fades and the Knight Witch emblem materializes."); note.setWordWrap(True); note.setObjectName("Note"); panel_layout.addWidget(note); panel_layout.addStretch(); outer.addWidget(panel)
        self.setStyleSheet("QMainWindow,QWidget{background:#040506;color:#eee8de;font-family:Inter,'Segoe UI';font-size:9.5pt} QLabel#LabTitle{font-size:18pt;letter-spacing:4px;background:transparent} QLabel#LabSubtitle{font-size:8pt;letter-spacing:2px;color:#aa9d87;background:transparent} QFrame#Panel{background:#0b0d10;border:1px solid #34302a;border-radius:5px} QLabel#Note{color:#8e8b86;background:transparent;font-size:8.2pt} QComboBox,QPushButton{background:#111318;border:1px solid #4d463d;border-radius:4px;padding:6px 8px} QPushButton:hover,QComboBox:hover{border-color:#cbb17e;background:#171a1f} QSlider::groove:horizontal{height:4px;background:#17191d;border-radius:2px} QSlider::sub-page:horizontal{background:#b4212c;border-radius:2px} QSlider::handle:horizontal{width:12px;margin:-5px 0;border-radius:6px;background:#e7d5ae}")
        self.hold = 0; self.timer = QTimer(self); self.timer.setInterval(34); self.timer.timeout.connect(self.loop); self.timer.start()

    def _add_slider(self, layout: QVBoxLayout, label: str, minimum: int, maximum: int, value: int, target: object, attribute: str) -> QSlider:
        layout.addWidget(QLabel(label)); slider = QSlider(Qt.Orientation.Horizontal); slider.setRange(minimum,maximum); slider.setValue(value); slider.valueChanged.connect(lambda raw,obj=target,attr=attribute:setattr(obj,attr,raw/100.0)); layout.addWidget(slider); return slider

    def loop(self) -> None:
        if not self.auto.isChecked(): return
        if self.progress.value() >= 100:
            self.hold += 1
            if self.hold >= 62: self.hold = 0; self.progress.setValue(0)
        else: self.progress.setValue(self.progress.value()+1)

    def background(self, index: int) -> None:
        if index == 5 and self.stage.custom.isNull(): self.choose_background()
        else: self.stage.index = index; self.stage.update()

    def choose_background(self) -> None:
        path,_ = QFileDialog.getOpenFileName(self,"Choose preview background","","Images (*.png *.jpg *.jpeg *.webp *.bmp)")
        if path and self.stage.load(path):
            self.bg.blockSignals(True); self.bg.setCurrentIndex(5); self.bg.blockSignals(False)

    def choose_emblem(self) -> None:
        path,_ = QFileDialog.getOpenFileName(self,"Choose emblem SVG","","SVG files (*.svg)")
        if not path: return
        if self.loader.load_emblem(path): self.emblem_status.setText(f"Emblem override: {Path(path).name}")
        else: self.emblem_status.setText("Emblem override failed to load; bundled emblem retained only if reloaded on restart.")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(); parser.add_argument("--smoke-test",action="store_true"); args = parser.parse_args(argv)
    app = QApplication(sys.argv[:1]); load_brand_fonts(app); window = MotionLab(); window.show()
    if args.smoke_test:
        window.loader.variant = 2; window.loader.set_progress(1.0); window.button.forced = "hover"; QTimer.singleShot(180,app.quit)
    return app.exec()

if __name__ == "__main__": raise SystemExit(main())
