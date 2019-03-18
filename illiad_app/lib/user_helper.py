# -*- coding: utf-8 -*-

import datetime, logging, pprint, random, time
from illiad_app import settings_app
# from illiad_app.lib.illiad3.account import Status as LibStatusModule
from illiad_app.lib.illiad3.account import IlliadSession


log = logging.getLogger(__name__)


class UserHelper( object ):

    def __init__( self ):
        self.request_id = random.randint( 1111, 9999 )  # to follow logic if simultaneous hits
        self.output_dct = {
            'user': None,
            'response': {'authenticated': None, 'registered': None, 'blocked': None, 'disavowed': None}
            }

    def data_check( self, request ):
        """ Checks data.
            Called by views.check_user() """
        log.debug( '%s - request.GET, `%s`' % (self.request_id, request.GET) )
        return_val = 'invalid'
        if 'user' in request.GET.keys():
            return_val = 'valid'
        log.debug( '%s - return_val, `%s`' % (self.request_id, return_val) )
        return return_val

    def manage_check( self, request, start_time ):
        """ Runs login and response evaluation.
            Called by views.check_user() """
        user = request.GET['user']
        log.debug( '%s - user, `%s`' % (self.request_id, user) )
        self.output_dct['user'] = user
        illiad_session = IlliadSession( settings_app.ILLIAD_REMOTE_AUTH_URL, settings_app.ILLIAD_REMOTE_AUTH_KEY, user )
        login_response_dct = illiad_session.login()
        for key in login_response_dct:
            if key in self.output_dct['response'].keys():  # ignores session_id
                self.output_dct['response'][key] = login_response_dct[key]
        log.debug( '%s - output_dct, ```%s```' % (self.request_id, pprint.pformat(self.output_dct)) )
        return self.output_dct

        ## TODO: timestamp
