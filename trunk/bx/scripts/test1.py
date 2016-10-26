#coding:utf-8
__author__ = 'admin'
# --------------------------------
# Created by admin  on 2016/10/14.
# ---------------------------------
import  urllib2

# def urllib2_get_httpproxy(ip,port):
#     proxy=urllib2.ProxyHandler({'http': 'http://%s:%s'%(ip,port)})
#     opener=urllib2.build_opener(proxy)
#     return  opener
#     #urllib2.install_opener(opener)
#
# def urllib2_get_httpsproxy(ip,port):
#     proxy=urllib2.ProxyHandler({'https': 'https://%s:%s'%(ip,port)})
#     opener=urllib2.build_opener(proxy)
#     return  opener
#
# urllib2.install_opener(urllib2_get_httpsproxy("192.168.8.33",888))
# print urllib2.urlopen("http://www.baidu.com/").read()