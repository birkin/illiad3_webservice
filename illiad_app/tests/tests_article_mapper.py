# -*- coding: utf-8 -*-

import base64, json, random
from illiad_app import settings_app
from django.test import Client, TestCase
from illiad_app.lib.cloud_article_request import ILLiadParamBuilder, Mapper


class ILLiadParamBuilder_Test( TestCase ):
    """ Tests parsing of notes in openurl.
        Notes-tests correspond to the `decoded_openurl` in `Article_Mapper_Test()` """

    def setUp(self):
        self.log_id = random.randint(1111, 9999)
        self.builder = ILLiadParamBuilder( self.log_id )

    def test_notes_A(self):
        decoded_openurl = 'rft_val_fmt=info:ofi/fmt:kev:mtx:journal&rfr_id=info:sid/Entrez:PubMed&rft.issue=2&rft.au=Manika,+Katerina&rft.pages=134+-+EOA&rft_id=info:pmid/18496984&rft.date=2007&rft.volume=24&rft.end_page=EOA&rft.atitle=Epstein-Barr+virus+DNA+in+bronchoalveolar+lavage+fluid+from+patients+with+idiopathic+pulmonary+fibrosis.&ctx_ver=Z39.88-2004&rft.jtitle=Sarcoidosis,+vasculitis,+and+diffuse+lung+diseases&rft.issn=1124-0490&rft.genre=article&rft.spage=134&Notes=`PMID:+18496984`;+`shortlink:+</easyaccess/find/permalink/Xqt/>`'
        self.assertEqual( self.builder.extract_notes(decoded_openurl), '`PMID: 18496984`; `shortlink: </easyaccess/find/permalink/Xqt/>`' )

    def test_notes_B(self):
        decoded_openurl = 'rft.pub=StatPearls+Publishing&rft_val_fmt=info:ofi/fmt:kev:mtx:journal&rfr_id=info:sid/Entrez:PubMed&rft.pages=?+-+?&rft_id=info:pmid/29083764&rft.date=2019&rft.atitle=Unknown&ctx_ver=Z39.88-2004&rft.jtitle=StatPearls&rft.genre=article&Notes=`PMID:+29083764`;+`not+enough+original-request+data`;+`shortlink:+</easyaccess/find/permalink/Du68/>`'
        self.assertEqual( self.builder.extract_notes(decoded_openurl), '`PMID: 29083764`; `not enough original-request data`; `shortlink: </easyaccess/find/permalink/Du68/>`' )

    def test_notes_C(self):
        decoded_openurl = 'rft_val_fmt=info:ofi/fmt:kev:mtx:journal&rfr_id=info:sid/Entrez:PubMed&rft.issue=3&rft.au=Unai,+Yuki&rft.pages=178+-+EOA&rft_id=info:pmid/29491331&rft.date=2018&rft.volume=58&rft.end_page=EOA&rft.atitle=[A+case+of+short-lasting+unilateral+neuralgiform+headache+with+conjunctival+injection+and+tearing+triggered+by+mumps+meningitis+in+a+patient+with+recurrent+primary+stabbing+headache].&ctx_ver=Z39.88-2004&rft.jtitle=Rinsho+shinkeigaku+=+Clinical+neurology&rft.issn=0009-918X&rft.genre=article&rft.spage=178&Notes=`PMID:+29491331`;+`shortlink:+</easyaccess/find/permalink/Du6U/>`'
        self.assertEqual( self.builder.extract_notes(decoded_openurl), '`PMID: 29491331`; `shortlink: </easyaccess/find/permalink/Du6U/>`' )

    def test_notes_D(self):
        decoded_openurl = 'rft_val_fmt=info:ofi/fmt:kev:mtx:journal&rfr_id=info:sid/&rft.issue=2&rft.au=Li,+Huifang&rft.eissn=2210-321X&rft.pages=335+-+EOA&rft_id=info:doi/10.1016/j.cjche.2018.04.010&rft.date=2019&rft.volume=27&rft.end_page=EOA&rft.atitle=Selective+recovery+of+lithium+from+simulated+brine+using+different+organic+synergist&ctx_ver=Z39.88-2004&rft.jtitle=Chinese+journal+of+chemical+engineering&rft.issn=1004-9541&rft.genre=article&rft.spage=335&Notes=`shortlink:+</easyaccess/find/permalink/DtZG/>`'
        self.assertEqual( self.builder.extract_notes(decoded_openurl), '`shortlink: </easyaccess/find/permalink/DtZG/>`' )

    def test_notes_E(self):
        decoded_openurl = 'rft_val_fmt=info:ofi/fmt:kev:mtx:journal&rfr_id=info:sid/&rft.issue=11&rft.au=Partibha,+Krishan&rft.pages=2557+-+EOA&rft_id=info:doi/10.14233/ajchem.2018.21598&rft.date=2018&rft.volume=30&rft.end_page=EOA&rft.atitle=Prediction+of+Interactions+between+Binary+Mixtures+of+Aliphatic+Amines+and+Aliphatic+Acetates&ctx_ver=Z39.88-2004&rft.jtitle=Asian+journal+of+chemistry&rft.issn=0970-7077&rft.genre=article&rft.spage=2557&Notes=`shortlink:+</easyaccess/find/permalink/DsvT/>`'
        self.assertEqual( self.builder.extract_notes(decoded_openurl), '`shortlink: </easyaccess/find/permalink/DsvT/>`' )

    def test_notes_F(self):
        decoded_openurl = 'rft_val_fmt=info:ofi/fmt:kev:mtx:journal&rfr_id=info:sid/info:sid/Elsevier:SD&rft.au=Glunz,+Stefan&rft.eissn=1879-3398&rft.pages=260+-+EOA&rft_id=info:doi/10.1016/j.solmat.2018.04.029&rft.date=2018&rft.volume=185&rft.end_page=EOA&rft.atitle=SiO2+surface+passivation+layers+?+a+key+technology+for+silicon+solar+cells&ctx_ver=Z39.88-2004&rft.jtitle=Solar+energy+materials+and+solar+cells&rft.issn=0927-0248&rft.genre=article&rft.spage=260&Notes=`shortlink:+</easyaccess/find/permalink/Dt6D/>`'
        self.assertEqual( self.builder.extract_notes(decoded_openurl), '`shortlink: </easyaccess/find/permalink/Dt6D/>`' )

    def test_notes_G(self):
        decoded_openurl = 'rft_val_fmt=info:ofi/fmt:kev:mtx:journal&rfr_id=info:sid/EBSCO:Business+Source+Premier&rft.issue=4&rft.au=Campbell,+Trevor&rft.eissn=1532-4265&rft.pages=284+-+EOA&rft.date=2016&rft.volume=39&rft.end_page=EOA&rft.atitle=The+Impact+of+the+Unemployment+Rate+on+Unemployment+Benefits+in+Barbados:+An+Impulse+Response+Approach.&ctx_ver=Z39.88-2004&rft.jtitle=International+journal+of+public+administration&rft.issn=0190-0692&rft.genre=article&rft.spage=284&Notes=`shortlink:+</easyaccess/find/permalink/Du4b/>`'
        self.assertEqual( self.builder.extract_notes(decoded_openurl), '`shortlink: </easyaccess/find/permalink/Du4b/>`' )

    def test_notes_H(self):
        decoded_openurl = 'rft_val_fmt=info:ofi/fmt:kev:mtx:journal&rfr_id=info:sid/&rft.au=Tojo+et+al.&rft.pages=120+-+EOA&rft.date=1977&rft.volume=73&rft.end_page=EOA&rft.atitle=Unknown&ctx_ver=Z39.88-2004&rft.jtitle=Anales+de+Quimica+(1968-1979)&rft.issn=0365-4990&rft.genre=article&rft.spage=120&Notes=`shortlink:+</easyaccess/find/permalink/63w/>`'
        self.assertEqual( self.builder.extract_notes(decoded_openurl), '`shortlink: </easyaccess/find/permalink/63w/>`' )

    def test_notes_I(self):
        decoded_openurl = 'rft_val_fmt=info:ofi/fmt:kev:mtx:journal&rfr_id=info:sid/EBSCO:Company+Information&rft.pages=?+-+?&rft.date=?&rft.atitle=Leroy+Seafood+Group+Asa&ctx_ver=Z39.88-2004&rft.jtitle=Leroy+Seafood+Group+Asa&rft.genre=article&Notes=`not+enough+original-request+data`;+`shortlink:+</easyaccess/find/permalink/Du4Z/>`'
        self.assertEqual( self.builder.extract_notes(decoded_openurl), '`not enough original-request data`; `shortlink: </easyaccess/find/permalink/Du4Z/>`' )

    ## end class ILLiadParamBuilder()


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

    def test_bib_dct_C(self):
        """ Checks mapping of bib_dct elements to illiad article keys for pmid `info:pmid/29491331`. """
        bib_dct = {
 'query': {'date_time': '2019-04-10 14:58:31.049638',
           'url': 'https://library.brown.edu/bib_ourl_api/v1/ourl_to_bib/?ourl=rft_val_fmt%3Dinfo%253Aofi%2Ffmt%253Akev%253Amtx%253Ajournal%26rfr_id%3Dinfo%253Asid%2FEntrez%253APubMed%26rft.issue%3D3%26rft.au%3DUnai%252C%2BYuki%26rft.pages%3D178%2B-%2BEOA%26rft_id%3Dinfo%253Apmid%2F29491331%26rft.date%3D2018%26rft.volume%3D58%26rft.end_page%3DEOA%26rft.atitle%3D%255BA%2Bcase%2Bof%2Bshort-lasting%2Bunilateral%2Bneuralgiform%2Bheadache%2Bwith%2Bconjunctival%2Binjection%2Band%2Btearing%2Btriggered%2Bby%2Bmumps%2Bmeningitis%2Bin%2Ba%2Bpatient%2Bwith%2Brecurrent%2Bprimary%2Bstabbing%2Bheadache%255D.%26ctx_ver%3DZ39.88-2004%26rft.jtitle%3DRinsho%2Bshinkeigaku%2B%253D%2BClinical%2Bneurology%26rft.issn%3D0009-918X%26rft.genre%3Darticle%26rft.spage%3D178%26Notes%3D%2560PMID%253A%2B29491331%2560%253B%2B%2560shortlink%253A%2B%253C%252Feasyaccess%252Ffind%252Fpermalink%252FDu6U%252F%253E%2560'},
 'response': {'bib': {'_rfr': 'info:sid/Entrez:PubMed',
                      'author': [{'name': 'Unai, Yuki'}],
                      'end_page': None,
                      'identifier': [{'id': 'info:pmid/29491331',
                                      'type': 'pmid'},
                                     {'id': '0009-918X', 'type': 'issn'}],
                      'issue': '3',
                      'journal': {'name': 'Rinsho shinkeigaku = Clinical '
                                          'neurology'},
                      'pages': '178 - EOA',
                      'place_of_publication': None,
                      'publisher': None,
                      'start_page': '178',
                      'title': '[A case of short-lasting unilateral '
                               'neuralgiform headache with conjunctival '
                               'injection and tearing triggered by mumps '
                               'meningitis in a patient with recurrent primary '
                               'stabbing headache].',
                      'type': 'article',
                      'volume': '58',
                      'year': '2018'},
              'decoded_openurl': 'rft_val_fmt=info:ofi/fmt:kev:mtx:journal&rfr_id=info:sid/Entrez:PubMed&rft.issue=3&rft.au=Unai,+Yuki&rft.pages=178+-+EOA&rft_id=info:pmid/29491331&rft.date=2018&rft.volume=58&rft.end_page=EOA&rft.atitle=[A+case+of+short-lasting+unilateral+neuralgiform+headache+with+conjunctival+injection+and+tearing+triggered+by+mumps+meningitis+in+a+patient+with+recurrent+primary+stabbing+headache].&ctx_ver=Z39.88-2004&rft.jtitle=Rinsho+shinkeigaku+=+Clinical+neurology&rft.issn=0009-918X&rft.genre=article&rft.spage=178&Notes=`PMID:+29491331`;+`shortlink:+</easyaccess/find/permalink/Du6U/>`',
              'elapsed_time': '0:00:00.018693'}}
        self.assertEqual( self.mapper.grab_journal_title(bib_dct), 'Rinsho shinkeigaku = Clinical neurology' )
        self.assertEqual( self.mapper.grab_article_title(bib_dct), '[A case of short-lasting unilateral neuralgiform headache with conjunctival injection and tearing triggered by mumps meningitis in a patient with recurrent primary stabbing headache].' )
        self.assertEqual( self.mapper.grab_author(bib_dct), 'Unai, Yuki' )
        self.assertEqual( self.mapper.grab_volume(bib_dct), '58' )
        self.assertEqual( self.mapper.grab_issue(bib_dct), '3' )
        self.assertEqual( self.mapper.grab_date(bib_dct), '2018' )
        self.assertEqual( self.mapper.grab_pages(bib_dct), '178 - EOA' )
        self.assertEqual( self.mapper.grab_issn(bib_dct), '0009-918X' )
        self.assertEqual( self.mapper.grab_espn(bib_dct), '' )
        self.assertEqual( self.mapper.grab_sid(bib_dct), 'info:sid/Entrez:PubMed' )

    def test_bib_dct_D(self):
        """ Checks mapping of bib_dct elements to illiad article keys for id `doi:10.1016/j.cjche.2018.04.010`. """
        bib_dct = {
 'query': {'date_time': '2019-04-10 15:00:15.789185',
           'url': 'https://library.brown.edu/bib_ourl_api/v1/ourl_to_bib/?ourl=rft_val_fmt%3Dinfo%253Aofi%2Ffmt%253Akev%253Amtx%253Ajournal%26rfr_id%3Dinfo%253Asid%2F%26rft.issue%3D2%26rft.au%3DLi%252C%2BHuifang%26rft.eissn%3D2210-321X%26rft.pages%3D335%2B-%2BEOA%26rft_id%3Dinfo%253Adoi%2F10.1016%2Fj.cjche.2018.04.010%26rft.date%3D2019%26rft.volume%3D27%26rft.end_page%3DEOA%26rft.atitle%3DSelective%2Brecovery%2Bof%2Blithium%2Bfrom%2Bsimulated%2Bbrine%2Busing%2Bdifferent%2Borganic%2Bsynergist%26ctx_ver%3DZ39.88-2004%26rft.jtitle%3DChinese%2Bjournal%2Bof%2Bchemical%2Bengineering%26rft.issn%3D1004-9541%26rft.genre%3Darticle%26rft.spage%3D335%26Notes%3D%2560shortlink%253A%2B%253C%252Feasyaccess%252Ffind%252Fpermalink%252FDtZG%252F%253E%2560'},
 'response': {'bib': {'_rfr': 'info:sid/',
                      'author': [{'name': 'Li, Huifang'}],
                      'end_page': None,
                      'identifier': [{'id': 'doi:10.1016/j.cjche.2018.04.010',
                                      'type': 'doi'},
                                     {'id': '1004-9541', 'type': 'issn'},
                                     {'id': '2210-321X', 'type': 'eissn'}],
                      'issue': '2',
                      'journal': {'name': 'Chinese journal of chemical '
                                          'engineering'},
                      'pages': '335 - EOA',
                      'place_of_publication': None,
                      'publisher': None,
                      'start_page': '335',
                      'title': 'Selective recovery of lithium from simulated '
                               'brine using different organic synergist',
                      'type': 'article',
                      'volume': '27',
                      'year': '2019'},
              'decoded_openurl': 'rft_val_fmt=info:ofi/fmt:kev:mtx:journal&rfr_id=info:sid/&rft.issue=2&rft.au=Li,+Huifang&rft.eissn=2210-321X&rft.pages=335+-+EOA&rft_id=info:doi/10.1016/j.cjche.2018.04.010&rft.date=2019&rft.volume=27&rft.end_page=EOA&rft.atitle=Selective+recovery+of+lithium+from+simulated+brine+using+different+organic+synergist&ctx_ver=Z39.88-2004&rft.jtitle=Chinese+journal+of+chemical+engineering&rft.issn=1004-9541&rft.genre=article&rft.spage=335&Notes=`shortlink:+</easyaccess/find/permalink/DtZG/>`',
              'elapsed_time': '0:00:00.018644'}}
        self.assertEqual( self.mapper.grab_journal_title(bib_dct), 'Chinese journal of chemical engineering' )
        self.assertEqual( self.mapper.grab_article_title(bib_dct), 'Selective recovery of lithium from simulated brine using different organic synergist' )
        self.assertEqual( self.mapper.grab_author(bib_dct), 'Li, Huifang' )
        self.assertEqual( self.mapper.grab_volume(bib_dct), '27' )
        self.assertEqual( self.mapper.grab_issue(bib_dct), '2' )
        self.assertEqual( self.mapper.grab_date(bib_dct), '2019' )
        self.assertEqual( self.mapper.grab_pages(bib_dct), '335 - EOA' )
        self.assertEqual( self.mapper.grab_issn(bib_dct), '1004-9541' )
        self.assertEqual( self.mapper.grab_espn(bib_dct), '' )
        self.assertEqual( self.mapper.grab_sid(bib_dct), 'info:sid/' )

    def test_bib_dct_E(self):
        """ Checks mapping of bib_dct elements to illiad article keys for doi `doi:10.14233/ajchem.2018.21598`. """
        bib_dct = {
 'query': {'date_time': '2019-04-10 15:01:30.132287',
           'url': 'https://library.brown.edu/bib_ourl_api/v1/ourl_to_bib/?ourl=rft_val_fmt%3Dinfo%253Aofi%2Ffmt%253Akev%253Amtx%253Ajournal%26rfr_id%3Dinfo%253Asid%2F%26rft.issue%3D11%26rft.au%3DPartibha%252C%2BKrishan%26rft.pages%3D2557%2B-%2BEOA%26rft_id%3Dinfo%253Adoi%2F10.14233%2Fajchem.2018.21598%26rft.date%3D2018%26rft.volume%3D30%26rft.end_page%3DEOA%26rft.atitle%3DPrediction%2Bof%2BInteractions%2Bbetween%2BBinary%2BMixtures%2Bof%2BAliphatic%2BAmines%2Band%2BAliphatic%2BAcetates%26ctx_ver%3DZ39.88-2004%26rft.jtitle%3DAsian%2Bjournal%2Bof%2Bchemistry%26rft.issn%3D0970-7077%26rft.genre%3Darticle%26rft.spage%3D2557%26Notes%3D%2560shortlink%253A%2B%253C%252Feasyaccess%252Ffind%252Fpermalink%252FDsvT%252F%253E%2560'},
 'response': {'bib': {'_rfr': 'info:sid/',
                      'author': [{'name': 'Partibha, Krishan'}],
                      'end_page': None,
                      'identifier': [{'id': 'doi:10.14233/ajchem.2018.21598',
                                      'type': 'doi'},
                                     {'id': '0970-7077', 'type': 'issn'}],
                      'issue': '11',
                      'journal': {'name': 'Asian journal of chemistry'},
                      'pages': '2557 - EOA',
                      'place_of_publication': None,
                      'publisher': None,
                      'start_page': '2557',
                      'title': 'Prediction of Interactions between Binary '
                               'Mixtures of Aliphatic Amines and Aliphatic '
                               'Acetates',
                      'type': 'article',
                      'volume': '30',
                      'year': '2018'},
              'decoded_openurl': 'rft_val_fmt=info:ofi/fmt:kev:mtx:journal&rfr_id=info:sid/&rft.issue=11&rft.au=Partibha,+Krishan&rft.pages=2557+-+EOA&rft_id=info:doi/10.14233/ajchem.2018.21598&rft.date=2018&rft.volume=30&rft.end_page=EOA&rft.atitle=Prediction+of+Interactions+between+Binary+Mixtures+of+Aliphatic+Amines+and+Aliphatic+Acetates&ctx_ver=Z39.88-2004&rft.jtitle=Asian+journal+of+chemistry&rft.issn=0970-7077&rft.genre=article&rft.spage=2557&Notes=`shortlink:+</easyaccess/find/permalink/DsvT/>`',
              'elapsed_time': '0:00:00.019117'}}
        self.assertEqual( self.mapper.grab_journal_title(bib_dct), 'Asian journal of chemistry' )
        self.assertEqual( self.mapper.grab_article_title(bib_dct), 'Prediction of Interactions between Binary Mixtures of Aliphatic Amines and Aliphatic Acetates' )
        self.assertEqual( self.mapper.grab_author(bib_dct), 'Partibha, Krishan' )
        self.assertEqual( self.mapper.grab_volume(bib_dct), '30' )
        self.assertEqual( self.mapper.grab_issue(bib_dct), '11' )
        self.assertEqual( self.mapper.grab_date(bib_dct), '2018' )
        self.assertEqual( self.mapper.grab_pages(bib_dct), '2557 - EOA' )
        self.assertEqual( self.mapper.grab_issn(bib_dct), '0970-7077' )
        self.assertEqual( self.mapper.grab_espn(bib_dct), '' )
        self.assertEqual( self.mapper.grab_sid(bib_dct), 'info:sid/' )

    def test_bib_dct_F(self):
        """ Checks mapping of bib_dct elements to illiad article keys for doi `doi:10.1016/j.solmat.2018.04.029`. """
        bib_dct = {
 'query': {'date_time': '2019-04-10 15:02:47.768342',
           'url': 'https://library.brown.edu/bib_ourl_api/v1/ourl_to_bib/?ourl=rft_val_fmt%3Dinfo%253Aofi%2Ffmt%253Akev%253Amtx%253Ajournal%26rfr_id%3Dinfo%253Asid%2Finfo%253Asid%2FElsevier%253ASD%26rft.au%3DGlunz%252C%2BStefan%26rft.eissn%3D1879-3398%26rft.pages%3D260%2B-%2BEOA%26rft_id%3Dinfo%253Adoi%2F10.1016%2Fj.solmat.2018.04.029%26rft.date%3D2018%26rft.volume%3D185%26rft.end_page%3DEOA%26rft.atitle%3DSiO2%2Bsurface%2Bpassivation%2Blayers%2B%253F%2Ba%2Bkey%2Btechnology%2Bfor%2Bsilicon%2Bsolar%2Bcells%26ctx_ver%3DZ39.88-2004%26rft.jtitle%3DSolar%2Benergy%2Bmaterials%2Band%2Bsolar%2Bcells%26rft.issn%3D0927-0248%26rft.genre%3Darticle%26rft.spage%3D260%26Notes%3D%2560shortlink%253A%2B%253C%252Feasyaccess%252Ffind%252Fpermalink%252FDt6D%252F%253E%2560'},
 'response': {'bib': {'_rfr': 'info:sid/info:sid/Elsevier:SD',
                      'author': [{'name': 'Glunz, Stefan'}],
                      'end_page': None,
                      'identifier': [{'id': 'doi:10.1016/j.solmat.2018.04.029',
                                      'type': 'doi'},
                                     {'id': '0927-0248', 'type': 'issn'},
                                     {'id': '1879-3398', 'type': 'eissn'}],
                      'issue': None,
                      'journal': {'name': 'Solar energy materials and solar '
                                          'cells'},
                      'pages': '260 - EOA',
                      'place_of_publication': None,
                      'publisher': None,
                      'start_page': '260',
                      'title': 'SiO2 surface passivation layers ? a key '
                               'technology for silicon solar cells',
                      'type': 'article',
                      'volume': '185',
                      'year': '2018'},
              'decoded_openurl': 'rft_val_fmt=info:ofi/fmt:kev:mtx:journal&rfr_id=info:sid/info:sid/Elsevier:SD&rft.au=Glunz,+Stefan&rft.eissn=1879-3398&rft.pages=260+-+EOA&rft_id=info:doi/10.1016/j.solmat.2018.04.029&rft.date=2018&rft.volume=185&rft.end_page=EOA&rft.atitle=SiO2+surface+passivation+layers+?+a+key+technology+for+silicon+solar+cells&ctx_ver=Z39.88-2004&rft.jtitle=Solar+energy+materials+and+solar+cells&rft.issn=0927-0248&rft.genre=article&rft.spage=260&Notes=`shortlink:+</easyaccess/find/permalink/Dt6D/>`',
              'elapsed_time': '0:00:00.018042'}}
        self.assertEqual( self.mapper.grab_journal_title(bib_dct), 'Solar energy materials and solar cells' )
        self.assertEqual( self.mapper.grab_article_title(bib_dct), 'SiO2 surface passivation layers ? a key technology for silicon solar cells' )
        self.assertEqual( self.mapper.grab_author(bib_dct), 'Glunz, Stefan' )
        self.assertEqual( self.mapper.grab_volume(bib_dct), '185' )
        self.assertEqual( self.mapper.grab_issue(bib_dct), '' )
        self.assertEqual( self.mapper.grab_date(bib_dct), '2018' )
        self.assertEqual( self.mapper.grab_pages(bib_dct), '260 - EOA' )
        self.assertEqual( self.mapper.grab_issn(bib_dct), '0927-0248' )
        self.assertEqual( self.mapper.grab_espn(bib_dct), '' )
        self.assertEqual( self.mapper.grab_sid(bib_dct), 'info:sid/info:sid/Elsevier:SD' )

    def test_bib_dct_G(self):
        """ Checks mapping of bib_dct elements to illiad article keys for issn `0190-0692`. """
        bib_dct = {
 'query': {'date_time': '2019-04-10 15:04:01.752378',
           'url': 'https://library.brown.edu/bib_ourl_api/v1/ourl_to_bib/?ourl=rft_val_fmt%3Dinfo%253Aofi%2Ffmt%253Akev%253Amtx%253Ajournal%26rfr_id%3Dinfo%253Asid%2FEBSCO%253ABusiness%2BSource%2BPremier%26rft.issue%3D4%26rft.au%3DCampbell%252C%2BTrevor%26rft.eissn%3D1532-4265%26rft.pages%3D284%2B-%2BEOA%26rft.date%3D2016%26rft.volume%3D39%26rft.end_page%3DEOA%26rft.atitle%3DThe%2BImpact%2Bof%2Bthe%2BUnemployment%2BRate%2Bon%2BUnemployment%2BBenefits%2Bin%2BBarbados%253A%2BAn%2BImpulse%2BResponse%2BApproach.%26ctx_ver%3DZ39.88-2004%26rft.jtitle%3DInternational%2Bjournal%2Bof%2Bpublic%2Badministration%26rft.issn%3D0190-0692%26rft.genre%3Darticle%26rft.spage%3D284%26Notes%3D%2560shortlink%253A%2B%253C%252Feasyaccess%252Ffind%252Fpermalink%252FDu4b%252F%253E%2560'},
 'response': {'bib': {'_rfr': 'info:sid/EBSCO:Business Source Premier',
                      'author': [{'name': 'Campbell, Trevor'}],
                      'end_page': None,
                      'identifier': [{'id': '0190-0692', 'type': 'issn'},
                                     {'id': '1532-4265', 'type': 'eissn'}],
                      'issue': '4',
                      'journal': {'name': 'International journal of public '
                                          'administration'},
                      'pages': '284 - EOA',
                      'place_of_publication': None,
                      'publisher': None,
                      'start_page': '284',
                      'title': 'The Impact of the Unemployment Rate on '
                               'Unemployment Benefits in Barbados: An Impulse '
                               'Response Approach.',
                      'type': 'article',
                      'volume': '39',
                      'year': '2016'},
              'decoded_openurl': 'rft_val_fmt=info:ofi/fmt:kev:mtx:journal&rfr_id=info:sid/EBSCO:Business+Source+Premier&rft.issue=4&rft.au=Campbell,+Trevor&rft.eissn=1532-4265&rft.pages=284+-+EOA&rft.date=2016&rft.volume=39&rft.end_page=EOA&rft.atitle=The+Impact+of+the+Unemployment+Rate+on+Unemployment+Benefits+in+Barbados:+An+Impulse+Response+Approach.&ctx_ver=Z39.88-2004&rft.jtitle=International+journal+of+public+administration&rft.issn=0190-0692&rft.genre=article&rft.spage=284&Notes=`shortlink:+</easyaccess/find/permalink/Du4b/>`',
              'elapsed_time': '0:00:00.017337'}}
        self.assertEqual( self.mapper.grab_journal_title(bib_dct), 'International journal of public administration' )
        self.assertEqual( self.mapper.grab_article_title(bib_dct), 'The Impact of the Unemployment Rate on Unemployment Benefits in Barbados: An Impulse Response Approach.' )
        self.assertEqual( self.mapper.grab_author(bib_dct), 'Campbell, Trevor' )
        self.assertEqual( self.mapper.grab_volume(bib_dct), '39' )
        self.assertEqual( self.mapper.grab_issue(bib_dct), '4' )
        self.assertEqual( self.mapper.grab_date(bib_dct), '2016' )
        self.assertEqual( self.mapper.grab_pages(bib_dct), '284 - EOA' )
        self.assertEqual( self.mapper.grab_issn(bib_dct), '0190-0692' )
        self.assertEqual( self.mapper.grab_espn(bib_dct), '' )
        self.assertEqual( self.mapper.grab_sid(bib_dct), 'info:sid/EBSCO:Business Source Premier' )

    def test_bib_dct_H(self):
        """ Checks mapping of bib_dct elements to illiad article keys for issn `0365-4990`. """
        bib_dct = {
 'query': {'date_time': '2019-04-10 15:05:26.760665',
           'url': 'https://library.brown.edu/bib_ourl_api/v1/ourl_to_bib/?ourl=rft_val_fmt%3Dinfo%253Aofi%2Ffmt%253Akev%253Amtx%253Ajournal%26rfr_id%3Dinfo%253Asid%2F%26rft.au%3DTojo%2Bet%2Bal.%26rft.pages%3D120%2B-%2BEOA%26rft.date%3D1977%26rft.volume%3D73%26rft.end_page%3DEOA%26rft.atitle%3DUnknown%26ctx_ver%3DZ39.88-2004%26rft.jtitle%3DAnales%2Bde%2BQuimica%2B%25281968-1979%2529%26rft.issn%3D0365-4990%26rft.genre%3Darticle%26rft.spage%3D120%26Notes%3D%2560shortlink%253A%2B%253C%252Feasyaccess%252Ffind%252Fpermalink%252F63w%252F%253E%2560'},
 'response': {'bib': {'_rfr': 'info:sid/',
                      'author': [{'name': 'Tojo et al.'}],
                      'end_page': None,
                      'identifier': [{'id': '0365-4990', 'type': 'issn'}],
                      'issue': None,
                      'journal': {'name': 'Anales de Quimica (1968-1979)'},
                      'pages': '120 - EOA',
                      'place_of_publication': None,
                      'publisher': None,
                      'start_page': '120',
                      'title': 'Unknown',
                      'type': 'article',
                      'volume': '73',
                      'year': '1977'},
              'decoded_openurl': 'rft_val_fmt=info:ofi/fmt:kev:mtx:journal&rfr_id=info:sid/&rft.au=Tojo+et+al.&rft.pages=120+-+EOA&rft.date=1977&rft.volume=73&rft.end_page=EOA&rft.atitle=Unknown&ctx_ver=Z39.88-2004&rft.jtitle=Anales+de+Quimica+(1968-1979)&rft.issn=0365-4990&rft.genre=article&rft.spage=120&Notes=`shortlink:+</easyaccess/find/permalink/63w/>`',
              'elapsed_time': '0:00:00.014483'}}
        self.assertEqual( self.mapper.grab_journal_title(bib_dct), 'Anales de Quimica (1968-1979)' )
        self.assertEqual( self.mapper.grab_article_title(bib_dct), 'Unknown' )
        self.assertEqual( self.mapper.grab_author(bib_dct), 'Tojo et al.' )
        self.assertEqual( self.mapper.grab_volume(bib_dct), '73' )
        self.assertEqual( self.mapper.grab_issue(bib_dct), '' )
        self.assertEqual( self.mapper.grab_date(bib_dct), '1977' )
        self.assertEqual( self.mapper.grab_pages(bib_dct), '120 - EOA' )
        self.assertEqual( self.mapper.grab_issn(bib_dct), '0365-4990' )
        self.assertEqual( self.mapper.grab_espn(bib_dct), '' )
        self.assertEqual( self.mapper.grab_sid(bib_dct), 'info:sid/' )

    def test_bib_dct_I(self):
        """ Checks mapping of bib_dct elements to illiad article keys for no id. """
        bib_dct = {
 'query': {'date_time': '2019-04-10 15:06:54.550762',
           'url': 'https://library.brown.edu/bib_ourl_api/v1/ourl_to_bib/?ourl=rft_val_fmt%3Dinfo%253Aofi%2Ffmt%253Akev%253Amtx%253Ajournal%26rfr_id%3Dinfo%253Asid%2FEBSCO%253ACompany%2BInformation%26rft.pages%3D%253F%2B-%2B%253F%26rft.date%3D%253F%26rft.atitle%3DLeroy%2BSeafood%2BGroup%2BAsa%26ctx_ver%3DZ39.88-2004%26rft.jtitle%3DLeroy%2BSeafood%2BGroup%2BAsa%26rft.genre%3Darticle%26Notes%3D%2560not%2Benough%2Boriginal-request%2Bdata%2560%253B%2B%2560shortlink%253A%2B%253C%252Feasyaccess%252Ffind%252Fpermalink%252FDu4Z%252F%253E%2560'},
 'response': {'bib': {'_rfr': 'info:sid/EBSCO:Company Information',
                      'author': [],
                      'end_page': None,
                      'identifier': [],
                      'issue': None,
                      'journal': {'name': 'Leroy Seafood Group Asa'},
                      'pages': '? - ?',
                      'place_of_publication': None,
                      'publisher': None,
                      'start_page': None,
                      'title': 'Leroy Seafood Group Asa',
                      'type': 'article',
                      'volume': None,
                      'year': '?'},
              'decoded_openurl': 'rft_val_fmt=info:ofi/fmt:kev:mtx:journal&rfr_id=info:sid/EBSCO:Company+Information&rft.pages=?+-+?&rft.date=?&rft.atitle=Leroy+Seafood+Group+Asa&ctx_ver=Z39.88-2004&rft.jtitle=Leroy+Seafood+Group+Asa&rft.genre=article&Notes=`not+enough+original-request+data`;+`shortlink:+</easyaccess/find/permalink/Du4Z/>`',
              'elapsed_time': '0:00:00.010208'}}
        self.assertEqual( self.mapper.grab_journal_title(bib_dct), 'Leroy Seafood Group Asa' )
        self.assertEqual( self.mapper.grab_article_title(bib_dct), 'Leroy Seafood Group Asa' )
        self.assertEqual( self.mapper.grab_author(bib_dct), '' )
        self.assertEqual( self.mapper.grab_volume(bib_dct), '' )
        self.assertEqual( self.mapper.grab_issue(bib_dct), '' )
        self.assertEqual( self.mapper.grab_date(bib_dct), '?' )
        self.assertEqual( self.mapper.grab_pages(bib_dct), '? - ?' )
        self.assertEqual( self.mapper.grab_issn(bib_dct), '' )
        self.assertEqual( self.mapper.grab_espn(bib_dct), '' )
        self.assertEqual( self.mapper.grab_sid(bib_dct), 'info:sid/EBSCO:Company Information' )

    ## end class class Article_Mapper_Test()
