# -*- coding: utf-8 -*-

from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic import RedirectView
from illiad_app import views


admin.autodiscover()

urlpatterns = [

    # url( r'^admin/', include(admin.site.urls) ),

    url( r'^info/$', views.info, name='info_url' ),

    url( r'^v2/make_request/$', views.make_request_v2, name='request_v2' ),

    url( r'^check_status_via_shib/$', views.check_status_via_shib, name='check_status_via_shib' ),  # status meaning 'Undergrad', 'Staff', etc.

    url( r'^update_status/$', views.update_status, name='update_status' ),

    url( r'^check_user/$', views.check_user, name='check_user' ),  # checks status meaning 'registered', 'blocked', etc.

    url( r'^error_check/$', views.error_check, name='error_check' ),  # only generates error if DEBUG == True

    url( r'^$',  RedirectView.as_view(pattern_name='info_url') ),

]
