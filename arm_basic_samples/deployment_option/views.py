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
from django.http import HttpResponse, HttpResponseRedirect
import json
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
import datetime, time
from arm_settings.models import AuthSettings,AuthSettings_Admin
import requests
import urllib
from requests import Request,Response, Session
import requests.auth, requests.status_codes
import utilities.arm_framework as arm_fw
import authentication.app_auth as app_auth


REDIRECT_URI ="http://127.0.0.1:8000/accesscode/"
# Create your views here.
@login_required
def get_subscription_list(request):
    if request.method=="GET":
        user_id = request.GET["user_id"]
        if AuthSettings.objects.filter(user_id=user_id):
            auth_setting = AuthSettings.objects.get(user_id_id=user_id)
            subscription_ids=auth_setting.subscription_id
    return HttpResponse(json.dumps(subscription_ids))

@login_required
def deployment(request):
    # Getting the list of locations
    locations = [{"id":"west us","name":"west us"},{"id":"east us","name":"east us"},{"id":"southeast asia","name":"southeast asia"}] 
    # Getting storage account type
    stor_acc_types = ["LRS","ZRS","GRS","RA-GRS"]    
    # Getting pricing tier
    #pricing_tier = 
    template_params = {}
    if AuthSettings_Admin.objects.filter(user_id='Admin').exists():
        admin_authsettings = AuthSettings_Admin.objects.filter(user_id='Admin')
        for admin_auth in admin_authsettings:
            client_id = admin_auth.client_id
            tenant_id=admin_auth.tenant_id
            subscription_id=admin_auth.subscription_id
            client_secret =admin_auth.client_secret
            token = get_access_token(tenant_id=tenant_id,client_id=client_id,client_secret=client_secret)
            if token["status"]=="1":
                ts = time.time()
                
                if (float(token["exp_date"]) - ts) > 10:
                    #arm_fw.get_list_regions
                    loc_list = arm_fw.get_list_regions(token["details"],subscription_id)
                    locations = []
                    for loc in loc_list:
                        locations.append({"id":loc["id"],"name":loc["name"]})
                    #locations = [{"id":"west us","name":"west us"},{"id":"east us","name":"east us"},{"id":"southeast asia","name":"southeast asia"}]                    
                    pricing_tier = arm_fw.get_list_vm_sizes(token["details"],subscription_id)
                    stor_acc_types = arm_fw.get_list_storage_types(token["details"],subscription_id)                    
                    #pub_list = getvmimagepublishers()
                    #tokenDet = pricing_tier
                    #stor_acc_types = ["LRS","ZRS","GRS","RA-GRS"]
                    #pricing_tier = ["A1","A2","A3","DS1","DS2"]
                    #vmimagelist = [{"imageid":"imageid1","imagelabel":"image label 1"},{"imageid":"image id 2","imagelabel":"image label 2"}]
                    template_params = {"location_list":locations,"storage_acc_type_list":stor_acc_types,"pricing_tier_list":pricing_tier,"token":loc_list}
    else:
        ## modify to read from storage
        locations = [{"id":"west us","name":"west us"},{"id":"east us","name":"east us"},{"id":"southeast asia","name":"southeast asia"}]
        stor_acc_types = ["LRS","ZRS","GRS","RA-GRS"]
        pricing_tier = ["A1","A2","A3","DS1","DS2"]
        vmimagelist = [{"imageid":"imageid1","imagelabel":"image label 1"},{"imageid":"image id 2","imagelabel":"image label 2"}]
        template_params = {"location_list":locations,"storage_acc_type_list":stor_acc_types,"pricing_tier_list":pricing_tier}
    

    
    return render(request,'deployment_option.html',template_params)

#def getvmimagepublishers(request):
#    vm_img_pub = []
#    if request.method == "GET":


@login_required
def getvmimagepublishers(request):
    pub_list = []
    if request.method == "GET":
        region_name = request.GET["region"]
        if AuthSettings_Admin.objects.filter(user_id="Admin").exists():
            admin_authsettings = AuthSettings_Admin.objects.filter(user_id="Admin")
            for admin_auth in admin_authsettings:
                client_id = admin_auth.client_id
                tenant_id=admin_auth.tenant_id
                subscription_id=admin_auth.subscription_id
                client_secret =admin_auth.client_secret
                token = get_access_token(tenant_id=tenant_id,client_id=client_id,client_secret=client_secret)
                if token["status"]=="1":
                    acc_token = token["details"]
                    pub_list = arm_fw.get_list_vm_publishers(access_token=acc_token, subscription_id=subscription_id,region_name=region_name)
    if pub_list.count <= 0:
        pub_list=[{"id":"Error","name":"Error retrieving publisher list"}]
    return HttpResponse(json.dumps(pub_list))

