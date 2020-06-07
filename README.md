[![Build Status](https://travis-ci.com/JBthePenguin/TestCasesExecutor.svg?branch=master)](https://travis-ci.com/JBthePenguin/TestCasesExecutor) [![Codacy Badge](https://api.codacy.com/project/badge/Grade/3a8b61108c5c4b6188ffa3396433ced9)](https://www.codacy.com/manual/JBthePenguin/TestCasesExecutor?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=JBthePenguin/TestCasesExecutor&amp;utm_campaign=Badge_Grade) ![GitHub top language](https://img.shields.io/github/languages/top/JBthePenguin/TestCasesExecutor) ![GitHub repo size](https://img.shields.io/github/repo-size/JBthePenguin/TestCasesExecutor) [![python](https://img.shields.io/badge/python-3.7.5-yellow.svg)](https://www.python.org/downloads/) [![License: GPL v3](https://img.shields.io/badge/License-GPLv3-black.svg)](https://www.gnu.org/licenses/gpl-3.0)
##  TestCasesExecutor :exclamation::exclamation::exclamation:***IN PROGRESS***:exclamation::exclamation::exclamation:

Execute TestCases ordered by group (configuring before), display human readable result in cli and generate a html file report.

### Install
```sh
$ pip install git+https://github.com/JBthePenguin/TestCasesExecutor.git
```
This also install [Jinja2](https://palletsprojects.com/p/jinja/) used to generate html report.

### Config
-  Create a file *testcases.py* in root directory of your project
-  Inside, import yours TestCases and make a list (or a tuple) named *groups*.
``` python
from your_app.test_script.py import TCaseOne, TCaseTwo, TCaseThree, TCaseFour
groups = [  # or (
    ('Group one', 'one', [TCaseThree, TCaseTwo]),  # or (TCaseThree, TCaseTwo)),
    ('Group two', 'two', [TCaseOne, TCaseFour]),  # or (TCaseOne, TCaseFour)),
]  # or )
```
groups's item must be a tuple with 3 items: group's name (str), argument's name used to run all group's testcases (str), unittest.TestCase subclasses (list or tuple).

### Usage
-  python -m testcases_executor
-  with custom groups of TestCase

### Tests
```sh
$ python -m unittest testcases_executor.tests -v
```
