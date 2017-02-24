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
                               (r"zixun/detail/(\d+)\.html",views.zixun_detail),
                               (r"product/add/",views.product_add),
                               (r"product/all/",views.product_all),
                               (r"product/detail/(\d+)\.html",views.product_detail),
                               (r"product/detail/delete/(\d+)\.html",views.product_delete),
                               (r"product/detail/delete/do/",views.product_delete_do),
                               (r"company/add/",views.company_add),
                               (r"company/all/",views.company_all),
                               (r"company/detail/(\d+).html",views.company_detail),
                               (r"company/detail/delete/(\d+)\.html",views.company_delete),
                               (r"company/detail/delete/do/",views.company_delete_do),
                               (r"logout/",views.logout),
                               (r"auth_user/",views.auth_user)
            )
        return urlpatterns
    @property
    def urls(self):
        return self.get_urls(),self.app_name,self.name
site=Manage()