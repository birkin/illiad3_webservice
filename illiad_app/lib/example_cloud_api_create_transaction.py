# POST https://your.illiad.edu/ILLiadWebPlatform/transaction/
# Content-Type: application/json
# {
#  "Username" : "jdoe",
#  "RequestType" : "Article",
#  "ProcessType" : "Borrowing",
#  "PhotoJournalTitle" : "Journal of Interlibrary Loan,Document Delivery & Electronic Reserve",
#  "PhotoArticleTitle" : "Interlibrary Loan in the United States: An Analysis of Academic Libraries in a Digital Age",
#  "PhotoArticleAuthor" : "Williams, Joseph; Woolwine, David",
#  "PhotoJournalVolume" : "21",
#  "PhotoJournalIssue" : "4",
#  "PhotoJournalYear" : "2011",
#  "PhotoJournalInclusivePages" : "165-183",
#  "ISSN": "1072-303X",
#  "TransactionStatus": "Awaiting Request Processing",
#  "CopyrightAlreadyPaid": "Yes",
# }


import os, requests

params = {
 "Username" : "bdoe",
 "RequestType" : "Article",
 "ProcessType" : "Borrowing",
 "PhotoJournalTitle" : "Journal of Interlibrary Loan,Document Delivery & Electronic Reserve",
 "PhotoArticleTitle" : "Interlibrary Loan in the United States: An Analysis of Academic Libraries in a Digital Age",
 "PhotoArticleAuthor" : "Williams, Joseph; Woolwine, David",
 "PhotoJournalVolume" : "21",
 "PhotoJournalIssue" : "4",
 "PhotoJournalYear" : "2011",
 "PhotoJournalInclusivePages" : "165-183",
 "ISSN": "1072-303X",
 "TransactionStatus": "Awaiting Request Processing",
 "CopyrightAlreadyPaid": False,
}

url = '%s%s' % ( os.environ['ILLIAD_WS__OFFICIAL_ILLIAD_API_URL'], 'Transaction' )  # root url contains ending-slash
print( 'url, ```%s```' % url )

headers = {
    'Accept-Type': 'application/json; charset=utf-8',
    'ApiKey': os.environ['ILLIAD_WS__OFFICIAL_ILLIAD_API_KEY']
    }

r = requests.post( url, data=params, headers=headers, timeout=60, verify=True )
print( r.status_code )

print( r.content )


