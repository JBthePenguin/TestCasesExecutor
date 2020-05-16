[![Build Status](https://travis-ci.com/JBthePenguin/TestCasesExecutor.svg?branch=master)](https://travis-ci.com/JBthePenguin/TestCasesExecutor)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/3a8b61108c5c4b6188ffa3396433ced9)](https://www.codacy.com/manual/JBthePenguin/TestCasesExecutor?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=JBthePenguin/TestCasesExecutor&amp;utm_campaign=Badge_Grade)
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-black.svg)](https://www.gnu.org/licenses/gpl-3.0)
![GitHub top language](https://img.shields.io/github/languages/top/JBthePenguin/TestCasesExecutor)
[![python](https://img.shields.io/badge/python-3.7.5-yellow.svg)](https://www.python.org/downloads/) ![GitHub repo size](https://img.shields.io/github/repo-size/JBthePenguin/TestCasesExecutor)
##  TestCasesExecutor :exclamation::exclamation::exclamation:***IN PROGRESS***:exclamation::exclamation::exclamation:

Desription...

### Install
-  pip install ....
-  clone requirements...

### Usage
-  Create a file *testcases.py* in root directory of your project
-  In it, import yours TestCases and make a list groups
``` python
from somewhere import TestCase1, TestCase2, TestCase3, TestCase4
groups = [('Foo', [TestCase1, TestCase3]), ('Bar', [TestCase2, TestCase4]), ...]  
```
-  python -m testcases_executor
-  with custom groups of TestCase
