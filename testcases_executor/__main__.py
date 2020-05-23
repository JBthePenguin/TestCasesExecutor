"""
Module testcases_executor.__main__

Contain main function that called when testcases_executor executed as module.

Functions:
    main()

Imports:
    sys
    from testcases_executor.tc_groups: TestCasesGroups
"""
import sys
from testcases_executor.tc_groups import TestCasesGroups
from testcases_executor.tc_parser import TestCasesParser


def main():
    """
    Parse and run groups's TestCases.
    """
    sys.tracebacklimit = 0
    tc_groups = TestCasesGroups()
    sys.tracebacklimit = 1000
    parser = TestCasesParser(tc_groups)
    parser.parse_args()


if __name__ == "__main__":
    main()
