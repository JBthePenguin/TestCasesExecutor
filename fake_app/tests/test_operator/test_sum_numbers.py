from unittest import TestCase
from fake_app.operator.sum_numbers import SumTwo, SumThree


class TestSumTwo(TestCase):
    """TestCase for SumTwo."""

    def test_int_result(self):
        """Assert the return of the method int_result."""
        self.assertEqual(SumTwo(3, 3.5).int_result(), 6)

    def test_float_result(self):
        """Assert the return of the method float_result."""
        self.assertEqual(SumTwo(3, 3.5).float_result(), 6.5)

    def test_bin_result(self):
        """Assert the return of the method bin_result."""
        self.assertEqual(SumTwo(3, 3).bin_result(), '0b110')


class TestSumThree(TestCase):
    """TestCase for SumThree."""

    def test_int_result(self):
        """Assert the return of the method int_result."""
        self.assertEqual(SumThree(3, 3.5, 3).int_result(), 9)

    def test_float_result(self):
        """Assert the return of the method float_result."""
        self.assertEqual(SumThree(3, 3.5, 3).float_result(), 9.5)

    def test_bin_result(self):
        """Assert the return of the method bin_result."""
        self.assertEqual(SumThree(3, 3, 3).bin_result(), '0b1001')
