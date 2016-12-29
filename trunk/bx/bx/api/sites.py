#coding:utf-8
__author__ = 'admin'
# --------------------------------
# Created by admin  on 2016/10/10.
# ---------------------------------

from django.conf.urls import  patterns,url
import  views
from django.conf import  settings
class Api(object):
    def __init__(self,name="api",app_name="api"):
        self.name=name
        self.app_name=app_name
    def get_urls(self):
        urlpatterns = patterns('',
            ("^upload_img$",views.upload_img),
                               ("^area_list",views.area_list),
                               ("^send_sms_validnumer",views.send_sms_validnumer),
                               ("^valid_sms_validnumer",views.valid_sms_validnumer),
            )
        return urlpatterns
    @property
    def urls(self):
        return self.get_urls(),self.app_name,self.name
site=Api()