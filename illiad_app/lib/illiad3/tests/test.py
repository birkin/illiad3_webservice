"""
To test all...
$ python3 ./test.py

To run specific test...
$ python3 ./test/account.py AccountTest.test_logout
"""

import logging, unittest
from . import account_test
from . import parser_test


logger = logging.getLogger(__name__)


ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
logger.addHandler(ch)


def suite():
    test_suite = unittest.TestSuite()
    test_suite.addTest(account_test.suite())
    test_suite.addTest(parser_test.suite())
    return test_suite

runner = unittest.TextTestRunner()
runner.run(suite())
