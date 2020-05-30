import os
from jinja2 import Environment, PackageLoader


class HtmlReport():

    def __init__(self, result):
        # load template
        env = Environment(loader=PackageLoader('testcases_executor.tc_reporter'))
        template = env.get_template('base.html')
        # dir destination
        dir_reports = './html_reports'
        if not os.path.exists(dir_reports):
            os.makedirs(dir_reports)
        # report_file
        report_file = os.path.join(dir_reports, 'report.html')
        with open(report_file, 'w') as fh:
            fh.write(template.render(
                h1="Hello Jinja2", show_one=False, show_two=True,
                names=["Foo", "Bar", "Qux"]))
