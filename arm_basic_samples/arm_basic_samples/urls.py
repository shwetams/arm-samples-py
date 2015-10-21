#!/usr/bin/env python

#
#
# Copyright (c) Microsoft Corporation
#
# All rights reserved.
#
# MIT License
#
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED *AS IS*, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.
"""arm_basic_samples URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from django.conf.urls.static import static
from django.contrib.staticfiles import views
#import settings
from django.conf.urls import include, url, patterns

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^home/','home.views.home',name='home_page'),
    url(r'^deployment/','deployment_option.views.deployment',name='deployment_option'),
    url(r'^static/(?P<path>.*)$', views.serve),
    url(r'^getvmimagelist/$','deployment_option.views.getvmimagelist',name='getvmimagelist'),    
    url(r'^getvmimagelistbypublishers/$','deployment_option.views.getvmimagepublishers',name='getvmimagepublishers'),
    url(r'^getvmimagelistbyskus/$','deployment_option.views.getvmimageskus',name='getvmimageskus'),
    url(r'^getvmimagelistbyoffers/$','deployment_option.views.getvmimageoffers',name='getvmimageoffers'),
    url(r'^getvmimagelistbyversions/$','deployment_option.views.getvmimageversions',name='getvmimageversions'),    
    url(r'^deploy/$','deployment_option.views.create_deployment',name='create_deployment'),
    url(r'^settings/$','arm_settings.views.set_auth_settings',name='set_auth_settings'),
    url(r'^accesscode/$','deployment_option.views.get_access_code'),
    url(r'^authdetails/$','deployment_option.views.authorization_details',name='get_auth_details'),
    url(r'^openidauth/$', 'aad_integration.views.authorise_user',name='automatic_settings'),
    url(r'^armaccess/$','aad_integration.views.armaccess'),
    url(r'^assignroles/$','aad_integration.views.assignrole'),
    url(r'^getsubscriptionlist/$','deployment_option.views.get_subscription_list',name='get_subscription_list')
]
urlpatterns += patterns('django.contrib.auth.views',url(r'login/$','login',{'template_name':'login.html'},name='deploy_login'),url(r'logout/$','logout',{'next_page':'home_page'},name='deploy_logout'))