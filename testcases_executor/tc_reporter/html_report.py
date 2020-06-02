"""
Module testcases_executor.tc_reporter.html_report

Contain necessary class to make html report of results for groups of TestCases.

Class:
    ContextHeader
    TestCasesHtmlReport

Imports:
    os
    from jinja2: Environment, PackageLoader
    from testcases_executor.tc_utils: format_duration, BOLD, MUTED, S_RESET
"""
import os
from jinja2 import Environment, PackageLoader
from testcases_executor.tc_utils import format_duration, BOLD, MUTED, S_RESET


class ContextHeader(dict):
    """
    A subclass of dict.

    Represent context with datas needed in template header.
    """

    def __init__(self, status, start_time, duration, n_tests):
        """
        Init dict, get color depending of status and add necessary keys values.

        Parameters
        ----------
            status: str
                'PASSED' or 'FAILED'.
            start_time: datetime
                when tests started.
            duration: float
                duration of all tests in second.
            n_tests: dict
                number of tests by type (fail, error...).

        Keys - Values
        ----------
            status: str
                same as parameter.
            status_color: str
                'success' or 'danger' ( bootstrap4 colors).
            start_time: str
                start time formated.
            duration: str
                duration formated.
            n_tests: dict
                same as parameter.
        """
        super().__init__()
        if status == 'PASSED':
            self['status_color'] = 'success'
        else:
            self['status_color'] = 'danger'
        self.update({
            'status': status, 'duration': format_duration(duration),
            'start_time': start_time.strftime("%Y-%m-%d %H:%M:%S"),
            'n_tests': n_tests})


class ContextGroup(dict):
    """
    A subclass of dict.

    Represent a group context with datas needed in template groups.
    """

    def __init__(self, status, g_name, n_tests, duration):
        """
        Init dict, get color depending of status and add necessary keys values.

        Parameters
        ----------
            result

        Items
        ----------
            (ContextGroup, )
        """
        super().__init__()
        if status == 'PASSED':
            self['status_color'] = 'success'
        else:
            self['status_color'] = 'danger'
        self.update({
            'name': g_name, 'status': status, 'n_tests': n_tests,
            'duration': format_duration(duration)})


class ContextMethod(dict):

    def __init__(self, t_method, duration, result):
        super().__init__()
        if t_method in [fail[0] for fail in result.failures]:
            self.update({
                'status_name': "FAIL", 'status_icon': "thumbs-o-down",
                'status_color': "warning"})
            for test, err in result.failures:
                if test == t_method:
                    self['error'] = err
                    break
        elif t_method in [err[0] for err in result.errors]:
            self.update({
                'status_name': "ERROR", 'status_icon': "times-circle",
                'status_color': "danger"})
            for test, err in result.errors:
                if test == t_method:
                    self['error'] = err
                    break
        elif t_method in [skp[0] for skp in result.skipped]:
            self.update({
                'status_name': "SKIP", 'status_icon': "cut",
                'status_color': "info"})
            for test, err in result.skipped:
                if test == t_method:
                    self['error'] = err
                    break
        elif t_method in [e_fail[0] for e_fail in result.expectedFailures]:
            self.update({
                'status_name': "Expected Fail", 'status_icon': "stop-circle-o",
                'status_color': "danger"})
            for test, err in result.expectedFailures:
                if test == t_method:
                    self['error'] = err
                    break
        else:
            self.update({'status_color': 'success', 'error': None})
            if t_method in result.unexpectedSuccesses:
                self.update({
                    'status_name': "Unexpected Success",
                    'status_icon': 'hand-stop-o'})
            else:
                self.update({
                    'status_name': "SUCCESS", 'status_icon': 'thumbs-o-up'})
        self.update({
            'name': t_method._testMethodName, 'doc': t_method._testMethodDoc,
            'duration': format_duration(duration)})


class ContextMethods(list):
    """
    A subclass of list.

    Represent methods context with datas needed in template testcase.
    """

    def __init__(self, t_methods, tm_durations, result):
        super().__init__()
        for t_method in t_methods:
            self.append(
                ContextMethod(t_method, tm_durations[t_method], result))


class ContextTestCase(dict):
    """
    A subclass of dict.

    Represent a testcase context with datas needed in template testcase.
    """

    def __init__(self, tc_name, tc_module, duration):
        super().__init__()
        self.update({
            'name': tc_name, 'module': tc_module,
            'duration': format_duration(duration)})


class ContextTestCases(list):
    """
    A subclass of list.

    Represent testcases context with datas needed in template groups.
    """

    def __init__(self, tc_tup, tc_durations, tm_durations, result):
        """
        Init dict, get color depending of status and add necessary keys values.

        Parameters
        ----------
            result

        Items
        ----------
            (ContextGroup, )
        """
        super().__init__()
        for testcase, t_methods in tc_tup:
            tc_context = ContextTestCase(
                testcase.__name__, testcase.__module__, tc_durations[testcase])
            test_methods = ContextMethods(t_methods, tm_durations, result)
            self.append((tc_context, test_methods))


class ContextGroups(list):
    """
    A subclass of list.

    Represent context with datas needed in template groups.
    """

    def __init__(self, result):
        """
        Init list, get color depending of status and add necessary keys values.

        Parameters
        ----------
            result

        Items
        ----------
            (ContextGroup, ContextTestCases)
        """
        super().__init__()
        for group, tc_tup in result.test_methods:
            group_context = ContextGroup(
                result.status['groups'][group], group.name,
                result.n_tests['groups'][group],
                result.durations['groups'][group])
            testcases_context = ContextTestCases(
                tc_tup, result.durations['testcases'],
                result.durations['tests'], result)
            self.append((group_context, testcases_context))


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
        # report_file
        report_path = os.path.join(dir_reports, 'report.html')
        with open(report_path, 'w') as report_file:
            report_file.write(template.render(
                title=f"{os.path.basename(os.getcwd())} Tests Results",
                header=ContextHeader(
                    result.status['total'], result.start_time,
                    result.durations['total'], result.n_tests['total']),
                groups=ContextGroups(result)))
        result.stream.writeln(
            f"---> {BOLD}{MUTED}{os.path.relpath(report_path)}{S_RESET}\n")
