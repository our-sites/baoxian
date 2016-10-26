#coding:utf-8
from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from django.http import  HttpResponseRedirect
admin.autodiscover()
from django.conf import  settings
import  myauth
import  api
import  ask
import  dingzhi
import  zixun
urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'bx.views.home', name='home'),
    # url(r'^bx/', include('bx.foo.urls')),
    url(r'^static/(?P<path>.*)$', 'django.views.static.serve',
      { 'document_root': settings.STATICFILES_DIRS[0]}),
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve',
      { 'document_root': settings.MEDIA_ROOT}),
    url(r"", include(myauth.site.urls)),  # 登录认证
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
                       (r"admin/bx/consult/\d+/themes/default/css/ueditor.css",lambda x:HttpResponseRedirect("/static/editor/themes/default/css/ueditor.css")),

    url(r'^admin/', include(admin.site.urls)),
    url(r"api/",include(api.site.urls)),
                       (r"ask/",include(ask.site.urls)),
                       (r"dingzhi/",include(dingzhi.site.urls)),
                       (r"zixun/",include(zixun.site.urls)),
                       (r'^ckeditor/', include('ckeditor_uploader.urls')),
)