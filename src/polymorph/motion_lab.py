from __future__ import annotations

import argparse
import math
import sys
from pathlib import Path

from PySide6.QtCore import QPointF, QRectF, Qt, QTimer
from PySide6.QtGui import QColor, QBrush, QFont, QLinearGradient, QPainter, QPainterPath, QPen, QPixmap, QRadialGradient, QTransform
from PySide6.QtSvg import QSvgRenderer
from PySide6.QtWidgets import QApplication, QCheckBox, QComboBox, QFileDialog, QFrame, QFormLayout, QHBoxLayout, QLabel, QMainWindow, QPushButton, QSlider, QVBoxLayout, QWidget

from .ui.brand_widgets import tracked_font
from .ui.fonts import load_brand_fonts

IVORY = QColor("#f4efe8")
GOLD = QColor("#e9d6ad")
MID_GOLD = QColor("#cdb583")
CRIMSON = QColor("#b51f2b")


def alpha(c: QColor, a: int) -> QColor:
    out = QColor(c); out.setAlpha(max(0, min(255, a))); return out


def polar(c: QPointF, r: float, d: float) -> QPointF:
    q = math.radians(d); return QPointF(c.x() + math.cos(q) * r, c.y() + math.sin(q) * r)


class Clock:
    def __init__(self, owner: QWidget) -> None:
        self.t = 0.0
        self.timer = QTimer(owner); self.timer.setInterval(16); self.timer.setTimerType(Qt.TimerType.PreciseTimer)
        self.timer.timeout.connect(self.tick); self.owner = owner; self.timer.start()

    def tick(self) -> None:
        self.t = (self.t + 0.016) % 100000.0; self.owner.update()


