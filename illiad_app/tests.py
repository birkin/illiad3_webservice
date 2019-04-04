# -*- coding: utf-8 -*-

import base64, json, random
from . import settings_app
from django.test import Client, TestCase


class ClientCloudCreateUser_Test( TestCase ):
    """ Tests views.cloud_create_user() """

    # def test_create_user__good_data(self):
    #     """ Checks successful new-user creation.
    #         NOTE: will really create new-user, so this test will likely be disabled. """
    #     c = Client()
    #     params = {
    #         'auth_key': settings_app.API_KEY,  # brown internal api
    #         'auth_id': '%s%s' % ( 'zzzz', random.randint(1111, 9999) ),
    #         # 'auth_id': settings_app.TEST_UNREGISTERED_USERNAME,
    #         'department': 'test-department',
    #         'email': 'test@test.edu',
    #         'first_name': 'test-first-name',
    #         'last_name': 'test-last-name',
    #         'phone': 'unavailable',
    #         'status': 'test-status'  # really 'type', eg 'Undergraduate Student'
    #         }
    #     response = c.post( '/cloud_create_user/', params )
    #     self.assertEqual( 200, response.status_code )
    #     jdct = json.loads( response.content )
    #     self.assertEqual( ['request', 'response'], sorted(list(jdct.keys())) )
    #     self.assertEqual( ['params', 'timestamp', 'url'], sorted(list(jdct['request'].keys())) )
    #     self.assertEqual( ['elapsed_time', 'raw_data', 'status_data'], sorted(list(jdct['response'].keys())) )
    #     self.assertEqual( {'status': 'Registered', 'status_code': 200}, jdct['response']['status_data'] )
    #     self.assertEqual( params['auth_id'], jdct['response']['raw_data']['UserName'] )

    def test_create_user__already_exists(self):
        """ Checks handling when user already exists. """
        c = Client()
        params = {
            'auth_key': settings_app.API_KEY,  # brown internal api
            'auth_id': settings_app.TEST_EXISTING_GOOD_USER,
            'department': 'test-department',
            'email': 'test@test.edu',
            'first_name': 'test-first-name',
            'last_name': 'test-last-name',
            'phone': 'unavailable',
            'status': 'test-status'  # really 'type', eg 'Undergraduate Student'
            }
        response = c.post( '/cloud_create_user/', params )
        self.assertEqual( 200, response.status_code )
        jdct = json.loads( response.content )
        self.assertEqual( ['request', 'response'], sorted(list(jdct.keys())) )
        self.assertEqual( ['params', 'timestamp', 'url'], sorted(list(jdct['request'].keys())) )
        self.assertEqual( ['elapsed_time', 'raw_data', 'status_data'], sorted(list(jdct['response'].keys())) )
        self.assertEqual( {'status': 'Failure', 'status_code': 400}, jdct['response']['status_data'] )  # see log for 'raw_data' response.

    ## end class ClientCloudCreateUser_Test()


# class ClientCreateUser_Test( TestCase ):
#     """ Tests views.create_user() """

#     def test_create_user__good_data(self):
#         """ Checks good data. """
#         c = Client()
#         params = {
#             'auth_key': settings_app.API_KEY,  # brown internal api
#             # 'auth_id': '%s%s' % ( 'zzzz', random.randint(1111, 9999) ),
#             'auth_id': settings_app.TEST_UNREGISTERED_USERNAME,  # functionally the line above is more accurate, but this is fine for regular automated tests.
#             'first_name': 'the-first-name',
#             'last_name': 'the-last-name',
#             'email': 'bar'
#             }
#         response = c.post( '/create_user/', params )
#         self.assertEqual( 200, response.status_code )
#         jdct = json.loads( response.content )
#         self.assertEqual( ['request', 'response'], sorted(list(jdct.keys())) )
#         self.assertEqual( ['params', 'timestamp', 'url'], sorted(list(jdct['request'].keys())) )
#         self.assertEqual( ['elapsed_time', 'status_data'], sorted(list(jdct['response'].keys())) )
#         self.assertEqual( {'status': 'Registered', 'status_code': 200}, jdct['response']['status_data'] )

#     def test_create_user__bad_data(self):
#         """ Checks bad data. """
#         c = Client()
#         response = c.post( '/create_user/', {'aa': 'foo_a', 'bb': 'foo_b'} )
#         self.assertEqual( 400, response.status_code )

