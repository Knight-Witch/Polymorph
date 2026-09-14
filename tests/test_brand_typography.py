import unittest

from polymorph.ui.styles import build_brand_stylesheet


class BrandTypographyStylesTests(unittest.TestCase):
    def test_global_widget_rule_does_not_override_display_fonts(self):
        stylesheet = build_brand_stylesheet(1.0)
        try:
            widget_rule = stylesheet.split("QWidget {", 1)[1].split("}", 1)[0]
        except IndexError as exc:
            self.fail(f"Global QWidget style rule is missing: {exc}")

        self.assertNotIn("font-family:", widget_rule)
        self.assertNotIn("font-size:", widget_rule)


if __name__ == "__main__":
    unittest.main()
