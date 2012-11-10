import web,twitUtil
from config import settings
from ..bitly import bitly

class api:
    #def foo()
    #    referer = web.ctx.env.get('User-Agent', 'ios')
    def sub_url(self,str1):
        import json
        def warpper(obj):
            if obj.has_key('text') and\
                obj.has_key('entities') and\
                obj['entities'].has_key('urls') and\
                len(obj['entities']['urls']) > 0:
                text = obj['text']
                added_len = 0
                for j,url in enumerate(obj['entities']['urls']):
                    if url and url['expanded_url']:
                        pos1 = url['indices'][0]
                        pos2 = url['indices'][1]
                        url['url'] = url['expanded_url']
                        print(url['url'])
                        if settings.no_jmp and\
                            url['url'].startswith('http://j.mp'):
                            try:
                                a = bitly.Api(settings.bitly_name,settings.bitly_key)
                                url['url'] = a.expand(url['url'])
                                url['expanded_url'] = url['url'] 
                            except:
                                pass
                        if url['url'].startswith('http://twitpic.com'):
                            #url['url'] = url['url'].replace('http', 'https', 1)
                            url['url'] = 'https://501fun.dabin.info/proxy?nojs=1&url=' +\
                                url['url']
                            url['expanded_url'] = url['url'] 
                        text = text[:pos1 + added_len] + url['url'] + text[pos2 + added_len:]
                        indices1 = [pos1 + added_len,pos1 + len(url['url']) + added_len]
                        url['indices'] = indices1
                        obj['entities']['urls'][j] = url
                        tmp_add_len = len(url['url']) - pos2 + pos1
                        added_len += tmp_add_len 
                        def increase(key): 
                            for j,each in enumerate(obj['entities'][key]):
                                if each['indices'][0] > pos1:
                                    each['indices'][0] += tmp_add_len
                                    each['indices'][1] += tmp_add_len
                                    obj['entities'][key][j] = each
                        #user mention
                        if obj['entities'].has_key('user_mentions'):
                            increase('user_mentions')
                        #media
                        if obj['entities'].has_key('media'):
                            increase('media')
                        #hashtags
                        if obj['entities'].has_key('hashtags'):
                            increase('hashtags')
                        #print "rt url['expanded_url'] is",url['expanded_url']
                obj['text'] = text
                return True
            return False
        rv = str1
        changed = 0
        try:
            o = json.loads(str1)
            if isinstance(o,list):
                for i,each in enumerate(o):
                    if warpper(each):
                        changed = 1
                        o[i] = each
                    if each.has_key('retweeted_status'):
                        rt_st = each['retweeted_status']
                        if warpper(rt_st):
                            changed = 1
                            each['retweeted_status'] = rt_st
                            o[i] = each
                if changed == 1:
                    rv = json.dumps(o)
                #print json.dumps(o,indent=4)
        except Exception,e:
            print '---------------------- e is',str(e)
            pass
        finally:
            pass
        return rv
        
    def apicall(self,type1):
        import json
        web.header('Content-Type','text/html; charset=utf-8', unique=True)

        access_token = {}
            
        f1 = open(settings.get_home_dir() + 'token.txt','r')
        str1 = f1.read()
        f1.close()
        l1 = str1.split(';')
        if '1' == l1[2].replace(r'ss=',''):
            access_token['oauth_token'] = l1[0].replace(r'ot=','')
            access_token['oauth_token_secret'] = l1[1].replace(r'ots=','')
            
        if web.url().startswith('/api/'):
            url1 = web.url().replace(r'/api/','',1)
        i1 = web.input().copy()

        #if url1.endswith('.json'):
        #    if i1.has_key('include_entities') is False:
        #        i1['include_entities'] = u'true'

        #for new twitter ,home_timeline
        #home timeline
        pop_earned = not -1 == url1.find('statuses/home_timeline') or\
            not -1 == url1.find('statuses/user_timeline') or\
            not -1 == url1.find('statuses/show')
        if pop_earned:
            if i1.has_key('earned'):
                i1.pop('earned')

        rv = twitUtil.MakeApiCall(access_token,url1,type1,dict(i1))
        #ndswith('/activity/summary.json'):
        if url1.endswith('.json'):
            #tmp_o = json.loads(rv)
            #print json.dumps(tmp_o,indent=4)
            rv = self.sub_url(rv)
        #print rv
        return rv
        
    def GET(self,para):
        return self.apicall('GET')

    def POST(self,para):
        return self.apicall('POST')

