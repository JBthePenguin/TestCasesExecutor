from unittest import TestCase
from unittest.mock import Mock, patch
from testcases_executor.__main__ import get_groups, check_components, main


class FakeTestCase(TestCase):
    pass


class TestMain(TestCase):
    """Test Case for testcases_executor/__main__.py"""

    def assert_get_groups(self, tc_value, desired_result):
        """Assert if get_groups return the desired result."""
        # simulate ModuleNotFoundError
        with patch.dict('sys.modules', {'testcases': tc_value}):
            self.assertEqual(desired_result, get_groups())

    def test_get_groups(self):
        """Assert get_groups returns for ModuleNotFounded and Import Errors,
        for groups is not and is instance list."""
        # simulate ModuleNotFoundError
        from os import curdir
        from os.path import basename, abspath
        root_dir = basename(abspath(curdir))
        self.assert_get_groups(
            None, f"\nFile testcases.py not founded in root -> {root_dir}.")
        # simulate ImportError
        self.assert_get_groups(
            'Nothing inside', "\nList groups not founded in testscases.py .")
        # simulate groups is not list instance
        self.assert_get_groups(
            Mock(groups='not list'), '\nInstance groups must to be a list.')
        # simulate groups is list instance
        self.assert_get_groups(Mock(groups=[1, 2, 3]), [1, 2, 3])

    def assert_check_components(self, groups_value, desired_result):
        """Assert if check_components return the desired result."""
        # simulate ModuleNotFoundError
        self.assertEqual(check_components(groups_value), desired_result)

    def test_check_components(self):
        """Assert check_components returns for component not a tuple,
        group's name(component[0]) not a string,
        group's testcases(component[1]) not a list,
        component of group's testcases is not a class,
        component of group's testcases is not and is a subclass of TestCase."""
        # simulate component not a tuple
        self.assert_check_components(
            [(1, 2), 3], "\nComponent of groups must to be a tuple.")
        # simulate component[0] not a string
        self.assert_check_components(
            [('a', 2), (3, 4)], "\nGroup's name must to be a string.")
        # simulate component[1] not a list
        self.assert_check_components(
            [('a', [1, ]), ('b', 4)], "\nGroup's testcases must to be a list.")
        # simulate component[1]'s component not a class
        self.assert_check_components(
            [('a', [FakeTestCase, ]), ('b', [1, ])], "".join([
                "\nComponent of group's testcases list ",
                "must to be a class (unittest.TestCase subclass)."]))
        # simulate component[1]'s component not a subclass of TestCase
        self.assert_check_components(
            [('a', [FakeTestCase, ]), ('b', [int, ])], "".join([
                "\nComponent of group's testcases list ",
                "must to be unittest.TestCase subclass."]))
        # simulate all component[1]'s components are a subclass of TestCase
        self.assert_check_components(
            [('a', [FakeTestCase, ]), ('b', [FakeTestCase, FakeTestCase])],
            [('a', [FakeTestCase, ]), ('b', [FakeTestCase, FakeTestCase])])

    def assert_main(self, mock_get, check_tup, print_tup, parser_tup):
        """Call main and assert if get_groups is called once,
        if check_components and print is not or is called once with arg."""
        main()
        mock_get.assert_called_once()
        mock_get.reset_mock()
        for mock_foo, arg_value in [check_tup, print_tup, parser_tup]:
            if arg_value is None:
                mock_foo.assert_not_called()
            else:
                mock_foo.assert_called_once_with(arg_value)
                mock_foo.reset_mock()

    @patch("builtins.print")
    @patch('testcases_executor.__main__.get_groups')
    @patch('testcases_executor.__main__.check_components')
    @patch('testcases_executor.__main__.TestCasesParser')
    def test_main(self, mock_parser, mock_check, mock_get, mock_print):
        """Assert main returns for get_groups return a string,
        for get_groups return a list and check_components a string,
        for get_groups return a list and check_components the same."""
        base_error_msg = "\n".join([
            "\nFor more infos about usage, see README.md:",
            "https://github.com/JBthePenguin/TestCasesExecutor\n"])
        # get_groups return a string
        mock_get.return_value = "a"
        self.assert_main(
            mock_get, (mock_check, None), (mock_print, f"a\n{base_error_msg}"),
            (mock_parser, None))
        # get_groups return a list
        mock_get.return_value = [1, 2, 3]
        # check_components return a string
        mock_check.return_value = "b"
        self.assert_main(
            mock_get, (mock_check, [1, 2, 3]),
            (mock_print, f"b\n{base_error_msg}"), (mock_parser, None))
        # check_components return same than get_groups
        mock_check.return_value = [1, 2, 3]
        self.assert_main(
            mock_get, (mock_check, [1, 2, 3]), (mock_print, None),
            (mock_parser, [1, 2, 3]))
