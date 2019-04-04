# -*- coding: utf-8 -*-

"""
Submits ILLiad request via hitting the ILLiad API instead of simulating browser GETs and POSTs.
Implemented in preparation for ILLiad cloud switch-over.
"""

import datetime, logging, pprint, random, time
from illiad_app import settings_app


log = logging.getLogger(__name__)


class BookRequestHandler( object ):
    """ `Book` hardcoded for now, for easyBorrow requests.
        Will later do the `Article` manager for easyAccess requests, and then refactor for common features. """

    def __init__( self, request_id ):
        # self.request_id = random.randint( 1111, 9999 )  # to follow logic if simultaneous hits
        self.request_id = request_id

    def check_validity( self, request ):
        """ Checks post, auth_key, ip, & params.
            Called by views.cloud_book_request() """
        log.debug( '%s - starting check_validity()' % self.request_id )
        return_val = False
        if request.method == 'POST':
            if self.check_params( request ) is True:
                if request.POST['auth_key'] == settings_app.API_KEY:
                    return_val = True
                else:
                    log.debug( '%s - ip, `%s`' % (self.request_id, request.META.get('REMOTE_ADDR', 'unavailable')) )
        log.debug( '%s - return_val, `%s`' % (self.request_id, return_val) )
        return return_val

    def check_params( self, request ):
        """ Checks params.
            Called by check_validity() """
        log.debug( '%s - request.POST, `%s`' % (self.request_id, request.POST) )
        return_val = None
        for param in [ 'auth_key', 'openurl', 'request_id', 'username' ]:
            log.debug( '%s - on param, `%s`' % (self.request_id, param) )
            if param not in request.POST.keys():
                return_val = False
                break
        return_val = True if ( return_val is None ) else False
        log.debug( '%s - return_val, `%s`' % (self.request_id, return_val) )
        return return_val

    def manage_request( self, request):
        """ - Parses openurl
            - Prepares other params.
            - Submits request to illiad-cloud-api transaction endpoint.
            - Prepares response.
            Called by views.cloud_book_request() """
        output_dct = { 'status': None, 'transaction_number': None, 'raw_data': None }
        open_url_params = self.parse_openurl( request.POST['openurl'] )
        log.debug( '%s - output_dct, `%s`' % (self.request_id, output_dct) )
        return output_dct

    ## end class BookRequestHandler()
