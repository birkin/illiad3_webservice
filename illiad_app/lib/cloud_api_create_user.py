# -*- coding: utf-8 -*-

import logging, random
from illiad_app import settings_app


log = logging.getLogger(__name__)


class CloudCreateUserHandler( object ):
    """ Creates new user via official illiad cloud api. """

    def __init__( self ):
        self.request_id = random.randint( 1111, 9999 )  # to follow logic if simultaneous hits
        self.required_elements = [ 'auth_id', 'department', 'email', 'first_name', 'last_name', 'phone', 'status' ]

    def data_check( self, request ):
        """ Checks data.
            Called by views.create_user() """
        ## auth-key check
        summary_check = 'invalid'
        if self.auth_key_good( request ) is True:
            ## data check
            if self.data_good( request ) is True:
                summary_check = 'valid'
        log.debug( 'summary_check, `%s`' % summary_check )
        return summary_check

    def auth_key_good( self, request ):
        """ Checks the auth_key and ip.
            Called by data_check() """
        auth_key_check = False
        if 'auth_key' in request.POST.keys():
            if request.POST['auth_key'] == settings_app.API_KEY:
                log.debug( 'auth_key ok' )
                source_ip = request.META.get('REMOTE_ADDR', 'unavailable')
                log.debug( 'source_ip, ```%s```' % source_ip )
                if source_ip in settings_app.LEGIT_IPS:
                    log.debug( 'source_ip ok' )
                    auth_key_check = True
        log.debug( 'auth_key_check, `%s`' % auth_key_check )
        return auth_key_check

    def data_good( self, request ):
        """ Checks for required params.
            Called by data_check() """
        ( data_good_check, user_keys, check_flag ) = ( False, list(request.POST.keys()), 'init' )
        for element in self.required_elements:
            if element not in user_keys:
                log.debug( 'missing element, `%s`; will return False' % element )
                check_flag = 'failed'
                break
        if check_flag == 'init':
            data_good_check  = True
        log.debug( 'data_good_check, `%s`' % data_good_check )
        return data_good_check


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
