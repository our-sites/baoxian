#!/usr/bin/python
#-*-coding:utf-8-*-
import base64
import random
from scrapy.contrib.downloadermiddleware.useragent import UserAgentMiddleware

"""避免被ban策略之一：使用proxy池。
使用注意：需在settings.py中进行相应的设置。
DOWNLOADER_MIDDLEWARES = {
    'scrapy.contrib.downloadermiddleware.useragent.UserAgentMiddleware' : None,
    'ganjiwang.middleware.RotateUserAgentMiddleware' :400,
    'scrapy.contrib.downloadermiddleware.httpproxy.HttpProxyMiddleware':543,
    #'ganjiwang.middleware.ProxyMiddleware':125
 }
"""
class ProxyMiddleware(object):
    # overwrite process request
    def process_request(self, request, spider):
        # Set the location of the proxy
        thisip = random.choice(self.proxy_list)
        request.meta['proxy'] = "http://"+thisip["ip_port"]
        # Use the following lines if your proxy requires authentication
        proxy_user_pass = thisip["user_pass"]
        # setup basic authentication for the proxy
        encoded_user_pass = base64.encodestring(proxy_user_pass)
        request.headers['Proxy-Authorization'] = 'Basic ' + encoded_user_pass

    #the default user_agent_list composes chrome,I E,firefox,Mozilla,opera,netscape
    #for more user agent strings,you can find it in http://www.useragentstring.com/pages/useragentstring.php
    proxy_list = [
        {'ip_port': '172.16.13.50:1228', 'user_pass': 'xidi:xidi2016'},
        {'ip_port': '172.16.13.51:1228', 'user_pass': 'xidi:xidi2016'},
        {'ip_port': '172.16.13.52:1228', 'user_pass': 'xidi:xidi2016'},
        {'ip_port': '172.16.13.53:1228', 'user_pass': 'xidi:xidi2016'},
        {'ip_port': '172.16.13.54:1228', 'user_pass': 'xidi:xidi2016'},
        {'ip_port': '172.16.13.55:1228', 'user_pass': 'xidi:xidi2016'},
        {'ip_port': '172.16.13.56:1228', 'user_pass': 'xidi:xidi2016'},
        {'ip_port': '172.16.13.57:1228', 'user_pass': 'xidi:xidi2016'},
        {'ip_port': '172.16.13.58:1228', 'user_pass': 'xidi:xidi2016'},
        {'ip_port': '172.16.13.59:1228', 'user_pass': 'xidi:xidi2016'}
    ]


"""避免被ban策略之一：使用useragent池。
使用注意：需在settings.py中进行相应的设置。
DOWNLOADER_MIDDLEWARES = {
    'scrapy.contrib.downloadermiddleware.useragent.UserAgentMiddleware' : None,
    'ganjiwang.middleware.RotateUserAgentMiddleware' :400,
    'scrapy.contrib.downloadermiddleware.httpproxy.HttpProxyMiddleware':543,
    #'ganjiwang.middleware.ProxyMiddleware':125
 }
"""
class RotateUserAgentMiddleware(UserAgentMiddleware):

    def __init__(self, user_agent=''):
        self.user_agent = user_agent

    def process_request(self, request, spider):
        #ua = random.choice(user_agent_list)
        ua = random.choice(self.user_agent_list)
        if ua:
            #显示当前使用的useragent
            #print "~~~Current UserAgent:%s~~~"%ua
            request.headers.setdefault('User-Agent', ua)

    #the default user_agent_list composes chrome,I E,firefox,Mozilla,opera,netscape
    #for more user agent strings,you can find it in http://www.useragentstring.com/pages/useragentstring.php
    user_agent_list = [
        #"Mozilla/5.0 (compatible; Baiduspider/2.0; +http://www.baidu.com/search/spider.html)",
        #"Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0); 360Spider",
        #"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36; 360Spider",
        #"Sogou web spider/4.0(+http://www.sogou.com/docs/help/webmasters.htm#07)",
        #"YisouSpider",
        "Mozilla/5.0 (Linux; Android 7.0; PRA-TL10 Build/HONORPRA-TL10) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.94 Mobile Safari/537.36",
        "Mozilla/5.0 (Linux; Android 6.0.1; Redmi Note 4X Build/MMB29M; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.49 Mobile MQQBrowser/6.2 TBS/043305 Safari/537.36 MicroMessenger/6.5.8.1060 NetType/4G Language/zh_CN",
        "Mozilla/5.0 (Linux; Android 5.1.1; 2014813 Build/LMY47V; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/51.0.2704.81 Mobile Safari/537.36",
        "Mozilla/5.0 (Linux; Android 4.4.4; CHM-CL00 Build/CHM-CL00) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/33.0.0.0 Mobile Safari/537.36",
        "Mozilla/5.0 (Linux; Android 4.4.2; SM-G7106 Build/KOT49H) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/30.0.0.0 Mobile Safari/537.36",
        "Mozilla/5.0 (Linux; U; Android 4.3; zh-cn; HUAWEI B199 Build/HuaweiB199) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30; 360browser(securitypay,securityinstalled); 360 Aphone Browser (Version 3.1.0ctch1)",
        "Mozilla/5.0 (Linux;u;Android 4.2.2;zh-cn;) AppleWebKit/534.46 (KHTML,like Gecko) Version/5.1 Mobile Safari/10600.6.3 (compatible; Baiduspider/2.0; +http://www.baidu.com/search/spider.html)",
        "Mozilla/5.0 (Linux; Android 4.0.4; Galaxy Nexus Build/IMM76B) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.133 Mobile Safari/535.19",
        "Mozilla/5.0 (Linux; U; Android 4.0.2; en-us; Galaxy Nexus Build/ICL53F) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30",
        "Mozilla/5.0 (Linux; U; Android 2.3.6; en-us; Nexus S Build/GRK39F) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
        "Mozilla/5.0 (Android; Mobile; rv:14.0) Gecko/14.0 Firefox/14.0",
        "Mozilla/5.0 (iPhone; CPU iPhone OS 10_2_1 like Mac OS X) AppleWebKit/602.4.6 (KHTML, like Gecko) Mobile/14D27 MicroMessenger/6.5.5 NetType/WIFI Language/zh_CN",
        "Mozilla/5.0 (iPhone; CPU iPhone OS 9_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13B143 Safari/601.1",
        "Mozilla/5.0 (iPhone; CPU iPhone OS 9_0 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Mobile/13A342 QHBrowser/274 QihooBrowser/4.0.4",
        "Mozilla/5.0 (iPhone; CPU iPhone OS 8_4 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 Mobile/12H143 Safari/600.1.4",
        "Mozilla/5.0 (iPhone; CPU iPhone OS 7_0 like Mac OS X; en-us) AppleWebKit/537.51.1 (KHTML, like Gecko) Version/7.0 Mobile/11A465 Safari/9537.53",
        "Mozilla/5.0 (iPhone; CPU iPhone OS 6_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/6.0 Mobile/10A5376e Safari/8536.25",
        "Mozilla/5.0 (iPhone; CPU iPhone OS 5_0 like Mac OS X) AppleWebKit/534.46 (KHTML, like Gecko) Version/5.1 Mobile/9A334 Safari/7534.48.3",
        "Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_3_2 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8H7 Safari/6533.18.5",
        "Mozilla/5.0 (iPad; CPU OS 5_0 like Mac OS X) AppleWebKit/534.46 (KHTML, like Gecko) Version/5.1 Mobile/9A334 Safari/7534.48.3",
        "Mozilla/5.0 (iPad; CPU OS 4_3_2 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8H7 Safari/6533.18.5"
    ]

