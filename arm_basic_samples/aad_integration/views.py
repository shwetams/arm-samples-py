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
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.contrib.auth.models import User
from arm_settings.models import AuthSettings, AuthSettings_Admin
from django.core.management.base import BaseCommand
from django.contrib.auth.decorators import login_required
#from jwkest import jwt
import jwt

import urllib
import uuid
from requests import Response, Session, Request
import json

client_id=""
tenant_id=""
subscription_id=""
client_secret=""
redirect_uri=""
### Predefined role definition ID
role_def_id_reader = "acdd72a7-3385-48ef-bd42-f606fba81ae7"
role_def_id_contributor = "b24988ac-6180-42a0-ab88-20f7382dd24c"

def initialise():
    if AuthSettings_Admin.objects.filter(user_id='AAD_Admin').exists():
         admin_authsettings = AuthSettings_Admin.objects.filter(user_id='AAD_Admin')
         for admin_auth in admin_authsettings:
             global client_id
             client_id=admin_auth.client_id
             global tenant_id
             tenant_id =admin_auth.tenant_id
             global subscription_id
             subscription_id = admin_auth.subscription_id
             global redirect_uri
             redirect_uri=admin_auth.redirect_uri
             global client_secret
             client_secret = admin_auth.client_secret
             #res = "Client iD " + admin_auth.client_id
    #else:
        #res = "False"
    #return res


# Create your views here.
def authorise_user(request):
    initialise()
    PROVIDER_ISSUER_URL = "https://login.windows.net/common/OAuth2/Authorize"
    if request.method == "GET":
        isMSA = False
        if(request.GET("isMSA").exists):
           isMSA = request.GET("isMSA")
        
        noonce_val = str(uuid.uuid4())
        if isMSA == True:
            PROVIDER_ISSUER_URL = "https://login.windows.net/common/OAuth2/Authorize?client_id="+client_id+"&response_mode=form_post&response_type=code+id_token&nonce="+ noonce_val + "&redirect_uri=http://127.0.0.1:8000/armaccess/&resource=https://management.azure.com/&scope=openid+profile&domain_hint=live.com"
        else:
            PROVIDER_ISSUER_URL ="https://login.windows.net/common/OAuth2/Authorize?client_id="+client_id+"&response_mode=form_post&response_type=code+id_token&nonce="+ noonce_val + "&redirect_uri=http://127.0.0.1:8000/armaccess/&resource=https://management.azure.com/&scope=openid+profile"
    return redirect(PROVIDER_ISSUER_URL)
    


def assignrole(request):
    initialise()
    subs_list_assigned = []
    if request.method == "POST":
        subs_list = json.loads(request.POST["subs_list"])
        user_id = request.POST["user_id"]
        t_id = request.POST["tenant_id"]
        token_user = request.POST["token_user"]
        global client_secret
        global client_id
        access_token = get_acacess_token_app(tenant_id=t_id,client_id=client_id,client_secret=client_secret,resource="https://graph.windows.net/")
        
        if access_token["status"] == "1":
            principal_id = get_principal_id(token=access_token["details"],tenant_id=t_id,client_id=client_id)
            
            for subs in subs_list:
                role_assgn_id = str(uuid.uuid4())
                global role_def_id_contributor
                put_url = "https://management.azure.com//subscriptions/" + subs +"/providers/Microsoft.Authorization/roleAssignments/" + role_assgn_id + "?api-version=2014-07-01-preview"
                body = {"properties":{"roleDefinitionId":"/subscriptions/"+ subs +"/providers/Microsoft.Authorization/roleDefinitions/" + role_def_id_contributor ,"principalId":principal_id}}
                
                headers_val = {"Authorization":"Bearer " + token_user, "Content-Type":"application/json"}
                req = Request(method="PUT",headers=headers_val,json=body,url=put_url)
                req_prepped = req.prepare()
                s = Session()
                res = Response()
                res = s.send(req_prepped)
                if res.status_code == 201:
                    subs_list_assigned.append({"subscriptionid":subs,"assigned_status":True})
    
    ### Save the subscription details in the model
    subscription_list = []
    for subs in subs_list_assigned:
        subscription_list.append(subs)

    auth_settings = {}
    auth_settings['auth_type']="A"
    auth_settings['client_id']=client_id
    auth_settings['tenant_id']=t_id
    auth_settings['redirect_uri']=redirect_uri
    auth_settings['client_secret']=client_secret
    auth_settings['subscription_id']=json.dumps(subscription_list)
    auth_settings['user'] = user_id
    user = User.objects.get(pk=auth_settings['user'])
    if AuthSettings.objects.filter(user_id_id=auth_settings['user']).exists():
         u = AuthSettings.objects.get(user_id_id=auth_settings['user'])
         u.delete()        
    settings = AuthSettings(user_id=user,auth_type=auth_settings['auth_type'],client_id=auth_settings['client_id'],tenant_id=auth_settings['tenant_id'],client_secret=auth_settings['client_secret'],redirect_uri=auth_settings['redirect_uri'],subscription_id=auth_settings['subscription_id'])        
    settings.save()  
    results = "<table><tr><td>You can now deploy resources through this application into following subscriptions</td></tr>" 
    for sa in subs_list_assigned:
        results += "<tr><td>"+ sa["subscriptionid"] +"</td></tr>"
    results += "</table>"
    
    return HttpResponse(results)



