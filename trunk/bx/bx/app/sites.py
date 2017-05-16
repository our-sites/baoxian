#coding:utf-8
__author__ = 'admin'
# --------------------------------
# Created by admin  on 2016/10/18.
# ---------------------------------
from django.conf.urls import  patterns,url
import views
import company
import product
import info
import ask
import users
#import custom
from django.conf import  settings

class App(object):
    def __init__(self,name="app",app_name="app"):
        self.name=name
        self.app_name=app_name

    def get_urls(self):
        urlpatterns = patterns('',
            #孙银
            ("^%s$" % settings.LOGIN_URL.lstrip("/"), views.login),
            ("^%s$" % settings.LOGOUT_URL.lstrip("/"), views.logout),
            (r"^register/", views.register),
            (r"^register_valid_phone/", views.register_valid_phone),
            (r"^register_send_sms/", views.register_send_sms),
            (r"^forgotpwd/", views.forgotpwd),
            (r"^forgotpwd_valid_phone", views.forgotpwd_valid_phone),
            (r"^users/msg/", users.msg),
            (r"^company/list/",  company.list),
            (r"^product/lunbo/",  product.lunbo),
            (r"^product/list/",  product.list),
            #(r"^add/", custom.add),
            #(r"^company/", company.add),
            #("^$", lambda x: HttpResponseRedirect("/product/search/")),
            #("^search/redirect/$", product.search_redirect),
            #("^detail/", product.detail),
            #("^search/", product.search),
            #周绍功
            (r"^info/lunbo/", info.lunbo),
            (r"^info/yuanchuang/", info.yuanchuang),
            (r"^info/duanzi/", info.duanzi),
            (r"^info/shequ/", info.shequ),
            (r"^info/pinglun/", info.pinglun),
            (r"^ask/huifu/", ask.huifu),
            )
        return urlpatterns
    @property
    def urls(self):
        return self.get_urls(),self.app_name,self.name

site=App()