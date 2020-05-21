"""
Module testcases_executor.tests.test_tc_groups .

Contain TestCase for testcases_executor.tc_groups .

Classes:
    TestGroupsFunctions(TestCase)
    TestGroup(TestCase)
    TestGroups(TestCase)

Imports:
    from unittest: TestCase
    from unittest.mock: patch
    from testcases_executor.tc_groupss: raise_error, check_type, BOLD, RED
"""
from unittest import TestCase
from unittest.mock import patch
from testcases_executor.tc_groups import import_groups


class TestGroupsFunctions(TestCase):
    """
    A subclass of unittest.TestCase .

    Tests for tc_groups functions, import_groups.

    Methods
    ----------
    test_import_groups():
        Assert if groups object imported from testscases.py is returned.
    """

    @patch("testcases_executor.tc_groups.raise_error")
    def test_import_groups(self, mock_raise_error):
        """
        Assert if groups object imported from testscases.py is returned.

        Call import_groups and assert if object is returned or an error raised.

        Parameters:
        ----------
        mock_raise_error : Mock
            Mock of tc_utils.raise_error function.

        Assertions:
        ----------
        assertRaisesRegex:
            Assert the type of error raised and his message.
        assert_called_once_with:
            Assert if raise_error is called once with Error and error msg.
        """
        # simulate ModuleNotFoundError
        with patch.dict('sys.modules', {'testcases': None}):
            import_groups()
            mock_raise_error.assert_called_once_with(
                ModuleNotFoundError,
                "File testcases.py not founded in root directory.")
