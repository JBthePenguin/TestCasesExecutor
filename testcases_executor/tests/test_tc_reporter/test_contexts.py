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
from unittest.mock import patch
from testcases_executor.tc_reporter.contexts import (
    ContextInfos)


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

    def test_init_context_header(self):
        """
        Assert ContextHeader (dict) is initialized with good keys / values.
        """
        pass


class TestContextGroup(TestCase):
    """
    A subclass of unittest.TestCase .

    Tests for tc_reporter.contexts.ContextGroup .

    Methods
    ----------
    test_init_context_group():
        Assert ContextGroup (dict) is initialized with good keys / values.
    """

    def test_init_context_group(self):
        """
        Assert ContextGroup (dict) is initialized with good keys / values.
        """
        pass


class TestContextTestCase(TestCase):
    """
    A subclass of unittest.TestCase .

    Tests for tc_reporter.contexts.ContextTestCase .

    Methods
    ----------
    test_init_context_testcase():
        Assert ContextTestCase (dict) is initialized with good keys / values.
    """

    def test_init_context_testcase(self):
        """
        Assert ContextTestCase (dict) is initialized with good keys / values.
        """
        pass


class TestContextMethod(TestCase):
    """
    A subclass of unittest.TestCase .

    Tests for tc_reporter.contexts.ContextMethod .

    Methods
    ----------
    test_init_context_method():
        Assert ContextMethod (dict) is initialized with good keys / values.
    """

    def test_init_context_method(self):
        """
        Assert ContextMethod (dict) is initialized with good keys / values.
        """
        pass


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
