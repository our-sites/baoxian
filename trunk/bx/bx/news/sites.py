#coding:utf-8
# write  by  zhou

from django.conf.urls import  patterns,url
import  views
from django.conf import  settings
class News(object):
    def __init__(self,name="news",app_name="news"):
        self.name=name
        self.app_name=app_name
    def get_urls(self):
        urlpatterns = patterns('',
      #      ("^%s$"%settings.LOGIN_URL.lstrip("/"),views.login),
      #      ("^%s$"%settings.LOGOUT_URL.lstrip("/"),views.logout),

                               # (r"^\d+\.html$",views.index),

                               (r"^add_news",views.add_news),
                               (r"^cate1_list",views.cate1_list),
                               (r"^cate2_list",views.cate2_list),
                               (r"^get_cate_id",views.get_cate_id),
                               (r"^detail/(\d+)\.html",views.detail),
                               (r"^tag/(?P<tag>.+)",views.index),
                               (r"^(?P<cateid>\d+)$",views.index),
                               (r"^(?P<cateid>\d+)/$",views.index),
                                (r"^",views.index),

            )
        return urlpatterns
    @property
    def urls(self):
        return self.get_urls(),self.app_name,self.name
site=News()