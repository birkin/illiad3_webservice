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

        api_response_dct = self.run_check( request )

        data_dct = self.prep_data_dct( api_response_dct, user )
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



    def prep_data_dct( self, api_response_dct, submitted_username ):
        """ Takes values from api_response_dct and prepares data-dct to be returned.
            The output_dct here is designed to maintain compatibility with calling code.
            If this were to be done over, there wouldn't be both (now-identical) `authenticated` and `registered` categories.
            Called by manage_check() """
        output_dct = {'authenticated': None, 'registered': None, 'blocked': None, 'disavowed': None, 'interpreted_new_user': None}
        if self.check_registered( api_response_dct, submitted_username ) is True:  # most common by _far_
            output_dct = {'authenticated': True, 'registered': True, 'blocked': False, 'disavowed': False, 'interpreted_new_user': False}
        elif self.check_blocked( api_response_dct ) is True:
            output_dct = {'authenticated': True, 'registered': True, 'blocked': True, 'disavowed': False, 'interpreted_new_user': False}
        elif self.check_disavowed( api_response_dct ) is True:
            output_dct = {'authenticated': False, 'registered': False, 'blocked': False, 'disavowed': True, 'interpreted_new_user': False}
        elif self.check_newuser( api_response_dct ) is True:
            output_dct = {'authenticated': False, 'registered': False, 'blocked': False, 'disavowed': False, 'interpreted_new_user': True}
        else:
            log.warning( '%s - should not get here' % self.request_id )
        log.debug( '%s - output_dct, ```%s```' % (self.request_id, pprint.pformat(output_dct)) )
        return output_dct



    def check_registered( self, api_response_dct, submitted_username ):
        """ Assesses if user is registered from cloud-api response.
            Called by prep_data_dct() """
        registered = False
        if 'UserName' in api_response_dct and api_response_dct['UserName'] == submitted_username:
            registered = True
        log.debug( '%s - registered, `%s`' % (self.request_id, registered) )
        return registered



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
