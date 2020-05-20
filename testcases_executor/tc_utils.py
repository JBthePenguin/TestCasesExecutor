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
