# -*- coding: utf-8 -*-

import datetime, json, logging, os, subprocess
from illiad_app import settings_app
from django.conf import settings
# from django.core.urlresolvers import reverse


log = logging.getLogger(__name__)


def get_commit():
    """ Returns commit-string.
        Called by views.info() """
    original_directory = os.getcwd()
    log.debug( 'BASE_DIR, ```%s```' % settings.BASE_DIR )
    git_dir = settings.BASE_DIR
    log.debug( 'git_dir, ```%s```' % git_dir )
    os.chdir( git_dir )
    output_utf8 = subprocess.check_output( ['git', 'log'], stderr=subprocess.STDOUT )
    output = output_utf8.decode( 'utf-8' )
    os.chdir( original_directory )
    lines = output.split( '\n' )
    commit = lines[0]
    return commit


def get_branch():
    """ Returns branch.
        Called by views.info() """
    ( original_directory, branch ) = ( os.getcwd(), 'init' )
    os.chdir( settings.BASE_DIR )
    output_utf8 = subprocess.check_output( ['git', 'branch'], stderr=subprocess.STDOUT )
    output = output_utf8.decode( 'utf-8' )
    os.chdir( original_directory )
    lines = output.split( '\n' )
    for line in lines:
        if line[0:1] == '*':
            branch = line[2:]
            break
    return branch


def make_context( request, rq_now, info_txt, taken ):
    """ Builds and returns context.
        Called by views.info() """
    cntxt = {
        'request': {
            'url': '%s://%s%s' % (
                request.scheme,
                request.META.get( 'HTTP_HOST', '127.0.0.1' ),  # HTTP_HOST doesn't exist for client-tests
                request.META.get('REQUEST_URI', request.META['PATH_INFO']) ),
            'timestamp': str( rq_now )
            },
        'response': assemble_response_dct( request, info_txt, taken )
        }
    return cntxt


def assemble_response_dct( request, info_txt, taken ):
    """ Returns response part of context dct.
        Called by make_context() """

    response_dct = {
        'documentation': settings_app.README_URL,
        'version': info_txt,
        'elapsed_time': str( taken ),
        }
    if settings.DEBUG == True:
        response_dct['ip'] = request.META.get( 'REMOTE_ADDR', 'unavailable' )
        response_dct['user_agent'] = request.META.get( 'HTTP_USER_AGENT', 'unavailable' )
    return response_dct
