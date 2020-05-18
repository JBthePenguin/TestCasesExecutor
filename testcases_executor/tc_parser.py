from argparse import ArgumentParser, HelpFormatter


class HelpFormatterTestCases(HelpFormatter):
    """A help formatter for TestCasesParser subclass argparse.HelpFormatter."""

    def __init__(self, prog, **kwargs):
        """Override init to change prog used in usage message."""
        prog = "python -m testcases_executor"
        super().__init__(prog, **kwargs)

    def add_usage(self, usage, actions, groups, prefix=None):
        """Override add_usage to change prefix used in usage message."""
        return super(HelpFormatterTestCases, self).add_usage(
            usage, actions, groups, '---\n\nUsage: ')

    def _format_args(self, action, default_metavar):
        """Override _format_args to change how to display nargs."""
        return "options:tests_names"

    def _join_parts(self, part_strings):
        """Override _join_parts to add space between each arg."""
        if part_strings:
            part_strings[0] = "\n" + part_strings[0]
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
                'with method names in options to a TestCase arg to run',
                'specific test methods.']),
            epilog="---", allow_abbrev=False)
        self._optionals.title = 'Options'  # help msg title for options
        self.add_argument(  # arg to open report diretly in browser
            "-t", "--timestamp", action='store_true',
            help="Add timestamp in report file name.")
        self.add_argument(  # arg to open report diretly in browser
            "-o", "--open", action='store_true',
            help="Open report in browser directly after tests.")
        self.make_arg_groups()  # groups
        # self.parse_and_run()  # check args and run the corresponding tests
        self.parse_args()

    def make_arg_groups(self):
        """ For each group of testcases, set help msg's title with his name,
        add argument with his name to run all his testases,
        for each of them, add argument with his name and for each test,
        add optionnal parameter with his name."""
        for group_name, testcases in self.tc_groups:  # group
            group = self.add_argument_group(f"{group_name.title()}")
            group.add_argument(  # arg group name to run all group's testcases
                f"-{group_name}", action='store_true',
                help=f"Run all {group_name} TestCases.")
            for tc in testcases:
                t_names = [n for n in tc.__dict__.keys() if n[:5] == 'test_']
                group.add_argument(  # arg with testcase's name
                    f"-{tc.__name__}", help=f"{' '.join(t_names)}",
                    nargs='*', choices=t_names)  # tests's names for params
