#!/usr/bin/env python
#  -*- coding: utf-8 -*-
# Copyright under  the latest Apache License 2.0

'''
A modification of the python twitter oauth library by Hameedullah Khan.
Instead of inheritance from the python-twitter library, it currently
exists standalone with an all encompasing ApiCall function. There are
plans to provide wrapper functions around common requests in the future.

Requires:
  simplejson
  oauth2
'''

__author__ = "Konpaku Kogasa, Hameedullah Khan"
__version__ = "0.1"

# Library modules
import urllib
import urllib2
import urlparse
import time
import logging

try:
    from urlparse import parse_qs, parse_qsl
except ImportError:
    from cgi import parse_qs, parse_qsl


from .. import oauth2 as oauth
from config import settings

# Taken from oauth implementation at: http://github.com/harperreed/twitteroauth-python/tree/master
REQUEST_TOKEN_URL = 'https://twitter.com/oauth/request_token'
ACCESS_TOKEN_URL = 'https://twitter.com/oauth/access_token'
AUTHORIZATION_URL = 'https://twitter.com/oauth/authorize'
SIGNIN_URL = 'https://twitter.com/oauth/authenticate'
API_URL = 'https://api.twitter.com/1/' 

class OAuthApi():
    def __init__(self, consumer_key, consumer_secret, token=None, token_secret=None):
        if token and token_secret:
            token = oauth.Token(token, token_secret)
        else:
            token = None
        self._Consumer = oauth.Consumer(consumer_key, consumer_secret)
        self._signature_method = oauth.SignatureMethod_HMAC_SHA1()
        self._access_token = token 

    def _GetOpener(self):
        opener = urllib2.build_opener()
        return opener

    def _FetchUrl(self,
                    url,
                    http_method=None,
                    parameters=None):
        '''Fetch a URL, optionally caching for a specified time.
    
        Args:
          url: The URL to retrieve
          http_method: 
          	One of "GET" or "POST" to state which kind 
          	of http call is being made
          parameters:
            A dict whose key/value pairs should encoded and added 
            to the query string, or generated into post data. [OPTIONAL]
            depending on the http_method parameter
    
        Returns:
          A string containing the body of the response.
        '''
        # Build the extra parameters dict
        extra_params = {}
        if parameters:
          extra_params.update(parameters)
        
        req = self._makeOAuthRequest(url, params=extra_params, 
                                                    http_method=http_method)
        
        # Get a url opener that can handle Oauth basic auth
        opener = self._GetOpener()

        if http_method == "POST":
            encoded_post_data = req.to_postdata()
            #print url,encoded_post_data
            url = req.normalized_url
        else:
            url = req.to_url()
            encoded_post_data = ""
        if encoded_post_data:
            url_data = opener.open(url, encoded_post_data).read()
        else:
            url_data = opener.open(url).read()
        opener.close()
    
        # Always return the latest version
        return url_data
    
    def _makeOAuthRequest(self, url, token=None,
                                        params=None, http_method="GET"):
        '''Make a OAuth request from url and parameters
        
        Args:
          url: The Url to use for creating OAuth Request
          parameters:
             The URL parameters
          http_method:
             The HTTP method to use
        Returns:
          A OAauthRequest object
        '''
        
        oauth_base_params = {
        'oauth_version': "1.0",
        'oauth_nonce': oauth.generate_nonce(),
        'oauth_timestamp': int(time.time())
        }
        
        if params:
            params.update(oauth_base_params)
        else:
            params = oauth_base_params
        
        if not token:
            token = self._access_token
        request = oauth.Request(method=http_method,url=url,parameters=params)
        request.sign_request(self._signature_method, self._Consumer, token)
        return request

    def getAuthorizationURL(self, token, url=AUTHORIZATION_URL):
        '''Create a signed authorization URL
        
        Returns:
          A signed OAuthRequest authooauth_token_secretrization URL 
        '''
        
        return "%s?oauth_token=%s" % (url, token['oauth_token'])

    def getRequestToken(self, url=REQUEST_TOKEN_URL):
        '''Get a Request Token from Twitter
        
        Returns:
          A OAuthToken object containing a request token
        '''
        resp, content = oauth.Client(self._Consumer).request(url, "GET")
        if resp['status'] != '200':
            raise Exception("Invalid response %s." % resp['status'])

        return dict(parse_qsl(content))
    
    def getAccessToken(self, token, verifier, url=ACCESS_TOKEN_URL):
        '''Get a Request Token from Twitter
        
        Returns:
          A OAuthToken object containing a request token
        '''
        token = oauth.Token(token['oauth_token'], token['oauth_token_secret'])
        token.set_verifier(verifier)
        client = oauth.Client(self._Consumer, token)
        resp, content = client.request(url, "POST")
        return dict(parse_qsl(content))
    
    
    def ApiCall1(self, call, type="GET", parameters={}):
        if parameters.has_key('x_auth_mode'):#twitter iphone xauth
            f1 = open(settings.get_home_dir() + 'token.txt','r')
            str1 = f1.read()
            f1.close()
            l1 = str1.split(';')
            print 'l1 is ', l1
            rv = u'oauth_token=' + l1[0].replace(r'ot=','').decode('utf-8')
            rv += u'&oauth_token_secret=' + l1[1].replace(r'ots=','').decode('utf-8')
            rv += u'&screen_name=' + l1[3].replace(r'sc_name=','').decode('utf-8')
            rv += u'&user_id=' + l1[4].replace(r'us_id=','').decode('utf-8')
            #rv += u'&x_auth_expires=0'
            return rv
        if parameters.has_key('oauth_nonce'):parameters.pop('oauth_nonce')
        if parameters.has_key('oauth_timestamp'):parameters.pop('oauth_timestamp')
        if parameters.has_key('oauth_consumer_key'):parameters.pop('oauth_consumer_key')
        if parameters.has_key('oauth_version'):parameters.pop('oauth_version')
        if parameters.has_key('oauth_token'):parameters.pop('oauth_token')
        if parameters.has_key('oauth_signature'):parameters.pop('oauth_signature')

        if parameters.has_key('application_id'):parameters.pop('application_id')
        if parameters.has_key('pc'):parameters.pop('pc')
        if parameters.has_key('send_error_codes'):parameters.pop('send_error_codes')

        if call.startswith('1/') or call.startswith('i/'):
            call = '1.1' + call[call.find('/'):]
        if not call.startswith('1.1/'):
            call = '1.1/' + call
        logging.debug('https://api.twitter.com/' + call + ' ' + str(parameters))
        data1 = self._FetchUrl('https://api.twitter.com/' + call , type, parameters)
        return data1 
