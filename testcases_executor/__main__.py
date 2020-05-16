import os
ROOT_DIR = os.path.basename(os.path.abspath(os.curdir))

error_msg = None
try:  # Try to import testscases.groups
    from testcases import groups
except ModuleNotFoundError:  # testscases.py not founded
    error_msg = "\n".join([
        f"\nFile testscases.py not founded in root -> {ROOT_DIR}.",
        "-> Create it, import TestCases and make a groups list."])
except ImportError:  # groups not founded
    error_msg = "\n".join([
        "\nList groups not founded in testscases.py .",
        "groups = [('group name', [TestCase1, TestCase2,...]), (...), ...] ."])

if error_msg is not None:  # error
    print("\n".join([
        error_msg,
        "\nFor more infos about usage, see README.md:",
        "https://github.com/JBthePenguin/TestCasesExecutor\n"]))
else:  # groups founded
    print(groups)
