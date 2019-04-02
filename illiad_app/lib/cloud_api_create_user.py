# -*- coding: utf-8 -*-

import logging, random


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
