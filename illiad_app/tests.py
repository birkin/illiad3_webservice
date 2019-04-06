# -*- coding: utf-8 -*-

import base64, json, random
from . import settings_app
from django.test import Client, TestCase
from illiad_app.lib.cloud_request import Mapper


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
        b64_bytes = base64.b64encode( b'%s:%s' % (settings_app.BASIC_AUTH_USER.encode('utf-8'), settings_app.BASIC_AUTH_PASSWORD.encode('utf-8')) )
        headers = {
            'HTTP_AUTHORIZATION': 'Basic ' + b64_bytes.decode('utf-8'),
            'User-Agent': 'bul-test-client' }
        c = Client()
        # response = c.get( '/cloud_check_user/', {'user': '%s%s' % ( 'zzzz', random.randint(1111, 9999) )}, **headers )
        response = c.get( '/check_user/', {'user': '%s%s' % ( 'zzzz', random.randint(1111, 9999) )}, **headers )
        self.assertEqual( 200, response.status_code )
        jdct = json.loads( response.content )
        self.assertEqual( ['request', 'response'], sorted(list(jdct.keys())) )
        self.assertEqual(
            {'authenticated': False, 'blocked': False, 'disavowed': False, 'registered': False, 'interpreted_new_user': True},
            jdct['response']['status_data']
            )

    ## end class ClientCloudCheckUser_Test()



# class ClientV2_Test( TestCase ):
#     """ Tests easyBorrow-api v2 """

#     def test__check_bad_method(self):
#         """ GET (api requires POST) should return 400. """
#         c = Client()
#         response = c.get( '/v2/make_request/', {'aa': 'foo_a', 'bb': 'foo_b'} )
#         self.assertEqual( 400, response.status_code )
#         self.assertEqual( b'Bad Request', response.content )

