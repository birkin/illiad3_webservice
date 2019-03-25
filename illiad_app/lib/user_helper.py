# -*- coding: utf-8 -*-

import datetime, logging, pprint, random, time
from illiad_app import settings_app
from illiad_app.lib.illiad3.account import IlliadSession
from illiad_app.lib import basic_auth


log = logging.getLogger(__name__)


class CreateUserHandler( object ):
    """ Creates new user. """

    def __init__( self ):
        self.request_id = random.randint( 1111, 9999 )  # to follow logic if simultaneous hits
        self.required_elements = [ 'auth_id', 'email' ]

    def data_check( self, request ):
        """ Checks data.
            Called by views.create_user() """
        log.debug( '%s - request.__dict__, `%s`' % (self.request_id, pprint.pformat(request.__dict__)) )
        log.debug( '%s - request.POST, `%s`' % (self.request_id, pprint.pformat(request.POST)) )
        ## auth-key check
        auth_key_good = False
        if 'auth_key' in request.POST.keys():
            if request.POST['auth_key'] == settings_app.API_KEY:
                source_ip = request.META.get('REMOTE_ADDR', 'unavailable')
                if source_ip in settings_app.LEGIT_IPS:
                    auth_key_good = True
        log.debug( 'auth_key_good, `%s`' % auth_key_good )
        if auth_key_good is False:
            return 'invalid'
        ## data-check
        data_good = False
        user_keys = list( request.POST.keys() )
        check_flag = 'init'
        for element in self.required_elements:
            if element not in user_keys:
                log.debug( 'missing element, `%s`; will return False' % element )
                check_flag = 'failed'
                break
        if check_flag == 'init':
            data_good  = True
        log.debug( 'data_good, `%s`' % data_good )
        if data_good is False:
            return 'invalid'
        return  # never gets here

    ## end class CreateUserHandler()


class CheckUserHelper( object ):
    """ Checks user status -- meaning 'registered', 'blocked', etc. """

    def __init__( self ):
        self.request_id = random.randint( 1111, 9999 )  # to follow logic if simultaneous hits

    # def data_check( self, request ):
    #     """ Checks data.
    #         Called by views.check_user() """
    #     log.debug( '%s - request.GET, `%s`' % (self.request_id, request.GET) )
    #     return_val = 'invalid'
    #     if 'user' in request.GET.keys():
    #         return_val = 'valid'
    #     log.debug( '%s - return_val, `%s`' % (self.request_id, return_val) )
    #     return return_val

    def data_check( self, request ):
        """ Checks data.
            Called by views.check_user() """
        log.debug( '%s - request.GET, `%s`' % (self.request_id, request.GET) )
        return_val = 'invalid'
        if 'user' in request.GET.keys():
            log.debug( 'user param exists' )
            if basic_auth.check_basic_auth( request ) is True:
                return_val = 'valid'
        log.debug( '%s - return_val, `%s`' % (self.request_id, return_val) )
        return return_val

    def manage_check( self, request, start_time ):
        """ Runs login and response evaluation.
            Called by views.check_user() """
        user = request.GET['user']
        log.debug( '%s - user, `%s`' % (self.request_id, user) )
        illiad_session = IlliadSession( settings_app.ILLIAD_REMOTE_AUTH_URL, settings_app.ILLIAD_REMOTE_AUTH_KEY, user )
        login_response_dct = illiad_session.login()
        data_dct = self.prep_data_dct( login_response_dct )
        output_dct = self.prep_output_dct( start_time, request, data_dct )
        return output_dct

    def prep_data_dct( self, login_response_dct ):
        """ Takes values from login_response_dct and prepares data-dct to be returned.
            Called by manage_check() """
        data_dct = {'authenticated': None, 'registered': None, 'blocked': None, 'disavowed': None, 'interpreted_new_user': None}
        for key in login_response_dct:
            if key in data_dct.keys():  # ignores session_id
                data_dct[key] = login_response_dct[key]
        data_dct = self.determine_new_user( data_dct )
        log.debug( '%s - data_dct, ```%s```' % (self.request_id, pprint.pformat(data_dct)) )
        return data_dct

    def determine_new_user( self, data_dct ):
        """ Adds new-user assessment from raw login-response.
            Called by prep_data_dct() """
        data_dct['interpreted_new_user'] = False
        if data_dct['blocked'] == None:
            if data_dct['disavowed'] == None:
                if data_dct['registered'] == None:
                    data_dct['interpreted_new_user'] == True
        log.debug( '%s - data_dct, ```%s```' % (self.request_id, pprint.pformat(data_dct)) )
        return data_dct

    def prep_output_dct( self, start_time, request, data_dct ):
        """ Preps output-dct.
            Called by manage_check() """
        output_dct = {
            'request': {
                'url': '%s://%s%s?%s' % (
                    request.scheme,
                    request.META.get( 'HTTP_HOST', '127.0.0.1' ),  # HTTP_HOST doesn't exist for client-tests
                    request.META['PATH_INFO'],
                    request.META['QUERY_STRING'] ),  # REQUEST_URI contains querystring but doesn't exist via run-server
                'timestamp': str( start_time ) },
            'response': self.prep_response_segment( start_time, data_dct ) }
        log.debug( '%s - output_dct, ```%s```' % (self.request_id, pprint.pformat(output_dct)) )
        return output_dct

    def prep_response_segment( self, start_time, data_dct ):
        """ Returns response part of context dct.
            Called by prep_output_dct() """
        response_dct = {
            'elapsed_time': str( datetime.datetime.now() - start_time ),
            'status_data': data_dct
            }
        return response_dct

    ## end class CheckUserHelper()
