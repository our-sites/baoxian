#coding:utf-8
__author__ = 'admin'
# --------------------------------
# Created by admin  on 2016/10/18.
# ---------------------------------

from django.conf.urls import  patterns,url
import  views
from django.conf import  settings
from django.http import  HttpResponseRedirect,HttpResponse
class WeixinDingyuehao(object):
    def __init__(self,name="weixin_dingyuehao",app_name="weixin_dingyuehao"):
        self.name=name
        self.app_name=app_name
    def get_urls(self):
        urlpatterns = patterns('',

                               ("^$",lambda x:HttpResponse("hello")),
                               ("^test_token/",views.weixin_test_token),  # test_token

            )
        return urlpatterns
    @property
    def urls(self):
        return self.get_urls(),self.app_name,self.name
site=WeixinDingyuehao()