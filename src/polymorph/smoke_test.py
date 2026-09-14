from __future__ import annotations

import os
import time
import traceback
from pathlib import Path

from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication, QLabel, QSplitter, QWidget

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
_CONCEPT_ICON_ASSETS = (
    "ui/aspect-ratio.png",
    "ui/crop.png",
    "ui/folder.png",
    "ui/priority.png",
    "ui/resize.png",
    "ui/trash.png",
    "ui/update.png",
)
_FONT_ASSETS = (
    "fonts/Polymorph-Regular.ttf.xz",
    "fonts/Polymorph-Bold.ttf.xz",
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


class _CheckpointLines(list[str]):
    """Persist every smoke checkpoint so a timeout still shows the last passed stage."""

    def append(self, item: str) -> None:
        super().append(item)
        _write_log(self)


def run_packaged_smoke_test(app: QApplication, sample: Path) -> int:
    lines: list[str] = _CheckpointLines()
    window: MainWindow | None = None
    try:
        sample = sample.resolve()
        if not sample.is_file():
            raise RuntimeError(f"Smoke-test WebP is missing: {sample}")

        tools = find_toolchain()
        for name, path in (("ffmpeg", tools.ffmpeg), ("ffprobe", tools.ffprobe), ("gifski", tools.gifski)):
            if not path.is_file():
                raise RuntimeError(f"Bundled {name} was not found: {path}")
        lines.append("PASS bundled conversion tools")

        for name in _ASSETS:
            path = asset_path(name)
            if not path.is_file() or QIcon(str(path)).isNull():
                raise RuntimeError(f"Packaged footer resource is missing or invalid: {path}")
        for name in _CONCEPT_ICON_ASSETS:
            path = asset_path(name)
            if not path.is_file():
                raise RuntimeError(f"Packaged concept icon is missing: {path}")
        lines.append("PASS packaged footer and supplied concept icon resources")

        for name in _FONT_ASSETS:
            path = asset_path(name)
            if not path.is_file():
                raise RuntimeError(f"Packaged font resource is missing: {path}")
        loaded_fonts = str(app.property("polymorphFontsLoaded") or "")
        for logical_name in ("Polymorph Regular", "Polymorph Bold", "Cinzel", "Inter"):
            if logical_name not in loaded_fonts:
                raise RuntimeError(
                    f"Required packaged font did not register ({logical_name}): {loaded_fonts!r}"
                )
        if app.property("polymorphDisplaySource") != "bundled-polymorph":
            raise RuntimeError(
                "Packaged build is not using its bundled Polymorph display assets: "
                f"{app.property('polymorphDisplaySource')!r}"
            )
        if not str(app.property("polymorphDisplayFont") or "").strip():
            raise RuntimeError("Bundled Polymorph regular family was not resolved")
        if not str(app.property("polymorphDisplayBoldFont") or "").strip():
            raise RuntimeError("Bundled Polymorph bold family was not resolved")
        lines.append("PASS packaged Polymorph display fonts and Inter body font")

        window = MainWindow()
        rebuild_brand_layout(window)
        apply_brand_skin(window)
        window.move(-4000, -4000)
        window.show()
        app.processEvents()
        if window.converter is None:
            raise RuntimeError("Main window could not resolve the bundled conversion toolchain")
        lines.append("PASS packaged main window initialization")

        if (window.width(), window.height()) != (1260, 820):
            raise RuntimeError(f"Default concept geometry regressed: {window.width()}x{window.height()}")
        if window.minimumWidth() != 920 or window.minimumHeight() != 640:
            raise RuntimeError(
                f"Responsive floor regressed: {window.minimumWidth()}x{window.minimumHeight()}"
            )
        lines.append("PASS responsive concept default/minimum geometry")

        title = window.findChild(QLabel, "BrandTitle")
        subtitle = window.findChild(QLabel, "BrandSubtitle")
        headings = window.findChildren(QLabel, "CardHeading")
        if window.property("polymorphSkin") != "occult-gold-v5":
            raise RuntimeError("Branded presentation skin was not applied")
        if window.property("polymorphFidelity") != "mockup-v1":
            raise RuntimeError("Mockup fidelity pass was not applied")
        if window.property("polymorphLayout") != "concept-match-v2":
            raise RuntimeError("Concept v2 layout was not applied")
        if subtitle is None or subtitle.text() != "Media conversion magic — by Knight Witch™":
            raise RuntimeError("Mixed-case branded subtitle/byline copy is missing")
        if window.convert_btn.text() != "POLYMORPH" or window.convert_btn.accessibleName() != "Polymorph":
            raise RuntimeError("Primary action did not return to POLYMORPH")

        stylesheet = window.styleSheet()
        try:
            widget_rule = stylesheet.split("QWidget {", 1)[1].split("}", 1)[0]
        except IndexError as exc:
            raise RuntimeError("Global QWidget style rule is missing") from exc
        if "font-family:" in widget_rule or "font-size:" in widget_rule:
            raise RuntimeError(
                "Global QWidget stylesheet is overriding explicit Polymorph display typography"
            )
        expected_regular = str(app.property("polymorphDisplayFont") or "").strip()
        expected_bold = str(app.property("polymorphDisplayBoldFont") or "").strip()
        if title is None or title.font().family() != expected_regular:
            raise RuntimeError(
                f"Brand title is not using Polymorph Regular: "
                f"{title.font().family() if title else None!r} != {expected_regular!r}"
            )
        if subtitle.font().family() != expected_regular:
            raise RuntimeError(
                f"Brand subtitle is not using Polymorph Regular: "
                f"{subtitle.font().family()!r} != {expected_regular!r}"
            )
        if title.font().letterSpacing() <= 0 or subtitle.font().letterSpacing() <= 0:
            raise RuntimeError("Brand title/subtitle tracking was not applied")
        if not headings:
            raise RuntimeError("No branded card headings were found")
        bad_headings = [
            (heading.text(), heading.font().family(), heading.font().bold())
            for heading in headings
            if heading.font().family() != expected_bold or not heading.font().bold()
        ]
        if bad_headings:
            raise RuntimeError(f"Card headings are not using Polymorph Bold: {bad_headings!r}")
        lines.append("PASS applied Polymorph title/subtitle/card-heading typography")

        splitter = window.findChild(QSplitter, "BrandMainSplitter")
        if splitter is None or splitter.count() != 2:
            raise RuntimeError("Main workspace is not the two-column composition")
        rail = window.findChild(QWidget, "ControlRailContent")
        if rail is None:
            raise RuntimeError("Responsive right settings rail is missing")
        lines.append("PASS title/byline, mockup fidelity, two-column shell, and POLYMORPH action")

        file_card = window.findChild(QWidget, "FileCard")
        file_count = window.findChild(QLabel, "FileCount")
        if file_card is None or file_count is None or file_card.layout() is None:
            raise RuntimeError("FILES card/header is missing")
        files_header = file_card.layout().itemAt(0).layout()
        if files_header is None:
            raise RuntimeError("FILES action row is missing")
        heading_index = -1
        for index in range(files_header.count()):
            widget = files_header.itemAt(index).widget()
            if isinstance(widget, QLabel) and widget.objectName() == "CardHeading":
                heading_index = index
                break
        if heading_index < 0 or files_header.indexOf(file_count) != heading_index + 1:
            raise RuntimeError("FILES count is not grouped directly with the FILES title")
        lines.append("PASS FILES title/count/action grouping")

        window.resize(920, 640)
        app.processEvents()
        scale = float(window.property("brandScale") or 1.0)
        if scale >= 0.99:
            raise RuntimeError(f"Responsive shrink mode did not engage: scale={scale}")
        bottom = window.convert_btn.mapTo(rail, window.convert_btn.rect().bottomRight()).y()
        if bottom > rail.height() + 2:
            raise RuntimeError(
                f"POLYMORPH action is clipped at minimum size: button bottom {bottom}, rail {rail.height()}"
            )
        lines.append("PASS responsive shrink keeps primary action visible")

        stylesheet = window.styleSheet()
        if "QAbstractSpinBox::up-button" not in stylesheet:
            raise RuntimeError("Resolution controls restored ticker-arrow styling")
        if "QSlider#CropZoomSlider" not in stylesheet or "QSlider#PlaybackTimeline" not in stylesheet:
            raise RuntimeError("Concept slider styling is missing")
        if "mockupIndented" not in stylesheet:
            raise RuntimeError("Mockup content-column alignment styling is missing")
        lines.append("PASS concept field, alignment, and slider styling")

        window.resize(1260, 820)
        app.processEvents()
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
        deadline = time.monotonic() + 2.0
        while window.preview._pixmap.isNull() and time.monotonic() < deadline:
            app.processEvents()
            time.sleep(0.02)
        if window.preview._pixmap.isNull():
            raise RuntimeError("Live preview did not produce a renderable WebP frame")
        if window.preview.total_frames() <= 0 or window.preview.duration_seconds() <= 0:
            raise RuntimeError("Preview timing metadata did not initialize")
        # Deliberately do not call QMovie.jumpToFrame() in the offscreen frozen smoke.
        # Qt's headless WebP plugin can wedge on random-access seeks even though the
        # normal interactive Windows plugin path is responsive. Real seek/playback
        # behavior remains available in the desktop UI and is human-testable.
        lines.append("PASS animated WebP preview decode and playback metadata")

        if not window.motion_preserve_radio.isChecked():
            raise RuntimeError("GIF motion priority did not default to Preserve motion")
        window.motion_favor_radio.setChecked(True)
        if window._make_settings().gif_motion_mode is not GifMotionMode.FAVOR_RESOLUTION:
            raise RuntimeError("Favor resolution UI did not map to conversion settings")
        lines.append("PASS adaptive GIF priority controls")

        window._brand_fit_radio.setChecked(True)
        app.processEvents()
        if window.color_btn.isVisible():
            raise RuntimeError("Fit background Fill control reappeared in the branded UI")
        window._brand_crop_radio.setChecked(True)
        window.ratio_combo.setCurrentText("16:9")
        window.crop_zoom_slider.setValue(150)
        app.processEvents()
        settings = window._make_settings()
        if settings.framing.mode is not FramingMode.CROP:
            raise RuntimeError("Branded Crop radio did not map to conversion settings")
        if abs(settings.framing.zoom - 1.5) > 1e-6:
            raise RuntimeError("Crop zoom UI did not map to conversion settings")
        lines.append("PASS framing radios, hidden Fit Fill, and crop zoom mapping")

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

        footer_meta = [label.text() for label in window.findChildren(QLabel, "FooterMeta")]
        if not any(text.startswith("Polymorph v0.1.0-dev.25") for text in footer_meta):
            raise RuntimeError(f"Footer version metadata is missing: {footer_meta}")
        if "Polymorph 2026, Knight Witch™" not in footer_meta:
            raise RuntimeError(f"Footer creator metadata is missing: {footer_meta}")
        lines.append("PASS footer version/creator metadata")

        lines.append("PACKAGED POLYMORPH SMOKE TEST PASSED")
        return 0
    except Exception as exc:
        lines.append(f"FAIL {exc}")
        lines.append(traceback.format_exc())
        return 1
    finally:
        if window is not None:
            window.close()
        app.processEvents()
