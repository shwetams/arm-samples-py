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
from django.shortcuts import render
from django.http import HttpResponse
import json
from django.contrib.auth.models import User
from arm_settings.models import AuthSettings
from django.core.management.base import BaseCommand
from django.contrib.auth.decorators import login_required




@login_required
def set_auth_settings(request):
    if request.method == "POST":
        print(request)
        auth_settings = {}
        auth_settings['auth_type']=request.POST['authtypeid']
        auth_settings['client_id']=request.POST['inp_clientid_txt']
        auth_settings['tenant_id']=request.POST['inp_tenantid_txt']
        auth_settings['redirect_uri']=request.POST['inp_redirecturi_txt']
        auth_settings['client_secret']=request.POST['inp_clientsecret_txt']
        auth_settings['subscription_id']=request.POST['inp_subsid_txt']
        auth_settings['user'] = request.POST['user_id']
        user = User.objects.get(pk=auth_settings['user'])
        if AuthSettings.objects.filter(user_id_id=auth_settings['user']).exists():
            u = AuthSettings.objects.get(user_id_id=auth_settings['user'])
            u.delete()        
        settings = AuthSettings(user_id=user,auth_type=auth_settings['auth_type'],client_id=auth_settings['client_id'],tenant_id=auth_settings['tenant_id'],client_secret=auth_settings['client_secret'],redirect_uri=auth_settings['redirect_uri'],subscription_id=auth_settings['subscription_id'])        
        settings.save()  
        return HttpResponse("Your settings have been saved")
    else:
        authorization_list = [{"id":"A","name":"Application only"},{"id":"U","name":"User based"}]
        template_params = {"authorization_list":authorization_list}
        return render(request,"set_authsettings.html",template_params)
