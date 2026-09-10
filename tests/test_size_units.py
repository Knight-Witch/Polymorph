import unittest

from polymorph.size_units import bytes_to_mb, mb_to_bytes


class SizeUnitTests(unittest.TestCase):
    def test_99_mb_is_decimal_bytes(self):
        self.assertEqual(mb_to_bytes(99.0), 99_000_000)

    def test_fractional_mb_is_decimal_bytes(self):
        self.assertEqual(mb_to_bytes(12.5), 12_500_000)

    def test_bytes_to_mb_uses_decimal_units(self):
        self.assertEqual(bytes_to_mb(99_000_000), 99.0)


if __name__ == "__main__":
    unittest.main()