class ArcaneLoader(QWidget):
    VARIANTS = ("A — Ritual", "B — Concentric", "C — Cipher", "D — Hybrid")

    def __init__(self, parent=None) -> None:
        super().__init__(parent); self.setFixedSize(330, 330); self.clock = Clock(self)
        self.variant = 3; self.progress = .62; self.glow = 1.0; self.rune_speed = 1.0; self.counter_speed = 1.0; self.trace_speed = 1.0
        self.emblem: QSvgRenderer | None = None

    def load_emblem(self, path: str) -> bool:
        r = QSvgRenderer(path)
        self.emblem = r if r.isValid() else None; self.update(); return self.emblem is not None

    def ring(self, p: QPainter, c: QPointF, r: float, a: int, w: float = 1.0) -> None:
        p.setBrush(Qt.BrushStyle.NoBrush); p.setPen(QPen(alpha(MID_GOLD, int(a*self.glow)), w)); p.drawEllipse(c, r, r)

    def ticks(self, p: QPainter, c: QPointF, r: float, angle: float, n: int) -> None:
        p.save(); p.translate(c); p.rotate(angle); p.translate(-c)
        for i in range(n):
            d = i*360/n; long = i % 4 == 0; p.setPen(QPen(alpha(GOLD, int((110 if long else 45)*self.glow)), 1.0 if long else .65))
            p.drawLine(polar(c, r-(7 if long else 3), d), polar(c, r+(6 if long else 2), d))
        p.restore()

    def runes(self, p: QPainter, c: QPointF, r: float, angle: float, n: int = 14) -> None:
        p.save(); p.translate(c); p.rotate(angle); p.translate(-c)
        for i in range(n):
            d=i*360/n; q=polar(c,r,d); p.save(); p.translate(q); p.rotate(d+90); s=4.8; path=QPainterPath(); m=i%4
            if m==0: path.moveTo(-s,s); path.lineTo(0,-s); path.lineTo(s,s); path.moveTo(-s*.5,0); path.lineTo(s*.5,0)
            elif m==1: path.moveTo(-s,-s); path.lineTo(s,s); path.moveTo(s,-s); path.lineTo(-s,s); path.moveTo(0,-s*1.2); path.lineTo(0,s*1.2)
            elif m==2: path.moveTo(-s,-s*.8); path.lineTo(-s,s*.8); path.lineTo(s,0); path.closeSubpath()
            else: path.moveTo(-s,0); path.lineTo(0,-s); path.lineTo(s,0); path.lineTo(0,s); path.closeSubpath()
            p.setPen(QPen(alpha(GOLD,int(118*self.glow)),.9)); p.drawPath(path); p.restore()
        p.restore()

    def geometry(self, p: QPainter, c: QPointF, r: float, angle: float, dense: bool) -> None:
        n=8 if dense else 6; pts=[polar(c,r,i*360/n-90) for i in range(n)]
        p.save(); p.translate(c); p.rotate(angle); p.translate(-c); p.setPen(QPen(alpha(MID_GOLD,int((78 if dense else 58)*self.glow)),.85))
        path=QPainterPath(); path.moveTo(pts[0]); [path.lineTo(x) for x in pts[1:]]; path.closeSubpath(); p.drawPath(path)
        step=3 if dense else 2
        for i,x in enumerate(pts): p.drawLine(x,pts[(i+step)%n])
        p.restore()

    def trace(self,p:QPainter,c:QPointF,r:float,phase:float,count:int=3)->None:
        for j in range(count):
            d=(phase*58*self.trace_speed+j*360/count)%360; a=polar(c,r,d); b=polar(c,r,d+24)
            for width,opacity in ((5.5,30),(2.4,90),(.85,235)):
                p.setPen(QPen(alpha(GOLD,int(opacity*self.glow)),width,Qt.PenStyle.SolidLine,Qt.PenCapStyle.RoundCap)); p.drawLine(a,b)

    def paintEvent(self,_event)->None:
        p=QPainter(self); p.setRenderHint(QPainter.RenderHint.Antialiasing,True); c=QPointF(self.width()/2,self.height()/2); r=128.0; t=self.clock.t
        haze=QRadialGradient(c,r*1.25); haze.setColorAt(0,alpha(GOLD,int(14*self.glow))); haze.setColorAt(.62,alpha(CRIMSON,int(7*self.glow))); haze.setColorAt(1,QColor(0,0,0,0)); p.setPen(Qt.PenStyle.NoPen); p.setBrush(haze); p.drawEllipse(c,r*1.25,r*1.25)
        ra=t*17*self.rune_speed; ca=-t*7.5*self.counter_speed
        if self.variant==0: self.geometry(p,c,r*.73,ca*.35,False); self.runes(p,c,r*.70,ra,12); self.ticks(p,c,r*.91,ca*.25,32)
        elif self.variant==1: [self.ring(p,c,r*f,a) for f,a in ((.82,65),(.66,50),(.48,40))]; self.ticks(p,c,r*.78,ra,40); self.runes(p,c,r*.57,ca,16); self.trace(p,c,r*.66,t,4)
        elif self.variant==2: self.geometry(p,c,r*.80,ca,True); self.ticks(p,c,r*.92,ra*.35,24); self.trace(p,c,r*.80,t*1.15,2)
        else: self.geometry(p,c,r*.76,ca*.45,True); self.runes(p,c,r*.69,ra,14); self.ticks(p,c,r*.91,ca*.24,36); self.trace(p,c,r*.76,t,3)
        self.ring(p,c,r*.84,74); self.ring(p,c,r*.52,58)
        rr=QRectF(c.x()-r,c.y()-r,2*r,2*r); p.setPen(QPen(alpha(MID_GOLD,40),2)); p.drawEllipse(rr); span=360*self.progress
        for width,opacity in ((7.5,42),(1.55,235)): p.setPen(QPen(alpha(GOLD if width>2 else IVORY,int(opacity*self.glow)),width,Qt.PenStyle.SolidLine,Qt.PenCapStyle.RoundCap)); p.drawArc(rr,90*16,int(-span*16))
        er=QRectF(c.x()-46,c.y()-46,92,92); p.save(); p.setOpacity(.22+.78*self.progress)
        if self.emblem: self.emblem.render(p,er)
        else:
            self.ring(p,c,38,220,1.2); self.ring(p,c,23,220,1.0); top=polar(c,21,-90); left=polar(c,21,150); right=polar(c,21,30); p.drawLine(top,left); p.drawLine(left,right); p.drawLine(right,top)
        p.restore()


