"""
Module testcases_executor.tc_runner

Contain necessary class to make a runner for groups of TestCases.

Class:
    TestCasesRunner

Imports:
    from datetime: datetime
    from unittest: TextTestRunner
    from testcases_executor.tc_utils: (
        format_duration, BOLD, MUTED, S_RESET, MAGENTA)
    from testcases_executor.tc_result: TestCasesResult
"""
from datetime import datetime
from unittest import TextTestRunner
from testcases_executor.tc_utils import (
    format_duration, BOLD, MUTED, S_RESET, MAGENTA)
from testcases_executor.tc_result import TestCasesResult


class TestCasesRunner(TextTestRunner):
    """
    A subclass of unittest.TextTestRunner .

    Use to run groups's tests suites and display result in shell.

    Methods
    ----------
    run_group_suites():
        Run suites for a group, update result durations and test_methods.
    run():
        Run all groups's suites, update result and return it.
    """

    def __init__(self):
        """
        Init unittest.TextTestRunner with TestCasesResult for result class.
        """
        super().__init__(resultclass=TestCasesResult)

    def run_group_suites(self, result, group):
        """
        Run suites for a group, update result durations and test_methods.

        Parameters
        ----------
            result: TestCasesResult
                needed to update his properties durations and test_methods.
            group : TestCasesGroup
                used suites property to get and run testcases with tests suite.
        """
        tc_group = []
        for testcase, suite in group.suites:
            test_methods = [test_method for test_method in suite._tests]
            tc_group.append((testcase, test_methods))
            self.stream.writeln(result.separator2)
            self.stream.writeln(  # test case title
                f"\n{BOLD} --- {testcase.__name__} ---{S_RESET}")
            self.stream.writeln(
                f"{MUTED} {testcase.__module__}.py{S_RESET}\n")
            suite(result)  # run tests suite
            tc_duration = 0  # calcul, save testcase duration
            for test_method in test_methods:
                tc_duration += result.durations['tests'][test_method]
            result.durations['testcases'][testcase] = tc_duration
            self.stream.writeln(  # display it
                f"\n ... {MAGENTA}{format_duration(tc_duration)}{S_RESET}\n")
        result.test_methods.append((group, tc_group))

    def run(self, groups):
        """
        Run all groups's suites, update result and return it.

        Parameters
            groups : TestCasesGroups
                used items to get and run group's tests suites.
        """
        result = self._makeResult()  # init result
        result.failfast = self.failfast
        self.stream.writeln("\nRunning tests...\n")
        self.stream.writeln(result.separator1)
        result.start_time = datetime.now()  # start tests
        for group in groups:
            self.stream.writeln(f"{result.separator1}\n")
            self.stream.writeln(f"{BOLD}{MUTED} {group.name}{S_RESET}\n")
            self.run_group_suites(result, group)  # run group's suites
            n_tests = 0   # calcul number of group's tests
            g_duration = 0   # calcul, save group duration
            for testcase, t_methods in result.test_methods[-1][1]:
                n_tests += len(t_methods)
                g_duration += result.durations['testcases'][testcase]
            result.durations['groups'][group] = g_duration
            self.stream.writeln(f"{result.separator2}\n {MUTED}")
            result.printTotal(n_tests, g_duration)  # display them
            self.stream.writeln(f"\n{result.separator1}")
        result.printErrors()  # display errors
        self.stream.writeln(
            f"{result.separator1}\n{result.separator1}\n{BOLD}")
        self.stream.writeln(result.separator1)  # calcul, save total duration
        total_duration = sum(result.durations['groups'].values())
        result.durations['total'] = total_duration
        result.printTotal(result.testsRun, total_duration)  # display it
        result.printInfos()  # display final infos
        self.stream.writeln(S_RESET)
        self.stream.writeln(f"{result.separator1}\n{result.separator1}\n")
        return result