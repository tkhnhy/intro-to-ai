from unittest import TestProgram
from .runner import LocalTestRunner
import sys


if sys.argv.__len__() > 1 and sys.argv[1] == 'available_points':
    LocalTestRunner().available_points()
    sys.exit()

main = TestProgram
main(testRunner=LocalTestRunner, module=None, failfast=False, buffer=True)