class ArcaneButton(QPushButton):
    def __init__(self,parent=None)->None:
        super().__init__(parent); self.setText(""); self.setMinimumWidth(430); self.setFixedHeight(98); self.setCursor(Qt.CursorShape.PointingHandCursor); self.clock=Clock(self)
        self.hover=.0; self.forced:str|None=None; self.glow=1.0; self.speed=1.0; self.trace_speed=1.0; self.debug=False; self.cast_at:float|None=None; self.clicked.connect(self.cast)

    def cast(self)->None: self.cast_at=self.clock.t; self.update()
    def set_debug(self,on:bool)->None: self.debug=on; self.setFixedHeight(260 if on else 98); self.update()
    def burst(self)->float:
        if self.cast_at is None:return 0.0
        age=self.clock.t-self.cast_at
        if age<0: age+=100000
        if age>=.9:self.cast_at=None;return 0.0
        return (1-age/.9)**2
    def target(self)->float:
        if self.forced=="hover" or self.forced=="pressed":return 1.0
        if self.forced=="rest":return 0.0
        return 1.0 if self.underMouse() else 0.0
    def mechanism(self,p:QPainter,rect:QRectF,clip:bool)->None:
        if clip:
            path=QPainterPath();path.addRoundedRect(rect,5,5);p.setClipPath(path)
        c=QPointF(rect.center().x()-rect.width()*.16,rect.center().y()); r=rect.height()*1.16; b=self.burst(); active=min(1.35,.16+self.hover*.84+b*.55); angle=self.clock.t*15*self.speed*(.22+self.hover*.78)+b*78
        for f,a,w in ((1,48,1),(.76,72,.85),(.51,45,.75)): p.setBrush(Qt.BrushStyle.NoBrush);p.setPen(QPen(alpha(GOLD,int(a*active*self.glow)),w));p.drawEllipse(c,r*f,r*f)
        p.save();p.translate(c);p.rotate(angle);p.translate(-c)
        for i in range(12): d=i*30;p.setPen(QPen(alpha(MID_GOLD,int((50+i%3*16)*active*self.glow)),.8));p.drawLine(polar(c,r*.56,d),polar(c,r*.94,d+(7 if i%2 else -5)))
        p.restore();p.save();p.translate(c);p.rotate(-angle*.42);p.translate(-c)
        for i in range(8): d=i*45;p.setPen(QPen(alpha(GOLD,int(78*active*self.glow)),.9));p.drawLine(polar(c,r*.77,d),polar(c,r*.64,d+17))
        p.restore()
        if self.hover>.08:
            d=(self.clock.t*72*self.trace_speed)%360;a=polar(c,r*.76,d);z=polar(c,r*.76,d+22)
            for w,o in ((5,30),(2.2,85),(.8,235)):p.setPen(QPen(alpha(GOLD,int(o*self.glow)),w,Qt.PenStyle.SolidLine,Qt.PenCapStyle.RoundCap));p.drawLine(a,z)
        if clip:p.setClipping(False)
    def text(self,p:QPainter,rect:QRectF)->None:
        tr=QRectF(rect.left()+60,rect.top()+15,rect.width()-120,42);path=QPainterPath();path.addText(QPointF(0,0),QFont(tracked_font(17,5.1)),"POLYMORPH");b=path.boundingRect();x=tr.center().x()-b.width()/2-b.left();y=tr.center().y()+b.height()/2-b.bottom();tf=QTransform();tf.translate(x,y);path=tf.map(path);p.setPen(Qt.PenStyle.NoPen);p.setBrush(IVORY);p.drawPath(path)
        if self.hover>.03:
            sweep=((self.clock.t*.22*self.trace_speed)%1.35)-.16;cx=tr.left()+tr.width()*sweep;w=max(28,tr.width()*.11);g=QLinearGradient(cx-w,0,cx+w,0);g.setColorAt(0,QColor(255,255,255,0));g.setColorAt(.5,alpha(IVORY,int(255*self.hover*self.glow)));g.setColorAt(1,QColor(255,255,255,0));p.save();p.setClipPath(path);p.fillRect(tr.adjusted(-30,-12,30,12),g);p.restore();p.setPen(QPen(QBrush(g),1.4));p.setBrush(Qt.BrushStyle.NoBrush);p.drawPath(path)
    def paintEvent(self,_event)->None:
        tgt=self.target();self.hover+=(tgt-self.hover)*(.11 if tgt>self.hover else .075)
        p=QPainter(self);p.setRenderHint(QPainter.RenderHint.Antialiasing,True);p.setRenderHint(QPainter.RenderHint.TextAntialiasing,True)
        rect=QRectF(30,(self.height()-98)/2,max(1,self.width()-60),98) if self.debug else QRectF(self.rect()).adjusted(1,1,-1,-1)
        if self.debug:p.save();p.setOpacity(.38);self.mechanism(p,rect,False);p.restore()
        pressed=self.isDown() or self.forced=="pressed";active=max(self.hover,.35 if pressed else 0,self.burst());path=QPainterPath();path.addRoundedRect(rect,5,5);p.setClipPath(path);g=QLinearGradient(rect.left(),rect.top(),rect.right(),rect.bottom());g.setColorAt(0,QColor("#180609"));g.setColorAt(.45,QColor("#78131d") if pressed else QColor("#621019"));g.setColorAt(1,QColor("#120507"));p.fillPath(path,g);wake=QRadialGradient(QPointF(rect.center().x()-rect.width()*.18,rect.center().y()),rect.width()*.62);wake.setColorAt(0,alpha(CRIMSON,int(50+80*active)));wake.setColorAt(.46,alpha(GOLD,int(7+17*active)));wake.setColorAt(1,QColor(0,0,0,0));p.fillPath(path,wake);p.setClipping(False);self.mechanism(p,rect,True);p.setPen(QPen(alpha(GOLD,115+int(75*active)),1));p.setBrush(Qt.BrushStyle.NoBrush);p.drawRoundedRect(rect,5,5);self.text(p,rect);p.setPen(alpha(GOLD,160));p.setFont(tracked_font(7,2.3));p.drawText(QRectF(rect.left(),rect.center().y()+18,rect.width(),22),Qt.AlignmentFlag.AlignHCenter|Qt.AlignmentFlag.AlignTop,"CONVERT MEDIA")
        if self.debug:p.setPen(QPen(QColor("#68c7ff"),1,Qt.PenStyle.DashLine));p.drawRoundedRect(rect,5,5)