@login_required
def getvmimageoffers(request):
    offer_list = []
    if request.method == "GET":
        region_name = request.GET["region"]
        publisher_name = request.GET["publisher"]
        if AuthSettings_Admin.objects.filter(user_id="Admin").exists():
            admin_authsettings = AuthSettings_Admin.objects.filter(user_id="Admin")
            for admin_auth in admin_authsettings:
                client_id = admin_auth.client_id
                tenant_id=admin_auth.tenant_id
                subscription_id=admin_auth.subscription_id
                client_secret =admin_auth.client_secret
                token = get_access_token(tenant_id=tenant_id,client_id=client_id,client_secret=client_secret)
                if token["status"]=="1":
                    acc_token = token["details"]
                    offer_list = arm_fw.get_list_vm_offers(access_token=acc_token, subscription_id=subscription_id,region_name=region_name,publisher_name=publisher_name)
    if offer_list.count <= 0:
        offer_list=[{"id":"Error","name":"Error retrieving publisher list"}]
    return HttpResponse(json.dumps(offer_list))

@login_required
def getvmimageskus(request):
    skus_list = []
    if request.method == "GET":
        region_name = request.GET["region"]
        publisher_name = request.GET["publisher"]
        offer = request.GET["offer"]
        if AuthSettings_Admin.objects.filter(user_id="Admin").exists():
            admin_authsettings = AuthSettings_Admin.objects.filter(user_id="Admin")
            for admin_auth in admin_authsettings:
                client_id = admin_auth.client_id
                tenant_id=admin_auth.tenant_id
                subscription_id=admin_auth.subscription_id
                client_secret =admin_auth.client_secret
                token = get_access_token(tenant_id=tenant_id,client_id=client_id,client_secret=client_secret)
                if token["status"]=="1":
                    acc_token = token["details"]
                    skus_list = arm_fw.get_list_vm_skus(access_token=acc_token, subscription_id=subscription_id,region_name=region_name,publisher_name=publisher_name,offer_name=offer)
    if skus_list.count <= 0:
        skus_list=[{"id":"Error","name":"Error retrieving publisher list"}]
    return HttpResponse(json.dumps(skus_list))

@login_required
def getvmimageversions(request):
    versions_list = []
    if request.method == "GET":
        region_name = request.GET["region"]
        publisher_name = request.GET["publisher"]
        offer = request.GET["offer"]
        skus = request.GET["skus"]
        if AuthSettings_Admin.objects.filter(user_id="Admin").exists():
            admin_authsettings = AuthSettings_Admin.objects.filter(user_id="Admin")
            for admin_auth in admin_authsettings:
                client_id = admin_auth.client_id
                tenant_id=admin_auth.tenant_id
                subscription_id=admin_auth.subscription_id
                client_secret =admin_auth.client_secret
                token = get_access_token(tenant_id=tenant_id,client_id=client_id,client_secret=client_secret)
                if token["status"]=="1":
                    acc_token = token["details"]
                    versions_list = arm_fw.get_list_vm_versions(access_token=acc_token, subscription_id=subscription_id,region_name=region_name,publisher_name=publisher_name,offer_name=offer,sku_name=skus)
    if versions_list.count <= 0:
        versions_list=[{"id":"Error","name":"Error retrieving publisher list"}]
    return HttpResponse(json.dumps(versions_list))

@login_required
def getvmimagelist(request):
    vm_img_list = [{}]
    if request.method == "GET":
        vm_img_list=[{"publisher":"pub 1","offer":"offer 1","skus":"skus 1","version":"ver 1"},{"publisher":"pub 2","offer":"offer 2","skus":"skus 2","version":"ver 2"}]
        #region_name = request.GET["region"]
        #if AuthSettings_Admin.objects.filter(user_id='Admin').exists():
        #    admin_authsettings = AuthSettings_Admin.objects.filter(user_id='Admin')
        #    for admin_auth in admin_authsettings:
        #        client_id = admin_auth.client_id
        #        tenant_id=admin_auth.tenant_id
        #        subscription_id=admin_auth.subscription_id
        #        client_secret =admin_auth.client_secret
        #        token = get_access_token(tenant_id=tenant_id,client_id=client_id,client_secret=client_secret)
        #        if token["status"]=="1":
        #            acc_token = token["details"]
        #            vm_img_list = arm_fw.get_list_vm_images(access_token=acc_token, subscription_id=subscription_id,region_name=region_name)
    if vm_img_list.count <= 0:
        vm_img_list = [{"publisher":"Error fetching details","offer":"Error fetching details","skus":"Error fetching details","version":"Error fetching details"}]
    return HttpResponse(json.dumps(vm_img_list),content_type='application/json')

