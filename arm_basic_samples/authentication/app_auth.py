#import oauthlib
#from oauthlib import oauth2
#import urllib.request
#import urllib.response, urllib.error
import requests
from requests import Request,Response, Session
import requests.auth, requests.status_codes

def get_access_token(tenant_id,client_id,client_secret):
    url = "https://login.windows.net/"+tenant_id + "/token"
    body_data = "grant_type=client_credentials&client_id="+ client_id + "&resource=https://graph.windows.net/&client_secret=" + client_secret
    headers = {"Content-Type":"application/x-www-form-urlencoded"}
    req = Request(method="POST",url=url,data=body_data)
    req_prepped = req.prepare()
    s = Session()
    res = Response()
    res = s.send(req_prepped)
    access_token_det = {}
    if (res.status_code == 200):
        responseJSON = json.loads(res.content)
        access_token_det= responseJSON
        access_token_det["status"]="1"
    else:
            access_token_det["status"]="0"
    return access_token_det