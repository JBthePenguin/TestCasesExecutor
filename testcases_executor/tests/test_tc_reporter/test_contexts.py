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


class TestContextInfos(TestCase):
    """
    A subclass of unittest.TestCase .

    Tests for tc_reporter.contexts.ContextInfos .

    Methods
    ----------
    test_init_context_infos():
        Assert ContextInfos (dict) is initialized with good keys / values.
    """

    def test_init_context_infos(self):
        """
        Assert ContextInfos (dict) is initialized with good keys / values.
        """
        pass


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
