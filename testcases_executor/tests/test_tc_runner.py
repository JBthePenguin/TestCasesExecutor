"""
Module testcases_executor.tests.test_tc_runner .

Contain TestCase for testcases_executor.tc_runner .

Classes:
    TestTestRunner(TestCase)

Imports:
    from unittest: TestCase, TestResult
    from unittest.mock: patch, call, Mock
    from testcases_executor.tc_result: TestCasesResult
"""
from unittest import TestCase, TextTestRunner
from unittest.mock import patch, call, Mock
from testcases_executor.tc_runner import TestCasesRunner
from testcases_executor.tc_result import TestCasesResult


class TestTestRunner(TestCase):
    """
    A subclass of unittest.TestCase .

    Tests for tc_runner.TestCasesRunner .

    Methods
    ----------
    test_init_runner():
        Assert if TestCasesRunner is initialized with good attributes.
    test_run_group_suites():
        Assert stream.writeln calls, if suites runned, properties updated.
    test_run():
        Assert stream.writeln calls, if groups suites runned, result updated.
    """

    @patch("testcases_executor.tc_runner.TextTestRunner.__init__")
    def test_init_runner(self, mock_runner_init):
        """
        Assert if TestCasesRunner is initialized with good attributes.

        Parameters:
        ----------
        mock_runner_init : Mock
            Mock of unittest.TextTestRunner.__init__ .

        Assertions:
        ----------
        assert_called_once_with:
            Assert if TextTestRunner.__init__ is called once with parameter.
        assertIsInstance:
            Assert if obj is instance TextTestRunner.
        """
        obj = TestCasesRunner()
        mock_runner_init.assert_called_once_with(resultclass=TestCasesResult)
        self.assertIsInstance(obj, TextTestRunner)

    def test_run_group_suites(self):
        """
        Assert stream.writeln calls, if suites runned, properties updated.
        """
        pass

    def test_run(self):
        """
        Assert stream.writeln calls, if groups suites runned, result updated.
        """
        pass
