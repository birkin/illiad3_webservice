# -*- coding: utf-8 -*-

import datetime, logging, os, pprint, random
import requests
from illiad_app import settings_app
from illiad_app.lib import basic_auth


log = logging.getLogger(__name__)


class CloudCheckUserHandler( object ):
    """ Creates user-status ('registered', 'new-user', etc.) via official illiad cloud api. """

    def __init__( self ):
        self.request_id = random.randint( 1111, 9999 )  # to follow logic if simultaneous hits
        self.required_elements = [ 'auth_id', 'department', 'email', 'first_name', 'last_name', 'phone', 'status' ]

    def data_check( self, request ):
        """ Checks data.
            Called by views.cloud_check_user() """
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
            Called by views.cloud_check_user() """
        user = request.GET['user']
        log.debug( '%s - user, `%s`' % (self.request_id, user) )

        login_response_dct = self.run_check( request )

        log.debug( 'login_response_dct, ```%s```' % pprint.pformat(login_response_dct) )
        data_dct = self.prep_data_dct( login_response_dct )
        output_dct = self.prep_output_dct( start_time, request, data_dct )
        return output_dct



    def run_check( self, request ):
        """ Hits cloud-api.
            Called by manage_check() """
        output_dct = { 'error_message': None, 'status_code': None }
        status_code = 'init'
        url = '%s%s/%s' % ( settings_app.ILLIAD_API_URL, 'Users', request.GET['user'] )  # root url contains ending-slash
        log.debug( 'url, ```%s```' % url )
        headers = {
            'Accept-Type': 'application/json; charset=utf-8',
            'ApiKey': os.environ['ILLIAD_WS__OFFICIAL_ILLIAD_API_KEY']
            }

        try:
            r = requests.get( url, headers=headers, timeout=60, verify=True )
            log.debug( 'status_code, `%s`; content-response, ```%s```' % (r.status_code, r.content.decode('utf-8')) )
        except Exception as e:
            message = 'exception making request, ```%s```' % repr(e)
            log.error( '%s - %s' % (self.request_id, message) )
            output_dct['error_message'] = message
            log.debug( 'output_dct, ```%s```' % pprint.pformat(output_dct) )
            return output_dct

        try:
            jdct_response = r.json()
        except Exception as e:
            message = 'exception reading response, ```%s```' % repr(e)
            log.error( '%s - %s' % (self.request_id, message) )
            output_dct['error_message'] = message
            output_dct['status_code'] = r.status_code
            log.debug( 'output_dct, ```%s```' % pprint.pformat(output_dct) )
            return output_dct

        output_dct.update( jdct_response )  # if here, we have a jdct_response
        log.debug( 'output_dct, ```%s```' % pprint.pformat(output_dct) )
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
        if data_dct['authenticated'] == True:
            if data_dct['blocked'] == None:
                if data_dct['disavowed'] == None:
                    if data_dct['registered'] == None or data_dct['registered'] == False:
                        data_dct['interpreted_new_user'] = True
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

    ## end class class CloudCheckUserHandler()
