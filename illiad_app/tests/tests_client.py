# -*- coding: utf-8 -*-

import base64, json, random
from illiad_app import settings_app
from django.test import Client, TestCase


class ClientCloudCreateUser_Test( TestCase ):
    """ Tests views.cloud_create_user() """

    def test_create_user__good_data(self):
        """ Checks successful new-user creation.
            NOTE: will really create new-user, so this test will likely be disabled. """
        pass
        # c = Client()
        # params = {
        #     'auth_key': settings_app.API_KEY,  # brown internal api
        #     'auth_id': '%s%s' % ( 'zzzz', random.randint(1111, 9999) ),
        #     # 'auth_id': settings_app.TEST_UNREGISTERED_USERNAME,
        #     'department': 'test-department',
        #     'email': 'test@test.edu',
        #     'first_name': 'test-first-name',
        #     'last_name': 'test-last-name',
        #     'phone': 'unavailable',
        #     'status': 'test-status'  # really 'type', eg 'Undergraduate Student'
        #     }
        # # response = c.post( '/cloud_create_user/', params )
        # response = c.post( '/create_user/', params )
        # self.assertEqual( 200, response.status_code )
        # jdct = json.loads( response.content )
        # self.assertEqual( ['request', 'response'], sorted(list(jdct.keys())) )
        # self.assertEqual( ['params', 'timestamp', 'url'], sorted(list(jdct['request'].keys())) )
        # self.assertEqual( ['elapsed_time', 'raw_data', 'status_data'], sorted(list(jdct['response'].keys())) )
        # self.assertEqual( {'status': 'Registered', 'status_code': 200}, jdct['response']['status_data'] )
        # self.assertEqual( params['auth_id'], jdct['response']['raw_data']['UserName'] )

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
        # response = c.post( '/cloud_create_user/', params )
        response = c.post( '/create_user/', params )
        self.assertEqual( 200, response.status_code )
        jdct = json.loads( response.content )
        self.assertEqual( ['request', 'response'], sorted(list(jdct.keys())) )
        self.assertEqual( ['params', 'timestamp', 'url'], sorted(list(jdct['request'].keys())) )
        self.assertEqual( ['elapsed_time', 'raw_data', 'status_data'], sorted(list(jdct['response'].keys())) )
        self.assertEqual( {'status': 'Failure', 'status_code': 400}, jdct['response']['status_data'] )  # see log for 'raw_data' response.

    ## end class ClientCloudCreateUser_Test()


class ClientCloudCheckUser_Test( TestCase ):
    """ Tests views.check_user() -- for status meaning `blocked`, `registered`, etc. """

    def test_check_good_existing_user(self):
        """ Checks happy path. """
        b64_bytes = base64.b64encode( b'%s:%s' % (settings_app.BASIC_AUTH_USER.encode('utf-8'), settings_app.BASIC_AUTH_PASSWORD.encode('utf-8')) )
        headers = {
            'HTTP_AUTHORIZATION': 'Basic ' + b64_bytes.decode('utf-8'),
            'User-Agent': 'bul-test-client' }
        c = Client()
        # response = c.get( '/cloud_check_user/', {'user': settings_app.TEST_EXISTING_GOOD_USER}, **headers )
        response = c.get( '/check_user/', {'user': settings_app.TEST_EXISTING_GOOD_USER}, **headers )
        self.assertEqual( 200, response.status_code )
        jdct = json.loads( response.content )
        self.assertEqual( ['request', 'response'], sorted(list(jdct.keys())) )
        self.assertEqual(
            {'authenticated': True, 'blocked': False, 'disavowed': False, 'registered': True, 'interpreted_new_user': False},
            jdct['response']['status_data']
            )

    def test_check_disavowed_user(self):
        """ Checks disavowed user. """
        b64_bytes = base64.b64encode( b'%s:%s' % (settings_app.BASIC_AUTH_USER.encode('utf-8'), settings_app.BASIC_AUTH_PASSWORD.encode('utf-8')) )
        headers = {
            'HTTP_AUTHORIZATION': 'Basic ' + b64_bytes.decode('utf-8'),
            'User-Agent': 'bul-test-client' }
        c = Client()
        # response = c.get( '/cloud_check_user/', {'user': settings_app.TEST_DISAVOWED_USERNAME}, **headers )
        response = c.get( '/check_user/', {'user': settings_app.TEST_DISAVOWED_USERNAME}, **headers )
        self.assertEqual( 200, response.status_code )
        jdct = json.loads( response.content )
        self.assertEqual( ['request', 'response'], sorted(list(jdct.keys())) )
        self.assertEqual(
            {'authenticated': False, 'blocked': False, 'disavowed': True, 'registered': False, 'interpreted_new_user': False},
            jdct['response']['status_data']
            )

    def test_check_blocked_user(self):
        """ Checks blocked user. """
        b64_bytes = base64.b64encode( b'%s:%s' % (settings_app.BASIC_AUTH_USER.encode('utf-8'), settings_app.BASIC_AUTH_PASSWORD.encode('utf-8')) )
        headers = {
            'HTTP_AUTHORIZATION': 'Basic ' + b64_bytes.decode('utf-8'),
            'User-Agent': 'bul-test-client' }
        c = Client()
        # response = c.get( '/cloud_check_user/', {'user': settings_app.TEST_BLOCKED_USERNAME}, **headers )
        response = c.get( '/check_user/', {'user': settings_app.TEST_BLOCKED_USERNAME}, **headers )
        self.assertEqual( 200, response.status_code )
        jdct = json.loads( response.content )
        self.assertEqual( ['request', 'response'], sorted(list(jdct.keys())) )
        self.assertEqual(
            {'authenticated': True, 'blocked': True, 'disavowed': False, 'registered': True, 'interpreted_new_user': False},
            jdct['response']['status_data']
            )

    def test_check_unregistered_user(self):
        """ Checks unregistered user.
            NOTE: any user 'new' to illiad is entered into the database and looks like this user.
                  ...meaning that this test WILL CREATE A NEW USER """
        pass
    #     b64_bytes = base64.b64encode( b'%s:%s' % (settings_app.BASIC_AUTH_USER.encode('utf-8'), settings_app.BASIC_AUTH_PASSWORD.encode('utf-8')) )
    #     headers = {
    #         'HTTP_AUTHORIZATION': 'Basic ' + b64_bytes.decode('utf-8'),
    #         'User-Agent': 'bul-test-client' }
    #     c = Client()
    #     # response = c.get( '/cloud_check_user/', {'user': '%s%s' % ( 'zzzz', random.randint(1111, 9999) )}, **headers )
    #     response = c.get( '/check_user/', {'user': '%s%s' % ( 'zzzz', random.randint(1111, 9999) )}, **headers )
    #     self.assertEqual( 200, response.status_code )
    #     jdct = json.loads( response.content )
    #     self.assertEqual( ['request', 'response'], sorted(list(jdct.keys())) )
    #     self.assertEqual(
    #         {'authenticated': False, 'blocked': False, 'disavowed': False, 'registered': False, 'interpreted_new_user': True},
    #         jdct['response']['status_data']
    #         )

    ## end class ClientCloudCheckUser_Test()


