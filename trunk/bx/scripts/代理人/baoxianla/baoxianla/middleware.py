#!/usr/bin/python
#-*-coding:utf-8-*-
import base64
import random
from baoxianla.settings import PROXIES
class ProxyMiddleware(object):
    # overwrite process request
    def process_request(self, request, spider):
        # Set the location of the proxy
        thisip = random.choice(PROXIES)
        request.meta['proxy'] = "http://"+thisip["ip_port"]
        # Use the following lines if your proxy requires authentication
        proxy_user_pass = thisip["user_pass"]
        # setup basic authentication for the proxy
        encoded_user_pass = base64.encodestring(proxy_user_pass)
        request.headers['Proxy-Authorization'] = 'Basic ' + encoded_user_pass

    #the default user_agent_list composes chrome,I E,firefox,Mozilla,opera,netscape
    #for more user agent strings,you can find it in http://www.useragentstring.com/pages/useragentstring.php