#     def test_create_user__missing_data(self):
#         """ Checks missing data. """
#         c = Client()
#         params = {
#             'auth_key': settings_app.API_KEY,  # brown internal api
#             'auth_id': settings_app.TEST_UNREGISTERED_USERNAME,
#             # 'first_name': 'the-first-name',  # first_name is required
#             'last_name': 'the-last-name',
#             'email': 'bar'
#             }
#         response = c.post( '/create_user/', params )
#         self.assertEqual( 400, response.status_code )

#     ## end class ClientCreateUser_Test()


# class ClientCheckUser_Test( TestCase ):
#     """ Tests views.check_user() -- for status meaning `blocked`, `registered`, etc. """

#     def test_check_good_existing_user(self):
#         """ Checks happy path. """
#         b64_bytes = base64.b64encode( b'%s:%s' % (settings_app.BASIC_AUTH_USER.encode('utf-8'), settings_app.BASIC_AUTH_PASSWORD.encode('utf-8')) )
#         headers = {
#             'HTTP_AUTHORIZATION': 'Basic ' + b64_bytes.decode('utf-8'),
#             'User-Agent': 'bul-test-client' }
#         c = Client()
#         response = c.get( '/check_user/', {'user': settings_app.TEST_EXISTING_GOOD_USER}, **headers )
#         self.assertEqual( 200, response.status_code )
#         jdct = json.loads( response.content )
#         self.assertEqual( ['request', 'response'], sorted(list(jdct.keys())) )
#         self.assertEqual(
#             {'authenticated': True, 'blocked': None, 'disavowed': None, 'registered': True, 'interpreted_new_user': False},
#             jdct['response']['status_data']
#             )

#     def test_check_disavowed_user(self):
#         """ Checks disavowed user. """
#         b64_bytes = base64.b64encode( b'%s:%s' % (settings_app.BASIC_AUTH_USER.encode('utf-8'), settings_app.BASIC_AUTH_PASSWORD.encode('utf-8')) )
#         headers = {
#             'HTTP_AUTHORIZATION': 'Basic ' + b64_bytes.decode('utf-8'),
#             'User-Agent': 'bul-test-client' }
#         c = Client()
#         response = c.get( '/check_user/', {'user': settings_app.TEST_DISAVOWED_USERNAME}, **headers )
#         self.assertEqual( 200, response.status_code )
#         jdct = json.loads( response.content )
#         self.assertEqual( ['request', 'response'], sorted(list(jdct.keys())) )
#         self.assertEqual(
#             {'authenticated': False, 'blocked': None, 'disavowed': True, 'registered': None, 'interpreted_new_user': False},
#             jdct['response']['status_data']
#             )

#     def test_check_blocked_user(self):
#         """ Checks blocked user. """
#         b64_bytes = base64.b64encode( b'%s:%s' % (settings_app.BASIC_AUTH_USER.encode('utf-8'), settings_app.BASIC_AUTH_PASSWORD.encode('utf-8')) )
#         headers = {
#             'HTTP_AUTHORIZATION': 'Basic ' + b64_bytes.decode('utf-8'),
#             'User-Agent': 'bul-test-client' }
#         c = Client()
#         response = c.get( '/check_user/', {'user': settings_app.TEST_BLOCKED_USERNAME}, **headers )
#         self.assertEqual( 200, response.status_code )
#         jdct = json.loads( response.content )
#         self.assertEqual( ['request', 'response'], sorted(list(jdct.keys())) )
#         self.assertEqual(
#             {'authenticated': True, 'blocked': True, 'disavowed': None, 'registered': True, 'interpreted_new_user': False},
#             jdct['response']['status_data']
#             )