def get_principal_id(token,tenant_id,client_id):
    initialise()
    
    get_url = "https://graph.windows.net/" + tenant_id + "/servicePrincipals?api-version=1.5&$filter=appid%20eq%20'"+  client_id +"'"
    headers = {"Authorization": "Bearer " + token}
    req = Request(method="GET",url=get_url,headers=headers)
    req_prepped = req.prepare()
    principalId = None
    s = Session()
    res = Response()
    res = s.send(req_prepped)
    if (res.status_code==200):
        responseJSON = json.loads(res.content)
        value = responseJSON["value"]
        for val in value:
            principalId = val["objectId"]
            #{"url":get_url,"headers":headers,"token":token,"tenant_id":tenant_id,"client_id":client_id}
    return principalId

def get_acacess_token_app(tenant_id,client_id,client_secret,resource):
    initialise()
    
    url = "https://login.windows.net/" + tenant_id + "/oauth2/token"        
    
    body_data = "&grant_type=client_credentials&resource="+ resource +"&client_id="+ client_id + "&client_secret="+  urllib.quote_plus(client_secret)
    
    headers = {"Content-Type":"application/x-www-form-urlencoded"}
    req = Request(method="POST",url=url,data=body_data)
    req_prepped = req.prepare()
    s = Session()
    res = Response()
    res = s.send(req_prepped)
    access_token_det = {}
    if (res.status_code == 200):
        responseJSON = json.loads(res.content)
        access_token_det["details"]= responseJSON["access_token"]
        access_token_det["status"]="1"
        access_token_det["exp_time"]=responseJSON["expires_in"]
        access_token_det["exp_date"]=responseJSON["expires_on"]
        access_token_det["accessDetails"]=responseJSON
    else:
        access_token_det["details"]= str(res.status_code) + str(res.json())
        access_token_det["status"]="0"
    return access_token_det


