
import os, requests

params = {
  "Username" : "bdoe",
  "ExternalUserId": "123456789",
  "FirstName":"Bailey",
  "LastName":"Doe",
  "EmailAddress" : "test@test.test" ,
  "DeliveryMethod" : "Hold for Pickup",
  "LoanDeliveryMethod" : "Mail to Address",
  "NotificationMethod" : "Electronic",
  "Phone" : "123-456-7890",
  "Status" : "Graduate",
  "PlainTextPassword": "zzzzzzzzzzzz",
  "AuthType" : "ILLiad",
  "Department" : "Music",
  "Web" : True,
  "Address" : "the address",
  "Address2" : "extra address info",
  "City" : "the city",
  "State" : "RI",
  "Zip" : "12345"
}

url = '%s%s' % ( os.environ['ILLIAD_WS__OFFICIAL_ILLIAD_API_URL'], 'Users' )  # root url contains ending-slash
print( 'url, ```%s```' % url )

headers = {
    'Accept-Type': 'application/json; charset=utf-8',
    'ApiKey': os.environ['ILLIAD_WS__OFFICIAL_ILLIAD_API_KEY']
    }

r = requests.post( url, data=params, headers=headers, timeout=60, verify=True )
print( r.status_code )

print( r.content )