class ClientCloudBookRequest_Test( TestCase ):
    """ Tests new easyBorrow-api using cloud ILLiad-api """

    def test__check_bad_method(self):
        """ GET (api requires POST) should return 400. """
        c = Client()
        # response = c.get( '/cloud_book_request/', {'aa': 'foo_a', 'bb': 'foo_b'} )
        response = c.get( '/v2/make_request/', {'aa': 'foo_a', 'bb': 'foo_b'} )  # easyBorrow April-2019 internal-api call-style
        self.assertEqual( 400, response.status_code )
        self.assertEqual( b'Bad Request', response.content )

    def test__check_bad_post_params(self):
        """ POST with bad params should return 400.
            eg: $ python ./manage.py test illiad_app.tests.ClientCloudBookRequest_Test.test__check_bad_post_params
            """
        c = Client()
        # response = c.post( '/cloud_book_request/', {'aa': 'foo_a', 'bb': 'foo_b'} )
        response = c.post( '/v2/make_request/', {'aa': 'foo_a', 'bb': 'foo_b'} )  # easyBorrow April-2019 internal-api call-style
        self.assertEqual( 400, response.status_code )
        self.assertEqual( b'Bad Request', response.content )

    def test__check_good_post_params__known_user(self):
        """ POST with good params should submit a request and return a transaction number.
            This test is GOOD, just disabled so as not to auto-submit real requests. """
        pass
        # c = Client()
        # response = c.post(
        #     # '/cloud_book_request/',
        #     '/v2/make_request/',
        #     { 'auth_key': settings_app.TEST_AUTH_KEY,
        #         'openurl': 'isbn=9780857021052&title=The%20SAGE%20Handbook%20of%20Remote%20Sensing&notes=p.barcode%2C+%6021236009704581%60+--+volumes%2C+%60N%2FA%60',
        #         'request_id': str(random.randint(1111, 9999)),
        #         'username': settings_app.TEST_EXISTING_GOOD_USER }
        #     )
        # self.assertEqual( 200, response.status_code )
        # response_dct = json.loads( response.content )
        # self.assertEqual( [u'status', u'transaction_number'], sorted(response_dct.keys()) )
        # self.assertEqual( 'submission_successful', response_dct['status'] )

    def test__check_good_content_that_failed(self):
        """ Checks seemingly good openurl with too-long publisher.
            This test is GOOD, just disabled so as not to auto-submit real requests. """
        pass
        # c = Client()
        # response = c.post(
        #     # '/cloud_book_request/',
        #     '/v2/make_request/',
        #     { 'auth_key': settings_app.TEST_AUTH_KEY,
        #         'openurl': 'sid=FirstSearch%3AWorldCat&genre=book&isbn=9780615686875&title=Desire+love&date=2012&aulast=Berlant&aufirst=Lauren&auinitm=Gail&id=doi%3A&pid=823176599%3Cfssessid%3E0%3C%2Ffssessid%3E&url_ver=Z39.88-2004&rfr_id=info%3Asid%2Ffirstsearch.oclc.org%3AWorldCat&rft_val_fmt=info%3Aofi%2Ffmt%3Akev%3Amtx%3Abook&rft.genre=book&req_dat=%3Csessionid%3E0%3C%2Fsessionid%3E&rfe_dat=%3Caccessionnumber%3E823176599%3C%2Faccessionnumber%3E&rft_id=info%3Aoclcnum%2F823176599&rft_id=urn%3AISBN%3A9780615686875&rft.aulast=Berlant&rft.aufirst=Lauren&rft.auinitm=Gail&rft.btitle=Desire+love&rft.date=2012&rft.isbn=9780615686875&rft.place=Brooklyn++New+York&rft.pub=Dead+Letter+Office++BABEL+Working+Group+an+imprint+of+Punctum+Books&rft.genre=book',
        #         'request_id': str(random.randint(1111, 9999)),
        #         'username': settings_app.TEST_EXISTING_GOOD_USER }
        #     )
        # self.assertEqual( 200, response.status_code )
        # response_dct = json.loads( response.content )
        # self.assertEqual( [u'status', u'transaction_number'], sorted(response_dct.keys()) )
        # self.assertEqual( 'submission_successful', response_dct['status'] )

    def test__check_no_title(self):
        """ Checks a url that should have been handled in the article flow of easyAccess...
            ...but got to easyBorrow and failed as an ILLiad book-request because of no title.
            This test is GOOD, just disabled so as not to auto-submit real requests. """
        pass
        # c = Client()
        # response = c.post(
        #     # '/cloud_book_request/',
        #     '/v2/make_request/',
        #     { 'auth_key': settings_app.TEST_AUTH_KEY,
        #         'openurl': 'sid=Entrez:PubMed&id=pmid:30989589',
        #         'request_id': str(random.randint(1111, 9999)),
        #         'username': settings_app.TEST_EXISTING_GOOD_USER }
        #     )
        # self.assertEqual( 200, response.status_code )
        # response_dct = json.loads( response.content )
        # self.assertEqual( [u'status', u'transaction_number'], sorted(response_dct.keys()) )
        # self.assertEqual( 'submission_successful', response_dct['status'] )

    ## end class ClientCloudBookRequest_Test()


