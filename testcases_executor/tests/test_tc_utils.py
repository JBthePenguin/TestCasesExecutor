"""
Module testcases_executor.tests.test_tc_utils .

Contain TestCase for testcases_executor.tc_utils .

Classes:
    TestUtils(TestCase)

Imports:
    from unittest: TestCase, patch
    from testcases_executor.tc_utils: raise_error, check_type
"""
from unittest import TestCase
from unittest.mock import patch
from testcases_executor.tc_utils import raise_error, check_type
from colorama import Fore, Style


class TestUtils(TestCase):
    """
    A subclass of unittest.TestCase .

    Test utils raise_error and check_type.

    Methods
    ----------
    test_raise_error():
        Assert if type and message of error raised.
    test_check_type():
        Assert if error is raised or not.
    """

    @patch("builtins.print")
    def test_raise_error(self, mock_print):
        """
        Assert if type and message of error raised.

        Call raise_error and assert if type and message are desired ones.

        Assertions:
        ----------
        assertRaisesRegex:
            Assert the type of error raised and his message.
        assert_called_once_with:
            Assert if print is called once to set color and style.
        """
        self.assertRaisesRegex(  # with TypeError
            TypeError, "error message.", raise_error,
            TypeError, "error message.")
        mock_print.assert_called_once_with(f"{Style.BRIGHT}{Fore.RED}")
        mock_print.reset_mock()
        self.assertRaisesRegex(  # with ModuleNotFoundError
            ModuleNotFoundError, "second error message.", raise_error,
            ModuleNotFoundError, "second error message.")
        mock_print.assert_called_once_with(f"{Style.BRIGHT}{Fore.RED}")
        mock_print.reset_mock()
