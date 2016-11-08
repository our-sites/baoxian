#coding:utf-8
__author__ = 'admin'
# --------------------------------
# Created by admin  on 2016/10/18.
# ---------------------------------

from django.conf.urls import  patterns,url
import  views
from django.conf import  settings

class Manage(object):
    def __init__(self,name="manage",app_name="manage"):
        self.name=name
        self.app_name=app_name
    def get_urls(self):
        urlpatterns = patterns('',
                               ("^$",views.home),
                               (r"^user/buy/$",views.user_buy),
                               (r"^user/buy/(\d+)\.html",views.user_buy_detail),
                               (r"user/buy/resetpwd/(\d+)\.html",views.user_buy_resetpwd),
                               (r"^user/proxy/$",views.user_proxy),
                               (r"^user/proxy/(\d+)\.html",views.user_proxy_detail),
                               (r"user/proxy/resetpwd/(\d+)\.html",views.user_proxy_resetpwd),
                               (r"^zixun/add/",views.zixun_add),
                               (r"^zixun/all/",views.zixun_all),
                               (r"logout/",views.logout)
            )
        return urlpatterns
    @property
    def urls(self):
        return self.get_urls(),self.app_name,self.name
site=Manage()