import inspect
from src.xayah.test_result import TestResult
import time


class Check:
    def __init__(self, name):
        self.name = name
        self.method_name = inspect.stack()[1][3]
        self.assertion_instance = AssertionError('test')
        self.start_time = 0.0
        self.end_time = 0.0
        self.execution_time = 0.0

    def __enter__(self):
        self.start_time = time.time()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.end_time = time.time()
        self.execution_time = (self.end_time - self.start_time) * 1000
        message = ''
        if exc_val:
            message = str(exc_val)
        if type(self.assertion_instance) == exc_type:
            TestResult().add_step(
                name=self.name,
                method_name=self.method_name,
                message=message,
                category='check',
                status='failed',
                start_time=self.start_time,
                end_time=self.end_time,
                execution_time=self.execution_time
            )
        else:
            TestResult().add_step(
                name=self.name,
                method_name=self.method_name,
                message=message,
                category='check',
                status='passed',
                start_time=self.start_time,
                end_time=self.end_time,
                execution_time=self.execution_time
            )
        return True
