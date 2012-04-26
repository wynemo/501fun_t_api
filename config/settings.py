#!/usr/bin/env python
# coding: utf-8
import web, os

def get_home_dir():
    try:
        dir1 = os.environ['OPENSHIFT_REPO_DIR']
        if dir1.endswith('/') == False:
            dir1 += '/'
        dir1 += 'wsgi/'
        return dir1
    except:
        return './'

render = web.template.render(get_home_dir() + 'templates/', cache=False)

web.config.debug = False

consumer_key = ""
consumer_secret = ""

#for j.mp link
no_jmp = True 
bitly_name = ''
bitly_key = ''

