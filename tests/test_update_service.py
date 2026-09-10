import unittest

from polymorph.update_service import is_newer


class UpdateVersionTests(unittest.TestCase):
    def test_newer_release(self):
        self.assertTrue(is_newer("1.0.0", "0.1.0-dev.1"))

    def test_same_release(self):
        self.assertFalse(is_newer("1.2.3", "1.2.3"))

    def test_older_release(self):
        self.assertFalse(is_newer("1.2.2", "1.2.3"))


if __name__ == "__main__":
    unittest.main()
