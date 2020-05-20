from unittest import TestCase
from testcases_executor.tc_utils import raise_error, check_type


def import_groups():
    """
    Import groups from testcases.py .

    Try to import groups, raise errors or return it.

    Returns:
        - instance: groups.

    Raises:
        - ModuleNotFoundError: testscases.py not founded.
        - ImportError: groups not founded in testscases.py ."""
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
                f"File testcases.py not founded in root directory.")
        raise_error(
            ImportError, "Object groups not founded in testscases.py .")
    return groups


class TestCasesGroup():
    """
    A group of TestCases.

    A group with a name and a list of TestCases.

    Properties:
        - name: string without space and not empty.
        - testases: list of instances subclass of unittest.TestCase .
    """

    def __init__(self, group_tup):
        """
        Init a TestCasesGroup instance.

        Set properties name (str without space) and testcases (list).

        Args:
            - group_tup (tuple): ('group_name', (TestCase1, TestCase2, ...))
            or ('group_name', [TestCase1, TestCase2, ...]) .

        Raises:
            - ValueError: name empty string or contain space
            - TypeError: testcase not a subclass of unittest.TestCase .
        """
        group_name, group_tc = group_tup
        check_type(group_name, (str, ), "Group's name")
        error_type = None
        if not group_name:  # name empty string
            error_type = "be an non empty string"
        elif " " in group_name:  # name contain space
            error_type = "not contain space"
        if error_type is not None:
            raise_error(
                ValueError, f"Group's name must {error_type}: '{group_name}'.")
        check_type(group_tup[1], (list, tuple), "Group's testcases")
        for tc_item in group_tc:
            error_type = None
            try:  # item in testcases not
                if not issubclass(tc_item, TestCase):  # a TestCase subclass
                    error_type = "unittest.TestCase subclass"
            except TypeError:  # a class
                error_type = "class (unittest.TestCase subclass)"
            if error_type is not None:  # TypeError for tc
                raise_error(TypeError, "".join([
                    "Item of group's testcases list or tuple must be ",
                    f"a {error_type}: {tc_item}"]))
        self.name, self.testcases = group_tup
        if isinstance(self.testcases, tuple):  # convert to list
            self.testcases = list(self.testcases)


class TestCasesGroups(list):
    """
    A list of TestCasesGroup instances.

    [TestCasesGroup1, TestCasesGroup2, ...].
    """

    def __init__(self, tc_groups=import_groups()):
        """
        Init a TestCasesGroup instance.

        Init self as list and append TestCasesGroup instances maked with items.

        Args:
            - tc_groups (list or tuple): [gr_tup1, gr_tup2, ...]
            or (gr_tup1, gr_tup2, ...) .

        Raises:
            - IndexError: group tup not contain 2 items.
            - ValueError: group's name or testcase not used once.
        """
        check_type(tc_groups, (list, tuple), "Object groups")
        super().__init__()
        for group_item in tc_groups:  # append TestCasesGroup instances
            check_type(group_item, (tuple, ), "Item of groups")
            if len(group_item) != 2:  # not contain 2 items
                raise_error(IndexError, "".join([
                    "Group tuple must contain 2 items (group's name, ",
                    f"testcases list or tuple), not {len(group_item)}"]))
            self.append(TestCasesGroup(group_item))
        group_names = [g.name for g in self]
        for group_name in group_names:  # group's name used once
            if group_names.count(group_name) != 1:
                raise_error(
                    ValueError,
                    f"Group's name must used once, '{group_name}'.")
        all_testcases = []
        for group in self:
            all_testcases += group.testcases
        for testcase in all_testcases:  # testcase used once
            if all_testcases.count(testcase) != 1:
                raise_error(
                    ValueError,
                    f"A Testcase must used once, '{testcase.__name__}'.")
