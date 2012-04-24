import web,twitUtil
from config import settings

class auth:
    def POST(self):
        import os.path
        import os
        web.header('Content-Type','text/html; charset=utf-8', unique=True)
        str1 = ''
        try:
            credentials,str1 = twitUtil.get_auth_url()

            ot = credentials['oauth_token']
            ots = credentials['oauth_token_secret']
            ss = '0'
            str2 = 'ot=' + ot + ';' + 'ots=' + ots + ';' + 'ss=' + ss
            folder1 = './'
            try:
                folder1 = os.environ['WEBPY_HOME']
            except:
                pass
            f2 = open(folder1 + settings.get_home_dir() + 'token.txt','w')
            f2.write(str2)
            f2.close()
        except Exception,e:
            str1 = str1 + ' ' + str(e)           
            return '<div>' + str1 + '</div>'
        return '<a  href="' + str1 + '">' + str1 + '</a>'
        

