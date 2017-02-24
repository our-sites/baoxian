#coding:utf-8
__author__ = 'admin'
# --------------------------------
# Created by admin  on 2016/10/18.
# ---------------------------------

from django.conf.urls import  patterns,url
import  views
from django.conf import  settings


class Company(object):
    def __init__(self,name="company",app_name="company"):
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

site=Company()