@csrf_exempt
def armaccess(request):
    initialise()
    if request.method == "POST":
        code=request.POST["code"]
        
        ## Validate the jwt token
        subscription_lists=[]
        id_token = request.POST["id_token"]
        
        token_payload = jwt.decode(id_token,verify=False)
        
    if token_payload != None:
        
        ## Get access token
        access_token = get_access_token(tenant_id=str(token_payload["tid"]),client_id=client_id,code=code,client_secret=client_secret,redirect_uri=redirect_uri)   
        token_det = access_token["details"]
        ## Get list of subscriptions the user has access to

        subscription_list = get_subscription_list(token_det=token_det)
        
        # Get list of subscriptions that have roleassignments/write action
        if subscription_list != None:
            for subs in subscription_list:
                subs_id = subs["subscriptionId"]
                isEnabled = subs["state"]
                if isEnabled == "Enabled" or isEnabled == "enabled":
                    hasPermission = get_subscription_permissions(token_det=token_det,subscription_id=subs_id)
                    
                    if hasPermission:
                        subscription_lists.append({"id":subs_id,"name":subs["displayName"]})
        
        else:
            subscription_lists.append({"id":"No subscriptions found","name":"No subscription found"})
        token_payload["code"]=code         
        template_params = {"subscriptions":subscription_lists,"tenant_id":str(token_payload["tid"]),"token_user":token_det}
        return render(request,'subscriptionlist.html',template_params)
    else:
        return render(request,subscription_lists)
    

def get_subscription_permissions(token_det, subscription_id):
    initialise()
    url = "https://management.azure.com/subscriptions/"+subscription_id+"/providers/microsoft.authorization/permissions?api-version=2014-07-01-preview"
    headers = {"Authorization":"Bearer " + token_det}
    req = Request(method="GET",url=url,headers=headers)
    req_prepped = req.prepare()
    s = Session()
    res = Response()
    hasPermission = False
    #hasPermission = {}
    res = s.send(req_prepped)
    per_sp = "microsoft.authorization/roleassignments/write"
    per_gen = "microsoft.authorization/*/write"
    hasPermission = res.content
    if (res.status_code == 200):
        resJSON = json.loads(res.content)
        actions_result = resJSON["value"]
        for actions_r in actions_result:
            actions = actions_r["actions"]
            notactions = actions_r["notActions"]
            if per_sp in actions:
                if per_gen not in notactions:
                    hasPermission = True
            else:
                if per_gen in actions:
                    if per_gen not in notactions:
                        hasPermission = True
    return hasPermission

def get_subscription_list(token_det):
    initialise()
    subs_url = "https://management.azure.com/subscriptions?api-version=2014-04-01-preview"
    headers = {"Authorization":"Bearer " + token_det }
    req = Request(method="GET",url=subs_url,headers=headers)
    req_prepped = req.prepare()
    s = Session()
    res = Response()
    res = s.send(req_prepped)
    subs_list = []
    if (res.status_code == 200):
        resJSON = json.loads(res.content)
        subs_list = resJSON["value"]
    else:
        subs_err = {}
        subs_err["state"]="error"
        subs_err["subscriptionId"]="Error"
        subs_err["displayName"] = res.content + "token " + token_det
        subs_list.append(subs_err)
    return subs_list

def get_access_token(tenant_id,client_id,code,client_secret,redirect_uri):
    initialise()
    url = "https://login.microsoftonline.com/" + tenant_id + "/oauth2/token"        
    #body_data_json = {"grant_type":"client_credentials","resource":"https://management.core.windows.net/","client_id":client_id,"client_secret":client_secret}
    body_data = "&grant_type=authorization_code&redirect_uri="+ urllib.quote_plus(redirect_uri) +"&client_id="+ client_id + "&code="+  urllib.quote_plus(code)+"&client_secret="+urllib.quote_plus(client_secret)
    #body_data = urllib.urlencode(body_data_json)
    headers = {"Content-Type":"application/x-www-form-urlencoded"}
    req = Request(method="POST",url=url,data=body_data)
    req_prepped = req.prepare()
    s = Session()
    res = Response()
    res = s.send(req_prepped)
    access_token_det = {}
    if (res.status_code == 200):
        responseJSON = json.loads(res.content)
        access_token_det["details"]= responseJSON["access_token"]
        access_token_det["status"]="1"
        access_token_det["exp_time"]=responseJSON["expires_in"]
        access_token_det["exp_date"]=responseJSON["expires_on"]
        access_token_det["accessDetails"]=responseJSON
    else:
        access_token_det["details"]= str(res.status_code) + str(res.json())
        access_token_det["status"]="0"
    return access_token_det

