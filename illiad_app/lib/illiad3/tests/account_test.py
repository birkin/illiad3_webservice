# import logging, os, sys, pprint, unittest

# ## add project parent-directory to sys.path
# parent_working_dir = os.path.abspath( os.path.join(os.getcwd(), os.pardir) )
# sys.path.append( parent_working_dir )

# from illiad_app.lib.illiad3.account import IlliadSession, Status


# log = logging.getLogger(__name__)


# class SessionTest(unittest.TestCase):

#     def setUp(self):
#         self.ILLIAD_REMOTE_AUTH_URL = os.environ['ILLIAD_MODULE__TEST_REMOTE_AUTH_URL']
#         self.ILLIAD_REMOTE_AUTH_KEY = os.environ['ILLIAD_MODULE__TEST_REMOTE_AUTH_KEY']
#         self.ILLIAD_USERNAME = os.environ['ILLIAD_MODULE__TEST_USERNAME']
#         self.BLOCKED_ILLIAD_USERNAME = os.environ['ILLIAD_MODULE__TEST_BLOCKED_USERNAME']
#         self.DISAVOWED_ILLIAD_USERNAME = os.environ['ILLIAD_MODULE__TEST_DISAVOWED_USERNAME']
#         self.ill = IlliadSession(
#             self.ILLIAD_REMOTE_AUTH_URL, self.ILLIAD_REMOTE_AUTH_KEY, self.ILLIAD_USERNAME )
#         log.debug( 'test setUp has self.ill now' )

#     def tearDown(self):
#         self.ill.logout()

#     def test_login(self):
#         """ Checks good existing-user login response.
#             NOTE: there is no 'login' test for a new-user, because the nature of submitting a new-user _creates_ the user. """
#         login_resp_dct = self.ill.login()
#         self.assertTrue( 'session_id' in login_resp_dct.keys()  )
#         self.assertTrue( 'authenticated' in login_resp_dct.keys() )
#         self.assertTrue( 'registered' in login_resp_dct.keys() )
#         self.assertTrue( 'blocked' not in login_resp_dct.keys() )
#         self.assertTrue( 'disavowed' not in login_resp_dct.keys() )
#         self.assertEqual( len(login_resp_dct['session_id']) > 0, True )
#         self.assertEqual( login_resp_dct['authenticated'], True )
#         self.assertEqual( login_resp_dct['registered'], True )

#     def test_disavowed_login(self):
#         """ Checks disavowed response. """
#         custom_ill = IlliadSession(
#             self.ILLIAD_REMOTE_AUTH_URL, self.ILLIAD_REMOTE_AUTH_KEY, self.DISAVOWED_ILLIAD_USERNAME )
#         login_resp_dct = custom_ill.login()
#         log.debug( 'TEMP; login_resp_dct, ```%s```' % pprint.pformat(login_resp_dct) )
#         self.assertTrue( 'session_id' in login_resp_dct.keys()  )
#         self.assertTrue( 'authenticated' in login_resp_dct.keys() )
#         self.assertTrue( 'registered' not in login_resp_dct.keys() )
#         self.assertTrue( 'blocked' not in login_resp_dct.keys() )
#         self.assertTrue( 'disavowed' in login_resp_dct.keys() )
#         self.assertEqual( login_resp_dct['session_id'], None  )
#         self.assertEqual( login_resp_dct['authenticated'], False  )
#         self.assertEqual( login_resp_dct['disavowed'], True  )
#         custom_ill.logout()

#     def test_blocked_login(self):
#         """ Checks blocked response.
#             NOTE: if this test fails, it's possible that the "blocked" test-user was deleted or unblocked. """
#         custom_ill = IlliadSession(
#             self.ILLIAD_REMOTE_AUTH_URL, self.ILLIAD_REMOTE_AUTH_KEY, self.BLOCKED_ILLIAD_USERNAME )
#         login_resp_dct = custom_ill.login()
#         log.debug( 'TEMP; login_resp_dct, ```%s```' % pprint.pformat(login_resp_dct) )
#         self.assertTrue( 'session_id' in login_resp_dct.keys()  )
#         self.assertTrue( 'authenticated' in login_resp_dct.keys() )
#         self.assertTrue( 'registered' in login_resp_dct.keys() )
#         # self.assertTrue( 'blocked' not in login_resp_dct.keys() )
#         self.assertTrue( 'blocked' in login_resp_dct.keys() )
#         self.assertTrue( 'disavowed' not in login_resp_dct.keys() )
#         # self.assertEqual( len(login_resp_dct['session_id']) > 0, True )
#         self.assertEqual( login_resp_dct['session_id'], None  )
#         self.assertEqual( login_resp_dct['authenticated'], True  )
#         self.assertEqual( login_resp_dct['registered'], True  )
#         custom_ill.logout()

