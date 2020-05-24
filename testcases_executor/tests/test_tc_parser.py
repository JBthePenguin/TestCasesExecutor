"""
Module testcases_executor.tests.test_tc_parser .

Contain TestCase for testcases_executor.tc_parser .

Classes:
    TestHelpFormatter(TestCase)
    TestParser(TestCase)

Imports:
    from unittest: TestCase
    from unittest.mock: patch, Mock
    from testcases_executor.tc_parser: TestCasesHelpFormatter, TestCasesParser
"""
from unittest import TestCase
from unittest.mock import patch
from testcases_executor.tc_parser import TestCasesHelpFormatter


class TestHelpFormatter(TestCase):
    """
    A subclass of unittest.TestCase .

    Tests for tc_parser.TestCasesHelpFormatter .

    Methods
    ----------
    test_init_formatter():
        Assert if TestCasesHelpFormatter's is initialized with good kwargs.
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
            Assert if HelpFormatter.__init__ is called once with prog and m_h_p.
        """
        TestCasesHelpFormatter(prog='foo')
        mock_formatter_init.assert_called_once_with(
            max_help_position=5,
            prog='\x1b[2mpython -m testcases_executor\x1b[0m\x1b[2m')