class Stage(QWidget):
    NAMES=("Black","Polymorph Gradient","Obsidian Grain","Slate Texture","Busy Test","Custom Image")
    def __init__(self,parent=None)->None:super().__init__(parent);self.index=1;self.custom=QPixmap();self.setMinimumSize(700,600)
    def load(self,path:str)->bool:self.custom=QPixmap(path);self.index=5;self.update();return not self.custom.isNull()
    def paintEvent(self,_event)->None:
        p=QPainter(self);r=QRectF(self.rect());i=self.index
        if i==0:p.fillRect(r,QColor("#000"));return
        if i==5 and not self.custom.isNull():
            q=self.custom.scaled(self.size(),Qt.AspectRatioMode.KeepAspectRatioByExpanding,Qt.TransformationMode.SmoothTransformation);x=(q.width()-self.width())//2;y=(q.height()-self.height())//2;p.drawPixmap(0,0,q,x,y,self.width(),self.height());return
        g=QLinearGradient(r.topLeft(),r.bottomRight());colors={1:("#050608","#0b0d11","#030405"),2:("#090a0c","#111318","#050607"),3:("#292d34","#171b21","#0d0f13"),4:("#23111b","#102332","#0b0d10")}[i];g.setColorAt(0,QColor(colors[0]));g.setColorAt(.5,QColor(colors[1]));g.setColorAt(1,QColor(colors[2]));p.fillRect(r,g)
        if i in (2,3,4):
            state=0xC0FFEE
            for n in range(640 if i==4 else 390):state=(1664525*state+1013904223+n)&0xffffffff;x=state%max(1,self.width());state=(1664525*state+1013904223)&0xffffffff;y=state%max(1,self.height());p.setPen(QColor(255,245,228,15 if i==4 else 8));p.drawPoint(int(x),int(y))
        if i==4:
            p.setPen(QPen(QColor(255,255,255,16),1))
            for x in range(-self.height(),self.width(),46):p.drawLine(x,0,x+self.height(),self.height())


