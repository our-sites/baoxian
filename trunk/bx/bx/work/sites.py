#coding:utf-8
__author__ = 'admin'
# --------------------------------
# Created by admin  on 2016/10/18.
# ---------------------------------

from django.conf.urls import  patterns,url
import  views
from django.conf import  settings
from django.http import  HttpResponseRedirect

class Work_Buy(object):
    def __init__(self,name="work",app_name="work"):
        self.name=name
        self.app_name=app_name
    def get_urls(self):
        urlpatterns = patterns('',
      #      ("^%s$"%settings.LOGIN_URL.lstrip("/"),views.login),
      #      ("^%s$"%settings.LOGOUT_URL.lstrip("/"),views.logout),
                               ("^$",views.index),
                               (r"all_msg/$",views.all_msg),
                               (r"myask/",views.my_ask),
                               (r"myans/",views.my_ans),
                               #(r"mydingzhi/",views.my_dingzhi),
                               (r"my/contact/",views.contact),
                               (r"my/img/",views.img),
                               (r"change_pwd",views.change_pwd),
                               (r"startproxy",views.startproxy),
                               (r"proxy/myinfo/",views.proxy_myinfo),
                               (r"proxy/myadd/", views.proxy_myadd),
                               (r"proxy/myshare", views.proxy_myshare),
                               (r"simple_upload",views.simple_upload),
                               (r"phonevalid",views.phonevalid),

            )
        return urlpatterns
    @property
    def urls(self):
        return self.get_urls(),self.app_name,self.name
site=Work_Buy()