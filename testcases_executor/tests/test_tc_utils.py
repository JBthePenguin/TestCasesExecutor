"""
Module testcases_executor.tests.test_tc_utils .

Contain TestCase for testcases_executor.tc_utils .

Classes:
    TestUtils(TestCase)

Imports:
    from unittest: TestCase
    from testcases_executor.tc_utils: raise_error, check_type
"""
from unittest import TestCase
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

    def test_raise_error(self):
        """
        Assert if type and message of error raised.

        Call raise_error and assert if type and message are desired ones.

        Assertions:
        ----------
        assertRaises:
            Assert the type of error raised
        assertEqual:
            Assert the error message
        """
        self.assertRaisesRegex(TypeError, "error message.", raise_error, TypeError, "error message.")
        print(f"{Fore.RESET}{Style.NORMAL}")
        # with self.assertRaises(TypeError) as cm:
        #     raise_error(TypeError, "error message.")
        # print(str(cm.exception))
        # self.assertEqual("error message.", str(cm.exception))
        # try:
        #     raise_error(TypeError, "error message.")
        #     self.assertFail()
        # except TypeError as inst:
        #     self.assertEqual(inst.exception.message, "error_msg")
        # with self.assertRaises(TypeError) as error:
        #     raise_error(TypeError, "error message.")
        # self.assertEqual(str(error.exception), '\x1b[39merror message.\x1b[22m\x1b[2m\nFo[94 chars]b[0m')
        #     # self.assertEqual(error.exception.message, 'error message.')
