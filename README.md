[![Build Status](https://travis-ci.com/JBthePenguin/TestCasesExecutor.svg?branch=master)](https://travis-ci.com/JBthePenguin/TestCasesExecutor) [![Codacy Badge](https://api.codacy.com/project/badge/Grade/3a8b61108c5c4b6188ffa3396433ced9)](https://www.codacy.com/manual/JBthePenguin/TestCasesExecutor?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=JBthePenguin/TestCasesExecutor&amp;utm_campaign=Badge_Grade) ![GitHub top language](https://img.shields.io/github/languages/top/JBthePenguin/TestCasesExecutor) ![GitHub repo size](https://img.shields.io/github/repo-size/JBthePenguin/TestCasesExecutor) [![python](https://img.shields.io/badge/python-3.8-yellow.svg)](https://www.python.org/downloads/) [![License: GPL v3](https://img.shields.io/badge/License-GPLv3-black.svg)](https://www.gnu.org/licenses/gpl-3.0)
# TestCasesExecutor
Execute configured groups of TestCases (subclasses of [unittest.TestCase](https://docs.python.org/3.8/library/unittest.html#unittest.TestCase)), display human readable result in terminal, ordered by group and testcase, and generate a html file report.

## Install
```sh
$ pip install testcases_executor
```
This also install [Jinja2](https://palletsprojects.com/p/jinja/) used to generate html report.

## Config
![Structure example](https://raw.githubusercontent.com/JBthePenguin/TestCasesExecutor/master/screenshots/structure.png)

Create a file named ***testcases.py*** in the root directory of your project.  
Inside it, import yours *TestCases* and make a list (or tuple) named **groups** that is made up of tuples, each representing a *group*. For example:
``` python
from your_app.test_script import TCaseOne, TCaseTwo, TCaseThree, TCaseFour
groups = [  # or (
    ('Group one', 'one', [TCaseThree, TCaseTwo]),  # or (TCaseThree, TCaseTwo)),
    ('Group two', 'two', [TCaseOne, TCaseFour]),  # or (TCaseOne, TCaseFour)),
]  # or )
```

### Constraints
*   **groups** must be a *list* or a *tuple*.

*   **groups's item** (group's representation) must be a *tuple*.

*   **each tuple** must contain *3 items*:
    *   **group's name** must be a *string*.
    *   **argument's name** used to run all group's testcases *string without space*.
    *   **[unittest.TestCase](https://docs.python.org/3.8/library/unittest.html#unittest.TestCase) subclasses** must be a *list* or a *tuple*.

*   **group and argument names**, **[unittest.TestCase](https://docs.python.org/3.8/library/unittest.html#unittest.TestCase) subclass** must *used once*.

## Usage
```sh
$ python -m testcases_executor
```
This run **all tests**, display **result in terminal** before generate, in the root directory, the **html report file** named *tc_executor_report.html*. It's possible to customize the command with following availabe arguments.
### Available arguments
*   Options
    *   **-h, --help**: *display help message.*
    *   **-o, --open**: *open html report in browser after test.*

*   Tests selection
    *   **-group_argument_name**: run all *group's testcases's tests*.
    *   **-TestCaseName**:(without parameter) run all *testcase's tests*.
    *   **-TestCaseName**:(with test's names in parameter) run *desired tests*.

Some examples:
```sh
$ python -m testcases_executor -two
$ python -m testcases_executor -one -TCaseFour -o
$ python -m testcases_executor -TCaseTwo test_one -TCaseOne test_three
...
```

## Result's screenshots
### Terminal
![Terminal group one](https://raw.githubusercontent.com/JBthePenguin/TestCasesExecutor/master/screenshots/terminal_one.png)
![Terminal group two](https://raw.githubusercontent.com/JBthePenguin/TestCasesExecutor/master/screenshots/terminal_two.png)
![Terminal errors](https://raw.githubusercontent.com/JBthePenguin/TestCasesExecutor/master/screenshots/terminal_three.png)
### Html Report
It use [Bootstrap4](https://getbootstrap.com/), [jQuery](https://jquery.com/) and [Fontawesome icons](https://fontawesome.com/v4.7.0/icons/) (via [stackpath cdn](https://www.stackpath.com/open-source/)).

![Html report](https://raw.githubusercontent.com/JBthePenguin/TestCasesExecutor/master/screenshots/html_report.png)

*Click on table's lines to see tests's infos.*

![Html errors](https://raw.githubusercontent.com/JBthePenguin/TestCasesExecutor/master/screenshots/html_errors.png)

## Test
For the same reasons that meeting your future self would cause a spacio temporal shock, testing a tester using this same tester would cause a spacio testorial shock. So above all, don't.  
Run **testcases_executor.tests**, using [unittest](https://docs.python.org/3.8/library/unittest.html#module-unittest):
```sh
$ python -m unittest testcases_executor.tests -v
```
:+1: *[HtmlTestRunner](https://github.com/oldani/HtmlTestRunner) was a great inspiration, so thank you for that.*
