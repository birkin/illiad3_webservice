"""
Parsing utilities for various Illiad account pages.

Parsers are separated so that they can be unit tested more easily and adjusted
without changing the application logic.
"""

import logging, pprint, re
from bs4 import BeautifulSoup


log = logging.getLogger(__name__)

DIGITS_RE = re.compile('(\d+)')


def main_menu( content ):
    """ Parses main illiad landing page.
        Called by IlliadSession.login() """
    log.debug( 'content, ```%s```' % content )
    out = {'authenticated': False,
           'session_id': None,
           'registered': None}
    soup = BeautifulSoup( content, 'html.parser' )
    page_title = soup.title.text
    #If the user is registered, the page title will be Illiad Main Menu.
    if page_title == 'ILLiad Main Menu':
        out['registered'] = True
    else:
        #To do - make this raise a module specific Exception that client
        #code can handle.
        out['registered'] = False
    session_id = soup.select('#SessionID')[0].attrs.get('value')
    out['session_id'] = session_id
    out['authenticated'] = True
    return out

###

def request_form(content):
    """ Parses illiad's openurl request form.
        Returns dct of values which will be POSTed to submit the request.
        Called by account.py IlliadSession.get_request_key() """
    submit_key = {}
    soup = BeautifulSoup( content, 'html.parser' )
    submit_key = _check_blocked( soup, submit_key )
    submit_key = _check_inputs( soup, submit_key )
    submit_key = _check_textareas( soup, submit_key )
    return submit_key

def _check_blocked( soup, submit_key ):
    """ Checks for blocked status.
        Called by request_form() """
    try:
        title = soup.title.text
        status_message = soup.select('#status')[0].text
    except IndexError:
        log.info("Unable to parse status from ILLiad request page %s." % title)
        status_message = None
    if status_message:
        if status_message.rfind('blocked') > 0:
            submit_key['errors'] = status_message
            submit_key['blocked'] = True
    return submit_key

def _check_inputs( soup, submit_key ):
    """ Updates key-dct with html input data.
        Called by request_form() """
    inputs = soup( 'input' )
    for item in inputs:
        attrs = item.attrs
        name = attrs.get('name')
        value = attrs.get('value')
        if (value is None) or (value == u'') or (value.startswith('Clear')) or (value.startswith('Cancel')):
            continue
        if name == 'IlliadForm':  # we're still capturing ILLiadForm (note case of 'L's)
            continue
        submit_key[name] = value
    return submit_key

def _check_textareas( soup, submit_key ):
    """ Updates key-dct with html textarea data.
        Called by request_form() """
    textareas = soup( 'textarea' )
    for box in textareas:
        name = box.attrs['name']
        value = box.text
        if (value is not None) and (value != ''):
            submit_key[name] = value
    return submit_key

###

def request_submission(content):
    """ Parses the submitted request response from Illiad.
        Called by IlliadSession.make_request() """
    out = {
           'transaction_number': None,
           'submitted': False,
           'error': False,
           'message': None
           }

    soup = BeautifulSoup( content, 'html.parser' )
    #Check for submission errors.
    try:
        errors = soup.select('.statusError')[0].text
    except IndexError:
        errors = None
    if errors:
        out['error'] = True
        out['message'] = errors
        return out

    #Get transaction number
    #Article Request Received. Transaction Number 473283
    try:
        confirm_message = soup.select('.statusInformation')[0].text
        out['message'] = confirm_message
        match = re.search(DIGITS_RE, confirm_message)
        if match:
            number = match.groups()[0]
            out['transaction_number'] = number
            out['submitted'] = True
    except IndexError:
        out['error'] = True
        out['message'] = "Unable to find confirmation message"

    return out

###

def parse_user_status( content ):
    """ Parses user-status from change-user-info form.
        Called by lib.illiad3.account.Status.check_user_status() """
    status = 'init'
    soup = BeautifulSoup( content, 'html.parser' )
    status_doc = soup.select( '#StatusGroup' )[0]  # grabs the status-html
    option_docs = status_doc( 'option' )  # grabs all the 'option' elements in the html-fragment
    for option_doc in option_docs:
        attr_dct = option_doc.attrs  # the element's attributes are returned as a dict
        attr_keys = attr_dct.keys()
        if 'selected' in attr_keys:
            status = option_doc.text
            break
    log.debug( 'status, `%s`' % status )
    return status


class UserInfoParser( object ):

    def __init__( self ):
        self.html = None
        self.soup = None

    def parse_user_info( self, username, user_html ):
        """ Parses all user-info from change-user-info form.
            Called by lib.illiad3.account.Status.update_user_status() """
        self.html = user_html
        self.soup = BeautifulSoup( content, 'html.parser' )
        usr_dct = {}

        # usr_dct['FirstName'] = self.parse_first_name()
        usr_dct['FirstName'] = self.parse_input_element( submitted_html=self.html, target_id='FirstName', target_attribute='value' )

        # usr_dct['LastName'] = self.parse_last_name()
        usr_dct['FirstName'] = self.parse_input_element( submitted_html=self.html, target_id='LasName', target_attribute='value' )

        # usr_dct['EMailAddress'] = self.parse_email()
        # usr_dct['Phone'] = self.parse_phone()
        # usr_dct['Address'] = self.parse_address()
        # usr_dct['Site'] = self.parse_site()
        # ## defaults
        # usr_dct['ILLiadForm'] = 'ChangeUserInformation'
        # usr_dct['NotifyGroup'] = 'E-Mail'
        # usr_dct['DeliveryGroup'] = 'Electronic Delivery if Possible'
        # usr_dct['LoanDeliveryGroup'] = 'Hold for Pickup'
        # usr_dct['WebDeliveryGroup'] = 'Yes'
        # usr_dct['NVTGC'] = 'ILL'
        # usr_dct['SubmitButton'] = 'Submit Information'
        # usr_dct['Department'] = self.parse_department()
        log.debug( 'parsed_usr_dct, ```%s```' % pprint.pformat(usr_dct) )
        return usr_dct

    # def parse_first_name( self, submitted_html=None ):
    #     """ Returns existing first-name.
    #         Called by parse_user_info() """
    #     html = self.html if self.html else submitted_html  # submitted_html useful for tests
    #     soup = self.soup if self.soup else BeautifulSoup(html, 'html.parser')
    #     input_doc = soup.select( '#FirstName' )[0]  # grabs the first-name <input> element
    #     attr_dct = input_doc.attrs  # the element's attributes are returned as a dict
    #     log.debug( 'attr_dct, ```%s```' % pprint.pformat(attr_dct) )
    #     first_name = attr_dct['value'].strip()
    #     log.debug( 'first_name, `%s`' % first_name )
    #     return first_name

    def parse_input_element( self, submitted_html, target_id, target_attribute ):
        """ Returns desired value.
            Called by parse_user_info() """
        html = self.html if self.html else submitted_html  # submitted_html useful for tests
        soup = self.soup if self.soup else BeautifulSoup(html, 'html.parser')
        input_doc = soup.select( '#%s' % target_id )[0]  # grabs the first-name <input> element
        attr_dct = input_doc.attrs  # the element's attributes are returned as a dict
        log.debug( 'attr_dct, ```%s```' % pprint.pformat(attr_dct) )
        desired_value = attr_dct[target_attribute].strip()
        log.debug( 'desired_value, `%s`' % desired_value )
        return desired_value

        return 'foo'


    ## end class UserInfoParser()
