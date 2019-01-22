# -*- coding: utf-8 -*-

import logging, random


log = logging.getLogger(__name__)


class CheckStatusHandler( object ):

    def __init__( self ):
        self.request_id = random.randint( 1111, 9999 )  # to follow logic if simultaneous hits

    def data_check( self, request ):
        """ Checks data.
            Called by views.check_status_v2() """
        log.debug( '%s - starting check_params()' % self.request_id )
        log.debug( '%s - request.GET, `%s`' % (self.request_id, request.GET) )
        return_val = 'invalid'
        if 'users' in request.GET.keys():
            return_val = 'valid'
        log.debug( '%s - return_val, `%s`' % (self.request_id, return_val) )
        return return_val

    ## end class CheckStatusHandler()
