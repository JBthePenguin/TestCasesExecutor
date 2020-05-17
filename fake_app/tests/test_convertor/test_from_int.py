from unittest import TestCase
from fake_app.convertor.from_int import FromInt


class TestFromInt(TestCase):
    """TestCase for FromInt."""

    def test_to_bin(self):
        """Assert the return of the method to_bin."""
        self.assertEqual(FromInt(3).to_bin(), '0b11')

    def test_to_hex(self):
        """Assert the return of the method to_hex."""
        self.assertEqual(FromInt(3).to_hex(), '0x3')

    def test_to_str(self):
        """Assert the return of the method to_str."""
        self.assertEqual(FromInt(3).to_str(), '3')
