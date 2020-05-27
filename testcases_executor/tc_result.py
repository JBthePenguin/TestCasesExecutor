import time
from unittest import TestResult
from testcases_executor.tc_utils import (
    format_duration, GREEN, BLUE, RED, YELLOW, MAGENTA, C_RESET,
    BOLD, MUTED, S_RESET)


class TestCasesResult(TestResult):
    """Override HtmlTestResult to change desription and format duration,
    and get a non alphabetical order for test methods."""
    separator1 = '=' * 70
    separator2 = '-' * 70

    def __init__(self, stream):
        super().__init__()
        self.stream = stream
        self.start_time = 0
        self.test_methods = []
        self.durations = {'groups': {}, 'testcases': {}, 'tests': {}}

    def getTestName(self, test):
        """Return the test description with the test method name."""
        return test._testMethodName

    def startTest(self, test):
        """ Called before execute each method. """
        super().startTest(test)
        self.stream.write(self.getTestName(test))
        self.stream.write(" ... ")
        self.stream.flush()
        self.test_t_start = time.time()

    def addFoo(self, test_t_stop, test, status):
        t_duration = test_t_stop - self.test_t_start
        self.durations['tests'][test] = t_duration
        duration_str = format_duration(t_duration)
        self.stream.writeln(
            f"{status} ... {MAGENTA}{duration_str}{C_RESET}")
        self.stream.flush()

    def addSuccess(self, test):
        self.addFoo(time.time(), test, f"{GREEN}OK{C_RESET}")

    def addError(self, test, err):
        self.addFoo(time.time(), test, f"{RED}ERROR{C_RESET}")
        super().addError(test, err)

    def addFailure(self, test, err):
        self.addFoo(time.time(), test, f"{YELLOW}FAIL{C_RESET}")
        super().addFailure(test, err)

    def addSkip(self, test, reason):
        self.addFoo(time.time(), test, f"{BLUE}SKIP{C_RESET}")
        super().addSkip(test, reason)

    def addExpectedFailure(self, test, err):
        self.addFoo(time.time(), test, f"{RED}expected failure{C_RESET}")
        super().addExpectedFailure(test, err)

    def addUnexpectedSuccess(self, test):
        self.addFoo(time.time(), test, f"{GREEN}unexpected success{C_RESET}")
        super().addUnexpectedSuccess(test)

    def printErrors(self):
        self.stream.writeln()
        self.printErrorList('ERROR', self.errors, RED)
        self.printErrorList('FAIL', self.failures, YELLOW)

    def printErrorList(self, flavour, errors, e_color):
        for test, err in errors:
            tc_name = test.__class__.__name__
            method_name = test._testMethodName
            test_str = f"{BOLD}{tc_name}{S_RESET}.{method_name}"
            self.stream.writeln(self.separator1)
            self.stream.writeln(
                f"{e_color}{flavour}{S_RESET}: {test_str}")
            self.stream.writeln(self.separator2)
            self.stream.writeln(
                f"{e_color}{err.splitlines()[-1]}{C_RESET}")
            self.stream.writeln(self.separator2)
            self.stream.writeln(f"{MUTED}{err}{S_RESET}")

    def printTotal(self, run, duration):
        s_test = "test"
        if run > 1:
            s_test += "s"
        ran_text = f"Ran {run} {s_test}{S_RESET}"
        self.stream.writeln(
            f"{ran_text} in {MAGENTA}{format_duration(duration)}{C_RESET}")

    def printInfos(self):
        """Print infos at the end of all tests."""
        expectedFails = len(self.expectedFailures)
        unexpectedSuccesses = len(self.unexpectedSuccesses)
        skipped = len(self.skipped)
        infos = []
        if not self.wasSuccessful():
            self.stream.writeln(f"\n{RED}FAILED{C_RESET}")
            failed, errors = map(len, (self.failures, self.errors))
            if failed:
                infos.append(f"{YELLOW}Failures={failed}{C_RESET}")
            if errors:
                infos.append(f"{RED}Errors={errors}{C_RESET}")
        else:
            self.stream.writeln(f"\n{GREEN}OK{C_RESET}")
        if skipped:
            infos.append(f"{BLUE}Skipped={skipped}{C_RESET}")
        if expectedFails:
            e_fail = "Expected Failures="
            infos.append(
                f"{RED}{e_fail}{expectedFails}{C_RESET}")
        if unexpectedSuccesses:
            u_suc = "Unexpected Successes="
            infos.append(
                f"{GREEN}{u_suc}{unexpectedSuccesses}{C_RESET}")
        if infos:
            self.stream.writeln(f" ({' , '.join(infos)})")
