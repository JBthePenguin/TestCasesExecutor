"""
Module testcases_executor.tests.test_tc_parser .

Contain TestCase for testcases_executor.tc_parser .

Classes:
    TestHelpFormatter(TestCase)
    TestParser(TestCase)

Imports:
    from unittest: TestCase
    from unittest.mock: patch
    from argparse: HelpFormatter
    from testcases_executor.tc_parser: TestCasesHelpFormatter, TestCasesParser
"""
from unittest import TestCase
from unittest.mock import patch
from argparse import HelpFormatter
from testcases_executor.tc_parser import TestCasesHelpFormatter


class TestHelpFormatter(TestCase):
    """
    A subclass of unittest.TestCase .

    Tests for tc_parser.TestCasesHelpFormatter .

    Methods
    ----------
    test_init_formatter():
        Assert if TestCasesHelpFormatter's is initialized with good kwargs.
    test_add_usage():
        Assert if TestCasesHelpFormatter.add_usage -> HelpFormatter.add_usage .
    test_format_args():
        Assert the return TestCasesHelpFormatter._format_args .
    test_join_parts()
        Assert the return TestCasesHelpFormatter._join_parts .
    """

    @patch("testcases_executor.tc_parser.HelpFormatter.__init__")
    def test_init_formatter(self, mock_formatter_init):
        """
        Assert if TestCasesHelpFormatter's is initialized with good kwargs.

        Parameters:
        ----------
        mock_formatter_init : Mock
            Mock of argparse.HelpFormatter.__init__ .

        Assertions:
        ----------
        assert_called_once_with:
            Assert if HelpFormatter.__init__ is called once with good kwargs.
        assertIsInstance:
            Assert if obj is instance HelpFormatter.
        """
        obj = TestCasesHelpFormatter(prog='foo', max_help_position=10)
        mock_formatter_init.assert_called_once_with(
            max_help_position=5,
            prog='\x1b[2mpython -m testcases_executor\x1b[0m\x1b[2m')
        self.assertIsInstance(obj, HelpFormatter)

    @patch("testcases_executor.tc_parser.HelpFormatter.add_usage")
    def test_add_usage(self, mock_formatter_add_usage):
        """
        Assert if TestCasesHelpFormatter.add_usage -> HelpFormatter.add_usage .

        Parameters:
        ----------
        mock_formatter_add_usage : Mock
            Mock of argparse.HelpFormatter.add_usage .

        Assertions:
        ----------
        assert_called_once_with:
            Assert if HelpFormatter.add_usage is called once with good kwargs.
        assertEqual:
            Assert the return of TestCasesHelpFormatter.add_usage .
        """
        mock_formatter_add_usage.return_value = "add_usage called"
        result = TestCasesHelpFormatter().add_usage('usg', 'act', 'grp')
        mock_formatter_add_usage.assert_called_once_with(
            'usg', 'act', 'grp', '\x1b[1m')
        self.assertEqual(result, "add_usage called")

    def test_format_args(self):
        """
        Assert the return TestCasesHelpFormatter._format_args .

        Assertions:
        ----------
        assertEqual:
            Assert if TestCasesHelpFormatter._format_args return '...' .
        """
        self.assertEqual(
            TestCasesHelpFormatter()._format_args('act', 'met'), "...")

    def test_join_parts(self):
        """
        Assert the return TestCasesHelpFormatter._join_parts .

        Assertions:
        ----------
        assertEqual:
            Assert if TestCasesHelpFormatter._format_args have good return.
        """
        for parameter, result in [
                (['foo', ], '\n\x1b[2mfoo\x1b[0m'),
                (['', 'foo\nbar'], '\n\x1b[2m\x1b[0mfoo\nbar'),
                (['', 'foo:\n'], '\n\x1b[2m\x1b[0m\x1b[1mfoo:\n\x1b[0m')]:
            self.assertEqual(
                TestCasesHelpFormatter()._join_parts(parameter), result)
