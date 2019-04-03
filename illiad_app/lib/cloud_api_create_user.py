# -*- coding: utf-8 -*-

import datetime, logging, os, pprint, random
import requests
from illiad_app import settings_app


log = logging.getLogger(__name__)


class CloudCreateUserHandler( object ):
    """ Creates new user via official illiad cloud api. """

    def __init__( self ):
        self.request_id = random.randint( 1111, 9999 )  # to follow logic if simultaneous hits
        self.required_elements = [ 'auth_id', 'department', 'email', 'first_name', 'last_name', 'phone', 'status' ]

    def data_check( self, request ):
        """ Checks data.
            Called by views.cloud_create_user() """
        ## auth-key check
        summary_check = 'invalid'
        if self.auth_key_good( request ) is True:
            ## data check
            if self.data_good( request ) is True:
                summary_check = 'valid'
        log.debug( '%s - summary_check, `%s`' % (self.request_id, summary_check) )
        return summary_check

    def auth_key_good( self, request ):
        """ Checks the auth_key and ip.
            Called by data_check() """
        auth_key_check = False
        if 'auth_key' in request.POST.keys():
            if request.POST['auth_key'] == settings_app.API_KEY:
                log.debug( '%s - auth_key ok' % self.request_id )
                source_ip = request.META.get('REMOTE_ADDR', 'unavailable')
                log.debug( '%s - source_ip, ```%s```' % (self.request_id, source_ip) )
                if source_ip in settings_app.LEGIT_IPS:
                    log.debug( '%s - source_ip ok' % self.request_id )
                    auth_key_check = True
        log.debug( '%s - auth_key_check, `%s`' % (self.request_id, auth_key_check) )
        return auth_key_check

    def data_good( self, request ):
        """ Checks for required params.
            Called by data_check() """
        ( data_good_check, user_keys, check_flag ) = ( False, list(request.POST.keys()), 'init' )
        for element in self.required_elements:
            if element not in user_keys:
                log.debug( '%s - missing element, `%s`; will return False' % (self.request_id, element) )
                check_flag = 'failed'
                break
        if check_flag == 'init':
            data_good_check  = True
        log.debug( '%s - data_good_check, `%s`' % (self.request_id, data_good_check) )
        return data_good_check

    def create_user( self, request ):
        """ Creates new user via official illiad cloud api.
            Called by views.cloud_create_user() """
        usr_dct = dict( request.POST.items() )
        params = {
            ## non-user
            'DeliveryMethod': 'Hold for Pickup',
            'LoanDeliveryMethod': 'Hold for Pickup',
            'NotificationMethod': 'Electronic',
            'Web': True,
            # 'AuthType': 'Default',  # don't send, will be set to `Default`
            ## user
            'Username': usr_dct['auth_id'],
            'FirstName': usr_dct['first_name'],
            'LastName': usr_dct['last_name'],
            'EmailAddress': usr_dct['email'],
            'Phone': usr_dct['phone'],
            'Status': usr_dct['status'],  # "type, eg `Undergraduate Student`"
            'Department': usr_dct['department'],
            'Address': '',
            'Address2': '',
            'City': '',
            'State': '',
            'Zip': '',
            # 'ExternalUserId': '',  # don't send
            # 'PlainTextPassword': '',  # don't send
            }
        log.debug( '%s - params, ```%s```' % (self.request_id, pprint.pformat(params)) )

        url = '%s%s' % ( settings_app.ILLIAD_API_URL, 'Users' )  # root url contains ending-slash
        log.debug( '%s - url, ```%s```' % (self.request_id, url) )

        headers = {
            'Accept-Type': 'application/json; charset=utf-8',
            'ApiKey': os.environ['ILLIAD_WS__OFFICIAL_ILLIAD_API_KEY']
            }
        try:
            r = requests.post( url, data=params, headers=headers, timeout=60, verify=True )
            response_dct = r.json()
            log.debug( '%s - response, ```%s```' % (self.request_id, pprint.pformat(response_dct)) )
            return response_dct
        except Exception as e:
            log.error( '%s - exception creating new user, ```%s```' % (self.request_id, repr(e)) )

    def prep_output_dct( self, start_time, request, data_dct ):
        """ Preps output-dct.
            Called by views.cloud_create_user() """
        params = dict( request.POST.items() )
        params.pop( 'auth_key', None )
        output_dct = {
            'request': {
                'url': '%s://%s%s' % (
                    request.scheme, request.META.get('HTTP_HOST', '127.0.0.1'), request.META['PATH_INFO'] ),  # HTTP_HOST doesn't exist for client-tests
                'params': params,
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

    ## end class class CloudCreateUserHandler()




# import os, requests

# params = {
#   "Username" : "bdoe",
#   "ExternalUserId": "123456789",
#   "FirstName":"Bailey",
#   "LastName":"Doe",
#   "EmailAddress" : "test@test.test" ,
#   "DeliveryMethod" : "Hold for Pickup",
#   "LoanDeliveryMethod" : "Mail to Address",
#   "NotificationMethod" : "Electronic",
#   "Phone" : "123-456-7890",
#   "Status" : "Graduate",
#   "PlainTextPassword": "zzzzzzzzzzzz",
#   "AuthType" : "ILLiad",
#   "Department" : "Music",
#   "Web" : True,
#   "Address" : "the address",
#   "Address2" : "extra address info",
#   "City" : "the city",
#   "State" : "RI",
#   "Zip" : "12345"
# }

# url = '%s%s' % ( os.environ['ILLIAD_WS__OFFICIAL_ILLIAD_API_URL'], 'Users' )  # root url contains ending-slash
# print( 'url, ```%s```' % url )

# headers = {
#     'Accept-Type': 'application/json; charset=utf-8',
#     'ApiKey': os.environ['ILLIAD_WS__OFFICIAL_ILLIAD_API_KEY']
#     }

# r = requests.post( url, data=params, headers=headers, timeout=60, verify=True )
# print( r.status_code )

# print( r.content )
