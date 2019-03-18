# -*- coding: utf-8 -*-

import datetime, logging, pprint, random, time
from illiad_app import settings_app
from illiad_app.lib.illiad3.account import Status as LibStatusModule


log = logging.getLogger(__name__)


class UserHandler( object ):

    def __init__( self ):
        self.request_id = random.randint( 1111, 9999 )  # to follow logic if simultaneous hits
        self.status_module = LibStatusModule( settings_app.ILLIAD_REMOTE_AUTH_URL, settings_app.ILLIAD_REMOTE_AUTH_KEY )
