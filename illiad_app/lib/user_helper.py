# -*- coding: utf-8 -*-

import datetime, logging, pprint, random, time
from illiad_app import settings_app
# from illiad_app.lib.illiad3.account import Status as LibStatusModule
from illiad_app.lib.illiad3.account import IlliadSession


log = logging.getLogger(__name__)


class UserHelper( object ):

    def __init__( self ):
        self.request_id = random.randint( 1111, 9999 )  # to follow logic if simultaneous hits
        # self.output_dct = None
        # self.output_dct = {
        #     'user': None,
        #     'response': {'authenticated': None, 'registered': None, 'blocked': None, 'disavowed': None}
        #     }

    def data_check( self, request ):
        """ Checks data.
            Called by views.check_user() """
        log.debug( '%s - request.GET, `%s`' % (self.request_id, request.GET) )
        return_val = 'invalid'
        if 'user' in request.GET.keys():
            return_val = 'valid'
        log.debug( '%s - return_val, `%s`' % (self.request_id, return_val) )
        return return_val

    # def manage_check( self, request, start_time ):
    #     """ Runs login and response evaluation.
    #         Called by views.check_user() """
    #     user = request.GET['user']
    #     log.debug( '%s - user, `%s`' % (self.request_id, user) )
    #     self.output_dct['user'] = user
    #     illiad_session = IlliadSession( settings_app.ILLIAD_REMOTE_AUTH_URL, settings_app.ILLIAD_REMOTE_AUTH_KEY, user )
    #     login_response_dct = illiad_session.login()
    #     for key in login_response_dct:
    #         if key in self.output_dct['response'].keys():  # ignores session_id
    #             self.output_dct['response'][key] = login_response_dct[key]
    #     log.debug( '%s - output_dct, ```%s```' % (self.request_id, pprint.pformat(self.output_dct)) )
    #     return self.output_dct

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
        data_dct = {'authenticated': None, 'registered': None, 'blocked': None, 'disavowed': None}
        for key in login_response_dct:
            if key in data_dct.keys():  # ignores session_id
                data_dct[key] = login_response_dct[key]
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
        log.debug( 'initialized output_dct, ```%s```' % pprint.pformat(output_dct) )
        return output_dct

    def prep_response_segment( self, start_time, data_dct ):
        """ Returns response part of context dct.
            Called by prep_output_dct() """
        response_dct = {
            'elapsed_time': str( datetime.datetime.now() - start_time ),
            'status_data': data_dct
            }
        return response_dct

    ## end class UserHelper()
