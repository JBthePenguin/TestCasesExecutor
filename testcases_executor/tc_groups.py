"""
Module testcases_executor.tc_groups

Contain necessary classes and functions to make groups of TestCases.

Classes:
    GroupTestLoader
    TestCasesGroup
    TestCasesGroups

Functions:
    import_groups()

Imports:
    sys
    from fnmatch: fnmatchcase
    from unittest: TestCase, TestLoader, TestSuite
    from testcases_executor.tc_utils: raise_error, check_type
"""
import sys
from fnmatch import fnmatchcase
from unittest import TestCase, TestLoader, TestSuite
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


class GroupTestLoader(TestLoader):
    """
    A subclass of unittest.TestLoader .

    Used to load test methods of testcase.

    Methods
    ----------
    getTestCaseNames():
        Override original one to ordered test methods by declaration.
    """

    def getTestCaseNames(self, testCaseClass):
        """
        Override original one to ordered test methods by declaration.

        Parameters
        ----------
            testCaseClass: subclass of unittest.TestCase object
                testcase to load tests.

        Returns
        ----------
            list maked with vars(testCaseClass).keys(), not dir(testCaseClass).
        """
        def shouldIncludeMethod(attrname):
            if not attrname.startswith(self.testMethodPrefix):
                return False
            testFunc = getattr(testCaseClass, attrname)
            if not callable(testFunc):
                return False
            fullName = f'%s.%s.%s' % (
                testCaseClass.__module__, testCaseClass.__qualname__, attrname
            )
            return self.testNamePatterns is None or \
                any(fnmatchcase(
                    fullName, pattern) for pattern in self.testNamePatterns)
        return list(filter(
            shouldIncludeMethod, vars(testCaseClass).keys()))


class TestCasesGroup():
    """
    A class to represent a group of TestCases.

    A group with a name and a list of TestCases.

    Attributes
    ----------
    name : str
        string not empty and capitalize.
    arg_name : str
        string name with '_' to replace all non alphanuneric charact.
    testases : list
        instances subclass of unittest.TestCase .
    suites : list
        tuples (testcase, unittest.TestSuite object).

    Methods
    ----------
    update_suites(testcase, test_methods):
        Extend suites with a tuple maked with parameters.
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
        g_name, self.testcases = group_tup
        self.name = g_name.capitalize()
        self.arg_name = "".join(
            [c if c.isalnum() else "_" for c in g_name.lower()])
        if isinstance(self.testcases, tuple):  # convert to list
            self.testcases = list(self.testcases)
        self.suites = []

    def update_suites(self, testcase, test_methods=None):
        """
        Append a tuple maked with parameters to suites attribute.

        Parameters
        ----------
            testcase : Unittest.Testase subclass object
                first item of tuple.
            test_methods: list (default: None)
                names of test methods (str)
        """
        if test_methods is None:
            suite = GroupTestLoader().loadTestsFromTestCase(testcase)
        else:
            suite = TestSuite([testcase(t_name) for t_name in test_methods])
        self.suites.append((testcase, suite))


class TestCasesGroups(list):
    """
    A class to represent a list of TestCasesGroup object.

    A list with TestCasesGroup's objects for items.

    Self
    ----------
    [TestCasesGroup1, TestCasesGroup2, ...]

    Methods
    ----------
    construct_suites(args):
        Check args, update group's testsuites and remove group without suite.
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
        sys.tracebacklimit = 0
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
                break
        if error_value is None:
            all_testcases = []
            for group in self:
                all_testcases.extend(group.testcases)
            for testcase in all_testcases:
                if all_testcases.count(testcase) != 1:
                    error_value = "".join([  # testcase not used once
                        "Testcase must used only in one group, ",
                        f"'{testcase.__name__}'"])
                    break
        if error_value is not None:
            raise_error(ValueError, error_value)
        sys.tracebacklimit = 1000

    def construct_suites(self, args):
        """
        Check args, update group's testsuites and remove group without suite.

        Parameters
        ----------
            args :
                result of TestCasesParser.parse_args() .
        """
        if (len(sys.argv) == 1) or (
            (len(sys.argv) == 2) and (args.open or args.timestamp)) or (
                (len(sys.argv) == 3) and args.open and args.timestamp):
            for tc_group in self:  # no arg or open -> all tests
                for testcase in tc_group.testcases:
                    tc_group.update_suites(testcase)
        else:
            args_dict = vars(args)
            for tc_group in self:
                if args_dict[tc_group.arg_name]:  # group name arg, group tests
                    for testcase in tc_group.testcases:
                        tc_group.update_suites(testcase)
                else:
                    for testcase in tc_group.testcases:
                        t_names = args_dict[testcase.__name__]
                        if isinstance(t_names, list):  # test case's name arg
                            if not t_names:  # no param -> test case's tests
                                tc_group.update_suites(testcase)
                            else:  # method name(s) param -> methods's tests
                                tc_group.update_suites(testcase, t_names)
            groups_to_remove = [g for g in self if not g.suites]
            for group in groups_to_remove:  # remove group without suite
                self.remove(group)