#     # def test_check_unregistered_user(self):
#     #     """ Checks unregistered user.
#     #         NOTE: any user 'new' to illiad is entered into the database and looks like this user.
#     #               ...meaning that this test WILL CREATE A NEW USER """
#     #     b64_bytes = base64.b64encode( b'%s:%s' % (settings_app.BASIC_AUTH_USER.encode('utf-8'), settings_app.BASIC_AUTH_PASSWORD.encode('utf-8')) )
#     #     headers = {
#     #         'HTTP_AUTHORIZATION': 'Basic ' + b64_bytes.decode('utf-8'),
#     #         'User-Agent': 'bul-test-client' }
#     #     c = Client()
#     #     # response = c.get( '/check_user/', {'user': settings_app.TEST_UNREGISTERED_USERNAME}, **headers )
#     #     response = c.get( '/check_user/', {'user': '%s%s' % ( 'zzzz', random.randint(1111, 9999) )}, **headers )
#     #     self.assertEqual( 200, response.status_code )
#     #     jdct = json.loads( response.content )
#     #     self.assertEqual( ['request', 'response'], sorted(list(jdct.keys())) )
#     #     self.assertEqual(
#     #         {'authenticated': True, 'blocked': None, 'disavowed': None, 'registered': False, 'interpreted_new_user': True},
#     #         jdct['response']['status_data']
#     #         )

#     ## end class ClientCheckUser_Test()


class ClientCloudCheckUser_Test( TestCase ):
    """ Tests views.check_user() -- for status meaning `blocked`, `registered`, etc. """

    def test_check_good_existing_user(self):
        """ Checks happy path. """
        b64_bytes = base64.b64encode( b'%s:%s' % (settings_app.BASIC_AUTH_USER.encode('utf-8'), settings_app.BASIC_AUTH_PASSWORD.encode('utf-8')) )
        headers = {
            'HTTP_AUTHORIZATION': 'Basic ' + b64_bytes.decode('utf-8'),
            'User-Agent': 'bul-test-client' }
        c = Client()
        response = c.get( '/cloud_check_user/', {'user': settings_app.TEST_EXISTING_GOOD_USER}, **headers )
        self.assertEqual( 200, response.status_code )
        jdct = json.loads( response.content )
        self.assertEqual( ['request', 'response'], sorted(list(jdct.keys())) )
        self.assertEqual(
            {'authenticated': True, 'blocked': None, 'disavowed': None, 'registered': True, 'interpreted_new_user': False},
            jdct['response']['status_data']
            )

    def test_check_disavowed_user(self):
        """ Checks disavowed user. """
        b64_bytes = base64.b64encode( b'%s:%s' % (settings_app.BASIC_AUTH_USER.encode('utf-8'), settings_app.BASIC_AUTH_PASSWORD.encode('utf-8')) )
        headers = {
            'HTTP_AUTHORIZATION': 'Basic ' + b64_bytes.decode('utf-8'),
            'User-Agent': 'bul-test-client' }
        c = Client()
        response = c.get( '/cloud_check_user/', {'user': settings_app.TEST_DISAVOWED_USERNAME}, **headers )
        self.assertEqual( 200, response.status_code )
        jdct = json.loads( response.content )
        self.assertEqual( ['request', 'response'], sorted(list(jdct.keys())) )
        self.assertEqual(
            {'authenticated': False, 'blocked': None, 'disavowed': True, 'registered': None, 'interpreted_new_user': False},
            jdct['response']['status_data']
            )

    def test_check_blocked_user(self):
        """ Checks blocked user. """
        b64_bytes = base64.b64encode( b'%s:%s' % (settings_app.BASIC_AUTH_USER.encode('utf-8'), settings_app.BASIC_AUTH_PASSWORD.encode('utf-8')) )
        headers = {
            'HTTP_AUTHORIZATION': 'Basic ' + b64_bytes.decode('utf-8'),
            'User-Agent': 'bul-test-client' }
        c = Client()
        response = c.get( '/cloud_check_user/', {'user': settings_app.TEST_BLOCKED_USERNAME}, **headers )
        self.assertEqual( 200, response.status_code )
        jdct = json.loads( response.content )
        self.assertEqual( ['request', 'response'], sorted(list(jdct.keys())) )
        self.assertEqual(
            {'authenticated': True, 'blocked': True, 'disavowed': None, 'registered': True, 'interpreted_new_user': False},
            jdct['response']['status_data']
            )

    def test_check_unregistered_user(self):
        """ Checks unregistered user.
            NOTE: any user 'new' to illiad is entered into the database and looks like this user.
                  ...meaning that this test WILL CREATE A NEW USER """
        b64_bytes = base64.b64encode( b'%s:%s' % (settings_app.BASIC_AUTH_USER.encode('utf-8'), settings_app.BASIC_AUTH_PASSWORD.encode('utf-8')) )
        headers = {
            'HTTP_AUTHORIZATION': 'Basic ' + b64_bytes.decode('utf-8'),
            'User-Agent': 'bul-test-client' }
        c = Client()
        # response = c.get( '/cloud_check_user/', {'user': settings_app.TEST_UNREGISTERED_USERNAME}, **headers )
        response = c.get( '/cloud_check_user/', {'user': '%s%s' % ( 'zzzz', random.randint(1111, 9999) )}, **headers )
        self.assertEqual( 200, response.status_code )
        jdct = json.loads( response.content )
        self.assertEqual( ['request', 'response'], sorted(list(jdct.keys())) )
        self.assertEqual(
            {'authenticated': True, 'blocked': None, 'disavowed': None, 'registered': False, 'interpreted_new_user': True},
            jdct['response']['status_data']
            )

    ## end class ClientCloudCheckUser_Test()



