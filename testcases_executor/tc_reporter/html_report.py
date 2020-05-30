import os
from jinja2 import Environment, PackageLoader
from testcases_executor.tc_utils import format_duration, BOLD, MUTED, S_RESET


class HtmlReport():

    def __init__(self, result):
        result.stream.writeln("Generating html report ...\n")
        # load template
        env = Environment(loader=PackageLoader('testcases_executor.tc_reporter'))
        template = env.get_template('report_template.html')
        # dir destination
        dir_reports = './html_reports'
        if not os.path.exists(dir_reports):
            os.makedirs(dir_reports)
        # report_file
        report_path = os.path.join(dir_reports, 'report.html')
        with open(report_path, 'w') as report_file:
            report_file.write(template.render(
                title=f"{os.path.basename(os.getcwd())} Tests Results",
                header=self.get_header(result)))
        result.stream.writeln(
            f"---> {BOLD}{MUTED}{os.path.relpath(report_path)}{S_RESET}\n")

    def get_header(self, result):
        return {
            'start_time': result.start_time.strftime("%Y-%m-%d %H:%M:%S"),
            'duration': format_duration(result.durations['total']),
            'total': result.testsRun, 'status': 'PASSED', 'status_color': 'success',
            'success': 0, 'failures': 0, 'errors': 0, 'skips': 0}
