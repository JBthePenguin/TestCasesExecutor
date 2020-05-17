from unittest import TestCase
from fake_app.convertor.from_float import FromFloat


class TestFromFloat(TestCase):
    """TestCase for FromFloat."""

    def test_to_int(self):
        """Assert the return of the method to_int."""
        self.assertEqual(FromFloat(3.5).to_int(), 3)

    def test_to_str(self):
        """Assert the return of the method to_str."""
        self.assertEqual(FromFloat(3.5).to_str(), '3,5')
