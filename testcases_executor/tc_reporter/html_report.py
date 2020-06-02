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


def get_icon_color(t_method, result):
    if t_method in [fail[0] for fail in result.failures]:
        status_icon, status_color = "thumbs-o-down", "warning"
        status_name = "FAIL"
    elif t_method in [err[0] for err in result.errors]:
        status_icon, status_color = "times-circle", "danger"
        status_name = "ERROR"
    elif t_method in [skp[0] for skp in result.skipped]:
        status_icon, status_color = "cut", "info"
        status_name = "SKIP"
    elif t_method in [e_fail[0] for e_fail in result.expectedFailures]:
        status_icon, status_color = "stop-circle-o", "danger"
        status_name = "Expected Fail"
    else:
        status_color = 'success'
        if t_method in result.unexpectedSuccesses:
            status_icon = 'hand-stop-o'
            status_name = "Unexpected Success"
        else:
            status_icon = 'thumbs-o-up'
            status_name = "SUCCESS"
    return status_name, status_icon, status_color


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
                test_methods = []
                for t_method in t_methods:
                    status_name, status_icon, status_color = (
                        get_icon_color(t_method, result))
                    t_method_dict = {
                        'name': t_method._testMethodName,
                        'duration': format_duration(
                            result.durations['tests'][t_method]),
                        'status_name': status_name,
                        'status_icon': status_icon,
                        'status_color': status_color,
                        'doc': t_method._testMethodDoc}
                    test_methods.append(t_method_dict)
                tc_methods.append((tc_dict, test_methods))
            groups.append((group_dict, tc_methods))
        return groups
