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
        log.debug( '%s - status_code, `%s`' % (self.request_id, r.status_code) )
        bib_json_dct = r.json()
        log.debug( '%s - bib-dct, ```%s```' % (self.request_id, pprint.pformat(bib_json_dct)) )
        notes = self.extract_notes( decoded_openurl_querystring )
        illiad_params = self.map_to_illiad_keys( bib_json_dct, notes )
        1/0

    def decode_openurl_querystring( self, querystring ):
        """ Runs one decode on the querystring.
            Called by parse_openurl() """
        decoded_querystring = urllib.parse.unquote( querystring )
        log.debug( '%s - decoded_querystring, ```%s```' % (self.request_id, decoded_querystring) )
        return decoded_querystring

    # def decode_openurl_querystring( self, querystring ):
    #     """ Fully decodes the querystring.
    #         Called by parse_openurl() """
    #     ( last_try, decoded_querystring, flag ) = ( 'init', 'init', 'continue' )
    #     while flag == 'continue':
    #         decoded_querystring = urllib.parse.unquote( querystring )
    #         if decoded_querystring == last_try:
    #             log.debug( '%s - decoding done' % self.request_id )
    #             flag = 'stop'
    #         else:
    #             last_try = decoded_querystring
    #             log.debug( '%s - will decode once more; decoded_querystring currently, ```%s```' % (self.request_id, decoded_querystring) )
    #     log.debug( '%s - final decoded_querystring, ```%s```' % (self.request_id, decoded_querystring) )
    #     return decoded_querystring

    def extract_notes( self, decoded_openurl_querystring ):
        """ Returns notes-dct.
            Called by parse_openurl() """
        notes = 'no notes'
        parts_dct = urllib.parse.parse_qs( decoded_openurl_querystring )  # <https://pymotw.com/3/urllib.parse/>
        log.debug( '%s - parts_dct, ```%s```' % (self.request_id, pprint.pformat(parts_dct)) )
        if 'notes' in parts_dct.keys():
            notes = parts_dct['notes'][0]  # all values are in list
        log.debug( '%s - notes, ```%s```' % (self.request_id, notes) )
        return notes

    def map_to_illiad_keys( self, bib_json_dct, notes ):
        """ Returns dct using illiad-cloud-api keys.
            Called by parse_openurl() """
        # defaults = {
        #     'RequestType': 'Book',
        #     'ProcessType' : 'Borrowing'
        #     }
        # user = {
        #     "Username" : None,  # fill later
        #     }
        mapper = Mapper( self.request_id )
        item = {
            'ESPNumber': mapper.grab_espn( bib_json_dct ),  # OCLC number
            'ISSN': mapper.grab_isbn( bib_json_dct ),  # really ISBN
            'LoanAuthor': mapper.grab_author( bib_json_dct ),
            'LoanDate': mapper.grab_date( bib_json_dct ),
            'LoanPlace': mapper.grab_place( bib_json_dct ),
            'LoanPublisher': mapper.grab_publisher( bib_json_dct ),
            'LoanTitle': mapper.grab_title( bib_json_dct ),
            'Notes': notes,
            }
        log.debug( '%s - illiad_dct, ```%s```' % (self.request_id, pprint.pformat(item)) )
        return item

    ## end class ILLiadParamBuilder()


class Mapper( object ):
    """ Extracts necessary values from bib_dct. """

    def __init__( self, request_id ):
        # self.request_id = random.randint( 1111, 9999 )  # to follow logic if simultaneous hits
        self.request_id = request_id

    def grab_espn( self, bib_dct ):
        """ Returns oclc number.
            Called by ILLiadParamBuilder.map_to_illiad_keys() """
        oclc = ''
        try:
            pass
        except Exception as e:
            log.error( '%s - repr(e)' )
        log.debug( '%s - oclc, `%s`' % (self.request_id, oclc) )
        return oclc

    def grab_isbn( self, bib_dct ):
        """ Returns isbn.
            Called by ILLiadParamBuilder.map_to_illiad_keys() """
        isbn = ''
        try:
            identifiers = bib_dct['response']['bib']['identifier']
            for element_dct in identifiers:
                if element_dct['type'] == 'isbn':
                    isbn = element_dct['id']
                    break
        except Exception as e:
            log.error( '%s - repr(e)' )
        log.debug( '%s - isbn, `%s`' % (self.request_id, isbn) )
        return isbn

    def grab_author( self, bib_dct ):
        """ Returns author.
            Called by ILLiadParamBuilder.map_to_illiad_keys() """
        author = ''
        try:
            pass
        except Exception as e:
            log.error( '%s - repr(e)' )
        log.debug( '%s - author, `%s`' % (self.request_id, author) )
        return author

    def grab_date( self, bib_dct ):
        """ Returns date number.
            Called by ILLiadParamBuilder.map_to_illiad_keys() """
        date = ''
        try:
            pass
        except Exception as e:
            log.error( '%s - repr(e)' )
        log.debug( '%s - date, `%s`' % (self.request_id, date) )
        return date

    def grab_place( self, bib_dct ):
        """ Returns place number.
            Called by ILLiadParamBuilder.map_to_illiad_keys() """
        place = ''
        try:
            pass
        except Exception as e:
            log.error( '%s - repr(e)' )
        log.debug( '%s - place, `%s`' % (self.request_id, place) )
        return place

    def grab_publisher( self, bib_dct ):
        """ Returns publisher number.
            Called by ILLiadParamBuilder.map_to_illiad_keys() """
        publisher = ''
        try:
            pass
        except Exception as e:
            log.error( '%s - repr(e)' )
        log.debug( '%s - publisher, `%s`' % (self.request_id, publisher) )
        return publisher

    def grab_title( self, bib_dct ):
        """ Returns title number.
            Called by ILLiadParamBuilder.map_to_illiad_keys() """
        title = ''
        try:
            title = bib_dct['response']['bib']['title']
        except Exception as e:
            log.error( '%s - repr(e)' )
        log.debug( '%s - title, `%s`' % (self.request_id, title) )
        return title

    ## end class Mapper()
