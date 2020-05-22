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


def main():
    """
    Parse and run groups's TestCases.
    """
    sys.tracebacklimit = 0
    tc_groups = TestCasesGroups()
    print(tc_groups)


if __name__ == "__main__":
    main()
