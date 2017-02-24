#coding:utf-8
__author__ = 'admin'
# --------------------------------
# Created by admin  on 2016/10/18.
# ---------------------------------

from django.conf.urls import  patterns,url
import  views
from django.conf import  settings


class App(object):
    def __init__(self,name="app",app_name="app"):
        self.name=name
        self.app_name=app_name

    def get_urls(self):
        urlpatterns = patterns('',
      #      ("^%s$"%settings.LOGIN_URL.lstrip("/"),views.login),
      #      ("^%s$"%settings.LOGOUT_URL.lstrip("/"),views.logout),
      #                          ("^detail/(\d+)\.html",views.detail),
      #                           ("^search/",views.search),
      #                          ("^$",views.index),
            )
        return urlpatterns
    @property
    def urls(self):
        return self.get_urls(),self.app_name,self.name

site=App()