##501fun twitter api

###python webpy
this a twitter api written in webpy
python version >= 2.6

###how to use
1. change key and secect in config/settings.py(you can get them from <https://dev.twitter.com>)
2. change callback url on <https://dev.twitter.com>: https://host_url
3. https://host_url/api is your api url(maybe https://host_url/api/)

###deploy uwsgi + nginx
> If you deploy it on dotcloud,please use https(example https://appurl.dotcloud.com) for security reason. 

###supported apps

+ twitbird <http://itunes.apple.com/us/app/twitbird-free-for-twitter/id352891124?mt=8>
+ twitter ios offical client <http://itunes.apple.com/us/app/twitter/id333903271?mt=8>
+ favawe <https://chrome.google.com/webstore/detail/aicelmgbddfgmpieedjiggifabdpcnln>


###recent changes
+ replace t.co link to origian link in tweet streams
+ support twitter ios offcial client auth

###todo
+ <del>replace t.co url with expanded url in retweet</del>
+ <del>replace j.mp url with original url</del>
+ fix http 403 error on twitter iphone

