"""
Module testcases_executor.tests.test_main .

Contain TestCase for testcases_executor.__main__ .

Classes:
    TestMain(TestCase)

Imports:
    from unittest: TestCase
    from unittest.mock: patch
    from testcases_executor.__main__: main
"""
from unittest import TestCase
from unittest.mock import patch, Mock
from testcases_executor.__main__ import main


class TestMainFunctions(TestCase):
    """
    A subclass of unittest.TestCase .

    Tests for __main__ functions, main.

    Methods
    ----------
    test_main():
        Assert if groups is constructed, parsed and testscases runned.
    """

    @patch('testcases_executor.__main__.TestCasesGroups')
    @patch('testcases_executor.__main__.TestCasesParser')
    def test_main(self, mock_parser, mock_groups):
        """
        Assert if groups is constructed, parsed and testscases runned.

        Call main and assert if a groups is initialized, ...

        Parameters:
        ----------
        mock_parser : Mock
            Mock of TestCasesParser.
        mock_groups : Mock
            Mock of TestCasesGroups.

        Assertions:
        ----------
        assert_called_once:
            Assert if TestCasesGroups, TestCasesParser.parse_args called once.
        assert_called_once_with:
            Assert if TestCasesParser called once with TestCasesGroups object.
        """
        main()
        mock_groups.assert_called_once()
        mock_parser.assert_called_once_with(mock_groups())
        mock_parser().parse_args.assert_called_once()
