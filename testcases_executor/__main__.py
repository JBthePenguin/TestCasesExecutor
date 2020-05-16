import os
ROOT_DIR = os.path.basename(os.path.abspath(os.curdir))


def get_groups():
    """Import and return testscases.groups if it's a list.
    If there is an error, return the corresponding message."""
    try:
        from testcases import groups
    except ModuleNotFoundError:  # testscases.py not founded
        return f"\nFile testcases.py not founded in root -> {ROOT_DIR}."
    except ImportError:  # groups not founded
        return "\nList groups not founded in testscases.py ."
    if not isinstance(groups, list):  # groups not a list
        return "\nInstance groups must to be a list."
    return groups


def check_components(groups_list):
    """Check if groups's components are instances tuple with,
    a string (group's name) and a list of TestCase's subclasses.
    If all is Ok, return groups_list, else the corresponding message."""
    for tc_tups in groups_list:
        if not isinstance(tc_tups, tuple):  # component not a tuple
            return "\nComponent of groups must to be a tuple."
        group_name, tc_list = tc_tups
        if not isinstance(group_name, str):  # name not a string
            return "\nGroup's name must to be a string."
        if not isinstance(tc_list, list):  # testcases not a list
            return "\nGroup's testcases must to be a list."
        from unittest import TestCase
        for tc in tc_list:
            if not issubclass(tc, TestCase):  # tc not TestCase
                return "".join([
                    "\nComponent of group's testcases list ",
                    "must to be unittest.TestCase subclass."])
    return groups_list


def main():
    """Get groups, if error print corresponding message,
    else verify groups is instance list of tuples,
    with group name and testases list, if error print corresponding message,
    else execute groups of testcases."""
    tc_groups = get_groups()
    if isinstance(tc_groups, list):
        tc_groups = check_components(tc_groups)
    if isinstance(tc_groups, str):  # error
        print("\n".join([
            tc_groups, "\nFor more infos about usage, see README.md:",
            "https://github.com/JBthePenguin/TestCasesExecutor\n"]))
    else:  # groups founded and checked
        print(tc_groups)


main()
