"""
Module testcases_executor.tests.test_tc_utils .

Contain TestCase for testcases_executor.tc_utils .

Classes:
    TestUtils(TestCase)

Imports:
    from unittest: TestCase, patch
    from testcases_executor.tc_utils: raise_error, check_type, BOLD, RED
"""
from unittest import TestCase
from unittest.mock import patch
from testcases_executor.tc_utils import raise_error, check_type, BOLD, RED


class TestUtils(TestCase):
    """
    A subclass of unittest.TestCase .

    Testase for tc_utils, raise_error and check_type.

    Methods
    ----------
    test_raise_error():
        Assert if type and message of error raised by raise_error.
    test_check_type():
        Assert if error is raised or not by check_type.
    """

    @patch("builtins.print")
    def test_raise_error(self, mock_print):
        """
        Assert if type and message of error raised.

        Call raise_error and assert if type and message are desired ones.

        Parameters:
        ----------
        mock_print : Mock
            Mock of print function.

        Assertions:
        ----------
        assertRaisesRegex:
            Assert the type of error raised and his message.
        assert_called_once_with:
            Assert if print is called once to set color and style.
        """
        for e_type, e_msg in [  # with TypeError, ModuleNotFoundError
                (TypeError, 'message 1'), (ModuleNotFoundError, 'message 2')]:
            self.assertRaisesRegex(e_type, e_msg, raise_error, e_type, e_msg)
            mock_print.assert_called_once_with(f"{BOLD}{RED}")
            mock_print.reset_mock()

    @patch("testcases_executor.tc_utils.raise_error")
    def test_check_type(self, mock_raise_error):
        """
        Assert if TypeError is raised or not by check_type.

        Call check_type, assert if raise_error is not called or once with args.

        Parameters:
        ----------
        mock_raise_error : Mock
            Mock of tc_utils.raise_error function.

        Assertions:
        ----------
        assert_not_called:
            Assert if raise_error is not called.
        assert_called_once_with:
            Assert if raise_error is called once with TypeError and error msg.
        """
        for obj, desired_classes, obj_msg in [  # check passed
                ([1, 2], (list, ), 'Obj 1'), ((1, 2), (list, tuple), 'Obj 2')]:
            check_type(obj, desired_classes, obj_msg)
            mock_raise_error.assert_not_called
        for obj, desired_classes, obj_msg, end_msg in [  # error raised
                ((1, 2), (list, ), 'Obj 3', "'list'"),
                ((1, 2), (int, str), 'Obj 4', "'int' or 'str'")]:
            check_type(obj, desired_classes, obj_msg)
            mock_raise_error.assert_called_once_with(
                TypeError, f"{obj_msg} must be {end_msg}, not 'tuple': (1, 2)")
            mock_raise_error.reset_mock()
