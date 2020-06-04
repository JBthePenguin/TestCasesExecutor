"""
Module testcases_executor.tests.test_tc_reporter.test_html_report .

Contain TestCase for testcases_executor.tc_reporter.html_report .

unittest.TestCase sublass:
    TestTestCasesHtmlReport

Imports:
    from unittest: TestCase
    from unittest.mock: patch, Mock, mock_open, call
    from testcases_executor.tc_reporter.html_report: TestCasesHtmlReport
"""
from unittest import TestCase
from unittest.mock import patch, Mock, mock_open, call
from testcases_executor.tc_reporter.html_report import TestCasesHtmlReport


class TestTestCasesHtmlReport(TestCase):
    """
    A subclass of unittest.TestCase .

    Tests for tc_reporter.html_reports. TestCasesHtmlReport .

    Methods
    ----------
    test_init_html_report():
        Assert TestCasesHtmlReport object is initialized with good attributes.
    """

    @patch("testcases_executor.tc_reporter.html_report.Environment")
    @patch("testcases_executor.tc_reporter.html_report.PackageLoader")
    @patch("testcases_executor.tc_reporter.html_report.path")
    @patch("testcases_executor.tc_reporter.html_report.makedirs")
    @patch("testcases_executor.tc_reporter.html_report.getcwd")
    @patch("testcases_executor.tc_reporter.html_report.ContextReport")
    def test_init_html_report(
            self, mock_context, mock_getcwd, mock_makedirs,
            mock_path, mock_loader, mock_env):
        """
        Assert TestCasesHtmlReport object is initialized with good attributes.

        Parameters:
        ----------
        mock_context : Mock
            Mock of ContextReport .
        mock_getcwd : Mock
            Mock of os.getcwd .
        mock_makedirs : Mock
            Mock of os.makedirs .
        mock_path : Mock
            Mock of os.path .
        mock_loader : Mock
            Mock of jinja2.PackageLoader .
        mock_env : Mock
            Mock of jinja2.Environment .

        Assertions:
        ----------
        assertEqual:
            Assert stream.writeln number of calls.
        assert_has_calls:
            Assert stream.write calls parameters.
        assert_called_once_with:
            Assert env, loader, env.get_template, context, path.basename,
            getcwd, path.join, open, open.write, template.render, makedirs,
            called once with parameter.
        assert_not_called:
            Assert makedirs not called if assert_not_called is True.

        """
        m = mock_open()  # make necessary mocks, set necessary return values
        result, obj_env, report_template = Mock(), Mock(), Mock()
        report_template.render.return_value = "template render"
        obj_env.get_template.return_value = report_template
        mock_path.exists.return_value = True
        mock_path.join.return_value = 'path'
        mock_path.relpath.return_value = 'relpath'
        mock_path.basename.return_value = 'basename'
        mock_getcwd.return_value = 'getcwd'
        mock_env.return_value = obj_env
        mock_loader.return_value = 'Loader'
        with patch('builtins.open', m):  # with mock open
            TestCasesHtmlReport(result)  # init obj and make all assertions
            self.assertEqual(result.stream.writeln.call_count, 2)
            result.stream.writeln.assert_has_calls([
                call("Generating html report ...\n"),
                call('---> \x1b[1m\x1b[2mrelpath\x1b[0m\n')])
            mock_env.assert_called_once_with(loader='Loader')
            mock_loader.assert_called_once_with(
                'testcases_executor.tc_reporter')
            obj_env.get_template.assert_called_once_with(
                'report_template.html')
            mock_makedirs.assert_not_called()
            mock_context.assert_called_once_with('basename', result)
            mock_path.basename.assert_called_once_with('getcwd')
            mock_getcwd.assert_called_once_with()
            mock_path.join.assert_called_once_with(
                './html_reports', 'report.html')
            m.assert_called_once_with('path', 'w')
            m().write.assert_called_once_with("template render")
            report_template.render.assert_called_once_with(
                title=mock_context().title, header=mock_context().header,
                groups=mock_context().groups)
            mock_path.exists.return_value = False  # path.exists: False
            TestCasesHtmlReport(result)
            mock_makedirs.assert_called_once_with('./html_reports')
