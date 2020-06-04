"""
Module testcases_executor.tc_reporter.html_report

Contain necessary class to make html report of results for groups of TestCases.

Class:
    TestCasesHtmlReport

Imports:
    from os: makedirs, path, getcwd
    from jinja2: Environment, PackageLoader
    from testcases_executor.tc_utils: BOLD, MUTED, S_RESET
    from testcases_executor.tc_reporter.contexts: ContextReport
"""
from os import makedirs, path, getcwd
from jinja2 import Environment, PackageLoader
from testcases_executor.tc_utils import BOLD, MUTED, S_RESET
from testcases_executor.tc_reporter.contexts import ContextReport


class TestCasesHtmlReport():
    """
    A class to generate html report.

    Use result to get context datas and with a base template construct file.
    """

    def __init__(self, result):
        """
        Init env, get template base and context to construct report file.

        Parameters
        ----------
            result: tc_result.TestCasesResult
                result of tests.
        """
        result.stream.writeln("Generating html report ...\n")
        env = Environment(  # load template base
            loader=PackageLoader('testcases_executor.tc_reporter'),
            autoescape=True)
        report_template = env.get_template('report_template.html')
        dir_reports = './html_reports'  # dir destination ...
        if not path.exists(dir_reports):
            makedirs(dir_reports)    # ... context, path to report file
        context_report = ContextReport(path.basename(getcwd()), result)
        report_path = path.join(dir_reports, 'report.html')
        with open(report_path, 'w') as report_file:
            report_file.write(report_template.render(  # html report file
                title=context_report.title, header=context_report.header,
                groups=context_report.groups))
        result.stream.writeln(
            f"---> {BOLD}{MUTED}{path.relpath(report_path)}{S_RESET}\n")
