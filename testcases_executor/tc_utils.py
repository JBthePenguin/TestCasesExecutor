"""
Module testcases_executor.tc_utils

Contain utils functions

Functions:
    raise_error(error_type, error_msg)
    check_type(obj, desired_classes, obj_msg)

Imports:
    from coloroma: Style, Fore
"""
from colorama import Style, Fore


def raise_error(error_type, error_msg):
    """
    Raise a speific type error with a formated message with info at the end.

        Parameters:
            error_type (Error): A specific type Error.
            error_msg (string): message to display.

        Raises:
            Exception (error_type): with formatted message
    """
    info_msg = "\n".join([
        f"{Style.DIM}\nFor more infos about usage, see README.md:",
        f"https://github.com/JBthePenguin/TestCasesExecutor{Style.RESET_ALL}"])
    print(f"{Style.BRIGHT}{Fore.RED}")
    raise error_type(f"{Fore.RESET}{error_msg}{Style.NORMAL}{info_msg}")


def check_type(obj, desired_classes, obj_msg):
    """
    Check if an object's class is one of the desired.

        Parameters:
            obj (?): instance checked.
            desired_classes (tuple): classes checked.
            obj_msg (str): obj name used in error message.

        Raises:
            TypeError: obj not one of desired classes.
    """
    if not isinstance(obj, desired_classes):
        end_msg = " or ".join([f"'{t.__name__}'" for t in desired_classes])
        raise_error(TypeError, "".join([
            f"{obj_msg} must be {end_msg}, ",
            f"not '{obj.__class__.__name__}': {obj}"]))