#     ## submit_key tests ##

#     def test_submit_key(self):
#         """ Tests submit_key on article openurl. """
#         ill = self.ill
#         ill.login()
#         #Url encoded
#         openurl = "rft_val_fmt=info%3Aofi%2Ffmt%3Akev%3Amtx%3Ajournal&rft.spage=538&rft.issue=5&rft.date=2010-02-11&rft.volume=16&url_ver=Z39.88-2004&rft.atitle=Targeting+%CE%B17+Nicotinic+Acetylcholine+Receptors+in+the+Treatment+of+Schizophrenia.&rft.jtitle=Current+pharmaceutical+design&rft.issn=1381-6128&rft.genre=article"
#         submit_key = ill.get_request_key(openurl)
#         log.debug( 'submit_key, ```%s```' % pprint.pformat(submit_key) )
#         # self.assertEqual( 1, 2 )
#         self.assertEqual(submit_key['ILLiadForm'],
#                         'ArticleRequest')
#         self.assertEqual(submit_key['PhotoJournalTitle'],
#                         'Current pharmaceutical design')

#     def test_book(self):
#         """ Tests submit_key on simple book openurl (includes a note). """
#         ill = self.ill
#         ill.login()
#         openurl = "sid=FirstSearch:WorldCat&genre=book&isbn=9780231122375&title=Mahatma%20Gandhi%20%3A%20nonviolent%20power%20in%20action&date=2000&rft.genre=book&notes=%E2%80%9Ci%C3%B1t%C3%ABrn%C3%A2ti%C3%B8n%C3%A0l%C4%ADz%C3%A6ti%D0%A4n%E2%80%9D"  # “iñtërnâtiønàlĭzætiФn”
#         submit_key = ill.get_request_key(openurl)
#         self.assertEqual( 'LoanRequest', submit_key['ILLiadForm'] )
#         self.assertEqual( 'Mahatma Gandhi : nonviolent power in action', submit_key['LoanTitle'] )
#         self.assertEqual( 'LoanRequest', submit_key['ILLiadForm'] )
#         self.assertEqual( '“iñtërnâtiønàlĭzætiФn”', submit_key['Notes'] )
#         self.assertEqual(
#             ['CitedIn', 'ILLiadForm', 'ISSN', 'LoanDate', 'LoanTitle', 'NotWantedAfter', 'Notes', 'SearchType', 'SessionID', 'SubmitButton', 'Username', 'blocked', 'errors'],
#             sorted(submit_key.keys()) )

#     def test_book_with_long_openurl(self):
#         """ Tests submit_key on long book openurl. """
#         ill = self.ill
#         ill.login()
#         openurl = 'sid=FirstSearch%3AWorldCat&genre=book&isbn=9784883195732&title=Shin+kanzen+masuta%CC%84.+Nihongo+no%CC%84ryoku+shiken&date=2011&aulast=Fukuoka&aufirst=Rieko&id=doi%3A&pid=858811926%3Cfssessid%3E0%3C%2Ffssessid%3E%3Cedition%3EShohan.%3C%2Fedition%3E&url_ver=Z39.88-2004&rfr_id=info%3Asid%2Ffirstsearch.oclc.org%3AWorldCat&rft_val_fmt=info%3Aofi%2Ffmt%3Akev%3Amtx%3Abook&rft.genre=book&req_dat=%3Csessionid%3E0%3C%2Fsessionid%3E&rfe_dat=%3Caccessionnumber%3E858811926%3C%2Faccessionnumber%3E&rft_id=info%3Aoclcnum%2F858811926&rft_id=urn%3AISBN%3A9784883195732&rft.aulast=Fukuoka&rft.aufirst=Rieko&rft.btitle=Shin+kanzen+masuta%CC%84.+Nihongo+no%CC%84ryoku+shiken&rft.date=2011&rft.isbn=9784883195732&rft.place=To%CC%84kyo%CC%84&rft.pub=Suri%CC%84e%CC%84+Nettowa%CC%84ku&rft.edition=Shohan.&rft.genre=book'
#         submit_key = ill.get_request_key( openurl )
#         self.assertEqual(
#             'LoanRequest', submit_key['ILLiadForm'] )
#         self.assertEqual(
#             ['CitedIn', 'ESPNumber', 'ILLiadForm', 'ISSN', 'LoanAuthor', 'LoanDate', 'LoanEdition', 'LoanPlace', 'LoanPublisher', 'LoanTitle', 'NotWantedAfter', 'SearchType', 'SessionID', 'SubmitButton', 'Username', 'blocked', 'errors'],
#             sorted(submit_key.keys()) )

