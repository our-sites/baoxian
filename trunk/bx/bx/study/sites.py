#coding:utf-8
# write  by  zhou

from django.conf.urls import  patterns
import  views

class Study(object):
    def __init__(self,name="study",app_name="study"):
        self.name=name
        self.app_name=app_name

    def get_urls(self):
        urlpatterns = patterns('',

                (r"^add_youkuvideo",views.add_youkuvideo),
            )
        return urlpatterns
    @property
    def urls(self):
        return self.get_urls(),self.app_name,self.name

site=Study()