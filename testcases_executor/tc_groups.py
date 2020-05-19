from colorama import Style, Fore

info_msg = "\n".join([
    f"{Style.DIM}",
    f"\nFor more infos about usage, see README.md:",
    "https://github.com/JBthePenguin/TestCasesExecutor",
    f"{Style.RESET_ALL}"])


def raise_error(error_type, error_msg):
    """Raise error with specific type and formated message."""
    print(f"{Style.BRIGHT}{Fore.RED}")
    raise error_type(f"{Fore.RESET}{error_msg}{Style.NORMAL}{info_msg}")


class TestCasesGroups(list):
    """A list of TestCasesGroups."""

    def __init__(self):
        super().__init__()
        self.import_groups()

    def import_groups(self):
        """Try to import groups objects, raise error or check is type."""
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
        self.check_type(groups, (list, tuple), "Object groups")  # check
        if isinstance(groups, tuple):  # change groups tuple to list
            groups = [g for g in groups]
        self += groups

    def check_type(self, obj, desired_types, obj_msg):
        """Check the type of an object, raise TypeError if not desired one."""
        if not isinstance(obj, desired_types):
            end_msg = " or ".join([t.__name__ for t in desired_types])
            raise_error(
                TypeError,
                f"{obj_msg} must be {end_msg}, not '{obj.__class__.__name__}'.")
