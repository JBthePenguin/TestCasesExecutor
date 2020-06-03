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
from testcases_executor.tc_utils import BOLD, MUTED, S_RESET
from testcases_executor.tc_reporter.contexts import (
    ContextHeader, ContextGroup, ContextTestCase, ContextMethod)


class TestCasesHtmlReport():
    """
    A class to generate html report.

    Use result to get context datas and with a base template construct file.
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
        # errors_dict
        t_errors = {}
        for error_key, errors_list in [
                ('failures', result.failures), ('errors', result.errors),
                ('skipped', result.skipped),
                ('exp_fails', result.expectedFailures)]:
            tests = []
            for test, err in errors_list:
                tests.append(test)
                t_errors[test] = err
            t_errors[error_key] = tests
        t_errors['unex_suc'] = result.unexpectedSuccesses
        # groups
        groups = []
        for group, tc_tup in result.test_methods:
            g_testcases = []  # group's testcases
            for testcase, t_methods in tc_tup:
                tc_methods = []  # testcase's methods
                for t_method in t_methods:
                    t_context = ContextMethod(
                        t_method, result.durations['tests'][t_method],
                        t_errors)
                    tc_methods.append(t_context)
                tc_context = ContextTestCase(
                    testcase.__name__, testcase.__module__,
                    result.durations['testcases'][testcase], tc_methods)
                g_testcases.append(tc_context)
            group_context = ContextGroup(
                group.name, result.status['groups'][group],
                result.n_tests['groups'][group],
                result.durations['groups'][group], g_testcases)
            groups.append(group_context)
        # report_file
        report_path = os.path.join(dir_reports, 'report.html')
        with open(report_path, 'w') as report_file:
            report_file.write(template.render(  # template with contexts
                title=f"{os.path.basename(os.getcwd())} Tests Results",
                header=ContextHeader(
                    result.status['total'], result.start_time,
                    result.n_tests['total'], result.durations['total']),
                groups=groups))
        result.stream.writeln(
            f"---> {BOLD}{MUTED}{os.path.relpath(report_path)}{S_RESET}\n")
