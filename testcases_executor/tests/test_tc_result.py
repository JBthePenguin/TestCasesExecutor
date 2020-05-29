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
    test_addSuccess():
        Assert if TestCasesResult.addSuccess call addFoo with good parameters.
    test_addError():
        Assert if TestCasesResult.addError call addFoo, TestResult.addError .
    test_addFailure():
        Assert TestCasesResult.addFailure call addFoo, TestResult.addFailure .
    test_addSkip():
        Assert TestCasesResult.addSkip call addFoo, TestResult.addSkip .
    test_addExpectedFailure():
        Assert TestCasesResult.addExpectedFailure call addFoo, same on super.
    test_addUnexpectedSuccess():
        Assert TestCasesResult.addUnexpectedSuccess call addFoo, same on super.
    test_printErrors():
        Assert stream.writeln called once, printErrorList 2 with parameters.
    test_printErrorList():
        Assert stream.writeln calls and parameters.
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

    @patch("testcases_executor.tc_result.time.time")
    def test_addSuccess(self, mock_time):
        """
        Assert if TestCasesResult.addSuccess call addFoo with good parameters.

        Parameters:
        ----------
        mock_time : Mock
            Mock of time.

        Assertions:
        ----------
        assertEqual:
            Assert if obj.addFoo call one.
        assert_has_calls:
            Assert obj.addFoo call parameters.
        """
        mock_time.return_value = 103
        obj = TestCasesResult(stream='stream')
        obj.addFoo = Mock()
        obj.addSuccess('test')
        self.assertEqual(1, obj.addFoo.call_count)
        obj.addFoo.assert_has_calls([call(103, 'test', '\x1b[32mOK\x1b[39m')])

    @patch("testcases_executor.tc_result.time.time")
    @patch("testcases_executor.tc_result.TestResult.addError")
    def test_addError(self, mock_add_error, mock_time):
        """
        Assert if TestCasesResult.addError call addFoo, TestResult.addError .

        Parameters:
        ----------
        mock_add_error : Mock
            Mock of TestResult.addError .
        mock_time : Mock
            Mock of time.

        Assertions:
        ----------
        assertEqual:
            Assert if obj.addFoo call one.
        assert_has_calls:
            Assert obj.addFoo call parameters.
        """
        mock_time.return_value = 103
        obj = TestCasesResult(stream='stream')
        obj.addFoo = Mock()
        obj.addError('test', 'error')
        self.assertEqual(1, obj.addFoo.call_count)
        obj.addFoo.assert_has_calls(
            [call(103, 'test', '\x1b[31mERROR\x1b[39m')])
        mock_add_error.assert_called_once_with('test', 'error')

    @patch("testcases_executor.tc_result.time.time")
    @patch("testcases_executor.tc_result.TestResult.addFailure")
    def test_addFailure(self, mock_add_fail, mock_time):
        """
        Assert TestCasesResult.addFailure call addFoo, TestResult.addFailure .

        Parameters:
        ----------
        mock_add_fail : Mock
            Mock of TestResult.addFailure .
        mock_time : Mock
            Mock of time.

        Assertions:
        ----------
        assertEqual:
            Assert if obj.addFoo call one.
        assert_has_calls:
            Assert obj.addFoo call parameters.
        """
        mock_time.return_value = 103
        obj = TestCasesResult(stream='stream')
        obj.addFoo = Mock()
        obj.addFailure('test', 'error')
        self.assertEqual(1, obj.addFoo.call_count)
        obj.addFoo.assert_has_calls(
            [call(103, 'test', '\x1b[33mFAIL\x1b[39m')])
        mock_add_fail.assert_called_once_with('test', 'error')

    @patch("testcases_executor.tc_result.time.time")
    @patch("testcases_executor.tc_result.TestResult.addSkip")
    def test_addSkip(self, mock_add_skip, mock_time):
        """
        Assert TestCasesResult.addSkip call addFoo, TestResult.addSkip .

        Parameters:
        ----------
        mock_add_skip : Mock
            Mock of TestResult.addSkip .
        mock_time : Mock
            Mock of time.

        Assertions:
        ----------
        assertEqual:
            Assert if obj.addFoo call one.
        assert_has_calls:
            Assert obj.addFoo call parameters.
        """
        mock_time.return_value = 103
        obj = TestCasesResult(stream='stream')
        obj.addFoo = Mock()
        obj.addSkip('test', 'reason')
        self.assertEqual(1, obj.addFoo.call_count)
        obj.addFoo.assert_has_calls(
            [call(103, 'test', '\x1b[36mSKIP\x1b[39m')])
        mock_add_skip.assert_called_once_with('test', 'reason')

    @patch("testcases_executor.tc_result.time.time")
    @patch("testcases_executor.tc_result.TestResult.addExpectedFailure")
    def test_addExpectedFailure(self, mock_add_ex_fail, mock_time):
        """
        Assert TestCasesResult.addExpectedFailure call addFoo, same on super.

        Parameters:
        ----------
        mock_add_ex_fail : Mock
            Mock of TestResult.addExpectedFailure .
        mock_time : Mock
            Mock of time.

        Assertions:
        ----------
        assertEqual:
            Assert if obj.addFoo call one.
        assert_has_calls:
            Assert obj.addFoo call parameters.
        """
        mock_time.return_value = 103
        obj = TestCasesResult(stream='stream')
        obj.addFoo = Mock()
        obj.addExpectedFailure('test', 'error')
        self.assertEqual(1, obj.addFoo.call_count)
        obj.addFoo.assert_has_calls(
            [call(103, 'test', '\x1b[31mexpected failure\x1b[39m')])
        mock_add_ex_fail.assert_called_once_with('test', 'error')

    @patch("testcases_executor.tc_result.time.time")
    @patch("testcases_executor.tc_result.TestResult.addUnexpectedSuccess")
    def test_addUnexpectedSuccess(self, mock_add_unex_suc, mock_time):
        """
        Assert TestCasesResult.addUnexpectedSuccess call addFoo, same on super.

        Parameters:
        ----------
        mock_add_unex_suc : Mock
            Mock of TestResult.addUnexpectedSuccess .
        mock_time : Mock
            Mock of time.

        Assertions:
        ----------
        assertEqual:
            Assert if obj.addFoo call one.
        assert_has_calls:
            Assert obj.addFoo call parameters.
        """
        mock_time.return_value = 103
        obj = TestCasesResult(stream='stream')
        obj.addFoo = Mock()
        obj.addUnexpectedSuccess('test')
        self.assertEqual(1, obj.addFoo.call_count)
        obj.addFoo.assert_has_calls(
            [call(103, 'test', '\x1b[32munexpected success\x1b[39m')])
        mock_add_unex_suc.assert_called_once_with('test')

    def test_printErrors(self):
        """
        Assert stream.writeln called once, printErrorList 2 with parameters.

        Assertions:
        ----------
        assertEqual:
            Assert if obj.printErrorList call 2.
        assert_has_calls:
            Assert obj.printErrorList call parameters.
        """
        obj = TestCasesResult(stream='stream')
        obj.stream = Mock()
        obj.printErrorList = Mock()
        obj.printErrors()
        obj.stream.writeln.assert_called_once_with()
        self.assertEqual(2, obj.printErrorList.call_count)
        obj.printErrorList.assert_has_calls([
            call('ERROR', obj.errors, '\x1b[31m'),
            call('FAIL', obj.failures, '\x1b[33m')])

    def test_printErrorList(self):
        """
        Assert stream.writeln calls and parameters.
        """
        class FakeTestOne():
            def __init__(self):
                self._testMethodName = 'test_one'

        class FakeTestTwo():
            def __init__(self):
                self._testMethodName = 'test_two'

        errors = [
            (FakeTestOne(), "error one\nline 2"),
            (FakeTestTwo(), "error two\nline 2")
        ]
        obj = TestCasesResult(stream='stream')
        obj.stream = Mock()
        obj.printErrorList('flavour', errors, '\x1b[31m')
        self.assertEqual(12, obj.stream.writeln.call_count)
        obj.stream.writeln.assert_has_calls([
            call(obj.separator1),
            call('\x1b[31mflavour\x1b[0m: \x1b[1mFakeTestOne\x1b[0m.test_one'),
            call(obj.separator2),
            call('\x1b[31mline 2\x1b[39m'),
            call(obj.separator2),
            call('\x1b[2merror one\nline 2\x1b[0m'),
            call(obj.separator1),
            call('\x1b[31mflavour\x1b[0m: \x1b[1mFakeTestTwo\x1b[0m.test_two'),
            call(obj.separator2),
            call('\x1b[31mline 2\x1b[39m'),
            call(obj.separator2),
            call('\x1b[2merror two\nline 2\x1b[0m')])
