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
 'query': {'date_time': '2019-04-09 16:27:29.219725',
           'url': 'https://library.brown.edu/bib_ourl_api/v1/ourl_to_bib/?ourl=sid%253Dgoogle%2526auinit%253DT%2526aulast%253DSOTA%2526atitle%253DPhylogeny%252Band%252Bdivergence%252Btime%252Bof%252Bisland%252Btiger%252Bbeetles%252Bof%252Bthe%252Bgenus%252BCylindera%252B(Coleoptera%253A%252BCicindelidae)%252Bin%252BEast%252BAsia%2526id%253Ddoi%253A10.1111%252Fj.1095-8312.2011.01617.x%2526title%253DBiological%252Bjournal%252Bof%252Bthe%252BLinnean%252BSociety%2526volume%253D102%2526issue%253D4%2526date%253D2011%2526spage%253D715%2526issn%253D0024-4066'},
 'response': {'bib': {'_rfr': 'google',
                      'author': [{'lastname': 'SOTA', 'name': 'SOTA'}],
                      'end_page': 'EOA',
                      'identifier': [{'id': 'doi:10.1111/j.1095-8312.2011.01617.x',
                                      'type': 'doi'},
                                     {'id': '0024-4066', 'type': 'issn'}],
                      'issue': '4',
                      'journal': {'name': 'Biological journal of the Linnean '
                                          'Society'},
                      'pages': '715 - EOA',
                      'place_of_publication': None,
                      'publisher': None,
                      'start_page': '715',
                      'title': 'Phylogeny and divergence time of island tiger '
                               'beetles of the genus Cylindera (Coleoptera: '
                               'Cicindelidae) in East Asia',
                      'type': 'article',
                      'volume': '102',
                      'year': '2011'},
              'decoded_openurl': 'sid=google&auinit=T&aulast=SOTA&atitle=Phylogeny+and+divergence+time+of+island+tiger+beetles+of+the+genus+Cylindera+(Coleoptera:+Cicindelidae)+in+East+Asia&id=doi:10.1111/j.1095-8312.2011.01617.x&title=Biological+journal+of+the+Linnean+Society&volume=102&issue=4&date=2011&spage=715&issn=0024-4066',
              'elapsed_time': '0:00:00.019502'}}
        self.assertEqual( self.mapper.grab_journal_title(bib_dct), 'Biological journal of the Linnean Society' )
        self.assertEqual( self.mapper.grab_article_title(bib_dct), 'Phylogeny and divergence time of island tiger beetles of the genus Cylindera (Coleoptera: Cicindelidae) in East Asia' )
        self.assertEqual( self.mapper.grab_author(bib_dct), 'SOTA' )
        self.assertEqual( self.mapper.grab_volume(bib_dct), '102' )
        self.assertEqual( self.mapper.grab_issue(bib_dct), '4' )
        self.assertEqual( self.mapper.grab_date(bib_dct), '2011' )
        self.assertEqual( self.mapper.grab_pages(bib_dct), '715 - EOA' )
        self.assertEqual( self.mapper.grab_issn(bib_dct), '0024-4066' )
        self.assertEqual( self.mapper.grab_espn(bib_dct), '' )
        self.assertEqual( self.mapper.grab_sid(bib_dct), 'google' )

    def test_bib_dct_B(self):
        """ Checks mapping of bib_dct elements to illiad article keys for pmid `info:pmid/29083764`. """
        bib_dct = {u'query': {u'date_time': u'2019-04-10 13:25:25.906071',
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
