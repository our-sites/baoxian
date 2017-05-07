#coding:utf-8
__author__ = 'admin'
# --------------------------------
# Created by admin  on 2016/10/18.
# ---------------------------------

from django.conf.urls import  patterns,url
import  views
from django.conf import  settings
class ZiXun(object):
    def __init__(self,name="zixun",app_name="zixun"):
        self.name=name
        self.app_name=app_name
    def get_urls(self):
        urlpatterns = patterns('',
      #      ("^%s$"%settings.LOGIN_URL.lstrip("/"),views.login),
      #      ("^%s$"%settings.LOGOUT_URL.lstrip("/"),views.logout),
                               ("^$",views.index),
                               (r"^add_xinwen",views.add_xinwen),
                               ("^detail/(\d+)\.html",views.detail),
                               (r"(baike)/",views.index_index),
                               (r"(anli)/",views.index_index),
                               (r"(dongtai)/",views.index_index),
                               (r"(guahua)/",views.index_index),
                               (r"(citiao)/",views.index_index),
                               (r"(xinwen)/",views.index_index),

            )
        return urlpatterns
    @property
    def urls(self):
        return self.get_urls(),self.app_name,self.name
site=ZiXun()