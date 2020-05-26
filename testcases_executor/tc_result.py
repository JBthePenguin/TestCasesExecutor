import time
from unittest import TestResult
from testcases_executor.tc_utils import (
    format_duration, GREEN, MAGENTA, C_RESET, BOLD, S_RESET)


class TestCasesResult(TestResult):
    """Override HtmlTestResult to change desription and format duration,
    and get a non alphabetical order for test methods."""
    separator1 = '=' * 70
    separator2 = '-' * 70

    def __init__(self, stream, descriptions, verbosity):
        super().__init__(stream, descriptions, verbosity)
        self.stream = stream
        # self.showAll = verbosity > 1
        # self.dots = verbosity == 1
        self.descriptions = descriptions
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
        super().addError(test, err)
        # if self.showAll:
        self.stream.writeln("ERROR")
        # elif self.dots:
        #    self.stream.write('E')
        self.stream.flush()

    def addFailure(self, test, err):
        super().addFailure(test, err)
        # if self.showAll:
        self.stream.writeln("FAIL")
        #elif self.dots:
        #    self.stream.write('F')
        self.stream.flush()

    def addSkip(self, test, reason):
        super().addSkip(test, reason)
        # if self.showAll:
        self.stream.writeln("skipped {0!r}".format(reason))
        # elif self.dots:
        #    self.stream.write("s")
        self.stream.flush()

    def addExpectedFailure(self, test, err):
        super().addExpectedFailure(test, err)
        # if self.showAll:
        self.stream.writeln("expected failure")
        # elif self.dots:
        # self.stream.write("x")
        self.stream.flush()

    def addUnexpectedSuccess(self, test):
        super().addUnexpectedSuccess(test)
        # if self.showAll:
        self.stream.writeln("unexpected success")
        # elif self.dots:
        self.stream.write("u")
        self.stream.flush()

    def printErrors(self):
        # if self.dots or self.showAll:
        self.stream.writeln()
        self.printErrorList('ERROR', self.errors)
        self.printErrorList('FAIL', self.failures)

    def printErrorList(self, flavour, errors):
        for test, err in errors:
            self.stream.writeln(self.separator1)
            self.stream.writeln(
                "%s: %s" % (flavour, self.getDescription(test)))
            self.stream.writeln(self.separator2)
            self.stream.writeln("%s" % err)

    def printTotal(self):
        run = self.testsRun
        s_test = "test"
        if run > 1:
            s_test += "s"
        ran_text = f"{BOLD}Ran {run} {s_test}{S_RESET}"
        full_time_str = format_duration(self.durations['total'])
        self.stream.writeln(
            f"\n{ran_text} in {MAGENTA}{full_time_str}{C_RESET}")
