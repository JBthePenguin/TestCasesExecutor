from unittest import TestCase
from colorama import Style, Fore

info_msg = "\n".join([
    f"{Style.DIM}",
    f"\nFor more infos about usage, see README.md:",
    "https://github.com/JBthePenguin/TestCasesExecutor",
    f"{Style.RESET_ALL}"])


def raise_error(error_type, error_msg):
    """Raise error with specific type and formated message with info at end."""
    print(f"{Style.BRIGHT}{Fore.RED}")
    raise error_type(f"{Fore.RESET}{error_msg}{Style.NORMAL}{info_msg}")


def check_type(obj, desired_types, obj_msg):
    """Check the type of an object, raise TypeError if not desired one."""
    if not isinstance(obj, desired_types):
        end_msg = " or ".join([f"'{t.__name__}'" for t in desired_types])
        raise_error(TypeError, "".join([
            f"{obj_msg} must be {end_msg}, ",
            f"not '{obj.__class__.__name__}': {obj}"]))


def import_groups():
    """Try to import groups, raise error if testcases.py or groups not founded,
    else return it."""
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
    """A Group: -name -list of instances (subclass of unittest.TestCases)."""

    def __init__(self, group_tup):
        """Raise error if group tuple not contain 2 items,
        for group's name, check type(str), not empty and space,
        for testcases, check type(list, tuple) and for each of his items,
        raise error if not a class subclass unittest.TestCase, else set
        properties name and testcases (convert it to list if it's tuple)."""
        if len(group_tup) != 2:  # not contain 2 items
            raise_error(IndexError, "".join([
                "Group tuple must contain 2 items (group's name, ",
                f"testcases list or tuple), not {len(group_tup)}"]))
        check_type(group_tup[0], (str, ), "Group's name")
        if not group_tup[0]:  # name empty string
            raise_error(ValueError, "Group's name can't be an empty string.")
        if " " in group_tup[0]:  # name contain space
            raise_error(
                ValueError,
                f"Group's name must not contain space, '{group_tup[0]}'.")
        check_type(group_tup[1], (list, tuple), "Group's testcases")
        for tc_item in group_tup[1]:
            error_type = None
            try:  # tc not
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
    """A list of TestCasesGroup instances."""

    def __init__(self):
        """Import groups and check his type(list, tup), init self as list and,
        for each groups's item, check his type(tup),
        append to self a TestCasesGroup instance maked with it."""
        tc_groups = import_groups()
        check_type(tc_groups, (list, tuple), "Object groups")
        super().__init__()
        for group_item in tc_groups:
            check_type(group_item, (tuple, ), "Item of groups")
            self.append(TestCasesGroup(group_item))
