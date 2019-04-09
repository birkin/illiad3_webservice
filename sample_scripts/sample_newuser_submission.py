# -*- coding: utf-8 -*-

"""
Shows sample call to internal illiad-api to create a new user.

Example json response:
{
  "request": {
    "params": {
      "auth_id": "xxxxx",
      "department": "zzzzz",
      "email": "zzzzz",
      "first_name": "zzzzz",
      "last_name": "zzzzz",
      "phone": "zzzzz",
      "status": "zzzzz"
    },
    "timestamp": "2019-04-02 11:19:39.859287",
    "url": "http://127.0.0.1:8000/create_user/"
  },
  "response": {
    "elapsed_time": "0:00:00.824721",
    "status_data": {
      "status": "Registered",
      "status_code": 200
    }
  }
}
"""

import json, logging, os, pprint, random
import requests


logging.basicConfig(
    level=logging.DEBUG,
    format='[%(asctime)s] %(levelname)s [%(module)s-%(funcName)s()::%(lineno)d] %(message)s',
    datefmt='%d/%b/%Y %H:%M:%S' )
log = logging.getLogger(__name__)


# ==============================
# settings
# ==============================

ILLIAD_API_URL = 'http://127.0.0.1:8000/'
ILLIAD_API_KEY = os.environ['ILLIAD_WS__API_AUTH_KEY']  # note: auth-key is checked, of course, but calling IP must also be in settings list of 'legitimate' IPs.
#
shib_dct = json.loads( os.environ['ILLIAD_WS_SAMPLE_SCRIPT__NEWUSER_SHIBDCT_JSON'] )
if shib_dct['department'] == '':
    shib_dct['department'] = '(not listed)'
AUTH_ID = shib_dct['eppn'].split('@')[0]
FIRST_NAME = shib_dct['name_first']
LAST_NAME = shib_dct['name_last']
EMAIL = shib_dct['email']
TYPE = shib_dct['brown_type']
PHONE = shib_dct['phone']
DEPARTMENT = shib_dct['department']


# ==============================
# hit api
# ==============================

params = {
    'auth_key': ILLIAD_API_KEY,
    'auth_id': AUTH_ID,
    'first_name': FIRST_NAME,
    'last_name': LAST_NAME,
    'email': EMAIL,
    'status': TYPE,
    'phone': PHONE,
    'department': DEPARTMENT
    }
log.debug( 'params, ```%s```' % pprint.pformat(params) )

url = '%s%s' % ( ILLIAD_API_URL, 'create_user/' )

try:
    r = requests.post( url, data=params, verify=True, timeout=10 )
    log.debug( 'response, ```%s```' % pprint.pformat(r.json()) )
except Exception as e:
    log.error( 'Exception on new user registration, ```%s```' % (repr(e)) )
