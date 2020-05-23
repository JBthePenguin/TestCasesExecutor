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
    from testcases_executor.tc_groups: (
        import_groups, TestCasesGroup, TestCasesGroups
"""
from unittest import TestCase
from unittest.mock import patch, Mock
from testcases_executor.tc_groups import (
    import_groups, TestCasesGroup, TestCasesGroups)


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


class SubclassTCone(TestCase):
    """
    A subclass of unittest.TestCase .

    Used in testcases list or tuple.
    """

    pass


class SubclassTCtwo(TestCase):
    """
    A subclass of unittest.TestCase .

    Used in testcases list or tuple to init obj with success.
    """

    pass


class TestGroup(TestCase):
    """
    A subclass of unittest.TestCase .

    Tests for tc_groups.TestCasesGroup .

    Methods
    ----------
    test_init_group():
        Assert TestCasesGroup's object is initialized with good attributes.
    """

    @patch("testcases_executor.tc_groups.raise_error")
    @patch("testcases_executor.tc_utils.raise_error")
    def test_init_group(self, mock_error_one, mock_error_two):
        """
        Assert TestCasesGroup's object is initialized with good attributes.

        Init TestCasesGroup and assert if object have desired properties.

        Parameters:
        ----------
        mock_error_one : Mock
            Mock of tc_utils.raise_error function (call in check_type in init).
        mock_error_two : Mock
            Mock of tc_groups.raise_error function (call in init).

        Assertions:
        ----------
        assert_called_once_with:
            Assert if raise_error is called once with Error and error msg.
        assert_not_called:
            Assert if raise_error is not called for init with success.
        assertEqual:
            Assert if obj name and arg name are correct.
        assertListEqual:
            Assert if obj.testcases is the correct list.
        """
        mock_error_one.side_effect = Exception("raise_error called")
        mock_error_two.side_effect = Exception("raise_error called")
        name_no_str = (  # group's name not str, tup[0]
            (1, 2), mock_error_one,
            TypeError, "Group's name must be 'str', not 'int': 1")
        name_empty = (  # group's name empty str, tup[0]
            ("", 2), mock_error_two,
            ValueError, "Group's name must be an non empty string.")
        tc_no_list_tup = (  # testcases not a list or tuple, tup[1]
            ("group test", 2), mock_error_one,
            TypeError,
            "Group's testcases must be 'list' or 'tuple', not 'int': 2")
        item_no_class = (  # item of testcases not a class
            ("group test", (1, )), mock_error_two,
            TypeError,
            "".join([
                "Item of group's testcases list or tuple must be ",
                "a class (unittest.TestCase subclass): 1"]))
        item_no_subclass = (  # item of testcases not a subclass
            ("group test", [int, ]), mock_error_two,
            TypeError,
            "".join([
                "Item of group's testcases list or tuple must be ",
                "a unittest.TestCase subclass: <class 'int'>"]))
        item_no_used_once = (  # testcase not used once
            ("group test", [SubclassTCone, SubclassTCone]), mock_error_two,
            ValueError,
            "Testcase's subclass must used once in group: 'SubclassTCone'.")
        for group_tup, mock_error, e_type, e_msg in [
                name_no_str, name_empty, tc_no_list_tup,
                item_no_class, item_no_subclass, item_no_used_once]:
            try:
                TestCasesGroup(group_tup)
            except Exception:
                mock_error.assert_called_once_with(e_type, e_msg)
                mock_error.reset_mock()
        # init success
        obj = TestCasesGroup(("group test", (SubclassTCone, SubclassTCtwo)))
        mock_error_one.assert_not_called()
        mock_error_two.assert_not_called()
        self.assertEqual(obj.name, "Group test")
        self.assertEqual(obj.arg_name, "group_test")
        self.assertListEqual(obj.testcases, [SubclassTCone, SubclassTCtwo])


class TestGroups(TestCase):
    """
    A subclass of unittest.TestCase .

    Tests for tc_groups.TestCasesGroups .

    Methods
    ----------
    test_init_groups():
        Assert TestCasesGroups's object is initialized.
    """

    @patch("testcases_executor.tc_groups.raise_error")
    @patch("testcases_executor.tc_utils.raise_error")
    def test_init_groups(self, mock_error_one, mock_error_two):
        """
        Assert TestCasesGroups's object is initialized.

        Init TestCasesGroups and assert if it's the desired list.

        Parameters:
        ----------
        mock_error_one : Mock
            Mock of tc_utils.raise_error function (call in check_type in init).
        mock_error_two : Mock
            Mock of tc_groups.raise_error function (call in init).

        Assertions:
        ----------
        assert_called_once_with:
            Assert if raise_error is called once with Error and error msg.
        assert_not_called:
            Assert if raise_error is not called for init with success.
        assertIsInstance:
            Assert if obj is a list and items TestCasesGroup.
        assertEqual:
            Assert if len obj is 2, if obj[i] name and arg name are correct.
        assertListEqual:
            Assert if obj[i].testcases is the correct list.
        """
        mock_error_one.side_effect = Exception("raise_error called")
        mock_error_two.side_effect = Exception("raise_error called")
        groups_no_list_tup = (  # groups not a list or tuple
            2, mock_error_one,
            TypeError,
            "Object groups must be 'list' or 'tuple', not 'int': 2")
        item_no_tup = (  # groups's item not a tuple
            [2, ], mock_error_one,
            TypeError,
            "Item of groups must be 'tuple', not 'int': 2")
        item_no_two_items = (  # groups's item not contain 2 items
            [(1, 2, 3), ], mock_error_two,
            IndexError, "".join([
                "Group tuple must contain 2 items (group's name, ",
                "testcases list or tuple), not 3"]))
        name_no_used_once = (  # group's name not used once
            (
                ("group test", [SubclassTCone, ]),
                ('group test', (SubclassTCtwo, ))),
            mock_error_two, ValueError,
            "Group's name must used once, 'Group test'.")
        tc_no_used_once = (  # testcase not used once
            (
                ("group test", [SubclassTCone, ]),
                ('group test two', (SubclassTCtwo, SubclassTCone))),
            mock_error_two, ValueError,
            "Testcase must used only in one group, 'SubclassTCone'")
        for tc_groups, mock_error, e_type, e_msg in [
                groups_no_list_tup, item_no_tup, item_no_two_items,
                name_no_used_once, tc_no_used_once]:
            try:
                TestCasesGroups(tc_groups)
            except Exception:
                mock_error.assert_called_once_with(e_type, e_msg)
                mock_error.reset_mock()
        # init success
        obj = TestCasesGroups([
            ("group test", [SubclassTCone, ]),
            ('group test*2', (SubclassTCtwo, ))])
        mock_error_one.assert_not_called()
        mock_error_two.assert_not_called()
        self.assertIsInstance(obj, list)
        self.assertEqual(len(obj), 2)
        for group in obj:
            self.assertIsInstance(group, TestCasesGroup)
        self.assertEqual(obj[0].name, "Group test")
        self.assertEqual(obj[0].arg_name, "group_test")
        self.assertListEqual(obj[0].testcases, [SubclassTCone, ])
        self.assertEqual(obj[1].name, "Group test*2")
        self.assertEqual(obj[1].arg_name, "group_test_2")
        self.assertListEqual(obj[1].testcases, [SubclassTCtwo, ])
