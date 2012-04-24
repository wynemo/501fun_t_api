#!/usr/bin/env python
#coding:utf-8

import web
from config import settings

urls = ('/','twitterapi.ttcbk.index',
    '/auth','twitterapi.ttauth.auth',
    '/api/(.*)','twitterapi.ttapi.api',
)

app = web.application(urls, globals())
application = app.wsgifunc()
if __name__=="__main__":
#    app.run()
    pass

