"""
Module testcases_executor.tc_runner

Contain the runner class.

Classes:
    TestCasesRunner

Functions:
    import_groups()

Imports:
    sys
    from fnmatch: fnmatchcase
    from unittest: TestCase, TestLoader, TestSuite
    from testcases_executor.tc_utils: raise_error, check_type
"""
from datetime import datetime
from unittest import TextTestRunner
from testcases_executor.tc_utils import (
    format_duration, BOLD, MUTED, S_RESET, MAGENTA)
from testcases_executor.tc_result import TestCasesResult


class TestCasesRunner(TextTestRunner):
    """A HTMLTestRunner for TestCase."""

    def __init__(self):
        super().__init__(resultclass=TestCasesResult)

    def run_g_suites(self, result, group):
        """Run all TestCases suites and display result in console."""
        tc_group = []
        for testcase, suite in group.suites:
            test_methods = [test_method for test_method in suite._tests]
            tc_group.append((testcase, test_methods))
            self.stream.writeln(result.separator2)
            self.stream.writeln(  # test case title
                f"\n{BOLD} --- {testcase.__name__} ---{S_RESET}")
            self.stream.writeln(
                f"{MUTED} {testcase.__module__}.py{S_RESET}\n")
            suite(result)  # run tests
            tc_duration = 0  # calculate  and display time for TestCase
            for test_method in test_methods:
                tc_duration += result.durations['tests'][test_method]
            result.durations['testcases'][testcase] = tc_duration
            self.stream.writeln(
                f"\n ... {MAGENTA}{format_duration(tc_duration)}{S_RESET}\n")
        result.test_methods.append((group, tc_group))

    def run(self, groups):
        """ Runs the given testcase or testsuite. """
        result = self._makeResult()
        result.failfast = self.failfast
        self.stream.writeln("\nRunning tests...\n")
        self.stream.writeln(result.separator1)
        result.start_time = datetime.now()
        for group in groups:
            self.stream.writeln(f"{result.separator1}\n")
            self.stream.writeln(f"{BOLD}{MUTED} {group.name}{S_RESET}\n")
            self.run_g_suites(result, group)
            n_tests = 0
            g_duration = 0
            for testcase, t_methods in result.test_methods[-1][1]:
                n_tests += len(t_methods)
                g_duration += result.durations['testcases'][testcase]
            result.durations['groups'][group] = g_duration
            self.stream.writeln(f"{result.separator2}\n {MUTED}")
            result.printTotal(n_tests, g_duration)
            self.stream.writeln(f"\n{result.separator1}")
        self.stream.writeln(result.separator1)
        total_duration = sum(result.durations['groups'].values())
        result.durations['total'] = total_duration
        result.printErrors()
        self.stream.writeln(
            f"{result.separator1}\n{result.separator1}\n{BOLD}")
        result.printTotal(result.testsRun, total_duration)
        result.printInfos()
        self.stream.writeln(S_RESET)
        self.stream.writeln(f"{result.separator1}\n{result.separator1}\n")
        # self.stream.writeln(f"Generating HTML reports...{Style.DIM}")
        # result.generate_reports(self)
        # if self.open_in_browser:
        #     import webbrowser
        #     for report in result.report_files:
        #         webbrowser.open_new_tab('file://' + report)
        return result