class ClientCloudArticleRequest_Test( TestCase ):
    """ Tests article-requesting via cloud ILLiad-api """

    def test__check_bad_method(self):
        """ GET (api requires POST) should return 400. """
        c = Client()
        response = c.get( '/request_article/', {'aa': 'foo_a', 'bb': 'foo_b'} )
        self.assertEqual( 400, response.status_code )
        self.assertEqual( b'Bad Request', response.content )

    def test__check_bad_post_params(self):
        """ POST with bad params should return 400.
            eg: $ python ./manage.py test illiad_app.tests.ClientCloudArticleRequest_Test.test__check_bad_post_params
            """
        c = Client()
        response = c.post( '/request_article/', {'aa': 'foo_a', 'bb': 'foo_b'} )
        self.assertEqual( 400, response.status_code )
        self.assertEqual( b'Bad Request', response.content )

    def test__check_good_post_happy_path(self):
        """ POST with good params should submit a request and return a transaction number.
            This test is GOOD, just disabled so as not to auto-submit real requests. """
        pass
        # c = Client()
        # response = c.post(
        #     '/request_article/',
        #     { 'auth_key': settings_app.TEST_AUTH_KEY,
        #         'openurl': 'rft_val_fmt=info%3Aofi/fmt%3Akev%3Amtx%3Ajournal&rfr_id=info%3Asid/Entrez%3APubMed&rft.issue=2&rft.au=Manika%2C+Katerina&rft.pages=134+-+EOA&rft_id=info%3Apmid/18496984&rft.date=2007&rft.volume=24&rft.end_page=EOA&rft.atitle=Epstein-Barr+virus+DNA+in+bronchoalveolar+lavage+fluid+from+patients+with+idiopathic+pulmonary+fibrosis.&ctx_ver=Z39.88-2004&rft.jtitle=Sarcoidosis%2C+vasculitis%2C+and+diffuse+lung+diseases&rft.issn=1124-0490&rft.genre=article&rft.spage=134&Notes=%60PMID%3A+18496984%60%3B+%60shortlink%3A+%3C%2Feasyaccess%2Ffind%2Fpermalink%2FXqt%2F%3E%60',
        #         'request_id': str(random.randint(1111, 9999)),
        #         'username': settings_app.TEST_EXISTING_GOOD_USER }
        #     )
        # self.assertEqual( 200, response.status_code )
        # response_dct = json.loads( response.content )
        # self.assertEqual( [u'status', u'transaction_number'], sorted(response_dct.keys()) )
        # self.assertEqual( 'submission_successful', response_dct['status'] )

    ## end class ClientCloudArticleRequest_Test()