@login_required
def get_access_code(request):
    query_string = request.META["QUERY_STRING"]
    code_det = {"code":query_string}
    htmlstring = "<html><head></title><script type='text/javascript'>window.opener.get_access_code("+json.dumps(code_det)+");window.close();</script></head><body></body></html>"
    return HttpResponse(htmlstring)


@login_required
def authorization_details(request):
    auth_response = {}
    #response = HttpResponse()
    if request.method== "POST":
        user_id = request.POST["user_id"]
        auth_setting = AuthSettings.objects.get(user_id_id=user_id)
        auth_type = auth_setting.auth_type
        client_id = auth_setting.client_id
        tenant_id = auth_setting.tenant_id
        client_secret = auth_setting.client_secret
        if(auth_type=="A"):
            auth_response["auth_type"] = auth_type
            #token = get_access_token(tenant_id=tenant_id,client_id=client_id,client_secret=client_secret)
            #auth_response["auth_token"] = token["details"]
        if(auth_type=="U"):
            authorize_url = "https://login.microsoftonline.com/" + tenant_id +"/oauth2/authorize?client_id="+client_id+"&response_type=code"
            auth_response["auth_type"] = auth_type
            auth_response["auth_code_url"] = authorize_url            
            auth_response["auth_token"]= None
            #response.content = auth_response
            #response.status_code = 200        
    else:
        auth_response["error"]="Invalid response"
        #response.status_code = 500
        #response.content = auth_response
    return HttpResponse(json.dumps(auth_response))

