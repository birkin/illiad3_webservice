# -*- coding: utf-8 -*-

import datetime, json, logging, os, pprint
from django.conf import settings as project_settings
from django.contrib.auth import logout
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseNotFound, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from illiad_app.lib import info_helper
from illiad_app.lib.status import CheckStatusHandler, UpdateStatusHandler
from illiad_app.models import V2_Helper


log = logging.getLogger(__name__)


def info( request ):
    """ Returns basic data including branch & commit. """
    log.debug( 'user-agent, ```%s```; ip, ```%s```; referrer, ```%s```' %
        (request.META.get('HTTP_USER_AGENT', None), request.META.get('REMOTE_ADDR', None), request.META.get('HTTP_REFERER', None)) )
    rq_now = datetime.datetime.now()
    commit = info_helper.get_commit()
    branch = info_helper.get_branch()
    info_txt = commit.replace( 'commit', branch )
    resp_now = datetime.datetime.now()
    taken = resp_now - rq_now
    context_dct = info_helper.make_context( request, rq_now, info_txt, taken )
    output = json.dumps( context_dct, sort_keys=True, indent=2 )
    return HttpResponse( output, content_type='application/json; charset=utf-8' )


def make_request_v2( request ):
    """ Handles current (October 2015) easyBorrow controller illiad call. """
    log.debug( 'starting' )
    # log.debug( 'request.__dict__, `%s`' % pprint.pformat(request.__dict__) )
    v2_helper = V2_Helper( request.POST.get('request_id', 'no_id') )
    if v2_helper.check_validity( request ) is False:
        return HttpResponseBadRequest( 'Bad Request' )
    v2_response_dct = v2_helper.run_request( request )
    output = json.dumps( v2_response_dct, sort_keys=True, indent=2 )
    return HttpResponse( output, content_type='application/json; charset=utf-8' )


def check_status_via_shib( request ):
    """ Handles shib-protected check-user-status. """
    # log.debug( 'request_dct, ```%s```' % pprint.pformat(request.__dict__) )
    rq_now = datetime.datetime.now()
    status_checker_handler = CheckStatusHandler()
    log.debug( '%s - starting' % status_checker_handler.request_id )
    if status_checker_handler.data_check( request ) == 'invalid':
        return HttpResponseBadRequest( 'Bad Request' )
    result_data = status_checker_handler.check_statuses( request )
    output_dct = status_checker_handler.prep_output_dct( rq_now, request, result_data )
    output = json.dumps( output_dct, sort_keys=True, indent=2 )
    return HttpResponse( output, content_type='application/json; charset=utf-8' )


def update_status( request ):
    """ Interface for updating user-status. """
    # log.debug( 'request_dct, ```%s```' % pprint.pformat(request.__dict__) )
    rq_now = datetime.datetime.now()
    status_update_handler = UpdateStatusHandler()
    log.debug( '%s - starting' % status_update_handler.request_id )
    if status_update_handler.data_check( request ) == 'invalid':
        return HttpResponseBadRequest( 'Bad Request' )
    result_data = status_update_handler.manage_status_update( request, rq_now )
    output_dct = json.dumps( result_data, sort_keys=True, indent=2 )
    return HttpResponse( output_dct, content_type='application/json; charset=utf-8' )


def error_check( request ):
    """ For checking that admins receive error-emails. """
    if project_settings.DEBUG == True:
        1/0
    else:
        return HttpResponseNotFound( '<div>404 / Not Found</div>' )
