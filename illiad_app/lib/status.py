# -*- coding: utf-8 -*-

import logging, pprint, random, time
from illiad_app import settings_app
from illiad_app.lib.illiad3.account import Status as LibStatusModule


log = logging.getLogger(__name__)
status_checker = LibStatusModule( settings_app.ILLIAD_REMOTE_AUTH_URL, settings_app.ILLIAD_REMOTE_AUTH_KEY )


class CheckStatusHandler( object ):

    def __init__( self ):
        self.request_id = random.randint( 1111, 9999 )  # to follow logic if simultaneous hits

    def data_check( self, request ):
        """ Checks data.
            Called by views.check_status_v2() """
        log.debug( '%s - request.GET, `%s`' % (self.request_id, request.GET) )
        return_val = 'invalid'
        if 'users' in request.GET.keys():
            return_val = 'valid'
        log.debug( '%s - return_val, `%s`' % (self.request_id, return_val) )
        return return_val

    def check_statuses( self, request ):
        """ Handles status check(s).
            Called by views.check_status_v2() """
        users = request.GET['users']
        log.debug( '%s - users, ```%s```' % (self.request_id, users) )
        user_list = users.split( ',' )
        log.debug( '%s - user_list, ```%s```' % (self.request_id, user_list) )
        result_dct = {}
        for user in user_list:
            result_dct[user] = status_checker.check_user_status( user )
            time.sleep( .5 )
        log.debug( '%s - result_dct, ```%s```' % (self.request_id, pprint.pformat(result_dct)) )
        return result_dct

    ## end class CheckStatusHandler()
