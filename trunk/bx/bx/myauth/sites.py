#coding:utf-8
__author__ = 'zhoukunpeng'
# --------------------------------
# Created by zhoukunpeng  on 2016/7/13.
# ---------------------------------
from django.conf.urls import  patterns,url
import  views
from django.conf import  settings
class SelfAuth(object):
    def __init__(self,name="myauth",app_name="myauth"):
        self.name=name
        self.app_name=app_name
    def get_urls(self):
        urlpatterns = patterns('',
            ("^%s$"%settings.LOGIN_URL.lstrip("/"),views.login),
            ("^%s$"%settings.LOGOUT_URL.lstrip("/"),views.logout),
                               (r"^register/parentid/(\d+)",views.register),
                               (r"^register/",views.register),
                               (r"^register_valid_phone",views.register_valid_phonenum),
                               (r"^register_send_sms/",views.register_send_sms),
                               (r"^forgotpwd/",views.forgotpwd),
                               (r"^forgotpwd_valid_phone",views.forgotpwd_valid_phone),
                               (r"get_qq_token",views.get_qq_token),
                               (r"get_taobao_token",views.get_taobao_token),
                              (r"get_weibo_token", views.get_weibo_token),
                               (r"m_register_valid_phone",views.m_register_valid_phone),
                               (r"m_forgotpwd_valid_phone",views.m_forgotpwd_valid_phone),
            )
        return urlpatterns
    @property
    def urls(self):
        return self.get_urls(),self.app_name,self.name
site=SelfAuth()