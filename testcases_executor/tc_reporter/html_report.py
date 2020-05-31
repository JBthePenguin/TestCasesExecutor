"""
Module testcases_executor.tc_reporter.html_report

Contain necessary class to make html report of results for groups of TestCases.

Class:
    TestCasesHtmlReport

Imports:
    os
    from jinja2: Environment, PackageLoader
    from testcases_executor.tc_utils: format_duration, BOLD, MUTED, S_RESET
"""
import os
from jinja2 import Environment, PackageLoader
from testcases_executor.tc_utils import format_duration, BOLD, MUTED, S_RESET


class TestCasesHtmlReport():
    """
    A class to generate a html report file.

    Use result datas to construct file with a base template.

    Methods
    ----------
    get_header():
        Called to get context with necessary datas for header.
    get_groups():
        Called to get context with necessary datas for all groups.
    """

    def __init__(self, result):
        """
        Load template base, get context and construct report file.

        Parameters
        ----------
            result: tc_result.TestCasesResult
                result of tests.
        """
        result.stream.writeln("Generating html report ...\n")
        # load template
        env = Environment(
            loader=PackageLoader('testcases_executor.tc_reporter'))
        template = env.get_template('report_template.html')
        # dir destination
        dir_reports = './html_reports'
        if not os.path.exists(dir_reports):
            os.makedirs(dir_reports)
        # report_file
        report_path = os.path.join(dir_reports, 'report.html')
        with open(report_path, 'w') as report_file:
            report_file.write(template.render(
                title=f"{os.path.basename(os.getcwd())} Tests Results",
                header=self.get_header(result),
                groups=self.get_groups(result)))
        result.stream.writeln(
            f"---> {BOLD}{MUTED}{os.path.relpath(report_path)}{S_RESET}\n")

    def get_header(self, result):
        """
        Called to get context with necessary datas for header.

        Parameters
        ----------
            result: tc_result.TestCasesResult
                result of tests.

        Return
        ----------
            context: dict
                time, duration, status, number of tests, successes, ...
        """
        # number of items for each list
        n_errors, n_fails = len(result.errors), len(result.failures)
        n_skips = len(result.skipped)
        n_exp_fails = len(result.expectedFailures)
        n_unexp_succ = len(result.unexpectedSuccesses)
        n_success = result.testsRun - sum([
            n_errors, n_fails, n_skips, n_exp_fails, n_unexp_succ])
        # status
        if result.wasSuccessful():
            status, status_color = 'PASSED', 'success'
        else:
            status, status_color = 'FAILED', 'danger'
        return {  # header context
            'start_time': result.start_time.strftime("%Y-%m-%d %H:%M:%S"),
            'duration': format_duration(result.durations['total']),
            'total': result.testsRun, 'status': status,
            'status_color': status_color, 'successes': n_success,
            'failures': n_fails, 'errors': n_errors, 'skips': n_skips,
            'expectedfails': n_exp_fails, 'unexpectedsuccesses': n_unexp_succ}

    def get_groups(self, result):
        """
        Called to get context with necessary datas for all groups.

        Parameters
        ----------
            result: tc_result.TestCasesResult
                result of tests.

        Return
        ----------
            context: dict
                time, duration, status, number of tests, successes, ...
        """
        groups = []
        for group, tc_methods in result.test_methods:
            group_dict = {
                'name': group.name, 'total': result.group_n_tests[group],
                'duration': format_duration(result.durations['groups'][group])}
            groups.append((group_dict, tc_methods))
        return groups
