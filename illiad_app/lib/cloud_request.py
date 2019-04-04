# -*- coding: utf-8 -*-

"""
Submits ILLiad request via hitting the ILLiad API instead of simulating browser GETs and POSTs.
Implemented in preparation for ILLiad cloud switch-over.
"""

import datetime, logging, pprint, random, time, urllib.parse
import requests
from illiad_app import settings_app


log = logging.getLogger(__name__)


class BookRequestHandler( object ):
    """ `Book` hardcoded for now, for easyBorrow requests.
        Will later do the `Article` manager for easyAccess requests, and then refactor for common features. """

    def __init__( self, request_id ):
        # self.request_id = random.randint( 1111, 9999 )  # to follow logic if simultaneous hits
        self.request_id = request_id
        self.API_KEY = settings_app.API_KEY

    def check_validity( self, request ):
        """ Checks post, auth_key, ip, & params.
            Called by views.cloud_book_request() """
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
        param_builder = ILLiadParamBuilder( self.request_id )
        open_url_params = param_builder.parse_openurl( request.POST['openurl'] )
        log.debug( '%s - output_dct, `%s`' % (self.request_id, output_dct) )
        return output_dct

    ## end class BookRequestHandler()


class ILLiadParamBuilder( object ):
    """ Handles conversion of openurl and mapping to illiad-cloud-api keys. """

    def __init__( self, request_id ):
        # self.request_id = random.randint( 1111, 9999 )  # to follow logic if simultaneous hits
        self.request_id = request_id
        self.OURL_API_URL = 'https://library.brown.edu/bib_ourl_api/v1/ourl_to_bib/'

    def parse_openurl( self, openurl ):
        """ Prepares ILLiad-compatible params.
            Called by manage_request() """
        log.debug( '%s - initial openurl, ```%s```' % (self.request_id, openurl) )
        decoded_openurl_querystring = self.decode_openurl_querystring( openurl )
        params = { 'ourl': decoded_openurl_querystring }
        r = requests.get( self.OURL_API_URL, params=params, timeout=30, verify=True )
        log.debug( '%s - full url, ```%s```' % (self.request_id, r.url) )
        log.debug( '%s - status_code, `%s`; content-response, ```%s```' % (self.request_id, r.status_code, r.content.decode('utf-8')) )
        illiad_params = self.map_to_illiad_keys( r.json() )
        1/0

    def decode_openurl_querystring( self, querystring ):
        """ Fully decodes the querystring.
            Called by parse_openurl() """
        ( last_try, decoded_querystring, flag ) = ( 'init', 'init', 'continue' )
        while flag == 'continue':
            decoded_querystring = urllib.parse.unquote( querystring )
            if decoded_querystring == last_try:
                log.debug( '%s - decoding done' % self.request_id )
                flag = 'stop'
            else:
                last_try = decoded_querystring
                log.debug( '%s - will decode once more; decoded_querystring currently, ```%s```' % (self.request_id, decoded_querystring) )
        log.debug( '%s - final decoded_querystring, ```%s```' % (self.request_id, decoded_querystring) )
        return decoded_querystring

    def map_to_illiad_keys( self, bib_json_dct ):
        """ Returns dct using illiad-cloud-api keys.
            Called by parse_openurl() """
        defaults = {
            'RequestType': 'Book',
            'ProcessType' : 'Borrowing'
            }
        user = {
            "Username" : None,  # fill later
            }
        item = {
            'ESPNumber'  # OCLC number
            'ISSN'  # really ISBN
            'LoanAuthor'
            'LoanDate'
            'LoanPlace'
            'LoanPublisher'
            'LoanTitle'
            'Notes'
            }

    ## end class ILLiadParamBuilder()
