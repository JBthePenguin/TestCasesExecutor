"""
Module testcases_executor.tc_reporter.contexts

Contain necessary context classes used in template to construct html report.

Classes:
    ContextInfos
    ContextHeader
    ContextGroup
    ContextMethod

Imports:
    from testcases_executor.tc_utils: format_duration
"""
from testcases_executor.tc_utils import format_duration


class ContextInfos(dict):
    """
    A subclass of dict.

    Represent infos context used to init ContextHeader and ContextGroup.

    Keys - Values
    ----------
    status: str
        'PASSED' or 'FAILED'.
    status_color: str
        'success' or 'danger' (bootstrap4 colors names).
    n_tests: dict
        number of tests by type (fail, error...).
    duration: str
        duration formated in second or millisecond.
    """

    def __init__(self, status, n_tests, duration):
        """
        Init dict, add color depending of status, update with parameters.

        Parameters
        ----------
            status: str
                'PASSED' or 'FAILED'.
            n_tests: dict
                number of tests by type (fail, error...).
            duration: float
                duration of all tests in second.
        """
        super().__init__()
        if status == 'PASSED':
            self['status_color'] = 'success'
        else:
            self['status_color'] = 'danger'
        self.update({
            'status': status, 'n_tests': n_tests,
            'duration': format_duration(duration)})


class ContextHeader(ContextInfos):
    """
    A subclass of ContextInfos.

    Represent context with datas needed in template header.html .

    Keys - Values
    ----------
    start_time: str
        start time formated (2020-03-30 12:00:00).
    """

    def __init__(self, status, start_time, n_tests, duration):
        """
        Init ContextInfos and add value for start_time key.

        Parameters
        ----------
            status: str
                'PASSED' or 'FAILED'.
            start_time: datetime
                when tests started.
            n_tests: dict
                number of tests by type (fail, error...).
            duration: float
                duration of all tests in second.
        """
        super().__init__(status, n_tests, duration)
        self['start_time'] = start_time.strftime("%Y-%m-%d %H:%M:%S")


class ContextGroup(ContextInfos):
    """
    A subclass of ContextInfos.

    Represent context with datas needed in template groups.html .

    Keys - Values
    ----------
    name: str
        group's name.
    testcases: list
        ContextTestCase objects.
    """

    def __init__(self, g_name, status, n_tests, duration, testcases):
        """
        Init ContextInfos and add value for start_time key.

        Parameters
        ----------
            g_name: str
                group's name.
            status: str
                'PASSED' or 'FAILED'.
            n_tests: dict
                number of tests by type (fail, error...).
            duration: float
                duration of all group's tests in second.
            testcases: list
                ContextTestCase objects.
        """
        super().__init__(status, n_tests, duration)
        self.update({'name': g_name, 'testcases': testcases})


class ContextTestCase(dict):
    """
    A subclass of dict.

    Represent a testcase context with datas needed in template testcase.html .

    Keys - Values
    ----------
    name: str
        testcase's name.
    module: str
        module's name.
    t_methods: list
        ContextMethod objects.
    duration: str
        duration formated in second or millisecond.
    """

    def __init__(self, tc_name, tc_module, duration, t_methods):
        """
        Init dict and update with parameters.

        Parameters
        ----------
            tc_name: str
                testcase's name.
            tc_module: str
                module's name.
            duration: float
                duration of all testcase's tests in second.
            t_methods: list
                ContextMethod objects.
        """
        super().__init__()
        self.update({
            'name': tc_name, 'module': tc_module, 't_methods': t_methods,
            'duration': format_duration(duration)})


class ContextMethod(dict):
    """
    A subclass of dict.

    Represent a testcase context with datas needed in template testcase.html .

    Keys - Values
    ----------
    status_name: str
        SUCCESS, FAIL, ERROR, SKIP, Unexpected Success or Expected Fail
    status_icon: str
        name of Fontawesome icon.
    status_color: str
        success, warning, danger, or info (bootstrap4 colors names).
    name: str
        test method's name.
    doc: str
        test method's docstring.
    t_methods: list
        ContextMethod objects.
    duration: str
        duration formated in second or millisecond.
    """

    def __init__(self, t_method, duration, t_errors):
        """
        Init dict, add status values by checking errors lists and update.

        Parameters
        ----------
            t_method: TestCase's method
                original test method used to construct self.
            duration: float
                duration of all tests in second.
            t_errors: dict
                key t_method -> error, errors failures skipped... -> list tests
        """
        super().__init__()
        if t_method in t_errors['failures']:
            self.update({
                'status_name': "FAIL", 'status_icon': "thumbs-o-down",
                'status_color': "warning", 'error': t_errors[t_method]})
        elif t_method in t_errors['errors']:
            self.update({
                'status_name': "ERROR", 'status_icon': "times-circle",
                'status_color': "danger", 'error': t_errors[t_method]})
        elif t_method in t_errors['skipped']:
            self.update({
                'status_name': "SKIP", 'status_icon': "cut",
                'status_color': "info", 'error': t_errors[t_method]})
        elif t_method in t_errors['exp_fails']:
            self.update({
                'status_name': "Expected Fail", 'status_icon': "stop-circle-o",
                'status_color': "danger", 'error': t_errors[t_method]})
        else:
            self.update({'status_color': 'success', 'error': None})
            if t_method in t_errors['unex_suc']:
                self.update({
                    'status_name': "Unexpected Success",
                    'status_icon': 'hand-stop-o'})
            else:
                self.update({
                    'status_name': "SUCCESS", 'status_icon': 'thumbs-o-up'})
        self.update({
            'name': t_method._testMethodName, 'doc': t_method._testMethodDoc,
            'duration': format_duration(duration)})
