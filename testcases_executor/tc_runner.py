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
import time
import warnings
from datetime import datetime
from unittest import TextTestRunner
from testcases_executor.tc_utils import BOLD, MUTED, S_RESET
from testcases_executor.tc_result import TestCasesResult


class TestCasesRunner(TextTestRunner):
    """A HTMLTestRunner for TestCase."""

    # def __init__(self, test_cases, add_timestamp, open_in_browser):
    #     """Set property suites a dict for all tests docs.
    #     For each tests cases list
    #     Init ArgumentParser with formatter class and description.
    #     Set help message's title for help command. Make argument groups.
    #     Check args and run the corresponding tests.
    #     ***arg_groups -> [('group_name', [TestCase1, ...]), (..)].***"""
    #     self.suites = []
    #     self.tests_docs = {}
    #     for test_case in test_cases:
    #         self.update_suites_docs(test_case)
    #     template_args = {'tests_docs': self.tests_docs}
    #     super().__init__(
    #         output='html_test_reports', combine_reports=True,
    #         report_name='result', add_timestamp=add_timestamp,
    #         resultclass=HtmlTestCaseResult, template_args=template_args,
    #         template=os.path.join(
    #             os.path.dirname(__file__), 'template', 'base_temp.html'),
    #         report_title=f"{os.path.basename(os.getcwd())} Unittest Results",
    #         open_in_browser=open_in_browser)
    def __init__(self):
        super().__init__(
            stream=None, descriptions=True, verbosity=2,
            failfast=False, buffer=False, resultclass=TestCasesResult,
            warnings=None, tb_locals=False)

    def run_suites(self, result, suites):
        """Run all TestCases suites and display result in console."""
        self.start_time = datetime.now()
        for test_case, suite in suites:
            self.stream.writeln(f"\n{result.separator2}")
            self.stream.writeln(  # test case title
                f"\n {BOLD}--- {test_case.__name__} ---{S_RESET}")
            self.stream.writeln(
                f" {MUTED}{test_case.__module__}.py{S_RESET}\n")
            suite(result)  # run tests
            t_case_time = 0  # calculate  and display time for TestCase
            # for t_result in result.successes + result.failures + (
            #         result.errors + result.skipped):
            #     if t_result.test_name.split('.')[-1] == test_case.__name__:
            #         t_case_time += t_result.elapsed_time
            # self.stream.writeln(
            #     f"\n {Fore.MAGENTA}{result._format_duration(t_case_time)}")
            # self.stream.writeln(f"{Fore.RESET}\n{result.separator2}")

    def run(self, groups):
        """ Runs the given testcase or testsuite. """
        result = self._makeResult()
        result.failfast = self.failfast
        self.stream.writeln(f"\nRunning tests...\n\n{result.separator1}")
        # self.stream.writeln(result.separator1)
        start_time = datetime.now()
        for group in groups:
            self.stream.writeln(f"{result.separator1}")
            self.stream.writeln(f"\n{BOLD}{MUTED} {group.name}{S_RESET}")
            # self.stream.writeln(result.separator2)
            self.run_suites(result, group.suites)
            self.stream.writeln(f"\n{result.separator1}")
        # result.printErrors()
        # self.stream.writeln(result.separator2)
        # result.printTotal()
        # self.stream.writeln()
        # result.printInfos()
        # self.stream.writeln(f"Generating HTML reports...{Style.DIM}")
        # result.generate_reports(self)
        self.stream.writeln(S_RESET)
        # if self.open_in_browser:
        #     import webbrowser
        #     for report in result.report_files:
        #         webbrowser.open_new_tab('file://' + report)
        return result
