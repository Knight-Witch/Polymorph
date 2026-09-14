from __future__ import annotations

import os
import unittest

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

from PySide6.QtWidgets import QApplication, QLabel, QWidget

from polymorph.ui.fonts import load_brand_fonts
from polymorph.ui.styles import _apply_typography, build_brand_stylesheet


class BrandTypographyStylesTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = QApplication.instance() or QApplication([])
        load_brand_fonts(cls.app)

    def test_global_widget_rule_does_not_override_display_fonts(self):
        stylesheet = build_brand_stylesheet(1.0)
        try:
            widget_rule = stylesheet.split("QWidget {", 1)[1].split("}", 1)[0]
        except IndexError as exc:
            self.fail(f"Global QWidget style rule is missing: {exc}")

        self.assertNotIn("font-family:", widget_rule)
        self.assertNotIn("font-size:", widget_rule)

    def test_direct_display_overrides_resolve_to_polymorph_under_inter_body_qss(self):
        root = QWidget()
        root.setObjectName("AppRoot")
        title = QLabel("POLYMORPH", root)
        title.setObjectName("BrandTitle")
        subtitle = QLabel("Media conversion magic — by Knight Witch™", root)
        subtitle.setObjectName("BrandSubtitle")
        heading = QLabel("OUTPUT FORMAT", root)
        heading.setObjectName("CardHeading")

        root.setStyleSheet(build_brand_stylesheet(1.0))
        _apply_typography(root, 1.0)
        root.show()
        self.app.processEvents()

        expected_regular = str(self.app.property("polymorphDisplayFont") or "").strip()
        expected_bold = str(self.app.property("polymorphDisplayBoldFont") or "").strip()
        self.assertTrue(expected_regular)
        self.assertTrue(expected_bold)
        self.assertEqual(title.font().family(), expected_regular)
        self.assertEqual(subtitle.font().family(), expected_regular)
        self.assertEqual(heading.font().family(), expected_bold)
        self.assertGreater(title.font().letterSpacing(), 0)
        self.assertGreater(subtitle.font().letterSpacing(), 0)
        self.assertTrue(heading.font().bold())
        root.close()


if __name__ == "__main__":
    unittest.main()
