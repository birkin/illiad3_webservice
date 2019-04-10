# -*- coding: utf-8 -*-

import base64, json, random
from illiad_app import settings_app
from django.test import Client, TestCase
from illiad_app.lib.cloud_article_request import Mapper


class Article_Mapper_Test( TestCase ):
    """ Tests parsing of bib-dcts. """

    def setUp(self):
        self.log_id = random.randint(1111, 9999)
        self.mapper = Mapper( self.log_id )

    def test_bib_dct_A(self):
        """ Checks mapping of bib_dct elements to illiad article keys for doi `doi:10.1111/j.1095-8312.2011.01617.x`. """
        bib_dct = {
 u'query': {u'date_time': u'2019-04-10 13:39:09.146627',
            u'url': u'https://library.brown.edu/bib_ourl_api/v1/ourl_to_bib/?ourl=rft_val_fmt%3Dinfo%253Aofi%2Ffmt%253Akev%253Amtx%253Ajournal%26rfr_id%3Dinfo%253Asid%2FEntrez%253APubMed%26rft.issue%3D2%26rft.au%3DManika%252C%2BKaterina%26rft.pages%3D134%2B-%2BEOA%26rft_id%3Dinfo%253Apmid%2F18496984%26rft.date%3D2007%26rft.volume%3D24%26rft.end_page%3DEOA%26rft.atitle%3DEpstein-Barr%2Bvirus%2BDNA%2Bin%2Bbronchoalveolar%2Blavage%2Bfluid%2Bfrom%2Bpatients%2Bwith%2Bidiopathic%2Bpulmonary%2Bfibrosis.%26ctx_ver%3DZ39.88-2004%26rft.jtitle%3DSarcoidosis%252C%2Bvasculitis%252C%2Band%2Bdiffuse%2Blung%2Bdiseases%26rft.issn%3D1124-0490%26rft.genre%3Darticle%26rft.spage%3D134%26Notes%3D%2560PMID%253A%2B18496984%2560%253B%2B%2560shortlink%253A%2B%253C%252Feasyaccess%252Ffind%252Fpermalink%252FXqt%252F%253E%2560'},
 u'response': {u'bib': {u'_rfr': u'info:sid/Entrez:PubMed',
                        u'author': [{u'name': u'Manika, Katerina'}],
                        u'end_page': None,
                        u'identifier': [{u'id': u'info:pmid/18496984',
                                         u'type': u'pmid'},
                                        {u'id': u'1124-0490',
                                         u'type': u'issn'}],
                        u'issue': u'2',
                        u'journal': {u'name': u'Sarcoidosis, vasculitis, and diffuse lung diseases'},
                        u'pages': u'134 - EOA',
                        u'place_of_publication': None,
                        u'publisher': None,
                        u'start_page': u'134',
                        u'title': u'Epstein-Barr virus DNA in bronchoalveolar lavage fluid from patients with idiopathic pulmonary fibrosis.',
                        u'type': u'article',
                        u'volume': u'24',
                        u'year': u'2007'},
               u'decoded_openurl': u'rft_val_fmt=info:ofi/fmt:kev:mtx:journal&rfr_id=info:sid/Entrez:PubMed&rft.issue=2&rft.au=Manika,+Katerina&rft.pages=134+-+EOA&rft_id=info:pmid/18496984&rft.date=2007&rft.volume=24&rft.end_page=EOA&rft.atitle=Epstein-Barr+virus+DNA+in+bronchoalveolar+lavage+fluid+from+patients+with+idiopathic+pulmonary+fibrosis.&ctx_ver=Z39.88-2004&rft.jtitle=Sarcoidosis,+vasculitis,+and+diffuse+lung+diseases&rft.issn=1124-0490&rft.genre=article&rft.spage=134&Notes=`PMID:+18496984`;+`shortlink:+</easyaccess/find/permalink/Xqt/>`',
               u'elapsed_time': u'0:00:00.018589'}}
        self.assertEqual( self.mapper.grab_journal_title(bib_dct), 'Sarcoidosis, vasculitis, and diffuse lung diseases' )
        self.assertEqual( self.mapper.grab_article_title(bib_dct), 'Epstein-Barr virus DNA in bronchoalveolar lavage fluid from patients with idiopathic pulmonary fibrosis.' )
        self.assertEqual( self.mapper.grab_author(bib_dct), 'Manika, Katerina' )
        self.assertEqual( self.mapper.grab_volume(bib_dct), '24' )
        self.assertEqual( self.mapper.grab_issue(bib_dct), '2' )
        self.assertEqual( self.mapper.grab_date(bib_dct), '2007' )
        self.assertEqual( self.mapper.grab_pages(bib_dct), '134 - EOA' )
        self.assertEqual( self.mapper.grab_issn(bib_dct), '1124-0490' )
        self.assertEqual( self.mapper.grab_espn(bib_dct), '' )
        self.assertEqual( self.mapper.grab_sid(bib_dct), 'info:sid/Entrez:PubMed' )

    def test_bib_dct_B(self):
        """ Checks mapping of bib_dct elements to illiad article keys for pmid `info:pmid/29083764`. """
        bib_dct = {
 u'query': {u'date_time': u'2019-04-10 13:25:25.906071',
            u'url': u'https://library.brown.edu/bib_ourl_api/v1/ourl_to_bib/?ourl=rft.pub%3DStatPearls%2BPublishing%26rft_val_fmt%3Dinfo%253Aofi%2Ffmt%253Akev%253Amtx%253Ajournal%26rfr_id%3Dinfo%253Asid%2FEntrez%253APubMed%26rft.pages%3D%253F%2B-%2B%253F%26rft_id%3Dinfo%253Apmid%2F29083764%26rft.date%3D2019%26rft.atitle%3DUnknown%26ctx_ver%3DZ39.88-2004%26rft.jtitle%3DStatPearls%26rft.genre%3Darticle%26Notes%3D%2560PMID%253A%2B29083764%2560%253B%2B%2560not%2Benough%2Boriginal-request%2Bdata%2560%253B%2B%2560shortlink%253A%2B%253C%252Feasyaccess%252Ffind%252Fpermalink%252FDu68%252F%253E%2560'},
 u'response': {u'bib': {u'_rfr': u'info:sid/Entrez:PubMed',
                        u'author': [],
                        u'end_page': None,
                        u'identifier': [{u'id': u'info:pmid/29083764',
                                         u'type': u'pmid'}],
                        u'issue': None,
                        u'journal': {u'name': u'StatPearls'},
                        u'pages': u'? - ?',
                        u'place_of_publication': None,
                        u'publisher': u'StatPearls Publishing',
                        u'start_page': None,
                        u'title': u'Unknown',
                        u'type': u'article',
                        u'volume': None,
                        u'year': u'2019'},
               u'decoded_openurl': u'rft.pub=StatPearls+Publishing&rft_val_fmt=info:ofi/fmt:kev:mtx:journal&rfr_id=info:sid/Entrez:PubMed&rft.pages=?+-+?&rft_id=info:pmid/29083764&rft.date=2019&rft.atitle=Unknown&ctx_ver=Z39.88-2004&rft.jtitle=StatPearls&rft.genre=article&Notes=`PMID:+29083764`;+`not+enough+original-request+data`;+`shortlink:+</easyaccess/find/permalink/Du68/>`',
               u'elapsed_time': u'0:00:00.012151'}}
        self.assertEqual( self.mapper.grab_journal_title(bib_dct), 'StatPearls' )
        self.assertEqual( self.mapper.grab_article_title(bib_dct), 'Unknown' )
        self.assertEqual( self.mapper.grab_author(bib_dct), '' )
        self.assertEqual( self.mapper.grab_volume(bib_dct), '' )
        self.assertEqual( self.mapper.grab_issue(bib_dct), '' )
        self.assertEqual( self.mapper.grab_date(bib_dct), '2019' )
        self.assertEqual( self.mapper.grab_pages(bib_dct), '? - ?' )
        self.assertEqual( self.mapper.grab_issn(bib_dct), '' )
        self.assertEqual( self.mapper.grab_espn(bib_dct), '' )
        self.assertEqual( self.mapper.grab_sid(bib_dct), 'info:sid/Entrez:PubMed' )

    ## end class class Article_Mapper_Test()
