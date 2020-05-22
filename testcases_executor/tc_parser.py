"""
Module testcases_executor.tc_parser

Contain necessary classes to make a parser for groups of TestCases.

Classes:
    HelpFormatterTestCases
    TestCasesParser

Imports:
    from argparse import ArgumentParser, HelpFormatter
    from testcases_executor.tc_utils: MUTED, BOLD, S_RESET
"""
from argparse import ArgumentParser, HelpFormatter
from testcases_executor.tc_utils import MUTED, BOLD, S_RESET


class HelpFormatterTestCases(HelpFormatter):
    """
    A subclass of argparse.HelpFormatter .

    Use to format help message with color and style.

    Methods
    ----------
    add_usage():
        Override original one to change a prefix.
    _format_args():
        Override original one to change how to display nargs.
    _join_parts():
        Override original one to add space between args.
    """

    def __init__(self, **kwargs):
        """
        Change prog and max_help_position before init HelpFormatter.

        Parameters
        ----------
            **kwargs : prog, indent_increment, max_help_position, width
                default kwargs passed to costruct HelpFormatter
        """
        kwargs['prog'] = f"{MUTED}python -m testcases_executor{S_RESET}"
        kwargs['max_help_position'] = 5
        super().__init__(**kwargs)

    def add_usage(self, usage, actions, groups, prefix=None):
        """
        Override original one to change prefix.

        Parameters
        ----------
            usage, actions, groups:
                default args passed.
            prefix : str (default: None)
                used in usage as title.

        Return
        ----------
            result of original add_usage() with prefix changed.
        """
        return super(HelpFormatterTestCases, self).add_usage(
            usage, actions, groups, f'{BOLD}Usage: ')

    def _format_args(self, action, default_metavar):
        """
        Override original one to change how to display nargs.

        Parameters
        ----------
            action, default_metavar:
                default args passed.

        Return
        ----------
            string to represent nargs.
        """
        return f"{MUTED}...{S_RESET}"

    def _join_parts(self, part_strings):
        """
        Override original one to add in string style and space between args.

        Parameters
        ----------
            part_strings : list of str
                default list of part string.

        Return
        ----------
            string constructed with the new part string.
        """
        if part_strings:
            part_strings[0] = (
                f"\n{BOLD}{part_strings[0]}{S_RESET}")
        return ''.join([
            part for part in part_strings if part and part != '==SUPPRESS=='])


class TestCasesParser(ArgumentParser):
    """
    A subclass of argparse.ArgumentParser .

    A custom ArgumentParser for groups of TestCases.

    Attributes
    ----------
    tc_groups : TestCasesGroups
        list with instances of TestCasesGroup for items.

    Methods
    ----------
    add_args_options:
        Add default options arguments.
    add_args_groups:
        Add groups of arguments for each TestCasesGroup.
    """

    def __init__(self, tc_groups):
        """
        Set attribute, init Parser with parameters and call add_args methods.

        Parameters
        ----------
            tc_groups : TestCasesGroups
                list with instances of TestCasesGroup for items.
        """
        self.tc_groups = tc_groups
        super().__init__(
            formatter_class=HelpFormatterTestCases, description=''.join([
                'Without argument to run all tests, or with optionnal ',
                'one(s) without option to run group or TestCase tests, or ',
                'with method names in options to a TestCase arg to run ',
                'specific test methods.']),
            epilog=f"{BOLD}", allow_abbrev=False)
        self.add_args_options()
        # self.make_args_groups()  # groups
        # self.parse_and_run()  # check args and run the corresponding tests
        # self.parse_args()

    def add_args_options(self):
        """
        Add default options arguments.
        """
        self._optionals.title = f"{BOLD}Options"  # title for options
        self.add_argument(  # arg to timestamp in html file name
            "-t", "--timestamp", action='store_true',
            help="Add timestamp in html report file name.")
        self.add_argument(  # arg to open report diretly in browser
            "-o", "--open", action='store_true',
            help="Open report in browser after tests.")

    def make_args_groups(self):
        """ For each group of testcases, set help msg's title with his name,
        add optionna argument with his name to run all his testases,
        for each of them, add option argument with his name and for each test,
        add optionnal parameter with his name."""
        for group_name, testcases in self.tc_groups:  # group
            group = self.add_argument_group(
                f"{BOLD}{group_name.title()}")
            if " " in group_name:  # name contain space
                group_name.replace(" ", "_")
            group.add_argument(  # arg group name to run all group's testcases
                f"-{group_name}", action='store_true',
                help=f"Run all {group_name.lower()} TestCases.")
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
