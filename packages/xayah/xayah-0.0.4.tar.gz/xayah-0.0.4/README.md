# xayah
A lightweight testing tool with test report functionality

## Table of contents
* [General info](#general-info)
* [Installation](#installation)
* [Features](#Features)
* [Usage](#usage)

## General info
Xayah is used to test and generate report for 
python application.

test suite example:
```
@TestSuite.init
class CheckTestCase:
    @TestCase.title('test case description')
    @TestCase.description('check whether title and description been added to test case')
    def test_test_case(self):
        with Step('check three'):
            assert 3 == 3
        with Step('check four'):
            assert 4 == 3, 'goodbye'
```

## Installation
Xayah is available on PyPI:
```commandline
python -m pip install xayah
```

## Features
* adding title, description, severity levels, etc.
* test parametrization
* steps
* skipping tests
* generating test report

## Usage
In order to generate report, the test class should be
decorated with TestSuite.init method:
```
@TestSuite.init
class CheckTestCase:
    def test_method(self):
        assert 1 == 1
```

then all test method (with test prefix) of the 
tested class can be executed by calling
run_test_cases method:
```
CheckTestCase.run_test_cases()
```

in order to created test result
TestResult().create_test_result() method should
be called:
```
result = TestResult().create_test_result()
```
then test result can be parsed in any format
