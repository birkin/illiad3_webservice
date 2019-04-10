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
        """ Checks mapping of bib_dct elements to illiad article keys. """
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

    ## end class class Article_Mapper_Test()
