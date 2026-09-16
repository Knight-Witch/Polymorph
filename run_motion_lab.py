from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from polymorph.motion_lab import MotionLab, main


_ORIGINAL_APPLY_STYLE = MotionLab._apply_style


def _apply_motion_lab_visual_override(self) -> None:
    _ORIGINAL_APPLY_STYLE(self)
    self.setStyleSheet(
        self.styleSheet()
        + " "
        + "QLabel#Section{font-size:9pt;font-weight:800;letter-spacing:1.6px;color:#ff4057;background:transparent;"
          "border:none;border-bottom:1px solid #7e0d18;padding:9px 0 6px 0;margin-top:9px} "
        + "QSlider::groove:horizontal{height:4px;background:transparent;border:none;border-radius:0} "
        + "QSlider::add-page:horizontal{background:transparent;border:none} "
        + "QSlider:disabled::groove:horizontal{background:transparent;border:none} "
        + "QSlider:disabled::add-page:horizontal{background:transparent;border:none}"
    )


MotionLab._apply_style = _apply_motion_lab_visual_override

if __name__ == "__main__":
    raise SystemExit(main())
