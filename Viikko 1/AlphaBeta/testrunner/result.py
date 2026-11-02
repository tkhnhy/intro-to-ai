from unittest.runner import TextTestResult
from .points import _parse_points, _name_test
import atexit
import json
import traceback

results = []


class LocalTestResult(TextTestResult):

    def __init__(self, stream, descriptions, verbosity):
        super(LocalTestResult, self).__init__(stream, descriptions, verbosity)

    def startTest(self, test):
        super(LocalTestResult, self).startTest(test)

    def addSuccess(self, test):
        super(LocalTestResult, self).addSuccess(test)
        self.addResult(test, 'passed')

    def addFailure(self, test, err):
        super(LocalTestResult, self).addFailure(test, err)
        self.addResult(test, 'failed', err)

    def addError(self, test, err):
        super(LocalTestResult, self).addError(test, err)
        self.addResult(test, 'errored', err)

    def addResult(self, test, status, err=None):
        points = _parse_points(test)
        message = ""
        backtrace = []
        if err is not None:
            message = str(err[1])
            backtrace = traceback.format_tb(err[2])

        details = {
            'name': _name_test(test),
            'status': status,
            'message': message,
            'passed': status == 'passed',
            'points': points,
            'backtrace': backtrace
        }
        results.append(details)

    # writes machine-readable results for local tooling
    @atexit.register
    def write_output():
        with open('.test_results.json', 'w', encoding='utf8') as f:
            json.dump(results, f, ensure_ascii=False)
