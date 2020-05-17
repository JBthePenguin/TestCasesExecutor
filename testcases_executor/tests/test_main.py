from unittest import TestCase
from unittest.mock import Mock, patch
from testcases_executor.__main__ import get_groups


class TestMain(TestCase):
    """Test Case for testcases_executor/__main__.py"""

    def test_get_groups(self):
        """Assert get_groups return for ModuleNotFounded and Import Errors,
        for groups is not and is instance list."""
        # simulate ModuleNotFoundError
        with patch.dict('sys.modules', {'testcases': None}):
            from os import curdir
            from os.path import basename, abspath
            root_dir = basename(abspath(curdir))
            groups_imported = get_groups()
            self.assertEqual(
                f"\nFile testcases.py not founded in root -> {root_dir}.",
                groups_imported)
        # simulate ImportError
        with patch.dict("sys.modules", {'testcases': 'Nothing inside'}):
            groups_imported = get_groups()
            self.assertEqual(
                "\nList groups not founded in testscases.py .",
                groups_imported)
        # simulate groups is not list instance
        with patch.dict("sys.modules", {'testcases': Mock(groups='not list')}):
            groups_imported = get_groups()
            self.assertEqual(
                '\nInstance groups must to be a list.',
                groups_imported)
        # simulate groups is list instance
        with patch.dict("sys.modules", {'testcases': Mock(groups=[1, 2, 3])}):
            # with patch("testcases.groups", result_value=[1, 2, 3]):
            groups_imported = get_groups()
            self.assertListEqual([1, 2, 3], groups_imported)
