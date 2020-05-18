from testcases_executor.tc_parser import TestCasesParser

# groups = [('Group_name', [<subclass 'unittest.TestCase'>, ...]), ...]


def get_groups():
    """Import and return testscases.groups if it's a list.
    If there is an error, return the corresponding message."""
    try:
        from testcases import groups
    except ModuleNotFoundError:  # testscases.py not founded
        from os import curdir
        from os.path import basename, abspath
        root_dir = basename(abspath(curdir))
        return f"\nFile testcases.py not founded in root -> {root_dir}."
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
    for tc_tups in groups_list:
        if not isinstance(tc_tups[0], str):  # name not a string
            return "\nGroup's name must to be a string."
        if " " in tc_tups[0]:  # name with space
            return "\nGroup's name must not contain space."
    for tc_tups in groups_list:
        if not isinstance(tc_tups[1], list):  # testcases not a list
            return "\nGroup's testcases must to be a list."
    from unittest import TestCase
    for tc_tups in groups_list:
        for tc in tc_tups[1]:
            try:
                if not issubclass(tc, TestCase):  # tc not TestCase
                    return "".join([
                        "\nComponent of group's testcases list ",
                        "must to be unittest.TestCase subclass."])
            except TypeError:
                return "".join([
                    "\nComponent of group's testcases list ",
                    "must to be a class (unittest.TestCase subclass)."])
    return groups_list


def main():
    """Get groups, check his componentssponding message,
    if error print corresponding message,
    else execute groups of testcases."""
    tc_groups = get_groups()  # get
    if isinstance(tc_groups, list):
        tc_groups = check_components(tc_groups)  # check
    if isinstance(tc_groups, str):  # error
        print("\n".join([
            tc_groups, "\nFor more infos about usage, see README.md:",
            "https://github.com/JBthePenguin/TestCasesExecutor\n"]))
    else:  # groups imported and checked
        TestCasesParser(tc_groups)


if __name__ == "__main__":
    main()
