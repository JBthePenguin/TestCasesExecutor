"""
Module testcases_executor.tests.test_tc_groups .

Contain TestCase for testcases_executor.tc_groups .

Classes:
    TestGroupsFunctions(TestCase)
    TestGroup(TestCase)
    TestGroups(TestCase)

Imports:
    from unittest: TestCase
    from unittest.mock: patch, Mock
    from testcases_executor.tc_groups: import_groups, TestCasesGroup
"""
from unittest import TestCase
from unittest.mock import patch, Mock
from testcases_executor.tc_groups import import_groups, TestCasesGroup


class TestGroupsFunctions(TestCase):
    """
    A subclass of unittest.TestCase .

    Tests for tc_groups functions, import_groups.

    Methods
    ----------
    test_import_groups():
        Assert if groups object imported from testscases.py is returned.
    """

    @patch('testcases_executor.tc_groups.raise_error')
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
        assert_called_once_with:
            Assert if raise_error is called once with Error and error msg.
        assert_not_called:
            Assert if raise_error is not called for an import without error.
        assertEqual:
            Assert if groups is imported correctly.
        """
        mock_raise_error.side_effect = Exception("raise_error called")
        for tc_value, e_type, e_msg in [
                (  # simulate ModuleNotFoundError
                    None, ModuleNotFoundError,
                    "File testcases.py not founded in root directory."),
                (  # simulate ImportError
                    'groups not inside', ImportError,
                    "Object groups not founded in testscases.py .")]:
            with patch.dict('sys.modules', {'testcases': tc_value}):
                try:
                    import_groups()
                except Exception:
                    mock_raise_error.assert_called_once_with(e_type, e_msg)
                    mock_raise_error.reset_mock()
        # import ok
        with patch.dict('sys.modules', {'testcases': Mock(groups='groups')}):
            groups_imported = import_groups()
            mock_raise_error.assert_not_called()
            self.assertEqual(groups_imported, 'groups')


class TestGroup(TestCase):
    """
    A subclass of unittest.TestCase .

    Tests for tc_groups.TestCasesGroup .

    Methods
    ----------
    test_init_group():
        Assert a group object is initialized with good attributes.
    """

    @patch("testcases_executor.tc_groups.raise_error")
    @patch("testcases_executor.tc_utils.raise_error")
    def test_init_group(self, mock_error_one, mock_error_two):
        """
        Assert a group object is initialized with good attributes.

        Init TestCasesGroup and assert if object have desired properties.

        Parameters:
        ----------
        mock_error_one : Mock
            Mock of tc_utils.raise_error function.
        mock_error_two : Mock
            Mock of tc_groups.raise_error function.

        Assertions:
        ----------
        assert_called_once_with:
            Assert if raise_error is called once with Error and error msg.
        assert_not_called:
            Assert if raise_error is not called for an import without error.
        assertEqual:
            Assert if groups is imported correctly.
        """
        mock_error_one.side_effect = Exception("raise_error called")
        mock_error_two.side_effect = Exception("raise_error called")
        # group's name not str, tup[0]
        try:
            TestCasesGroup((1, 2))
        except Exception:
            mock_error_one.assert_called_once_with(
                TypeError, "Group's name must be 'str', not 'int': 1")
            mock_error_one.reset_mock()
        # group's name empty str, tup[0]
        try:
            TestCasesGroup(("", 2))
        except Exception:
            mock_error_two.assert_called_once_with(
                ValueError, "Group's name must be an non empty string.")
            mock_error_two.reset_mock()
        # testcases not a list or tuple, tup[1]
        try:
            TestCasesGroup(("group test", 2))
        except Exception:
            mock_error_one.assert_called_once_with(
                TypeError,
                "Group's testcases must be 'list' or 'tuple', not 'int': 2")
            mock_error_one.reset_mock()
        # item of testcases not a class
        try:
            TestCasesGroup(("group test", (1, )))
        except Exception:
            mock_error_two.assert_called_once_with(
                TypeError,
                "".join([
                    "Item of group's testcases list or tuple must be ",
                    "a class (unittest.TestCase subclass): 1"]))
            mock_error_two.reset_mock()
        # item of testcases not a subclass
        try:
            TestCasesGroup(("group test", [int, ]))
        except Exception:
            mock_error_two.assert_called_once_with(
                TypeError,
                "".join([
                    "Item of group's testcases list or tuple must be ",
                    "a unittest.TestCase subclass: <class 'int'>"]))
            mock_error_two.reset_mock()
