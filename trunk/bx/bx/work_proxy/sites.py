#coding:utf-8
__author__ = 'admin'
# --------------------------------
# Created by admin  on 2016/10/18.
# ---------------------------------

from django.conf.urls import  patterns,url
import  views
from django.conf import  settings
from django.http import  HttpResponseRedirect

class Work_Proxy(object):
    def __init__(self,name="work_proxy",app_name="work_proxy"):
        self.name=name
        self.app_name=app_name
    def get_urls(self):
        urlpatterns = patterns('',


            )
        return urlpatterns
    @property
    def urls(self):
        return self.get_urls(),self.app_name,self.name
site=Work_Proxy()