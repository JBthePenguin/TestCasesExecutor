import sys
# from testcases_executor.tc_parser import TestCasesParser
from testcases_executor.tc_groups import TestCasesGroups


def main():
    """Get groups, check his componentssponding message,
    if error print corresponding message,
    else execute groups of testcases."""
    sys.tracebacklimit = 0
    tc_groups = TestCasesGroups()
    # print(tc_groups)
    # tc_groups = get_groups()  # get
    # if isinstance(tc_groups, list):
    #     tc_groups = check_components_type(tc_groups)  # check
    # if isinstance(tc_groups, str):  # error
    #     print("\n".join([
    #         f"{Style.BRIGHT}{tc_groups}{Style.NORMAL}{Style.DIM}",
    #         info_msg]))
    # else:  # groups imported and checked
    #     try:
    #         parser = TestCasesParser(tc_groups)
    #     except ArgumentError as e:
    #         print(e)
    #     else:
    #         parser.parse_args()


if __name__ == "__main__":
    main()
