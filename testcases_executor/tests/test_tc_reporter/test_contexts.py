"""
Module testcases_executor.tests.test_tc_reporter.test_contexts .

Contain TestCase for testcases_executor.tc_reporter.contexts .

unittest.TestCase sublasses:
    TestContextInfos
    TestContextHeader
    TestContextGroup
    TestContextTestCase
    TestContextMethod
    TestContextReport

Imports:
    from unittest: TestCase
"""
from unittest import TestCase
from unittest.mock import patch, Mock
from testcases_executor.tc_reporter.contexts import (
    ContextInfos, ContextHeader, ContextGroup, ContextTestCase, ContextMethod)


class TestContextInfos(TestCase):
    """
    A subclass of unittest.TestCase .

    Tests for tc_reporter.contexts.ContextInfos .

    Methods
    ----------
    test_init_context_infos():
        Assert ContextInfos (dict) is initialized with good keys / values.
    """

    @patch("testcases_executor.tc_reporter.contexts.format_duration")
    def test_init_context_infos(self, mock_format_duration):
        """
        Assert ContextInfos (dict) is initialized with good keys / values.

        Parameters:
        ----------
        mock_format_duration : Mock
            Mock of tc_utils.format_duration .

        Assertions:
        ----------
        assert_called_once_with:
            Assert format_duration called once with 'duration'.
        assertDictEqual:
            Assert if obj is the desired dict.
        assertEqual:
            If FAILED, assert values for keys status and status_color.
        """
        mock_format_duration.return_value = 'duration formated'
        obj = ContextInfos('PASSED', 'n_tests', 'duration')
        mock_format_duration.assert_called_once_with('duration')
        self.assertDictEqual(obj, {
            'status': 'PASSED', 'n_tests': 'n_tests',
            'duration': 'duration formated', 'status_color': 'success'})
        obj = ContextInfos('FAILED', 'n_tests', 'duration')
        self.assertEqual(obj['status'], 'FAILED')
        self.assertEqual(obj['status_color'], 'danger')


class TestContextHeader(TestCase):
    """
    A subclass of unittest.TestCase .

    Tests for tc_reporter.contexts.ContextHeader .

    Methods
    ----------
    test_init_context_header():
        Assert ContextHeader (dict) is initialized with good keys / values.
    """

    @patch("testcases_executor.tc_reporter.contexts.ContextInfos.__init__")
    def test_init_context_header(self, mock_context_infos):
        """
        Assert ContextHeader (dict) is initialized with good keys / values.

        Parameters:
        ----------
        mock_context_infos : Mock
            Mock of tc_reporter.contexts.ContextInfos.__init__ .

        Assertions:
        ----------
        assert_called_once_with:
            Assert ContextInfos, strftime called once with parameters.
        assertDictEqual:
            Assert if obj is the desired dict.
        """
        mock_context_infos.return_value = {}
        mock_start_time = Mock()
        mock_start_time.strftime.return_value = 'datetime formatted'
        obj = ContextHeader('status', mock_start_time, 'n_tests', 'duration')
        mock_context_infos.assert_called_once_with(
            'status', 'n_tests', 'duration')
        mock_start_time.strftime.assert_called_once_with("%Y-%m-%d %H:%M:%S")
        self.assertDictEqual(obj, {'start_time': 'datetime formatted'})


class TestContextGroup(TestCase):
    """
    A subclass of unittest.TestCase .

    Tests for tc_reporter.contexts.ContextGroup .

    Methods
    ----------
    test_init_context_group():
        Assert ContextGroup (dict) is initialized with good keys / values.
    """

    @patch("testcases_executor.tc_reporter.contexts.ContextInfos.__init__")
    def test_init_context_group(self,  mock_context_infos):
        """
        Assert ContextGroup (dict) is initialized with good keys / values.

        Parameters:
        ----------
        mock_context_infos : Mock
            Mock of tc_reporter.contexts.ContextInfos.__init__ .

        Assertions:
        ----------
        assert_called_once_with:
            Assert ContextInfos.__init__ called once with parameters.
        assertDictEqual:
            Assert if obj is the desired dict.
        """
        mock_context_infos.return_value = {}
        obj = ContextGroup(
            'group name', 'status', 'n_tests', 'duration', 'TestCases')
        mock_context_infos.assert_called_once_with(
            'status', 'n_tests', 'duration')
        self.assertDictEqual(
            obj, {'name': 'group name', 'testcases': 'TestCases'})


