# -*- coding: utf-8 -*-

import base64, json, random
from . import settings_app
from django.test import Client, TestCase
from illiad_app.lib.cloud_request import Mapper


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
    #     # response = c.post( '/cloud_create_user/', params )
    #     response = c.post( '/create_user/', params )
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
            { 'auth_key': settings_app.TEST_AUTH_KEY,
                'openurl': 'isbn=9780857021052&title=The%20SAGE%20Handbook%20of%20Remote%20Sensing&notes=p.barcode%2C+%6021236009704581%60+--+volumes%2C+%60N%2FA%60',
                'request_id': str(random.randint(1111, 9999)),
                'username': settings_app.TEST_EXISTING_GOOD_USER }
            )
        self.assertEqual( 200, response.status_code )
        response_dct = json.loads( response.content )
        self.assertEqual( [u'status', u'transaction_number'], sorted(response_dct.keys()) )
        self.assertEqual( 'submission_successful', response_dct['status'] )

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
        """ Checks mapping of FirstSearch oclc# 254605206. """
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
        """ Checks mapping of BUL:Josiah:b8160392. """
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
        """ Checks mapping of WorldCat oclc# 918241430. """
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
