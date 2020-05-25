"""
Module testcases_executor.tc_runner

Contain the runner class.

Classes:
    TestCasesRunner

Functions:
    import_groups()

Imports:
    sys
    from fnmatch: fnmatchcase
    from unittest: TestCase, TestLoader, TestSuite
    from testcases_executor.tc_utils: raise_error, check_type
"""
import time
import warnings
from unittest import TextTestRunner
from unittest.signals import registerResult


class TestCasesRunner(TextTestRunner):
    """A HTMLTestRunner for TestCase."""

    # def __init__(self, test_cases, add_timestamp, open_in_browser):
    #     """Set property suites a dict for all tests docs.
    #     For each tests cases list
    #     Init ArgumentParser with formatter class and description.
    #     Set help message's title for help command. Make argument groups.
    #     Check args and run the corresponding tests.
    #     ***arg_groups -> [('group_name', [TestCase1, ...]), (..)].***"""
    #     self.suites = []
    #     self.tests_docs = {}
    #     for test_case in test_cases:
    #         self.update_suites_docs(test_case)
    #     template_args = {'tests_docs': self.tests_docs}
    #     super().__init__(
    #         output='html_test_reports', combine_reports=True,
    #         report_name='result', add_timestamp=add_timestamp,
    #         resultclass=HtmlTestCaseResult, template_args=template_args,
    #         template=os.path.join(
    #             os.path.dirname(__file__), 'template', 'base_temp.html'),
    #         report_title=f"{os.path.basename(os.getcwd())} Unittest Results",
    #         open_in_browser=open_in_browser)
    def __init__(self):
        super().__init__(
            stream=None, descriptions=True, verbosity=2,
            failfast=False, buffer=False, resultclass=None,
            warnings=None, tb_locals=False)

    def run(self, tc_groups):
        "Run the given test case or test suite."
        result = self._makeResult()
        registerResult(result)
        result.failfast = self.failfast
        result.buffer = self.buffer
        result.tb_locals = self.tb_locals
        with warnings.catch_warnings():
            if self.warnings:
                # if self.warnings is set, use it to filter all the warnings
                warnings.simplefilter(self.warnings)
                # if the filter is 'default' or 'always', special-case the
                # warnings from the deprecated unittest methods to show them
                # no more than once per module, because they can be fairly
                # noisy.  The -Wd and -Wa flags can be used to bypass this
                # only when self.warnings is None.
                if self.warnings in ['default', 'always']:
                    warnings.filterwarnings('module',
                            category=DeprecationWarning,
                            message=r'Please use assert\w+ instead.')
            startTime = time.perf_counter()
            startTestRun = getattr(result, 'startTestRun', None)
            if startTestRun is not None:
                startTestRun()
            try:
                for tc_group in tc_groups:
                    for tc, suite in tc_group.suites:
                        suite(result)
            finally:
                stopTestRun = getattr(result, 'stopTestRun', None)
                if stopTestRun is not None:
                    stopTestRun()
            stopTime = time.perf_counter()
        timeTaken = stopTime - startTime
        result.printErrors()
        if hasattr(result, 'separator2'):
            self.stream.writeln(result.separator2)
        run = result.testsRun
        self.stream.writeln("Ran %d test%s in %.3fs" %
                            (run, run != 1 and "s" or "", timeTaken))
        self.stream.writeln()

        expectedFails = unexpectedSuccesses = skipped = 0
        try:
            results = map(len, (result.expectedFailures,
                                result.unexpectedSuccesses,
                                result.skipped))
        except AttributeError:
            pass
        else:
            expectedFails, unexpectedSuccesses, skipped = results

        infos = []
        if not result.wasSuccessful():
            self.stream.write("FAILED")
            failed, errored = len(result.failures), len(result.errors)
            if failed:
                infos.append("failures=%d" % failed)
            if errored:
                infos.append("errors=%d" % errored)
        else:
            self.stream.write("OK")
        if skipped:
            infos.append("skipped=%d" % skipped)
        if expectedFails:
            infos.append("expected failures=%d" % expectedFails)
        if unexpectedSuccesses:
            infos.append("unexpected successes=%d" % unexpectedSuccesses)
        if infos:
            self.stream.writeln(" (%s)" % (", ".join(infos),))
        else:
            self.stream.write("\n")
        return result
