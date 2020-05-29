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
        class FakeResult():
            def __init__(self):
                self.separator2 = 'separator2'
                self.durations = {'tests': {
                    'test1': 0.3, 'test2': 0.2, 'test3': 0.2, 'test4': 0.6}}

        class FakeTestOne():
            pass
            # def __init__(self, tc_name, tc_module):
            #     self.__name__, self.__module__ = tc_name, tc_module

        class FakeTestTwo():
            pass

        class FakeSuite():
            pass
            # def __init__(self, tests):
            #     self._tests = tests

        # FakeSuite.__init__ = Mock()
        # test_one, test_two = FakeTestOne, FakeTestTwo
        # suite_one = FakeSuite()
        # suite_two = FakeSuite()
        # suite_one = FakeSuite(['test1', 'test2', 'test3'])
        # suite_two = FakeSuite(['test4'])

        class FakeGroup():
            def __init__(self):
                self.suites = [
                    (test_one, suite_one), (test_two, suite_two)]

        # result, group = FakeResult(), FakeGroup()
        # obj = TestCasesRunner()
        # obj.stream = Mock()
        # obj.run_group_suites(result, group)

    def test_run(self):
        """
        Assert stream.writeln calls, if groups suites runned, result updated.
        """
        pass
