# -*- coding: utf-8 -*-

import json, os


README_URL = os.environ['ILLIAD_WS__DOCS']

API_KEY = os.environ['ILLIAD_WS__API_AUTH_KEY']
LEGIT_IPS = json.loads( os.environ['ILLIAD_WS__LEGIT_IPS_JSON'] )

ILLIAD_REMOTE_AUTH_URL = os.environ['ILLIAD_WS__REMOTE_AUTH_URL']
ILLIAD_REMOTE_AUTH_KEY = os.environ['ILLIAD_WS__REMOTE_AUTH_KEY']


## for testing

TEST_AUTH_KEY = os.environ['ILLIAD_WS__API_AUTH_KEY']

TEST_EXISTING_GOOD_USER = os.environ['ILLIAD_WS__TEST_EXISTING_GOOD_USER']
TEST_NEW_USER_ROOT = os.environ['ILLIAD_WS__TEST_NEW_USER_ROOT']
