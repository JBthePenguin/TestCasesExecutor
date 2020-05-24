"""
Module testcases_executor.__main__

Contain main function that called when testcases_executor executed as module.

Functions:
    main()

Imports:
    from testcases_executor.tc_groups: TestCasesGroups
    from testcases_executor.tc_parser: TestCasesParser
"""
from testcases_executor.tc_groups import TestCasesGroups
from testcases_executor.tc_parser import TestCasesParser


def main():
    """
    Parse and run groups's TestCases.
    """
    tc_groups = TestCasesGroups()
    parser = TestCasesParser(tc_groups)
    args = parser.parse_args()
    tc_groups.construct_suites(args)
    # for group in tc_groups:
    #     print(group.name, len(group.suites))


if __name__ == "__main__":
    main()
