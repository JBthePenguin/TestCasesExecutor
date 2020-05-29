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

        Classes:
        ----------
        FakeResult:
            Fake a result to get properties to assert if updated correctly.
        FakeTestOne, FakeTestTwo:
            Fake tests to get __name__ and __module__ properties.
        FakeSuiteOne, FakeSuiteTwo:
            Fake suite with property _tests, to pass init during test.
        FakeGroup:
            Fake group with suites property.
        """
        class FakeResult():

            def __init__(self):
                self.separator2 = 'separator2'
                self.durations = {
                    'tests': {
                        'test1': 0.3, 'test2': 0.2,
                        'test3': 0.2, 'test4': 0.6},
                    'testcases': {}}
                self.test_methods = []

        class FakeTestOne():
            pass

        class FakeTestTwo():
            pass

        class FakeSuiteOne():
            _tests = ['test1', 'test2', 'test3']

            def __init__(self, result):
                pass

        class FakeSuiteTwo():
            _tests = ['test4']

            def __init__(self, result):
                pass

        test_one, test_two = FakeTestOne, FakeTestTwo
        suite_one, suite_two = FakeSuiteOne, FakeSuiteTwo

        class FakeGroup():
            def __init__(self):
                self.suites = [
                    (test_one, suite_one), (test_two, suite_two)]

        result, group = FakeResult(), FakeGroup()
        obj = TestCasesRunner()
        obj.stream = Mock()
        obj.run_group_suites(result, group)
        self.assertEqual(8, obj.stream.writeln.call_count)
        obj.stream.writeln.assert_has_calls([
            call('separator2'),
            call('\n\x1b[1m --- FakeTestOne ---\x1b[0m'),
            call(
                '\x1b[2m testcases_executor.tests.test_tc_runner.py\x1b[0m\n'),
            call('\n ... \x1b[35m700.0 ms\x1b[0m\n'),
            call('separator2'),
            call('\n\x1b[1m --- FakeTestTwo ---\x1b[0m'),
            call(
                '\x1b[2m testcases_executor.tests.test_tc_runner.py\x1b[0m\n'),
            call('\n ... \x1b[35m600.0 ms\x1b[0m\n')])
        self.assertEqual(result.durations['testcases'][test_one], 0.7)
        self.assertEqual(result.durations['testcases'][test_two], 0.6)
        self.assertEqual(len(result.test_methods), 1)
        self.assertTupleEqual(result.test_methods[0], (
            group, [
                (test_one, ['test1', 'test2', 'test3']),
                (test_two, ['test4'])]))

    def test_run(self):
        """
        Assert stream.writeln calls, if groups suites runned, result updated.
        """
        pass
