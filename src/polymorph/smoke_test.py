from __future__ import annotations

import os
import time
import traceback
from pathlib import Path

from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication, QFrame, QLabel, QScrollArea, QSplitter

from .models import FramingMode, GifMotionMode
from .resources import asset_path
from .tools import find_toolchain
from .ui.adaptive_main_window import MainWindow
from .ui.branded_layout import QueueRow, rebuild_brand_layout
from .ui.styles import apply_brand_skin

_ASSETS = (
    "update.svg",
    "github.svg",
    "kofi.svg",
    "patreon.svg",
    "discord.svg",
)
_FONT_ASSETS = (
    "fonts/Cinzel-wght.ttf",
    "fonts/Inter-opsz-wght.ttf",
)


def _write_log(lines: list[str]) -> None:
    log_path = os.environ.get("POLYMORPH_SMOKE_LOG")
    if not log_path:
        return
    path = Path(log_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def run_packaged_smoke_test(app: QApplication, sample: Path) -> int:
    """Exercise the frozen application without exposing a user-facing test mode."""
    lines: list[str] = []
    window: MainWindow | None = None
    try:
        sample = sample.resolve()
        if not sample.is_file():
            raise RuntimeError(f"Smoke-test WebP is missing: {sample}")

        tools = find_toolchain()
        for name, path in (
            ("ffmpeg", tools.ffmpeg),
            ("ffprobe", tools.ffprobe),
            ("gifski", tools.gifski),
        ):
            if not path.is_file():
                raise RuntimeError(f"Bundled {name} was not found: {path}")
        lines.append("PASS bundled conversion tools")

        for name in _ASSETS:
            path = asset_path(name)
            if not path.is_file():
                raise RuntimeError(f"Packaged UI resource is missing: {path}")
            if QIcon(str(path)).isNull():
                raise RuntimeError(f"Packaged UI resource could not be loaded: {path}")
        lines.append("PASS packaged footer SVG resources")

        for name in _FONT_ASSETS:
            path = asset_path(name)
            if not path.is_file():
                raise RuntimeError(f"Packaged font resource is missing: {path}")
        loaded_fonts = str(app.property("polymorphFontsLoaded") or "")
        if "Cinzel" not in loaded_fonts or "Inter" not in loaded_fonts:
            raise RuntimeError(f"Bundled brand fonts did not load: {loaded_fonts!r}")
        lines.append("PASS bundled Cinzel and Inter fonts")

        window = MainWindow()
        rebuild_brand_layout(window)
        apply_brand_skin(window)
        window.show()
        app.processEvents()
        if window.converter is None:
            raise RuntimeError("Main window could not resolve the bundled conversion toolchain")

        if window.width() < 1200 or window.height() < 800:
            raise RuntimeError(
                f"Default window geometry regressed: got {window.width()}x{window.height()}, "
                "expected at least 1200x800"
            )
        if window.minimumWidth() < 1080 or window.minimumHeight() < 700:
            raise RuntimeError(
                f"Minimum window geometry regressed: got {window.minimumWidth()}x"
                f"{window.minimumHeight()}, expected >=1080x700"
            )
        lines.append("PASS compact concept-matched default geometry")

        subtitle = window.findChild(QLabel, "BrandSubtitle")
        if window.property("polymorphSkin") != "occult-gold-v3":
            raise RuntimeError("Branded presentation skin was not applied")
        if window.property("polymorphLayout") != "concept-match-v1":
            raise RuntimeError("Concept-matched branded layout was not applied")
        if subtitle is None or subtitle.text() != "MEDIA CONVERSION MAGIC — BY KNIGHT WITCH™":
            raise RuntimeError("Branded subtitle/byline copy is missing")
        if window.convert_btn.accessibleName() != "Cast Polymorph":
            raise RuntimeError("Primary action accessible copy regressed")
        cast_title = window.findChild(QLabel, "CastTitle")
        if cast_title is None or cast_title.text() != "CAST POLYMORPH":
            raise RuntimeError("Concept-style Cast Polymorph face is missing")
        splitter = window.findChild(QSplitter, "BrandMainSplitter")
        if splitter is None or splitter.count() != 2:
            raise RuntimeError("Main workspace is not the two-column composition")
        rail = window.findChild(QScrollArea, "ControlRail")
        if rail is None:
            raise RuntimeError("Right settings rail is missing")
        app.processEvents()
        if rail.horizontalScrollBar().maximum() != 0:
            raise RuntimeError("Right settings rail requires horizontal scrolling/clips content")
        if len(window.findChildren(QFrame, "ControlCard")) < 6:
            raise RuntimeError("Right control rail is missing branded section cards")
        lines.append("PASS concept shell, byline, paired controls, and unclipped rail")

        tooltip_widgets = {
            "file queue": window.file_list,
            "preview": window.preview,
            "GIF format": window.gif_radio,
            "MP4 format": window.mp4_radio,
            "file-size mode": window.size_radio,
            "file-size limit": window.max_mb,
            "resolution mode": window.res_radio,
            "width": window.width_spin,
            "height": window.height_spin,
            "preserve motion": window.motion_preserve_radio,
            "favor resolution": window.motion_favor_radio,
            "framing mode": window.frame_mode,
            "aspect ratio": window.ratio_combo,
            "crop zoom": window.crop_zoom_slider,
            "center framing": window.center_btn,
            "fit background": window.color_btn,
            "output folder": window.output_path,
            "convert": window.convert_btn,
        }
        missing_tooltips = [
            name for name, widget in tooltip_widgets.items() if not widget.toolTip().strip()
        ]
        if missing_tooltips:
            raise RuntimeError(
                "Missing hover tooltip(s): " + ", ".join(missing_tooltips)
            )
        stylesheet = window.styleSheet()
        if "QRadioButton::indicator:checked" not in stylesheet:
            raise RuntimeError("Selected radio controls do not have an explicit visible style")
        if "qradialgradient" not in stylesheet:
            raise RuntimeError("Selected radio controls do not use the centered filled-dot style")
        if '"Cinzel"' not in stylesheet or '"Inter"' not in stylesheet:
            raise RuntimeError("Branded type families are missing from the packaged stylesheet")
        if "QAbstractSpinBox::up-button" not in stylesheet:
            raise RuntimeError("Resolution controls did not suppress ticker-arrow styling")
        lines.append("PASS compact branded typography, tooltips, and field styling")

        window._add_files([sample])
        app.processEvents()

        if window.file_list.count() != 1:
            raise RuntimeError("Main window did not accept the smoke-test WebP")
        item_widget = window.file_list.itemWidget(window.file_list.item(0))
        if not isinstance(item_widget, QueueRow):
            raise RuntimeError("File queue did not create concept-style media rows")
        meta = item_widget.findChild(QLabel, "QueueMeta")
        if meta is None or "×" not in meta.text() or "s" not in meta.text():
            raise RuntimeError(f"File row metadata is incomplete: {meta.text() if meta else None!r}")
        lines.append("PASS file queue thumbnail/metadata row")

        movie = window.preview._movie
        if movie is None or not movie.isValid():
            raise RuntimeError("Qt could not initialize animated WebP playback")
        if not movie.jumpToFrame(0):
            raise RuntimeError("Qt could not decode the first animated WebP frame")

        deadline = time.monotonic() + 2.0
        while window.preview._pixmap.isNull() and time.monotonic() < deadline:
            app.processEvents()
            time.sleep(0.02)
        if window.preview._pixmap.isNull():
            raise RuntimeError("Live preview did not produce a renderable WebP frame")
        lines.append("PASS animated WebP live preview")

        if not window.motion_preserve_radio.isChecked():
            raise RuntimeError("GIF motion priority did not default to Preserve motion")
        window.motion_favor_radio.setChecked(True)
        if window._make_settings().gif_motion_mode is not GifMotionMode.FAVOR_RESOLUTION:
            raise RuntimeError("Favor resolution UI did not map to conversion settings")
        lines.append("PASS adaptive GIF priority controls")

        window._brand_crop_radio.setChecked(True)
        window.ratio_combo.setCurrentText("16:9")
        window.crop_zoom_slider.setValue(150)
        app.processEvents()
        settings = window._make_settings()
        if settings.framing.mode is not FramingMode.CROP:
            raise RuntimeError("Branded Crop radio did not map to conversion settings")
        if abs(settings.framing.zoom - 1.5) > 1e-6:
            raise RuntimeError("Crop zoom UI did not map to conversion settings")
        lines.append("PASS branded framing radios and crop zoom controls")

        window.res_radio.setChecked(True)
        window.width_spin.setValue(64)
        app.processEvents()
        if (window.width_spin.value(), window.height_spin.value()) != (64, 36):
            raise RuntimeError(
                "Linked resolution controls failed for 16:9: "
                f"{window.width_spin.value()}x{window.height_spin.value()}"
            )
        if window.motion_favor_radio.isEnabled():
            raise RuntimeError("Favor resolution should disable in fixed-resolution mode")
        lines.append("PASS linked 16:9 resolution controls")

        lines.append("PACKAGED POLYMORPH SMOKE TEST PASSED")
        _write_log(lines)
        return 0
    except Exception as exc:
        lines.append(f"FAIL {exc}")
        lines.append(traceback.format_exc())
        _write_log(lines)
        return 1
    finally:
        if window is not None:
            window.close()
        app.processEvents()
