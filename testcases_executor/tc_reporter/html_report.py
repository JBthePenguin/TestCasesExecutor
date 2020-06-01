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
        # status
        status = result.status['total']
        if status == 'PASSED':
            status_color = 'success'
        else:
            status_color = 'danger'
        return {  # header context
            'start_time': result.start_time.strftime("%Y-%m-%d %H:%M:%S"),
            'duration': format_duration(result.durations['total']),
            'status': status, 'status_color': status_color,
            'n_tests': result.n_tests['total']}

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
        for group, g_tests in result.test_methods:
            # status
            status = result.status['groups'][group]
            if status == 'PASSED':
                status_color = 'success'
            else:
                status_color = 'danger'
            group_dict = {
                'name': group.name, 'status': status,
                'status_color': status_color,
                'n_tests': result.n_tests['groups'][group],
                'duration': format_duration(result.durations['groups'][group])}
            tc_methods = []
            for testcase, t_methods in g_tests:
                tc_dict = {
                    'name': testcase.__name__, 'module': testcase.__module__,
                    'duration': format_duration(
                        result.durations['testcases'][testcase])}
                tc_methods.append((tc_dict, t_methods))
            groups.append((group_dict, tc_methods))
        return groups