class MotionLab(QMainWindow):
    def __init__(self)->None:
        super().__init__();self.setWindowTitle("Polymorph Motion Lab");self.resize(1180,820);root=QWidget();self.setCentralWidget(root);outer=QHBoxLayout(root);outer.setContentsMargins(18,18,18,18);outer.setSpacing(18);self.stage=Stage();sl=QVBoxLayout(self.stage);sl.setContentsMargins(34,28,34,28);title=QLabel("POLYMORPH MOTION LAB");title.setObjectName("LabTitle");title.setAlignment(Qt.AlignmentFlag.AlignHCenter);sl.addWidget(title);self.loader=ArcaneLoader();row=QHBoxLayout();row.addStretch();row.addWidget(self.loader);row.addStretch();sl.addLayout(row,1);self.button=ArcaneButton();row=QHBoxLayout();row.addStretch();row.addWidget(self.button);row.addStretch();sl.addLayout(row);sl.addStretch();outer.addWidget(self.stage,1);panel=QFrame();panel.setObjectName("Panel");panel.setFixedWidth(330);pl=QVBoxLayout(panel);pl.setContentsMargins(15,15,15,15);form=QFormLayout();self.bg=QComboBox();self.bg.addItems(Stage.NAMES);self.bg.setCurrentIndex(1);self.bg.currentIndexChanged.connect(self.background);form.addRow("Background",self.bg);self.variant=QComboBox();self.variant.addItems(ArcaneLoader.VARIANTS);self.variant.setCurrentIndex(3);self.variant.currentIndexChanged.connect(lambda v:setattr(self.loader,"variant",v));form.addRow("Loader",self.variant);self.progress=QSlider(Qt.Orientation.Horizontal);self.progress.setRange(0,100);self.progress.setValue(62);self.progress.valueChanged.connect(lambda v:setattr(self.loader,"progress",v/100));form.addRow("Progress",self.progress);self.auto=QCheckBox("Auto loop 0–100%");self.auto.setChecked(True);form.addRow("",self.auto);pl.addLayout(form)
        for label,lo,hi,val,target,attr in (("Loader glow",20,180,100,self.loader,"glow"),("Rune speed",10,220,100,self.loader,"rune_speed"),("Counter speed",10,220,100,self.loader,"counter_speed"),("Trace speed",10,260,100,self.loader,"trace_speed"),("Button glow",20,180,100,self.button,"glow"),("Button rotation",10,240,100,self.button,"speed")):
            pl.addWidget(QLabel(label));s=QSlider(Qt.Orientation.Horizontal);s.setRange(lo,hi);s.setValue(val);s.valueChanged.connect(lambda v,o=target,a=attr:setattr(o,a,v/100));pl.addWidget(s)
            if label=="Trace speed":s.valueChanged.connect(lambda v:setattr(self.button,"trace_speed",v/100))
        b=QPushButton("Load custom background…");b.clicked.connect(self.choose_background);pl.addWidget(b);b=QPushButton("Load emblem SVG…");b.clicked.connect(self.choose_emblem);pl.addWidget(b);pl.addWidget(QLabel("BUTTON STATE"));states=QHBoxLayout()
        for label,state in (("Rest","rest"),("Hover","hover"),("Pressed","pressed"),("Live",None)):
            b=QPushButton(label);b.clicked.connect(lambda _=False,s=state:setattr(self.button,"forced",s));states.addWidget(b)
        pl.addLayout(states);dbg=QCheckBox("Reveal full button mechanism");dbg.toggled.connect(self.button.set_debug);pl.addWidget(dbg);note=QLabel("Hover the real POLYMORPH button to wake it. Click it for the cast burst. Debug reveal shows the oversized mechanism around the cyan clipping window.");note.setWordWrap(True);note.setObjectName("Note");pl.addWidget(note);pl.addStretch();outer.addWidget(panel);self.setStyleSheet("QMainWindow,QWidget{background:#040506;color:#eee8de;font-family:Inter,'Segoe UI';font-size:10pt} QLabel#LabTitle{font-size:18pt;letter-spacing:4px;background:transparent} QFrame#Panel{background:#0b0d10;border:1px solid #34302a;border-radius:5px} QLabel#Note{color:#8e8b86;background:transparent} QComboBox,QPushButton{background:#111318;border:1px solid #4d463d;border-radius:4px;padding:6px 8px} QPushButton:hover,QComboBox:hover{border-color:#cbb17e;background:#171a1f} QSlider::groove:horizontal{height:4px;background:#17191d;border-radius:2px} QSlider::sub-page:horizontal{background:#b4212c;border-radius:2px} QSlider::handle:horizontal{width:12px;margin:-5px 0;border-radius:6px;background:#e7d5ae}");self.hold=0;self.timer=QTimer(self);self.timer.setInterval(34);self.timer.timeout.connect(self.loop);self.timer.start()
    def loop(self)->None:
        if not self.auto.isChecked():return
        if self.progress.value()>=100:
            self.hold+=1
            if self.hold>=22:self.hold=0;self.progress.setValue(0)
        else:self.progress.setValue(self.progress.value()+1)
    def background(self,i:int)->None:
        if i==5 and self.stage.custom.isNull():self.choose_background()
        else:self.stage.index=i;self.stage.update()
    def choose_background(self)->None:
        path,_=QFileDialog.getOpenFileName(self,"Choose preview background","","Images (*.png *.jpg *.jpeg *.webp *.bmp)")
        if path and self.stage.load(path):self.bg.blockSignals(True);self.bg.setCurrentIndex(5);self.bg.blockSignals(False)
    def choose_emblem(self)->None:
        path,_=QFileDialog.getOpenFileName(self,"Choose emblem SVG","","SVG files (*.svg)")
        if path:self.loader.load_emblem(path)


def main(argv:list[str]|None=None)->int:
    ap=argparse.ArgumentParser();ap.add_argument("--smoke-test",action="store_true");args=ap.parse_args(argv);app=QApplication(sys.argv[:1]);load_brand_fonts(app);w=MotionLab();w.show()
    if args.smoke_test:w.loader.variant=2;w.loader.progress=.88;w.button.forced="hover";QTimer.singleShot(100,app.quit)
    return app.exec()

if __name__=="__main__":raise SystemExit(main())
