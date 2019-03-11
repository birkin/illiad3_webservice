# -*- coding: utf-8 -*-

"""
Submits ILLiad request via hitting the ILLiad API instead of simulating browser GETs and POSTs.
Implemented in preparation for ILLiad cloud switch-over.
"""

import datetime, logging, pprint, random, time
from illiad_app import settings_app


log = logging.getLogger(__name__)


class MakeBookRequestManager( object ):
    """ `Book` hardcoded for now, for easyBorrow requests.
        Will later do the `Article` manager for easyAccess requests, and then refactor for common features. """

    def __init__( self, request_id ):
        # self.request_id = random.randint( 1111, 9999 )  # to follow logic if simultaneous hits
        self.request_id = request_id

    def check_validity( self, request ):
        """ Checks post, auth_key, ip, & params.
            Called by views.make_request_v3() """
        log.debug( '%s - starting check_validity()' % self.request_id )
        return_val = False
        if request.method == 'POST':
            if self.check_params( request ) is True:
                if request.POST['auth_key'] == self.API_KEY:
                    return_val = True
                else:
                    log.debug( '%s - ip, `%s`' % (self.request_id, request.META.get('REMOTE_ADDR', 'unavailable')) )
        log.debug( '%s - return_val, `%s`' % (self.request_id, return_val) )
        return return_val

    ## end class MakeRequestManager()