#     def test_bookitem(self):
#         """ Tests submit_key on genre=bookitem openurl. """
#         ill = self.ill
#         ill.login()
#         openurl = 'url_ver=Z39.88-2004&rft_val_fmt=info%3Aofi%2Ffmt%3Akev%3Amtx%3Abook&rft.genre=bookitem&rft.btitle=Current%20Protocols%20in%20Immunology&rft.atitle=Isolation%20and%20Functional%20Analysis%20of%20Neutrophils&rft.date=2001-05-01&rft.isbn=9780471142737&rfr_id=info%3Asid%2Fwiley.com%3AOnlineLibrary'
#         submit_key = ill.get_request_key( openurl )
#         self.assertEqual(
#             'BookChapterRequest', submit_key['ILLiadForm'] )
#         self.assertEqual(
#             ['CitedIn', 'ILLiadForm', 'ISSN', 'NotWantedAfter', 'PhotoArticleTitle', 'PhotoJournalInclusivePages', 'PhotoJournalTitle', 'PhotoJournalYear', 'SearchType', 'SessionID', 'SubmitButton', 'Username', 'blocked', 'errors'],
#             sorted(submit_key.keys()) )

#     def test_tiny_openurl(self):
#         """ Tests submit_key on painfully minimalist openurl. """
#         ill = self.ill
#         ill.login()
#         openurl = 'sid=Entrez:PubMed&id=pmid:23671965'
#         submit_key = ill.get_request_key( openurl )
#         self.assertEqual(
#             'LoanRequest', submit_key['ILLiadForm'] )
#         self.assertEqual(
#             ['CitedIn', 'ILLiadForm', 'LoanDate', 'LoanTitle', 'NotWantedAfter', 'Notes', 'SearchType', 'SessionID', 'SubmitButton', 'Username', 'blocked', 'errors'],
#             sorted(submit_key.keys()) )
#         self.assertEqual(
#             'entire openurl: `sid=Entrez:PubMed&id=pmid:23671965`', submit_key['Notes'] )

#     def test_logout(self):
#         """ Tests logout. """
#         response_dct = self.ill.logout()
#         self.assertTrue( 'authenticated' in response_dct.keys() )
#         self.assertFalse(response_dct['authenticated'])

#     ## end class SessionTest()


# class StatusTest(unittest.TestCase):

#     def setUp(self):
#         self.ILLIAD_REMOTE_AUTH_URL = os.environ['ILLIAD_MODULE__TEST_REMOTE_AUTH_URL']
#         self.ILLIAD_REMOTE_AUTH_KEY = os.environ['ILLIAD_MODULE__TEST_REMOTE_AUTH_KEY']
#         self.ILLIAD_USERNAME = os.environ['ILLIAD_MODULE__TEST_USERNAME']
#         self.status = Status(
#             self.ILLIAD_REMOTE_AUTH_URL, self.ILLIAD_REMOTE_AUTH_KEY )

#     def test_initialize_status(self):
#         """ Checks initial status.
#             Logs in user if necessary. """
#         self.assertEqual(
#             'registered',
#             self.status.initialize_status( self.ILLIAD_USERNAME )
#             )
#         self.assertEqual(
#             "<class 'illiad_app.lib.illiad3.account.IlliadSession'>",
#             repr( type(self.status.session) )
#             )

#     def test_check_user_status(self):
#         """ Checks user status (Undergraduate, Graduate, Faculty, Staff, Distance Ed Grad -- as of 2018-Nov-28) """
#         self.assertEqual(
#             'Staff',
#             self.status.check_user_status( self.ILLIAD_USERNAME )
#             )

#     ## end class StatusTest()



# def suite():
#     suite = unittest.makeSuite(SessionTest, 'test')
#     suite.addTest( unittest.makeSuite(StatusTest) )
#     return suite


# if __name__ == '__main__':
#     unittest.main()
