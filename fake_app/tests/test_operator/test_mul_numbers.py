from unittest import TestCase
from fake_app.operator.mul_numbers import MulTwo, MulThree


class TestMulTwo(TestCase):
    """TestCase for MulTwo."""

    def test_int_result(self):
        """Assert the return of the method int_result."""
        self.assertEqual(MulTwo(3, 3.5).int_result(), 10)

    def test_float_result(self):
        """Assert the return of the method float_result."""
        self.assertEqual(MulTwo(3, 3.5).float_result(), 10.5)

    def test_bin_result(self):
        """Assert the return of the method bin_result."""
        self.assertEqual(MulTwo(3, 3).bin_result(), '0b1001')


class TestMulThree(TestCase):
    """TestCase for MulThree."""

    def test_int_result(self):
        """Assert the return of the method int_result."""
        self.assertEqual(MulThree(3, 3.5, 3).int_result(), 31)

    def test_float_result(self):
        """Assert the return of the method float_result."""
        self.assertEqual(MulThree(3, 3.5, 3).float_result(), 31.5)

    def test_bin_result(self):
        """Assert the return of the method bin_result."""
        self.assertEqual(MulThree(3, 3, 3).bin_result(), '0b11011')