class TestContextTestCase(TestCase):
    """
    A subclass of unittest.TestCase .

    Tests for tc_reporter.contexts.ContextTestCase .

    Methods
    ----------
    test_init_context_testcase():
        Assert ContextTestCase (dict) is initialized with good keys / values.
    """

    @patch("testcases_executor.tc_reporter.contexts.format_duration")
    def test_init_context_testcase(self, mock_format_duration):
        """
        Assert ContextTestCase (dict) is initialized with good keys / values.

        Parameters:
        ----------
        mock_format_duration : Mock
            Mock of tc_utils.format_duration .

        Assertions:
        ----------
        assert_called_once_with:
            Assert format_duration called once with 'duration'.
        assertDictEqual:
            Assert if obj is the desired dict.
        """
        mock_format_duration.return_value = 'duration formated'
        obj = ContextTestCase('TestCase name', 'module', 'duration', 'methods')
        mock_format_duration.assert_called_once_with('duration')
        self.assertDictEqual(obj, {
            'name': 'TestCase name', 'module': 'module',
            't_methods': 'methods', 'duration': 'duration formated'})


class TestContextMethod(TestCase):
    """
    A subclass of unittest.TestCase .

    Tests for tc_reporter.contexts.ContextMethod .

    Methods
    ----------
    test_init_context_method():
        Assert ContextMethod (dict) is initialized with good keys / values.
    """

    @patch("testcases_executor.tc_reporter.contexts.format_duration")
    def test_init_context_method(self, mock_format_duration):
        """
        Assert ContextMethod (dict) is initialized with good keys / values.

        Parameters:
        ----------
        mock_format_duration : Mock
            Mock of tc_utils.format_duration .

        Class:
        ----------
        FakeTestMethod:
            objet with needed test's argument to init ContextMethod.

        Assertions:
        ----------
        assert_called_once_with:
            Assert format_duration called once with 'duration'.
        assertDictEqual:
            Assert if obj is the desired dict depending of test.
        """
        class FakeTestMethod():

            def __init__(self, t_name):
                self._testMethodName = t_name
                self._testMethodDoc = f"{t_name} doc"

        t1, t2 = FakeTestMethod('t1'), FakeTestMethod('t2'),
        t3, t4 = FakeTestMethod('t3'), FakeTestMethod('t4')
        t5, t6 = FakeTestMethod('t5'), FakeTestMethod('t6')
        t_errors = {
            'failures': [t2], 'errors': [t4],
            'skipped': [t1], 'exp_fails': [t6], 'unex_suc': [t3],
            t1: 'error t1', t2: 'error t2', t6: 'error t6', t4: 'error t4'}
        mock_format_duration.return_value = 'duration formated'
        obj = ContextMethod(t2, 'duration', t_errors)  # failures
        mock_format_duration.assert_called_once_with('duration')
        self.assertDictEqual(obj, {
            'status_name': "FAIL", 'status_icon': "thumbs-o-down",
            'status_color': "warning", 'error': 'error t2',
            'name': 't2', 'doc': 't2 doc', 'duration': 'duration formated'})
        obj = ContextMethod(t4, 'duration', t_errors)  # error
        self.assertDictEqual(obj, {
            'status_name': "ERROR", 'status_icon': "times-circle",
            'status_color': "danger", 'error': 'error t4',
            'name': 't4', 'doc': 't4 doc', 'duration': 'duration formated'})
        obj = ContextMethod(t1, 'duration', t_errors)  # skip
        self.assertDictEqual(obj, {
            'status_name': "SKIP", 'status_icon': "cut",
            'status_color': "info", 'error': 'error t1',
            'name': 't1', 'doc': 't1 doc', 'duration': 'duration formated'})
        obj = ContextMethod(t6, 'duration', t_errors)  # Expected Fail
        self.assertDictEqual(obj, {
            'status_name': "Expected Fail", 'status_icon': "stop-circle-o",
            'status_color': "danger", 'error': 'error t6',
            'name': 't6', 'doc': 't6 doc', 'duration': 'duration formated'})
        obj = ContextMethod(t3, 'duration', t_errors)  # Unexpected Success"
        self.assertDictEqual(obj, {
            'status_name': "Unexpected Success", 'status_color': 'success',
            'status_icon': 'hand-stop-o', 'error': None,
            'name': 't3', 'doc': 't3 doc', 'duration': 'duration formated'})
        obj = ContextMethod(t5, 'duration', t_errors)  # Success
        self.assertDictEqual(obj, {
            'status_name': "SUCCESS", 'status_color': 'success',
            'status_icon': 'thumbs-o-up', 'error': None,
            'name': 't5', 'doc': 't5 doc', 'duration': 'duration formated'})


class TestContextReport(TestCase):
    """
    A subclass of unittest.TestCase .

    Tests for tc_reporter.contexts.ContextReport .

    Methods
    ----------
    test_init_context_report():
        Assert ContextReport object is initialized with good attributes.
    test_make_errors_dict():
        Assert if ContextReport.t_errors is desired dict.
    """

    def test_init_context_report(self):
        """
        Assert ContextReport object is initialized with good attributes.
        """
        pass

    def test_make_errors_dict(self):
        """
        Assert if ContextReport.t_errors is desired dict.
        """
        pass