class ClientV2_Test( TestCase ):
    """ Tests easyBorrow-api v2 """

    def test__check_bad_method(self):
        """ GET (api requires POST) should return 400. """
        c = Client()
        response = c.get( '/v2/make_request/', {'aa': 'foo_a', 'bb': 'foo_b'} )
        self.assertEqual( 400, response.status_code )
        self.assertEqual( b'Bad Request', response.content )

    def test__check_bad_post_params(self):
        """ POST with bad params should return 400. """
        c = Client()
        response = c.post( '/v2/make_request/', {'aa': 'foo_a', 'bb': 'foo_b'} )
        self.assertEqual( 400, response.status_code )
        self.assertEqual( b'Bad Request', response.content )

    # def test__check_good_post_params__known_user(self):
    #     """ POST with good params should submit a request and return a transaction number.
    #         This test is good, just disabled so as not to submit unnecessary real requests. """
    #     c = Client()
    #     response = c.post(
    #         '/v2/make_request/',
    #         { 'auth_key': settings_app.TEST_AUTH_KEY, 'openurl': 'foo_b', 'request_id': 'foo_c', 'username': settings_app.TEST_EXISTING_GOOD_USER }
    #         )
    #     self.assertEqual( 200, response.status_code )
    #     response_dct = json.loads( response.content )
    #     self.assertEqual( [u'status', u'transaction_number'], sorted(response_dct.keys()) )
    #     self.assertEqual( 'submission_successful', response_dct['status'] )

    # def test__blocked_user(self):
    #     """ TODO """

    # def test__disavowed_user(self):
    #     """ TODO """

    ## end class ClientV2_Test()


class ClientCloudBookRequest_Test( TestCase ):
    """ Tests new easyBorrow-api using cloud ILLiad-api """

    def test__check_bad_method(self):
        """ GET (api requires POST) should return 400. """
        c = Client()
        response = c.get( '/cloud_book_request/', {'aa': 'foo_a', 'bb': 'foo_b'} )
        self.assertEqual( 400, response.status_code )
        self.assertEqual( b'Bad Request', response.content )

    def test__check_bad_post_params(self):
        """ POST with bad params should return 400.
            eg: $ python ./manage.py test illiad_app.tests.ClientV3_MakeBookRequest_Test.test__check_bad_post_params
            """
        c = Client()
        response = c.post( '/cloud_book_request/', {'aa': 'foo_a', 'bb': 'foo_b'} )
        self.assertEqual( 400, response.status_code )
        self.assertEqual( b'Bad Request', response.content )

    def test__check_good_post_params__known_user(self):
        """ POST with good params should submit a request and return a transaction number.
            This test is good, just disabled so as not to auto-submit real requests. """
        c = Client()
        response = c.post(
            '/cloud_book_request/',
            { 'auth_key': settings_app.TEST_AUTH_KEY, 'openurl': 'foo_b', 'request_id': 'foo_c', 'username': settings_app.TEST_EXISTING_GOOD_USER }
            )
        self.assertEqual( 200, response.status_code )
        response_dct = json.loads( response.content )
        self.assertEqual( [u'status', u'transaction_number'], sorted(response_dct.keys()) )
        self.assertEqual( 'submission_successful', response_dct['status'] )

    ## end class ClientCloudBookRequest_Test()
