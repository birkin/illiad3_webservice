# POST https://your.illiad.edu/ILLiadWebPlatform/Users
# Accept-Type: application/json
# {
#   "Username" : "bdoe",
#   "ExternalUserId": "Z20181116",
#   "FirstName":"Bailey",
#   "LastName":"Doe",
#   "EmailAddress" : "bailey@test.com" ,
#   "DeliveryMethod" : "Hold for Pickup",
#   "LoanDeliveryMethod" : "Mail to Address",
#   "NotificationMethod" : "Electronic",
#   "Phone" : "757-123-4568",
#   "Status" : "Graduate",
#   "PlainTextPassword": "MySpecialPassword1234!",
#   "AuthType" : "ILLiad",
#   "Department" : "Music",
#   "Web" : true,
#   "Address" : "123 Oak St",
#   "Address2" : "Apt 4E",
#   "City" : "Virgia Beach",
#   "State" : "VA",
#   "Zip" : "23462"
# }


import os, requests

params = {
  "Username" : "bdoe",
  "ExternalUserId": "Z20181116",
  "FirstName":"Bailey",
  "LastName":"Doe",
  "EmailAddress" : "birkin_diana@brown.edu" ,
  "DeliveryMethod" : "Hold for Pickup",
  "LoanDeliveryMethod" : "Mail to Address",
  "NotificationMethod" : "Electronic",
  "Phone" : "757-123-4568",
  "Status" : "Graduate",
  "PlainTextPassword": "MySpecialPassword1234!",
  "AuthType" : "ILLiad",
  "Department" : "Music",
  "Web" : True,
  "Address" : "123 Oak St",
  "Address2" : "Apt 4E",
  "City" : "Virgia Beach",
  "State" : "VA",
  "Zip" : "23462"
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


