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
from unittest.mock import patch
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

    @patch("builtins.print")
    @patch('testcases_executor.__main__.TestCasesGroups')
    def test_main(self, mock_groups, mock_print):
        """
        Assert if groups is constructed, parsed and testscases runned.

        Call main and assert if a groups is initialized, ...

        Parameters:
        ----------
        mock_groups : Mock
            Mock of TestCasesGroups.
        mock_print : Mock
            Mock of print function.

        Assertions:
        ----------
        assert_called_once:
            Assert if TestCasesGroups is called once.
        assertTrue:
            Assert if print is called.
        """
        main()
        mock_groups.assert_called_once()
        self.assertTrue(mock_print.called)
