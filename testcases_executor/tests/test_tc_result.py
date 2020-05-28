"""
Module testcases_executor.tests.test_tc_result .

Contain TestCase for testcases_executor.tc_result .

Classes:
    TestTestCasesResult(TestCase)

Imports:
    from unittest: TestCase, TestResult
    from unittest.mock: patch
    from argparse: HelpFormatter
    from testcases_executor.tc_parser: TestCasesHelpFormatter, TestCasesParser
"""
from unittest import TestCase, TestResult
from unittest.mock import patch, call
from argparse import HelpFormatter, ArgumentParser
from testcases_executor.tc_result import TestCasesResult


class TestTestCasesResult(TestCase):
    """
    A subclass of unittest.TestCase .

    Tests for tc_result.TestCasesResult .

    Methods
    ----------
    test_init_result():
        Assert if TestCasesResult is initialized with good attributes.
    test_startTest():
        Assert if TestCasesResult.startTest write good things in stream.
    test_addFoo():
        Assert if TestCasesResult.addFoo save duration write it with status.
    test_addSuccess()
        Assert addFoo is called with good parameters.
    """

    @patch("testcases_executor.tc_result.TestResult.__init__")
    def test_init_result(self, mock_result_init):
        """
        Assert if TestCasesResult is initialized with good attributes.

        Parameters:
        ----------
        mock_result_init : Mock
            Mock of unittest.TestResult.__init__ .

        Assertions:
        ----------
        assert_called_once_with:
            Assert if TestResult.__init__ is called once without parameter.
        assertIsInstance:
            Assert if obj is instance TestResult.
        assertEqual:
            Assert attributes values of object.
        """
        obj = TestCasesResult(stream='stream')
        mock_result_init.assert_called_once_with()
        self.assertIsInstance(obj, TestResult)
        self.assertEqual(obj.separator1, '=' * 70)
        self.assertEqual(obj.separator2, '-' * 70)
        self.assertEqual(obj.stream, 'stream')
        self.assertEqual(obj.start_time, 0)
        self.assertEqual(obj.test_methods, [])
        self.assertEqual(
            obj.durations, {'groups': {}, 'testcases': {}, 'tests': {}})
