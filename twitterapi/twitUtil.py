#!/usr/bin/python
#coding:utf-8

import oauth2 as oauth
from oauthtwitter import OAuthApi
from config import settings

def get_auth_url():
    twitter = OAuthApi(settings.consumer_key, settings.consumer_secret)
    temp_credentials = twitter.getRequestToken()
    return temp_credentials,twitter.getAuthorizationURL(temp_credentials)

def get_access_token(credentials,oauth_verifier):
    twitter = OAuthApi(settings.consumer_key, settings.consumer_secret)
    access_token = twitter.getAccessToken(credentials, oauth_verifier)
    return access_token
    
def MakeApiCall(access_token, call, type="GET", Parameters={}):
    for each in Parameters.keys():
        Parameters[each] = Parameters[each].encode('utf-8')
    twitter = OAuthApi(settings.consumer_key, settings.consumer_secret, access_token['oauth_token'], access_token['oauth_token_secret'])
    return twitter.ApiCall1(call,type,Parameters)
    
