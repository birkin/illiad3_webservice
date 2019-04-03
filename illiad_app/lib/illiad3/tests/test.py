# """
# To run all module-tests directly...
# $ python3 ./test.py

# To run all module-tests from django...
# $ python3 ./manage.py test

# To run specific test directly...
# $ python3 ./test/account.py AccountTest.test_login

# To run specific test from django...
# $ python3 ./manage.py test illiad_app.lib.illiad3.tests.account_test.AccountTest.test_login
# """

# import logging, unittest
# from . import account_test
# from . import parser_test


# logger = logging.getLogger(__name__)


# ch = logging.StreamHandler()
# ch.setLevel(logging.DEBUG)
# logger.addHandler(ch)


# def suite():
#     test_suite = unittest.TestSuite()
#     test_suite.addTest(account_test.suite())
#     test_suite.addTest(parser_test.suite())
#     return test_suite

# runner = unittest.TextTestRunner()
# runner.run(suite())
