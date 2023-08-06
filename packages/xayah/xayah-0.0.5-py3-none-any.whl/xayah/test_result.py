from .test_result_models import TestCaseModel, TestSuiteModel, StepModel, TestClassesModel
from typing import List, Dict


class MetaSingleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(MetaSingleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class TestResult(metaclass=MetaSingleton):
    """
    storing test documentation: test cases, its steps and so on
    and generating test result based on it
    attributes:
    - test classes: list of all classes that been decorated with TestScenario
    - test cases: all test methods of particular class
    - test suites: object of class_name and its methods (test cases)
    - steps: steps of a test case
    """
    def __init__(self):
        self.test_classes = []
        self.test_cases = {}
        self.test_suites = {}
        self.steps = {}

    def __repr__(self):
        return f'''
            test_classes: {self.test_classes}\n 
            test_cases: {self.test_cases}\n 
            test_suites: {self.test_suites}\n 
            steps: {self.steps}
        '''

    def get_test_case(self, name: str) -> TestCaseModel:
        """
        get test case by its name (class_name:method_name)
        :param name: test case name ({class_name}::{method_name})
        :return: TestCaseModel
        """
        return self.test_cases.get(name)

    def add_test_case(self, **kwargs: str or StepModel) -> None:
        class_name = kwargs.get('class_name', "")
        method_name = kwargs.get('method_name', "")
        test_case_name = f'{class_name}::{method_name}'

        test_case = self.test_cases.get(test_case_name)

        kwargs.update({'name': test_case_name})

        if test_case:
            test_case.update(**kwargs)
        else:
            test_case = TestCaseModel(**kwargs)
            self.test_cases[test_case_name] = test_case.dict()

    def add_test_case_old(self, **kwargs: str or StepModel) -> None:
        class_name = kwargs.get('class_name', "")
        method_name = kwargs.get('method_name', "")
        test_name = f'{class_name}::{method_name}'
        steps = kwargs.get('steps')
        if steps is None:
            steps = []
        data = {
            "name": test_name,
            "class_name": class_name,
            "method_name": method_name,
            "status": kwargs.get('status', ""),
            "steps": steps,
            "assertion_message": kwargs.get('assertion_message', ""),
            "description": kwargs.get('description', "")
        }
        test_case = TestCaseModel(**data)
        self.test_cases[test_name] = test_case.dict()

    def add_test_suite(self, **kwargs):
        class_name = kwargs.get('class_name', '')
        test_suite = self.test_suites.get(class_name)

        if test_suite:
            test_suite.update(**kwargs)
        else:
            test_suite = TestSuiteModel(**kwargs)
            self.test_suites[class_name] = test_suite.dict()

    def add_test_classes(self, class_name: str, methods: List[str]) -> None:
        data = {
            "class_name": class_name,
            "method_names": methods
        }
        test_class = TestClassesModel(**data)
        self.test_classes.append(test_class.dict())

    def create_test_result(self) -> Dict[str, TestSuiteModel]:
        for test_class in self.test_classes:
            class_name = test_class.get('class_name', '')
            methods = []
            for method_name in test_class['method_names']:
                name = f'{class_name}::{method_name}'
                test_case = self.test_cases.get(name)
                methods.append(test_case)

            data = {
                "class_name": class_name,
                "test_cases": methods
            }
            self.add_test_suite(**data)

        return self.test_suites

    def add_step(self, **kwargs) -> None:
        method_name = kwargs.get('method_name', '')
        step = StepModel(**kwargs).dict()
        if not self.steps.get(method_name):
            steps = [step]
            self.steps[method_name] = steps
        else:
            self.steps[method_name].append(step)

    def get_steps(self, method_name: str) -> List[StepModel]:
        return self.steps.get(method_name, [])

    def clear_test_result(self) -> None:
        self.test_classes = []
        self.test_cases = {}
        self.test_suites = {}
        self.steps = {}
