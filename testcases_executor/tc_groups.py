"""
Module testcases_executor.tc_groups

Contain necessary classes and functions to make groups of TestCases.

Classes:
    TestCasesGroup
    TestCasesGroups

Functions:
    import_groups()

Imports:
    from unittest: TestCase
    from testcases_executor.tc_utils: raise_error, check_type
"""
from unittest import TestCase
from testcases_executor.tc_utils import raise_error, check_type


def import_groups():
    """
    Try to import groups, raise errors or return it.

        Returns:
            object: groups.

        Raises:
            ModuleNotFoundError: testscases.py not founded.
            ImportError: groups not founded in testscases.py .
    """
    error_type = None
    try:
        from testcases import groups
    except ModuleNotFoundError:  # testscases.py not founded
        error_type = "ModuleNotFound"
    except ImportError:  # groups not founded in testscases.py
        error_type = "Import"
    if error_type is not None:  # error during import
        if error_type == "ModuleNotFound":
            raise_error(
                ModuleNotFoundError,
                "File testcases.py not founded in root directory.")
        raise_error(
            ImportError, "Object groups not founded in testscases.py .")
    return groups


class TestCasesGroup():
    """
    A class to represent a group of TestCases.

    A group with a name and a list of TestCases.

    Attributes
    ----------
    name : str
        string not empty.
    testases : list
        instances subclass of unittest.TestCase .
    """

    def __init__(self, group_tup):
        """
        Constructs all the necessary attributes for the group object.

        Parameters
        ----------
            group_tup : tuple
                name and testcases's list or tuple.

        Raises
        ----------
            ValueError: name empty string, subclass not used once.
            TypeError: testcase not a subclass of unittest.TestCase .
        """
        group_name, group_tc = group_tup
        check_type(group_name, (str, ), "Group's name")
        if not group_name:  # name empty string
            raise_error(
                ValueError, "Group's name must be an non empty string.")
        check_type(group_tc, (list, tuple), "Group's testcases")
        for testcase in group_tc:
            error_type = None
            try:  # item in testcases not
                if not issubclass(testcase, TestCase):  # a TestCase subclass
                    error_type = "unittest.TestCase subclass"
            except TypeError:  # a class
                error_type = "class (unittest.TestCase subclass)"
            if error_type is not None:  # TypeError for tc
                raise_error(TypeError, "".join([
                    "Item of group's testcases list or tuple must be ",
                    f"a {error_type}: {testcase}"]))
            if group_tc.count(testcase) != 1:  # testcase not used once
                raise_error(ValueError, "".join([
                    "Testcase's subclass must used once in group: ",
                    f"'{testcase.__name__}'."]))
        self.name, self.testcases = group_tup
        if isinstance(self.testcases, tuple):  # convert to list
            self.testcases = list(self.testcases)


class TestCasesGroups(list):
    """
    A class to represent a list of TestCasesGroup object.

    A list with TestCasesGroup's objects for items.

    Self
    ----------
    [TestCasesGroup1, TestCasesGroup2, ...]
    """

    def __init__(self, tc_groups=import_groups()):
        """
        Constructs list of TestCasesGroup's objects initialized with tc_groups.

        Parameters
        ----------
            tc_groups : list or tuple (default: import_groups())
                tuples with 2 items each for items

        Raises
        ----------
            IndexError: group tup not contain 2 items.
            ValueError: group's name or testcase not used once.
        """
        check_type(tc_groups, (list, tuple), "Object groups")
        super().__init__()
        for group_item in tc_groups:
            check_type(group_item, (tuple, ), "Item of groups")
            if len(group_item) != 2:
                raise_error(IndexError, "".join([  # not contain 2 items
                    "Group tuple must contain 2 items (group's name, ",
                    f"testcases list or tuple), not {len(group_item)}"]))
            self.append(TestCasesGroup(group_item))
        error_value = None
        group_names = [g.name for g in self]
        for group_name in group_names:
            if group_names.count(group_name) != 1:  # name not used once
                error_value = f"Group's name must used once, '{group_name}'."
        if error_value is None:
            all_testcases = []
            for group in self:
                all_testcases.extend(group.testcases)
            for testcase in all_testcases:
                if all_testcases.count(testcase) != 1:
                    error_value = "".join([  # testcase not used once
                        "Testcase must used only in one group, ",
                        f"'{testcase.__name__}'"])
        if error_value is not None:
            raise_error(ValueError, error_value)
