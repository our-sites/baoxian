#!/usr/bin/python
#-*-coding:utf-8-*-
import base64
import random
"""避免被ban策略之一：使用proxy池。
使用注意：需在settings.py中进行相应的设置。
DOWNLOADER_MIDDLEWARES = {
     'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware' : None,
     'm58com.rotate_useragent.RotateUserAgentMiddleware' :400,
     'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware':None,
     'm58com.middleware.ProxyMiddleware':410
 }
"""
class ProxyMiddleware(object):
    # overwrite process request
    def process_request(self, request, spider):
        # Set the location of the proxy
        thisproxy = random.choice(self.proxy_list)
        request.meta['proxy'] = "http://"+thisproxy["ip_port"]
        # Use the following lines if your proxy requires authentication
        proxy_user_pass = thisproxy["user_pass"]
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
