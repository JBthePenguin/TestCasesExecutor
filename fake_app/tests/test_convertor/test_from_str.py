from unittest import TestCase
from fake_app.convertor.from_str import FromStr


class TestFromStr(TestCase):
    """TestCase for FromStr."""

    def test_to_int(self):
        """Assert the return of the method to_int."""
        self.assertEqual(FromStr('5').to_int(), 5)

    def test_to_float(self):
        """Assert the return of the method to_float."""
        self.assertEqual(FromStr('5,3').to_float(), 5.3)

    def test_to_bin(self):
        """Assert the return of the method to_bin."""
        self.assertEqual(FromStr('jb').to_bin(), '11010101100010')