#     def test__check_bad_post_params(self):
#         """ POST with bad params should return 400. """
#         c = Client()
#         response = c.post( '/v2/make_request/', {'aa': 'foo_a', 'bb': 'foo_b'} )
#         self.assertEqual( 400, response.status_code )
#         self.assertEqual( b'Bad Request', response.content )

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
        # response = c.get( '/cloud_book_request/', {'aa': 'foo_a', 'bb': 'foo_b'} )
        response = c.get( '/v2/make_request/', {'aa': 'foo_a', 'bb': 'foo_b'} )  # easyBorrow April-2019 internal-api call-style
        self.assertEqual( 400, response.status_code )
        self.assertEqual( b'Bad Request', response.content )

    def test__check_bad_post_params(self):
        """ POST with bad params should return 400.
            eg: $ python ./manage.py test illiad_app.tests.ClientV3_MakeBookRequest_Test.test__check_bad_post_params
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
        #     '/cloud_book_request/',
        #     { 'auth_key': settings_app.TEST_AUTH_KEY,
        #         'openurl': 'isbn=9780857021052&title=The%20SAGE%20Handbook%20of%20Remote%20Sensing&notes=p.barcode%2C+%6021236009704581%60+--+volumes%2C+%60N%2FA%60',
        #         'request_id': str(random.randint(1111, 9999)),
        #         'username': settings_app.TEST_EXISTING_GOOD_USER }
        #     )
        # self.assertEqual( 200, response.status_code )
        # response_dct = json.loads( response.content )
        # self.assertEqual( [u'status', u'transaction_number'], sorted(response_dct.keys()) )
        # self.assertEqual( 'submission_successful', response_dct['status'] )

    ## end class ClientCloudBookRequest_Test()


class Mapper_Test( TestCase ):
    """ Tests parsing of bib-dcts. """

    def setUp(self):
        self.log_id = random.randint(1111, 9999)
        self.mapper = Mapper( self.log_id )

    def test_bib_dct_A(self):
        """ Checks mapping of isbn and title. """
        bib_dct = {
 'query': {'date_time': '2019-04-05 12:50:30.120365',
           'url': 'https://library.brown.edu/bib_ourl_api/v1/ourl_to_bib/?ourl=isbn%3D9780857021052%26title%3DThe+SAGE+Handbook+of+Remote+Sensing%26notes%3Dp.barcode%2C%2B%6021236009704581%60%2B--%2Bvolumes%2C%2B%60N%2FA%60'},
 'response': {'bib': {'_rfr': None,
                      'author': [],
                      'end_page': None,
                      'identifier': [{'id': '9780857021052', 'type': 'isbn'}],
                      'issue': None,
                      'pages': None,
                      'place_of_publication': None,
                      'publisher': None,
                      'start_page': None,
                      'title': 'The SAGE Handbook of Remote Sensing',
                      'type': 'book',
                      'volume': None},
              'decoded_openurl': 'isbn=9780857021052&title=The SAGE Handbook '
                                 'of Remote '
                                 'Sensing&notes=p.barcode,+`21236009704581`+--+volumes,+`N/A`',
              'elapsed_time': '0:00:00.008798'}}
        self.assertEqual( self.mapper.grab_title(bib_dct), 'The SAGE Handbook of Remote Sensing' )
        self.assertEqual( self.mapper.grab_author(bib_dct), '' )
        self.assertEqual( self.mapper.grab_sid(bib_dct), '' )
        self.assertEqual( self.mapper.grab_espn(bib_dct), '' )
        self.assertEqual( self.mapper.grab_isbn(bib_dct), '9780857021052' )
        self.assertEqual( self.mapper.grab_date(bib_dct), '' )
        self.assertEqual( self.mapper.grab_place(bib_dct), '' )
        self.assertEqual( self.mapper.grab_publisher(bib_dct), '' )

    def test_bib_dct_B(self):
        """ Checks mapping of FirstSearch oclc# `254605206`. """
        bib_dct = {
 'query': {'date_time': '2019-04-05 14:20:42.044218',
           'url': 'https://library.brown.edu/bib_ourl_api/v1/ourl_to_bib/?ourl=sid%3DFirstSearch%253AWorldCat%26genre%3Dbook%26isbn%3D9780300059915%26title%3DThe%2Btexture%2Bof%2Bmemory%2B%253A%2BHolocaust%2Bmemorials%2Band%2Bmeaning%26date%3D2000%26aulast%3DYoung%26aufirst%3DJames%26auinitm%3DEdward%26id%3Ddoi%253A%26pid%3D254605206%253Cfssessid%253E0%253C%252Ffssessid%253E%253Cedition%253E%255BNachdr.%255D%253C%252Fedition%253E%26url_ver%3DZ39.88-2004%26rfr_id%3Dinfo%253Asid%252Ffirstsearch.oclc.org%253AWorldCat%26rft_val_fmt%3Dinfo%253Aofi%252Ffmt%253Akev%253Amtx%253Abook%26rft.genre%3Dbook%26req_dat%3D%253Csessionid%253E0%253C%252Fsessionid%253E%26rfe_dat%3D%253Caccessionnumber%253E254605206%253C%252Faccessionnumber%253E%26rft_id%3Dinfo%253Aoclcnum%252F254605206%26rft_id%3Durn%253AISBN%253A9780300059915%26rft.aulast%3DYoung%26rft.aufirst%3DJames%26rft.auinitm%3DEdward%26rft.btitle%3DThe%2Btexture%2Bof%2Bmemory%2B%253A%2BHolocaust%2Bmemorials%2Band%2Bmeaning%26rft.date%3D2000%26rft.isbn%3D9780300059915%26rft.place%3DNew%2BHaven%2B%2BCT%26rft.pub%3DYale%2BUniv.%2BPress%26rft.edition%3D%255BNachdr.%255D%26rft.genre%3Dbook'},
 'response': {'bib': {'_rfr': 'info:sid/firstsearch.oclc.org:WorldCat',
                      'author': [{'_minitial': 'Edward',
                                  'firstname': 'James',
                                  'lastname': 'Young',
                                  'name': 'Young, James'}],
                      'end_page': None,
                      'identifier': [{'id': '9780300059915', 'type': 'isbn'},
                                     {'id': '254605206', 'type': 'oclc'}],
                      'issue': None,
                      'pages': None,
                      'place_of_publication': 'New Haven  CT',
                      'publisher': 'Yale Univ. Press',
                      'start_page': None,
                      'title': 'The texture of memory : Holocaust memorials '
                               'and meaning',
                      'type': 'book',
                      'volume': None,
                      'year': '2000'},
              'decoded_openurl': 'sid=FirstSearch:WorldCat&genre=book&isbn=9780300059915&title=The+texture+of+memory+:+Holocaust+memorials+and+meaning&date=2000&aulast=Young&aufirst=James&auinitm=Edward&id=doi:&pid=254605206<fssessid>0</fssessid><edition>[Nachdr.]</edition>&url_ver=Z39.88-2004&rfr_id=info:sid/firstsearch.oclc.org:WorldCat&rft_val_fmt=info:ofi/fmt:kev:mtx:book&rft.genre=book&req_dat=<sessionid>0</sessionid>&rfe_dat=<accessionnumber>254605206</accessionnumber>&rft_id=info:oclcnum/254605206&rft_id=urn:ISBN:9780300059915&rft.aulast=Young&rft.aufirst=James&rft.auinitm=Edward&rft.btitle=The+texture+of+memory+:+Holocaust+memorials+and+meaning&rft.date=2000&rft.isbn=9780300059915&rft.place=New+Haven++CT&rft.pub=Yale+Univ.+Press&rft.edition=[Nachdr.]&rft.genre=book',
              'elapsed_time': '0:00:00.016884'}}
        self.assertEqual( self.mapper.grab_title(bib_dct), 'The texture of memory : Holocaust memorials and meaning' )
        self.assertEqual( self.mapper.grab_author(bib_dct), 'Young, James' )
        self.assertEqual( self.mapper.grab_sid(bib_dct), 'info:sid/firstsearch.oclc.org:WorldCat' )
        self.assertEqual( self.mapper.grab_espn(bib_dct), '254605206' )
        self.assertEqual( self.mapper.grab_isbn(bib_dct), '9780300059915' )
        self.assertEqual( self.mapper.grab_date(bib_dct), '2000' )
        self.assertEqual( self.mapper.grab_place(bib_dct), 'New Haven  CT' )
        self.assertEqual( self.mapper.grab_publisher(bib_dct), 'Yale Univ. Press' )

    def test_bib_dct_C(self):
        """ Checks mapping of `BUL:Josiah:b8160392`. """
        bib_dct = {
 'query': {'date_time': '2019-04-05 16:16:45.638661',
           'url': 'https://library.brown.edu/bib_ourl_api/v1/ourl_to_bib/?ourl=url_ver%3DZ39.88-2004%26url_ctx_fmt%3Dinfo%253Aofi%252Ffmt%253Akev%253Amtx%253Actx%26ctx_ver%3DZ39.88-2004%26ctx_tim%3D2019-04-05T13%253A54%253A31-04%253A00%26ctx_id%3D%26ctx_enc%3Dinfo%253Aofi%252Fenc%253AUTF-8%26rft.btitle%3DThe%2Bline%2Bbecomes%2Ba%2Briver%26rft.au%3DCant%25C3%25BA%252C%2BFrancisco%2B%2528Essayist%2529%26rft.date%3D2018%26rft.format%3Dbook%26rft.sid%3DBUL%253AJosiah%253Ab8160392%26rft.isbn%3D9780735217713%26rft_val_fmt%3Dinfo%253Aofi%252Ffmt%253Akev%253Amtx%253Abook'},
 'response': {'bib': {'_rfr': None,
                      'author': [{'name': 'Cantú, Francisco (Essayist)'}],
                      'end_page': None,
                      'identifier': [{'id': '9780735217713', 'type': 'isbn'}],
                      'issue': None,
                      'pages': None,
                      'place_of_publication': None,
                      'publisher': None,
                      'start_page': None,
                      'title': 'The line becomes a river',
                      'type': 'book',
                      'volume': None,
                      'year': '2018'},
              'decoded_openurl': 'url_ver=Z39.88-2004&url_ctx_fmt=info:ofi/fmt:kev:mtx:ctx&ctx_ver=Z39.88-2004&ctx_tim=2019-04-05T13:54:31-04:00&ctx_id=&ctx_enc=info:ofi/enc:UTF-8&rft.btitle=The+line+becomes+a+river&rft.au=Cantú,+Francisco+(Essayist)&rft.date=2018&rft.format=book&rft.sid=BUL:Josiah:b8160392&rft.isbn=9780735217713&rft_val_fmt=info:ofi/fmt:kev:mtx:book',
              'elapsed_time': '0:00:00.013324'}}
        self.assertEqual( self.mapper.grab_title(bib_dct), 'The line becomes a river' )
        self.assertEqual( self.mapper.grab_author(bib_dct), 'Cantú, Francisco (Essayist)' )
        self.assertEqual( self.mapper.grab_sid(bib_dct), 'BUL:Josiah:b8160392' )
        self.assertEqual( self.mapper.grab_espn(bib_dct), '' )
        self.assertEqual( self.mapper.grab_isbn(bib_dct), '9780735217713' )
        self.assertEqual( self.mapper.grab_date(bib_dct), '2018' )
        self.assertEqual( self.mapper.grab_place(bib_dct), '' )
        self.assertEqual( self.mapper.grab_publisher(bib_dct), '' )

    def test_bib_dct_D(self):
        """ Checks mapping of WorldCat oclc# `918241430`. """
        bib_dct = {
 'query': {'date_time': '2019-04-05 16:53:50.905525',
           'url': 'https://library.brown.edu/bib_ourl_api/v1/ourl_to_bib/?ourl=sid%3DFirstSearch%253AWorldCat%26isbn%3D9781452691848%26title%3DGod%2527s%2Bhotel%2B%253A%2Ba%2Bdoctor%252C%2Ba%2Bhospital%252C%2Band%2Ba%2Bpilgrimage%2Bto%2Bthe%2Bheart%2Bof%2Bmedicine%26date%3D2015%26aulast%3DSweet%26aufirst%3DVictoria%26id%3Ddoi%253A%26pid%3D918241430%253Cfssessid%253E0%253C%252Ffssessid%253E%26url_ver%3DZ39.88-2004%26rfr_id%3Dinfo%253Asid%252Ffirstsearch.oclc.org%253AWorldCat%26rft_val_fmt%3Dinfo%253Aofi%252Ffmt%253Akev%253Amtx%253Abook%26rft.genre%3Dunknown%26req_dat%3D%253Csessionid%253E0%253C%252Fsessionid%253E%26rfe_dat%3D%253Caccessionnumber%253E918241430%253C%252Faccessionnumber%253E%26rft_id%3Dinfo%253Aoclcnum%252F918241430%26rft_id%3Durn%253AISBN%253A9781452691848%26rft.aulast%3DSweet%26rft.aufirst%3DVictoria%26rft.title%3DGod%2527s%2Bhotel%2B%253A%2Ba%2Bdoctor%252C%2Ba%2Bhospital%252C%2Band%2Ba%2Bpilgrimage%2Bto%2Bthe%2Bheart%2Bof%2Bmedicine%26rft.date%3D2015%26rft.isbn%3D9781452691848%26rft.aucorp%3DTantor%2BMedia.%26rft.place%3DOld%2BSaybrook%252C%2BConn.%2B%253A%26rft.pub%3DTantor%2BMedia%252C%26rft.genre%3Dunknown'},
 'response': {'bib': {'_rfr': 'info:sid/firstsearch.oclc.org:WorldCat',
                      'author': [{'firstname': 'Victoria',
                                  'lastname': 'Sweet',
                                  'name': 'Sweet, Victoria'}],
                      'end_page': None,
                      'identifier': [{'id': '9781452691848', 'type': 'isbn'},
                                     {'id': '918241430', 'type': 'oclc'}],
                      'issue': None,
                      'pages': None,
                      'place_of_publication': 'Old Saybrook, Conn. :',
                      'publisher': 'Tantor Media,',
                      'start_page': None,
                      'title': "God's hotel : a doctor, a hospital, and a "
                               'pilgrimage to the heart of medicine',
                      'type': 'book',
                      'volume': None,
                      'year': '2015'},
              'decoded_openurl': "sid=FirstSearch:WorldCat&isbn=9781452691848&title=God's+hotel+:+a+doctor,+a+hospital,+and+a+pilgrimage+to+the+heart+of+medicine&date=2015&aulast=Sweet&aufirst=Victoria&id=doi:&pid=918241430<fssessid>0</fssessid>&url_ver=Z39.88-2004&rfr_id=info:sid/firstsearch.oclc.org:WorldCat&rft_val_fmt=info:ofi/fmt:kev:mtx:book&rft.genre=unknown&req_dat=<sessionid>0</sessionid>&rfe_dat=<accessionnumber>918241430</accessionnumber>&rft_id=info:oclcnum/918241430&rft_id=urn:ISBN:9781452691848&rft.aulast=Sweet&rft.aufirst=Victoria&rft.title=God's+hotel+:+a+doctor,+a+hospital,+and+a+pilgrimage+to+the+heart+of+medicine&rft.date=2015&rft.isbn=9781452691848&rft.aucorp=Tantor+Media.&rft.place=Old+Saybrook,+Conn.+:&rft.pub=Tantor+Media,&rft.genre=unknown",
              'elapsed_time': '0:00:00.017019'}}
        self.assertEqual( self.mapper.grab_title(bib_dct), "God's hotel : a doctor, a hospital, and a pilgrimage to the heart of medicine" )
        self.assertEqual( self.mapper.grab_author(bib_dct), 'Sweet, Victoria' )
        self.assertEqual( self.mapper.grab_sid(bib_dct), 'info:sid/firstsearch.oclc.org:WorldCat' )
        self.assertEqual( self.mapper.grab_espn(bib_dct), '918241430' )
        self.assertEqual( self.mapper.grab_isbn(bib_dct), '9781452691848' )
        self.assertEqual( self.mapper.grab_date(bib_dct), '2015' )
        self.assertEqual( self.mapper.grab_place(bib_dct), 'Old Saybrook, Conn. :' )
        self.assertEqual( self.mapper.grab_publisher(bib_dct), 'Tantor Media,' )

    def test_bib_dct_E(self):
        """ Checks mapping of WorlCat oclc# `973822484`. """
        bib_dct = {
 'query': {'date_time': '2019-04-05 17:01:04.738055',
           'url': 'https://library.brown.edu/bib_ourl_api/v1/ourl_to_bib/?ourl=sid%3DFirstSearch%253AWorldCat%26genre%3Dbook%26isbn%3D9780863584305%26title%3DTrauma%2Band%2Brecovery%26date%3D2015%26aulast%3DHerman%26aufirst%3DJudith%26auinitm%3DLewis%26id%3Ddoi%253A%26pid%3D973822484%253Cfssessid%253E0%253C%252Ffssessid%253E%253Cedition%253E%255BNew%2Bed.%255D.%253C%252Fedition%253E%26url_ver%3DZ39.88-2004%26rfr_id%3Dinfo%253Asid%252Ffirstsearch.oclc.org%253AWorldCat%26rft_val_fmt%3Dinfo%253Aofi%252Ffmt%253Akev%253Amtx%253Abook%26rft.genre%3Dbook%26req_dat%3D%253Csessionid%253E0%253C%252Fsessionid%253E%26rfe_dat%3D%253Caccessionnumber%253E973822484%253C%252Faccessionnumber%253E%26rft_id%3Dinfo%253Aoclcnum%252F973822484%26rft_id%3Durn%253AISBN%253A9780863584305%26rft.aulast%3DHerman%26rft.aufirst%3DJudith%26rft.auinitm%3DLewis%26rft.btitle%3DTrauma%2Band%2Brecovery%26rft.date%3D2015%26rft.isbn%3D9780863584305%26rft.place%3DLondon%26rft.pub%3DPandora%26rft.edition%3D%255BNew%2Bed.%255D.%26rft.genre%3Dbook'},
 'response': {'bib': {'_rfr': 'info:sid/firstsearch.oclc.org:WorldCat',
                      'author': [{'_minitial': 'Lewis',
                                  'firstname': 'Judith',
                                  'lastname': 'Herman',
                                  'name': 'Herman, Judith'}],
                      'end_page': None,
                      'identifier': [{'id': '9780863584305', 'type': 'isbn'},
                                     {'id': '973822484', 'type': 'oclc'}],
                      'issue': None,
                      'pages': None,
                      'place_of_publication': 'London',
                      'publisher': 'Pandora',
                      'start_page': None,
                      'title': 'Trauma and recovery',
                      'type': 'book',
                      'volume': None,
                      'year': '2015'},
              'decoded_openurl': 'sid=FirstSearch:WorldCat&genre=book&isbn=9780863584305&title=Trauma+and+recovery&date=2015&aulast=Herman&aufirst=Judith&auinitm=Lewis&id=doi:&pid=973822484<fssessid>0</fssessid><edition>[New+ed.].</edition>&url_ver=Z39.88-2004&rfr_id=info:sid/firstsearch.oclc.org:WorldCat&rft_val_fmt=info:ofi/fmt:kev:mtx:book&rft.genre=book&req_dat=<sessionid>0</sessionid>&rfe_dat=<accessionnumber>973822484</accessionnumber>&rft_id=info:oclcnum/973822484&rft_id=urn:ISBN:9780863584305&rft.aulast=Herman&rft.aufirst=Judith&rft.auinitm=Lewis&rft.btitle=Trauma+and+recovery&rft.date=2015&rft.isbn=9780863584305&rft.place=London&rft.pub=Pandora&rft.edition=[New+ed.].&rft.genre=book',
              'elapsed_time': '0:00:00.017204'}}
        self.assertEqual( self.mapper.grab_title(bib_dct), 'Trauma and recovery' )
        self.assertEqual( self.mapper.grab_author(bib_dct), 'Herman, Judith' )
        self.assertEqual( self.mapper.grab_sid(bib_dct), 'info:sid/firstsearch.oclc.org:WorldCat' )
        self.assertEqual( self.mapper.grab_espn(bib_dct), '973822484' )
        self.assertEqual( self.mapper.grab_isbn(bib_dct), '9780863584305' )
        self.assertEqual( self.mapper.grab_date(bib_dct), '2015' )
        self.assertEqual( self.mapper.grab_place(bib_dct), 'London' )
        self.assertEqual( self.mapper.grab_publisher(bib_dct), 'Pandora' )

    def test_bib_dct_F(self):
        """ Checks mapping of WorldCat oclc# `1083853313`. """
        bib_dct = {
 'query': {'date_time': '2019-04-05 17:07:01.482800',
           'url': 'https://library.brown.edu/bib_ourl_api/v1/ourl_to_bib/?ourl=sid%3DFirstSearch%253AWorldCat%26genre%3Dbook%26isbn%3D9780692196380%26title%3DLinear%2Balgebra%2Band%2Blearning%2Bfrom%2Bdata%26date%3D2019%26aulast%3DStrang%26aufirst%3DGilbert%26id%3Ddoi%253A%26pid%3D1083853313%253Cfssessid%253E0%253C%252Ffssessid%253E%26url_ver%3DZ39.88-2004%26rfr_id%3Dinfo%253Asid%252Ffirstsearch.oclc.org%253AWorldCat%26rft_val_fmt%3Dinfo%253Aofi%252Ffmt%253Akev%253Amtx%253Abook%26rft.genre%3Dbook%26req_dat%3D%253Csessionid%253E0%253C%252Fsessionid%253E%26rfe_dat%3D%253Caccessionnumber%253E1083853313%253C%252Faccessionnumber%253E%26rft_id%3Dinfo%253Aoclcnum%252F1083853313%26rft_id%3Durn%253AISBN%253A9780692196380%26rft.aulast%3DStrang%26rft.aufirst%3DGilbert%26rft.btitle%3DLinear%2Balgebra%2Band%2Blearning%2Bfrom%2Bdata%26rft.date%3D2019%26rft.isbn%3D9780692196380%26rft.genre%3Dbook'},
 'response': {'bib': {'_rfr': 'info:sid/firstsearch.oclc.org:WorldCat',
                      'author': [{'firstname': 'Gilbert',
                                  'lastname': 'Strang',
                                  'name': 'Strang, Gilbert'}],
                      'end_page': None,
                      'identifier': [{'id': '9780692196380', 'type': 'isbn'},
                                     {'id': '1083853313', 'type': 'oclc'}],
                      'issue': None,
                      'pages': None,
                      'place_of_publication': None,
                      'publisher': None,
                      'start_page': None,
                      'title': 'Linear algebra and learning from data',
                      'type': 'book',
                      'volume': None,
                      'year': '2019'},
              'decoded_openurl': 'sid=FirstSearch:WorldCat&genre=book&isbn=9780692196380&title=Linear+algebra+and+learning+from+data&date=2019&aulast=Strang&aufirst=Gilbert&id=doi:&pid=1083853313<fssessid>0</fssessid>&url_ver=Z39.88-2004&rfr_id=info:sid/firstsearch.oclc.org:WorldCat&rft_val_fmt=info:ofi/fmt:kev:mtx:book&rft.genre=book&req_dat=<sessionid>0</sessionid>&rfe_dat=<accessionnumber>1083853313</accessionnumber>&rft_id=info:oclcnum/1083853313&rft_id=urn:ISBN:9780692196380&rft.aulast=Strang&rft.aufirst=Gilbert&rft.btitle=Linear+algebra+and+learning+from+data&rft.date=2019&rft.isbn=9780692196380&rft.genre=book',
              'elapsed_time': '0:00:00.014083'}}
        self.assertEqual( self.mapper.grab_title(bib_dct), 'Linear algebra and learning from data' )
        self.assertEqual( self.mapper.grab_author(bib_dct), 'Strang, Gilbert' )
        self.assertEqual( self.mapper.grab_sid(bib_dct), 'info:sid/firstsearch.oclc.org:WorldCat' )
        self.assertEqual( self.mapper.grab_espn(bib_dct), '1083853313' )
        self.assertEqual( self.mapper.grab_isbn(bib_dct), '9780692196380' )
        self.assertEqual( self.mapper.grab_date(bib_dct), '2019' )
        self.assertEqual( self.mapper.grab_place(bib_dct), '' )
        self.assertEqual( self.mapper.grab_publisher(bib_dct), '' )

    def test_bib_dct_G(self):
        """ Checks mapping of WorldCat oclc# `19056429`. """
        bib_dct = {
 'query': {'date_time': '2019-04-06 09:54:58.656953',
           'url': 'https://library.brown.edu/bib_ourl_api/v1/ourl_to_bib/?ourl=sid%3DFirstSearch%253AWorldCat%26genre%3Dbook%26isbn%3D9780062508591%26title%3DJambalaya%2B%253A%2Bthe%2Bnatural%2Bwoman%2527s%2Bbook%2Bof%2Bpersonal%2Bcharms%2Band%2Bpractical%2Brituals%26date%3D1988%26aulast%3DTeish%26aufirst%3DLuisah%26id%3Ddoi%253A%26pid%3D19056429%253Cfssessid%253E0%253C%252Ffssessid%253E%253Cedition%253E1st%2BHarper%2B%2526%2BRow%2Bpbk.%2Bed.%253C%252Fedition%253E%26url_ver%3DZ39.88-2004%26rfr_id%3Dinfo%253Asid%252Ffirstsearch.oclc.org%253AWorldCat%26rft_val_fmt%3Dinfo%253Aofi%252Ffmt%253Akev%253Amtx%253Abook%26rft.genre%3Dbook%26req_dat%3D%253Csessionid%253E0%253C%252Fsessionid%253E%26rfe_dat%3D%253Caccessionnumber%253E19056429%253C%252Faccessionnumber%253E%26rft_id%3Dinfo%253Aoclcnum%252F19056429%26rft_id%3Durn%253AISBN%253A9780062508591%26rft.aulast%3DTeish%26rft.aufirst%3DLuisah%26rft.btitle%3DJambalaya%2B%253A%2Bthe%2Bnatural%2Bwoman%2527s%2Bbook%2Bof%2Bpersonal%2Bcharms%2Band%2Bpractical%2Brituals%26rft.date%3D1988%26rft.isbn%3D9780062508591%26rft.place%3DSan%2BFrancisco%26rft.pub%3DHarper%2B%2526%2BRow%26rft.edition%3D1st%2BHarper%2B%2526%2BRow%2Bpbk.%2Bed.%26rft.genre%3Dbook'},
 'response': {'bib': {'_rfr': 'info:sid/firstsearch.oclc.org:WorldCat',
                      'author': [{'firstname': 'Luisah',
                                  'lastname': 'Teish',
                                  'name': 'Teish, Luisah'}],
                      'end_page': None,
                      'identifier': [{'id': '9780062508591', 'type': 'isbn'},
                                     {'id': '19056429', 'type': 'oclc'}],
                      'issue': None,
                      'pages': None,
                      'place_of_publication': 'San Francisco',
                      'publisher': 'Harper ',
                      'start_page': None,
                      'title': "Jambalaya : the natural woman's book of "
                               'personal charms and practical rituals',
                      'type': 'book',
                      'volume': None,
                      'year': '1988'},
              'decoded_openurl': "sid=FirstSearch:WorldCat&genre=book&isbn=9780062508591&title=Jambalaya+:+the+natural+woman's+book+of+personal+charms+and+practical+rituals&date=1988&aulast=Teish&aufirst=Luisah&id=doi:&pid=19056429<fssessid>0</fssessid><edition>1st+Harper+&+Row+pbk.+ed.</edition>&url_ver=Z39.88-2004&rfr_id=info:sid/firstsearch.oclc.org:WorldCat&rft_val_fmt=info:ofi/fmt:kev:mtx:book&rft.genre=book&req_dat=<sessionid>0</sessionid>&rfe_dat=<accessionnumber>19056429</accessionnumber>&rft_id=info:oclcnum/19056429&rft_id=urn:ISBN:9780062508591&rft.aulast=Teish&rft.aufirst=Luisah&rft.btitle=Jambalaya+:+the+natural+woman's+book+of+personal+charms+and+practical+rituals&rft.date=1988&rft.isbn=9780062508591&rft.place=San+Francisco&rft.pub=Harper+&+Row&rft.edition=1st+Harper+&+Row+pbk.+ed.&rft.genre=book",
              'elapsed_time': '0:00:00.016115'}}
        self.assertEqual( self.mapper.grab_title(bib_dct), "Jambalaya : the natural woman's book of personal charms and practical rituals" )
        self.assertEqual( self.mapper.grab_author(bib_dct), 'Teish, Luisah' )
        self.assertEqual( self.mapper.grab_sid(bib_dct), 'info:sid/firstsearch.oclc.org:WorldCat' )
        self.assertEqual( self.mapper.grab_espn(bib_dct), '19056429' )
        self.assertEqual( self.mapper.grab_isbn(bib_dct), '9780062508591' )
        self.assertEqual( self.mapper.grab_date(bib_dct), '1988' )
        self.assertEqual( self.mapper.grab_place(bib_dct), 'San Francisco' )
        self.assertEqual( self.mapper.grab_publisher(bib_dct), 'Harper ' )

    def test_bib_dct_H(self):
        """ Checks mapping of WorldCat oclc# `1041433507`. """
        bib_dct = {
 'query': {'date_time': '2019-04-06 10:01:24.174221',
           'url': 'https://library.brown.edu/bib_ourl_api/v1/ourl_to_bib/?ourl=sid%3DFirstSearch%253AWorldCat%26genre%3Dbook%26isbn%3D9781107670815%26title%3DBefore%2Bmestizaje%2B%253A%2Bthe%2Bfrontiers%2Bof%2Brace%2Band%2Bcaste%2Bin%2Bcolonial%2BMexico%26date%3D2018%26aulast%3DVinson%26aufirst%3DBen%26id%3Ddoi%253A%26pid%3D1041433507%253Cfssessid%253E0%253C%252Ffssessid%253E%26url_ver%3DZ39.88-2004%26rfr_id%3Dinfo%253Asid%252Ffirstsearch.oclc.org%253AWorldCat%26rft_val_fmt%3Dinfo%253Aofi%252Ffmt%253Akev%253Amtx%253Abook%26rft.genre%3Dbook%26req_dat%3D%253Csessionid%253E0%253C%252Fsessionid%253E%26rfe_dat%3D%253Caccessionnumber%253E1041433507%253C%252Faccessionnumber%253E%26rft_id%3Dinfo%253Aoclcnum%252F1041433507%26rft_id%3Durn%253AISBN%253A9781107670815%26rft.aulast%3DVinson%26rft.aufirst%3DBen%26rft.btitle%3DBefore%2Bmestizaje%2B%253A%2Bthe%2Bfrontiers%2Bof%2Brace%2Band%2Bcaste%2Bin%2Bcolonial%2BMexico%26rft.date%3D2018%26rft.isbn%3D9781107670815%26rft.place%3DNew%2BYork%26rft.pub%3DCambridge%2BUniversity%2BPress%26rft.genre%3Dbook'},
 'response': {'bib': {'_rfr': 'info:sid/firstsearch.oclc.org:WorldCat',
                      'author': [{'firstname': 'Ben',
                                  'lastname': 'Vinson',
                                  'name': 'Vinson, Ben'}],
                      'end_page': None,
                      'identifier': [{'id': '9781107670815', 'type': 'isbn'},
                                     {'id': '1041433507', 'type': 'oclc'}],
                      'issue': None,
                      'pages': None,
                      'place_of_publication': 'New York',
                      'publisher': 'Cambridge University Press',
                      'start_page': None,
                      'title': 'Before mestizaje : the frontiers of race and '
                               'caste in colonial Mexico',
                      'type': 'book',
                      'volume': None,
                      'year': '2018'},
              'decoded_openurl': 'sid=FirstSearch:WorldCat&genre=book&isbn=9781107670815&title=Before+mestizaje+:+the+frontiers+of+race+and+caste+in+colonial+Mexico&date=2018&aulast=Vinson&aufirst=Ben&id=doi:&pid=1041433507<fssessid>0</fssessid>&url_ver=Z39.88-2004&rfr_id=info:sid/firstsearch.oclc.org:WorldCat&rft_val_fmt=info:ofi/fmt:kev:mtx:book&rft.genre=book&req_dat=<sessionid>0</sessionid>&rfe_dat=<accessionnumber>1041433507</accessionnumber>&rft_id=info:oclcnum/1041433507&rft_id=urn:ISBN:9781107670815&rft.aulast=Vinson&rft.aufirst=Ben&rft.btitle=Before+mestizaje+:+the+frontiers+of+race+and+caste+in+colonial+Mexico&rft.date=2018&rft.isbn=9781107670815&rft.place=New+York&rft.pub=Cambridge+University+Press&rft.genre=book',
              'elapsed_time': '0:00:00.017586'}}
        self.assertEqual( self.mapper.grab_title(bib_dct), 'Before mestizaje : the frontiers of race and caste in colonial Mexico' )
        self.assertEqual( self.mapper.grab_author(bib_dct), 'Vinson, Ben' )
        self.assertEqual( self.mapper.grab_sid(bib_dct), 'info:sid/firstsearch.oclc.org:WorldCat' )
        self.assertEqual( self.mapper.grab_espn(bib_dct), '1041433507' )
        self.assertEqual( self.mapper.grab_isbn(bib_dct), '9781107670815' )
        self.assertEqual( self.mapper.grab_date(bib_dct), '2018' )
        self.assertEqual( self.mapper.grab_place(bib_dct), 'New York' )
        self.assertEqual( self.mapper.grab_publisher(bib_dct), 'Cambridge University Press' )

    def test_bib_dct_I(self):
        """ Checks mapping of WorldCat oclc# `7390570323`. """
        bib_dct = {
 'query': {'date_time': '2019-04-06 10:06:39.005840',
           'url': 'https://library.brown.edu/bib_ourl_api/v1/ourl_to_bib/?ourl=sid%3DFirstSearch%253AWorldCat%26genre%3Dbook%26isbn%3D978-0-415-27557-6%26title%3DMaritime%2BEconomics%2B3e%26date%3D2009%26aulast%3DStopford%26aufirst%3DMartin%26id%3Ddoi%253A%26pid%3D7390570323%253Cfssessid%253E0%253C%252Ffssessid%253E%26url_ver%3DZ39.88-2004%26rfr_id%3Dinfo%253Asid%252Ffirstsearch.oclc.org%253AWorldCat%26rft_val_fmt%3Dinfo%253Aofi%252Ffmt%253Akev%253Amtx%253Abook%26rft.genre%3Dbook%26req_dat%3D%253Csessionid%253E0%253C%252Fsessionid%253E%26rfe_dat%3D%253Caccessionnumber%253E7390570323%253C%252Faccessionnumber%253E%26rft_id%3Dinfo%253Aoclcnum%252F7390570323%26rft_id%3Durn%253AISBN%253A978-0-415-27557-6%26rft.aulast%3DStopford%26rft.aufirst%3DMartin%26rft.btitle%3DMaritime%2BEconomics%2B3e%26rft.date%3D2009%26rft.isbn%3D978-0-415-27557-6%26rft.pub%3DRoutledge%26rft.genre%3Dbook'},
 'response': {'bib': {'_rfr': 'info:sid/firstsearch.oclc.org:WorldCat',
                      'author': [{'firstname': 'Martin',
                                  'lastname': 'Stopford',
                                  'name': 'Stopford, Martin'}],
                      'end_page': None,
                      'identifier': [{'id': '978-0-415-27557-6',
                                      'type': 'isbn'},
                                     {'id': '7390570323', 'type': 'oclc'}],
                      'issue': None,
                      'pages': None,
                      'place_of_publication': None,
                      'publisher': 'Routledge',
                      'start_page': None,
                      'title': 'Maritime Economics 3e',
                      'type': 'book',
                      'volume': None,
                      'year': '2009'},
              'decoded_openurl': 'sid=FirstSearch:WorldCat&genre=book&isbn=978-0-415-27557-6&title=Maritime+Economics+3e&date=2009&aulast=Stopford&aufirst=Martin&id=doi:&pid=7390570323<fssessid>0</fssessid>&url_ver=Z39.88-2004&rfr_id=info:sid/firstsearch.oclc.org:WorldCat&rft_val_fmt=info:ofi/fmt:kev:mtx:book&rft.genre=book&req_dat=<sessionid>0</sessionid>&rfe_dat=<accessionnumber>7390570323</accessionnumber>&rft_id=info:oclcnum/7390570323&rft_id=urn:ISBN:978-0-415-27557-6&rft.aulast=Stopford&rft.aufirst=Martin&rft.btitle=Maritime+Economics+3e&rft.date=2009&rft.isbn=978-0-415-27557-6&rft.pub=Routledge&rft.genre=book',
              'elapsed_time': '0:00:00.015365'}}
        self.assertEqual( self.mapper.grab_title(bib_dct), 'Maritime Economics 3e' )
        self.assertEqual( self.mapper.grab_author(bib_dct), 'Stopford, Martin' )
        self.assertEqual( self.mapper.grab_sid(bib_dct), 'info:sid/firstsearch.oclc.org:WorldCat' )
        self.assertEqual( self.mapper.grab_espn(bib_dct), '7390570323' )
        self.assertEqual( self.mapper.grab_isbn(bib_dct), '978-0-415-27557-6' )
        self.assertEqual( self.mapper.grab_date(bib_dct), '2009' )
        self.assertEqual( self.mapper.grab_place(bib_dct), '' )
        self.assertEqual( self.mapper.grab_publisher(bib_dct), 'Routledge' )

    def test_bib_dct_J(self):
        """ Checks mapping of WorlCat oclc# `989593565`. """
        bib_dct = {
 'query': {'date_time': '2019-04-06 10:13:24.926351',
           'url': 'https://library.brown.edu/bib_ourl_api/v1/ourl_to_bib/?ourl=sid%3DFirstSearch%253AWorldCat%26genre%3Dbook%26isbn%3D9783883757346%26title%3DTerritories%2B%253A%2Bislands%252C%2Bcamps%2Band%2Bother%2Bstates%2Bof%2Butopia%26date%3D2003%26aulast%3DBiesenbach%26aufirst%3DKlaus%26id%3Ddoi%253A%26pid%3D989593565%253Cfssessid%253E0%253C%252Ffssessid%253E%26url_ver%3DZ39.88-2004%26rfr_id%3Dinfo%253Asid%252Ffirstsearch.oclc.org%253AWorldCat%26rft_val_fmt%3Dinfo%253Aofi%252Ffmt%253Akev%253Amtx%253Abook%26rft.genre%3Dbook%26req_dat%3D%253Csessionid%253E0%253C%252Fsessionid%253E%26rfe_dat%3D%253Caccessionnumber%253E989593565%253C%252Faccessionnumber%253E%26rft_id%3Dinfo%253Aoclcnum%252F989593565%26rft_id%3Durn%253AISBN%253A9783883757346%26rft.aulast%3DBiesenbach%26rft.aufirst%3DKlaus%26rft.btitle%3DTerritories%2B%253A%2Bislands%252C%2Bcamps%2Band%2Bother%2Bstates%2Bof%2Butopia%26rft.date%3D2003%26rft.isbn%3D9783883757346%26rft.place%3DKo%25CC%2588ln%26rft.pub%3DKo%25CC%2588nig%26rft.genre%3Dbook'},
 'response': {'bib': {'_rfr': 'info:sid/firstsearch.oclc.org:WorldCat',
                      'author': [{'firstname': 'Klaus',
                                  'lastname': 'Biesenbach',
                                  'name': 'Biesenbach, Klaus'}],
                      'end_page': None,
                      'identifier': [{'id': '9783883757346', 'type': 'isbn'},
                                     {'id': '989593565', 'type': 'oclc'}],
                      'issue': None,
                      'pages': None,
                      'place_of_publication': 'Köln',
                      'publisher': 'König',
                      'start_page': None,
                      'title': 'Territories : islands, camps and other states '
                               'of utopia',
                      'type': 'book',
                      'volume': None,
                      'year': '2003'},
              'decoded_openurl': 'sid=FirstSearch:WorldCat&genre=book&isbn=9783883757346&title=Territories+:+islands,+camps+and+other+states+of+utopia&date=2003&aulast=Biesenbach&aufirst=Klaus&id=doi:&pid=989593565<fssessid>0</fssessid>&url_ver=Z39.88-2004&rfr_id=info:sid/firstsearch.oclc.org:WorldCat&rft_val_fmt=info:ofi/fmt:kev:mtx:book&rft.genre=book&req_dat=<sessionid>0</sessionid>&rfe_dat=<accessionnumber>989593565</accessionnumber>&rft_id=info:oclcnum/989593565&rft_id=urn:ISBN:9783883757346&rft.aulast=Biesenbach&rft.aufirst=Klaus&rft.btitle=Territories+:+islands,+camps+and+other+states+of+utopia&rft.date=2003&rft.isbn=9783883757346&rft.place=Köln&rft.pub=König&rft.genre=book',
              'elapsed_time': '0:00:00.017138'}}
        self.assertEqual( self.mapper.grab_title(bib_dct), 'Territories : islands, camps and other states of utopia' )
        self.assertEqual( self.mapper.grab_author(bib_dct), 'Biesenbach, Klaus' )
        self.assertEqual( self.mapper.grab_sid(bib_dct), 'info:sid/firstsearch.oclc.org:WorldCat' )
        self.assertEqual( self.mapper.grab_espn(bib_dct), '989593565' )
        self.assertEqual( self.mapper.grab_isbn(bib_dct), '9783883757346' )
        self.assertEqual( self.mapper.grab_date(bib_dct), '2003' )
        self.assertEqual( self.mapper.grab_place(bib_dct), 'Köln' )
        self.assertEqual( self.mapper.grab_publisher(bib_dct), 'König' )

    def test_bib_dct_K(self):
        """ Checks mapping of WorlCat oclc# `1053904626`. """
        bib_dct = {
 'query': {'date_time': '2019-04-06 10:18:39.101961',
           'url': 'https://library.brown.edu/bib_ourl_api/v1/ourl_to_bib/?ourl=sid%3DFirstSearch%253AWorldCat%26genre%3Dbook%26isbn%3D9781780723723%26title%3DThe%2Binflamed%2Bmind%2B%253A%2Ba%2Bradical%2Bnew%2Bapproach%2Bto%2Bdepression%26date%3D2019%26aulast%3DBullmore%26aufirst%3DEdward%26auinitm%3DT%26id%3Ddoi%253A%26pid%3D1053904626%253Cfssessid%253E0%253C%252Ffssessid%253E%26url_ver%3DZ39.88-2004%26rfr_id%3Dinfo%253Asid%252Ffirstsearch.oclc.org%253AWorldCat%26rft_val_fmt%3Dinfo%253Aofi%252Ffmt%253Akev%253Amtx%253Abook%26rft.genre%3Dbook%26req_dat%3D%253Csessionid%253E0%253C%252Fsessionid%253E%26rfe_dat%3D%253Caccessionnumber%253E1053904626%253C%252Faccessionnumber%253E%26rft_id%3Dinfo%253Aoclcnum%252F1053904626%26rft_id%3Durn%253AISBN%253A9781780723723%26rft.aulast%3DBullmore%26rft.aufirst%3DEdward%26rft.auinitm%3DT%26rft.btitle%3DThe%2Binflamed%2Bmind%2B%253A%2Ba%2Bradical%2Bnew%2Bapproach%2Bto%2Bdepression%26rft.date%3D2019%26rft.isbn%3D9781780723723%26rft.genre%3Dbook'},
 'response': {'bib': {'_rfr': 'info:sid/firstsearch.oclc.org:WorldCat',
                      'author': [{'_minitial': 'T',
                                  'firstname': 'Edward',
                                  'lastname': 'Bullmore',
                                  'name': 'Bullmore, Edward'}],
                      'end_page': None,
                      'identifier': [{'id': '9781780723723', 'type': 'isbn'},
                                     {'id': '1053904626', 'type': 'oclc'}],
                      'issue': None,
                      'pages': None,
                      'place_of_publication': None,
                      'publisher': None,
                      'start_page': None,
                      'title': 'The inflamed mind : a radical new approach to '
                               'depression',
                      'type': 'book',
                      'volume': None,
                      'year': '2019'},
              'decoded_openurl': 'sid=FirstSearch:WorldCat&genre=book&isbn=9781780723723&title=The+inflamed+mind+:+a+radical+new+approach+to+depression&date=2019&aulast=Bullmore&aufirst=Edward&auinitm=T&id=doi:&pid=1053904626<fssessid>0</fssessid>&url_ver=Z39.88-2004&rfr_id=info:sid/firstsearch.oclc.org:WorldCat&rft_val_fmt=info:ofi/fmt:kev:mtx:book&rft.genre=book&req_dat=<sessionid>0</sessionid>&rfe_dat=<accessionnumber>1053904626</accessionnumber>&rft_id=info:oclcnum/1053904626&rft_id=urn:ISBN:9781780723723&rft.aulast=Bullmore&rft.aufirst=Edward&rft.auinitm=T&rft.btitle=The+inflamed+mind+:+a+radical+new+approach+to+depression&rft.date=2019&rft.isbn=9781780723723&rft.genre=book',
              'elapsed_time': '0:00:00.014576'}}
        self.assertEqual( self.mapper.grab_title(bib_dct), 'The inflamed mind : a radical new approach to depression' )
        self.assertEqual( self.mapper.grab_author(bib_dct), 'Bullmore, Edward' )
        self.assertEqual( self.mapper.grab_sid(bib_dct), 'info:sid/firstsearch.oclc.org:WorldCat' )
        self.assertEqual( self.mapper.grab_espn(bib_dct), '1053904626' )
        self.assertEqual( self.mapper.grab_isbn(bib_dct), '9781780723723' )
        self.assertEqual( self.mapper.grab_date(bib_dct), '2019' )
        self.assertEqual( self.mapper.grab_place(bib_dct), '' )
        self.assertEqual( self.mapper.grab_publisher(bib_dct), '' )

    ## end class class Mapper_Test()
