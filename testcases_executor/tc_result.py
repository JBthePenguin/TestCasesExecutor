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

    def __init__(self, stream, descriptions, verbosity):
        super().__init__(stream, descriptions, verbosity)
        self.stream = stream
        self.descriptions = descriptions
        self.start_time = 0
        self.durations = {'groups': {}, 'testcases': {}, 'tests': {}}

    def getDescription(self, test):
        """Return the test description with the test method name."""
        return test._testMethodName

    def startTest(self, test):
        """ Called before execute each method. """
        self.test_t_start = time.time()
        super().startTest(test)
        self.stream.write(self.getDescription(test))
        self.stream.write(" ... ")
        self.stream.flush()

    def save_t_duration(self, test):
        t_duration = time.time() - self.test_t_start
        self.durations['tests'][test] = t_duration
        return t_duration

    def addSuccess(self, test):
        t_duration = self.save_t_duration(test)
        super().addSuccess(test)
        status = f"{GREEN}OK{C_RESET}"
        duration_str = format_duration(t_duration)
        self.stream.writeln(
            f"{status} ... {MAGENTA}{duration_str}{C_RESET}")
        self.stream.flush()

    def addError(self, test, err):
        t_duration = self.save_t_duration(test)
        super().addError(test, err)
        status = f"{RED}ERROR{C_RESET}"
        duration_str = format_duration(t_duration)
        self.stream.writeln(
            f"{status} ... {MAGENTA}{duration_str}{C_RESET}")
        self.stream.flush()

    def addFailure(self, test, err):
        t_duration = self.save_t_duration(test)
        super().addFailure(test, err)
        status = f"{YELLOW}FAIL{C_RESET}"
        duration_str = format_duration(t_duration)
        self.stream.writeln(
            f"{status} ... {MAGENTA}{duration_str}{C_RESET}")
        self.stream.flush()

    def addSkip(self, test, reason):
        t_duration = self.save_t_duration(test)
        super().addSkip(test, reason)
        status = f"{BLUE}SKIP{C_RESET}"
        duration_str = format_duration(t_duration)
        self.stream.writeln(
            f"{status} ... {MAGENTA}{duration_str}{C_RESET}")
        self.stream.flush()

    def addExpectedFailure(self, test, err):
        t_duration = self.save_t_duration(test)
        super().addExpectedFailure(test, err)
        status = f"{RED}expected failure{C_RESET}"
        duration_str = format_duration(t_duration)
        self.stream.writeln(
            f"{status} ... {MAGENTA}{duration_str}{C_RESET}")
        self.stream.flush()

    def addUnexpectedSuccess(self, test):
        t_duration = self.save_t_duration(test)
        super().addUnexpectedSuccess(test)
        status = f"{GREEN}unexpected success{C_RESET}"
        duration_str = format_duration(t_duration)
        self.stream.writeln(
            f"{status} ... {MAGENTA}{duration_str}{C_RESET}")
        self.stream.flush()

    def printErrors(self):
        self.stream.writeln()
        self.printErrorList('ERROR', self.errors)
        self.printErrorList('FAIL', self.failures)

    def printErrorList(self, flavour, errors):
        for test, err in errors:
            if flavour == "ERROR":
                t_color = RED
            else:
                t_color = YELLOW
            tc_name = test.__class__.__name__
            method_name = test._testMethodName
            test_str = f"{BOLD}{tc_name}{S_RESET}.{method_name}"
            # print(err.splitlines())
            self.stream.writeln(self.separator1)
            # c_flavour = f"{t_color}{flavour}"
            # test_name = f"{test_info.test_id}".split('.')[-2:]
            # test_str = f"{BOLD}{test_name[0]}{S_RESET}"
            # test_str += f".{test_name[1]}"
            time_str = f"{MAGENTA}"
            time_str += f"{format_duration(self.durations['tests'][test])}"
            # error_name = f"{t_color}{test_info.err[0].__name__}"
            # traceback = test_info.get_error_info()
            self.stream.writeln(
                f"{t_color}{flavour}{S_RESET}: {test_str}")
            self.stream.writeln(self.separator2)
            self.stream.writeln(
                f"{t_color}{err.splitlines()[-1]}{C_RESET}")
            self.stream.writeln(self.separator2)
            self.stream.writeln(f"{MUTED}{err}{S_RESET}")

    def printTotal(self):
        run = self.testsRun
        s_test = "test"
        if run > 1:
            s_test += "s"
        ran_text = f"{BOLD}Ran {run} {s_test}{S_RESET}"
        full_time_str = format_duration(self.durations['total'])
        self.stream.writeln(
            f"\n{ran_text} in {MAGENTA}{full_time_str}{C_RESET}")

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