@login_required
def create_deployment(request):
    token_result = {}
    res_grp_created = False
    vnet_created = False
    stor_acc_created = False

    while True:
        try:
            
            if request.method == "POST":
                status = True                       
                # Get User details
                user_id = request.POST["user_id"]
                client_id=None
                tenant_id=None
                client_id=None
                client_secret = None
                redirect_uri=None
                subscription_id=None
                if user_id != None:
                    auth_setting = AuthSettings.objects.get(user_id_id=user_id)
                    auth_type = auth_setting.auth_type
                    client_id = auth_setting.client_id
                    tenant_id = auth_setting.tenant_id
                    client_secret =  auth_setting.client_secret
                    redirect_uri=auth_setting.redirect_uri
                    
                    if auth_type == "U":
                        auth_code = request.POST["auth_code"]
                        token_url = "https://login.microsoftonline.com/" + tenant_id+"/oauth2/token"
                        #body_json = {"grant_type":"authorization_code","code":auth_code,"redirect_uri":redirect_uri,"client_id":client_id,"client_secret":client_secret,"resource":"https://management.core.windows.net/"}
                        #body = urllib.urlencode(body_json)
                        body="grant_type=authorization_code&code="+auth_code+"&redirect_uri="+redirect_uri+"&client_id="+client_id+"&client_secret="+ urllib.quote_plus(client_secret)+"&resource=https://management.core.windows.net/"
                        #body="grant_type=authorization_code&code="+auth_code+"&redirect_uri="+redirect_uri+"&resource=https://management.core.windows.net/"
                        #body="grant_type=authorization_code&code="+auth_code+"&redirect_uri="+REDIRECT_URI+"&client_id="+client_id+"&client_secret="+client_secret+"&resource=https://management.core.windows.net/"
                        headers ={"Content-Type":"application/x-www-form-urlencoded"}
                        #proxies={'https':'http://127.0.0.1:8888'}
                        req = Request(method="POST",url=token_url,data=body)
                        req_prepped = req.prepare()
                        s = Session()                        
                        #s.proxies = proxies
                        #s.verify = False
                        res = Response()
                        res = s.send(req_prepped)
                        
                        responseJSON = json.loads(res.content)
                        #token = "code"
                        token = responseJSON["access_token"]
                        #token = responseJSON
                        token_result = {"POSTURL":token_url,"body":body,"headers":headers,"Response":responseJSON}
                    else:
                        res = get_access_token(tenant_id=tenant_id,client_id=client_id,client_secret=client_secret)
                        token_result = {"Response":res}
                        if(res["status"]=="1"):
                            token = res["details"]
                        else:
                            token=None
                    deploymentDetails = request.POST
                    subscription_id=deploymentDetails["subscriptionID"]    
                
                else:
                    status = False
                if token != None and subscription_id != None and deploymentDetails["resourceGroupName"] != None and deploymentDetails["location"] != None:
                    #res_grp_created = {"Token":token,"subs_id:":subscription_id,"client_id":client_id,"tenant_id":tenant_id,"auth_type":auth_type,"client_secret":client_secret}
                    res_grp_name_created = False
                    vnet_created = False
                    stor_acc_created = False
                    vm_created = False
                    stor_acc_created_name = None
                    vnet_name_created = None
                    res_grp_created_status = arm_fw.create_resource_group(access_token=token,subscription_id=subscription_id,resource_group_name=deploymentDetails["resourceGroupName"],region=deploymentDetails["location"])
                    if res_grp_created_status["success"]:
                        res_grp_created = True
                        res_grp_name_created = res_grp_created_status["resource_created"]
                        token_result["res_grp_status"] = {"res_group_created":True, "res_grp_name":res_grp_name_created}
                    if res_grp_created:
                        vnet_created_status = arm_fw.create_virtual_network(access_token=token,subscription_id=subscription_id,resource_group_name=res_grp_name_created,virtualnetwork_name=deploymentDetails["vnetName"],region=deploymentDetails["location"], subnets=None,addresses=None,dns_servers=None)
                        if vnet_created_status["success"]:
                            vnet_created = True
                            vnet_name_created = vnet_created_status["resource_created"]
                            subnet_name_created = vnet_created_status["subnet_name"]
                            token_result["vnet_status"]= {"vnet_created":True,"vnet_name":vnet_created_status["resource_created"]} 
                    if vnet_created:
                         
                        stor_acc_created_status = arm_fw.create_storage_account(access_token=token,subscription_id=subscription_id,resource_group_name=res_grp_name_created,storage_account_name=deploymentDetails["storageAccountName"],region=deploymentDetails["location"],storage_type=deploymentDetails["storageAccountType"])
                        if stor_acc_created_status["success"]:
                            stor_acc_created = True
                            stor_acc_created_name = stor_acc_created_status["resource_created"]
                            token_result["stor_acc_status"]={"stor_acc_created":True,"stor_acc_name":stor_acc_created_status["resource_created"]}
                        #############
                    if stor_acc_created:
                        vm_created_status = arm_fw.create_virtual_machine(access_token=token,subscription_id=subscription_id,resource_group_name=res_grp_name_created,vm_name=deploymentDetails["vmName"],vnet_name=vnet_name_created,subnet_name=subnet_name_created,vm_size=deploymentDetails["vmPricingTier"],storage_name=stor_acc_created_name,region=deploymentDetails["location"],vm_username=deploymentDetails["vmUserName"],vm_password=deploymentDetails["vmPassword"],publisher=deploymentDetails["vmPublisher"],offer=deploymentDetails["vmOffer"],sku=deploymentDetails["vmSKU"],version=deploymentDetails["vmVersion"])
                        
                        if vm_created_status["success"]:
                            vm_created = True
                            vm_created_name = vm_created_status["resource_created"]
                            token_result["vm_status"]={"vm_created":True,"vm_name_created":vm_created_name}
                        token_result["vmdetails"]= {"access_token":token,"subscription_id":subscription_id,"resource_group_name":res_grp_name_created,"vm_name":deploymentDetails["vmName"],"vnet_name":vnet_name_created,"subnet_name":subnet_name_created,"vm_size":deploymentDetails["vmPricingTier"],"storage_name":stor_acc_created_name,"region":deploymentDetails["location"],"vm_username":deploymentDetails["vmUserName"],"vm_password":deploymentDetails["vmPassword"],"publisher":deploymentDetails["vmPublisher"],"offer":deploymentDetails["vmOffer"],"sku":deploymentDetails["vmSKU"],"version":deploymentDetails["vmVersion"]}
                else:
                    res_grp_created = "Insufficient data to create resource group"
                    token_result = {"status":res_grp_created}
            break

        except RuntimeError as e:
            token = {"error":e.strerror}
            #deploymentDetails = 
            #access_token = app_auth.get_access_token()
        
            # Create Resource Group
            # Create VNet
            # create Storage Account
            # Create VM
    return HttpResponse(json.dumps(token_result),content_type='application/json')

def get_access_token(tenant_id,client_id,client_secret):    
    
    url = "https://login.microsoftonline.com/" + tenant_id + "/oauth2/token"        
    #body_data_json = {"grant_type":"client_credentials","resource":"https://management.core.windows.net/","client_id":client_id,"client_secret":client_secret}
    body_data = "&grant_type=client_credentials&resource=https://management.core.windows.net/&client_id="+ client_id + "&client_secret="+  urllib.quote_plus(client_secret)
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

