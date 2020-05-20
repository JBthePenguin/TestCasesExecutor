from colorama import Style, Fore

info_msg = "\n".join([
    f"{Style.DIM}",
    f"\nFor more infos about usage, see README.md:",
    "https://github.com/JBthePenguin/TestCasesExecutor",
    f"{Style.RESET_ALL}"])


def raise_error(error_type, error_msg):
    """
    Raise an error.

    Raise a speific type error with a formated message with info at the end.

    Args:
        - error_type (Exception subclass): ImportError or KeyError or ...
        - error_msg (string): message to display.

    Raises:
        Exception (error_type): with formatted message

    """
    print(f"{Style.BRIGHT}{Fore.RED}")
    raise error_type(f"{Fore.RESET}{error_msg}{Style.NORMAL}{info_msg}")


def check_type(obj, desired_classes, obj_msg):
    """
    Check object's class.

    Check if an object's class is one of the desired.

    Args:
        - obj (?): instance checked.
        - desired_classes (tuple): classes checked.
        - obj_msg (str): obj name used in error message.

    Raises:
        TypeError: obj not one of desired classes.

    """
    if not isinstance(obj, desired_classes):
        end_msg = " or ".join([f"'{t.__name__}'" for t in desired_classes])
        raise_error(TypeError, "".join([
            f"{obj_msg} must be {end_msg}, ",
            f"not '{obj.__class__.__name__}': {obj}"]))
