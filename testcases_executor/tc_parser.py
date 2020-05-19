from argparse import ArgumentParser, HelpFormatter
from colorama import Style


class HelpFormatterTestCases(HelpFormatter):
    """A help formatter for TestCasesParser subclass argparse.HelpFormatter."""

    def __init__(self, prog, **kwargs):
        """Override init to change prog used in usage message."""
        prog = f"{Style.DIM}python -m testcases_executor{Style.NORMAL}"
        super().__init__(
            prog, indent_increment=2,
            max_help_position=5,
            width=None)

    def add_usage(self, usage, actions, groups, prefix=None):
        """Override add_usage to change prefix used in usage message."""
        return super(HelpFormatterTestCases, self).add_usage(
            usage, actions, groups,
            f'{Style.BRIGHT}Usage: ')

    def _format_args(self, action, default_metavar):
        """Override _format_args to change how to display nargs."""
        return f"{Style.DIM}...{Style.NORMAL}"

    def _join_parts(self, part_strings):
        """Override _join_parts to add space between each arg."""
        if part_strings:
            part_strings[0] = (
                f"\n{Style.BRIGHT}{part_strings[0]}{Style.NORMAL}")
        return ''.join([
            part for part in part_strings if part and part != '==SUPPRESS=='])


class TestCasesParser(ArgumentParser):
    """An Argument Parser for groups of TestCases."""

    def __init__(self, tc_groups):
        """Set properties tc_groups with the list groups of testcases.
        Init ArgumentParser with formatter class, description,
        epilog and allow_abbrev to False, set help message's title for options.
        Make groups of arguments, parse args and run the corresponding tests.
        ***tc_groups -> [('group_name', [TestCase1, ...]), (..)].***"""
        self.tc_groups = tc_groups
        super().__init__(  # init ArgumentParser
            formatter_class=HelpFormatterTestCases,
            description=''.join([
                'Without argument to run all tests, or with optionnal ',
                'one(s) without option to run group or TestCase tests, or ',
                'with method names in options to a TestCase arg to run ',
                'specific test methods.']),
            epilog=f"{Style.BRIGHT}", allow_abbrev=False)
        self._optionals.title = f"{Style.BRIGHT}Options"  # title for options
        self.add_argument(  # arg to open report diretly in browser
            "-t", "--timestamp", action='store_true',
            help="Add timestamp in report file name.")
        self.add_argument(  # arg to open report diretly in browser
            "-o", "--open", action='store_true',
            help="Open report in browser after tests.")
        self.make_arg_groups()  # groups
        # self.parse_and_run()  # check args and run the corresponding tests
        # self.parse_args()

    def make_arg_groups(self):
        """ For each group of testcases, set help msg's title with his name,
        add optionna argument with his name to run all his testases,
        for each of them, add option argument with his name and for each test,
        add optionnal parameter with his name."""
        for group_name, testcases in self.tc_groups:  # group
            group = self.add_argument_group(
                f"{Style.BRIGHT}{group_name.title()}")
            group.add_argument(  # arg group name to run all group's testcases
                f"-{group_name}", action='store_true',
                help=f"Run all {group_name} TestCases.")
            for tc in testcases:
                t_names = [n for n in tc.__dict__.keys() if n[:5] == 'test_']
                group.add_argument(  # arg with testcase's name
                    f"-{tc.__name__}", help=f"{' '.join(t_names)}",
                    nargs='*', choices=t_names)  # tests's names for params

    # def parse_and_run(self):
    #     """Check args, set a list and append to it corresponding tests cases,
    #     before run it."""
    #     all_test_cases = []
    #     args = self.parse_args()
    #     if (len(sys.argv) == 1) or (
    #             (len(sys.argv) == 2) and (args.open or args.timestamp)) or (
    #                 (len(sys.argv) == 3) and args.open and args.timestamp):
    #         all_test_cases += self.all_tests  # no arg or open -> all tests
    #     else:
    #         args_dict = vars(args)
    #         for group_name, test_cases in self.tests_groups:
    #             if args_dict[group_name]:  # group's name arg -> group tests
    #                 all_test_cases += test_cases
    #         for test_case in self.all_tests:
    #             # t_case_name = test_case.__name__
    #             options = args_dict[test_case.__name__]
    #             if isinstance(options, list):  # test case's name arg
    #                 if not options:  # no param -> test case's tests
    #                     all_test_cases.append(test_case)
    #                 else:  # method name(s) param -> methods's tests
    #                     all_test_cases.append((test_case, options))
    #     TestCaseRunner(all_test_cases, args.timestamp, args.open).run()
