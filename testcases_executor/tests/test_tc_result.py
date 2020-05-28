"""
Module testcases_executor.tests.test_tc_result .

Contain TestCase for testcases_executor.tc_result .

Classes:
    TestTestCasesResult(TestCase)

Imports:
    from unittest: TestCase, TestResult
    from unittest.mock: patch, call, Mock
    from testcases_executor.tc_result: TestCasesResult
"""
from unittest import TestCase, TestResult
from unittest.mock import patch, call, Mock
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

    @patch("testcases_executor.tc_result.time.time")
    @patch("testcases_executor.tc_result.TestResult.startTest")
    def test_startTest(self, mock_start_test, mock_time):
        """
        Assert if TestCasesResult.startTest write good things in stream.

        Parameters:
        ----------
        mock_start_test : Mock
            Mock of unittest.TestResult.startTest .
        mock_time : Mock
            Mock of time.

        Classes:
        ----------
        FakeTest:
            A fake test with property _testMethodName.

        Assertions:
        ----------
        assert_called_once_with:
            Assert if TestResult.startTest is called with test in parameter,
            stream.flush without parameter.
        assertEqual:
            Assert if stream.write called 2 and value of test_t_start property.
        assert_has_calls:
            Assert stream.write calls parameters.
        """
        class FakeTest():

            def __init__(self):
                self._testMethodName = 'test'

        test = FakeTest()
        obj = TestCasesResult(stream='stream')
        obj.stream = Mock()
        mock_time.return_value = 103
        obj.startTest(test)
        mock_start_test.assert_called_once_with(test)
        self.assertEqual(2, obj.stream.write.call_count)
        obj.stream.write.assert_has_calls([call('test'), call(" ... ")])
        obj.stream.flush.assert_called_once_with()
        self.assertEqual(obj.test_t_start, 103)

    def test_addFoo(self):
        """
        Assert if TestCasesResult.addFoo save duration write it with status.

        Assertions:
        ----------
        assert_called_once_with:
            Assert if stream.write called with good parameter,
            stream.flush without.
        assertEqual:
            Assert if value with key test in durations property with key tests.
        """
        obj = TestCasesResult(stream='stream')
        obj.test_t_start = 1000.00234862
        obj.stream = Mock()
        obj.addFoo(1000.00523, 'test', 'OK')
        obj.stream.writeln.assert_called_once_with(
            "OK ... \x1b[35m2.881 ms\x1b[39m")
        obj.stream.flush.assert_called_once_with()
        self.assertEqual(obj.durations['tests']['test'], 0.002881)
