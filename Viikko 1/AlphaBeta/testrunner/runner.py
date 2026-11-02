from unittest import TextTestRunner, TestLoader
from .result import LocalTestResult
from .points import _parse_points, _name_test
from itertools import chain
import json


class LocalTestRunner(TextTestRunner):
    """A local test runner for course exercises.
    """

    resultclass = LocalTestResult

    def __init__(self, *args, **kwargs):
        super(LocalTestRunner, self).__init__(*args, **kwargs)

    def run(self, test):
        print('Running local tests...')
        return super(LocalTestRunner, self).run(test)

    def available_points(self):
        testLoader = TestLoader()
        tests = testLoader.discover('.', 'test*.py', None)
        try:
            tests = list(chain(*chain(*tests._tests)))
        except Exception as error:
            print("Received following Exception:", error)
            tests.debug()

        points = map(_parse_points, tests)
        names = map(_name_test, tests)

        result = dict(zip(names, points))

        with open('.available_points.json', 'w') as f:
            json.dump(result, f, ensure_ascii=False)
