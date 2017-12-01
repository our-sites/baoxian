#coding:utf-8
__author__ = 'admin'
# --------------------------------
# Created by admin  on 2016/10/18.
# ---------------------------------
from django.conf.urls import  patterns,url
from  views import  *
import  sys


class App(object):
    def __init__(self,name="app",app_name="app"):
        self.name=name
        self.app_name=app_name

    def get_urls(self):
        urlpatterns = patterns('',

                               (r"^get_session_key$",get_session_key),
                               (r"^meta_test",meta_test),
                               (r"^api_gateway",api_gateway),
                               (r"^api_document",api_document),

            )
        # if getattr(sys,"bxappapi_config",None):
        #     print sys.bxappapi_config.items()
        #     urlpatterns+=patterns("",*sys.bxappapi_config.items())
        return urlpatterns
    @property
    def urls(self):
        return self.get_urls(),self.app_name,self.name

site=App()