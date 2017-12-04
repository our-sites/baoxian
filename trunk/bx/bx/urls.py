#coding:utf-8
from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from django.http import  HttpResponseRedirect,Http404,HttpResponseNotFound
admin.autodiscover()
from django.conf import  settings
import  myauth
import  api
import  ask
import  dingzhi
import  zixun
import  views
import  manage
import  product
import  dailiren
import work
import  company
import  app
import  weixin_dingyuehao
import news
import study

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
       (r"^favicon.ico$",lambda x:HttpResponseRedirect('/static/favicon.ico')),
    url(r'^admin/', include(admin.site.urls)),
       (r"^manage/",include(manage.site.urls)),
    url(r"api/",include(api.site.urls)),
       (r"^$",views.home),
        (r"^about",views.about),
                       (r"testpost",views.testpost),



       (r"^ask/",include(ask.site.urls)),
       (r"^dingzhi/",include(dingzhi.site.urls)),
       (r"^zixun/",include(zixun.site.urls)),
       (r"^product/",include(product.site.urls)),
       (r"^dailiren/",include(dailiren.site.urls)),
       (r"^work/",include(work.site.urls)),
       (r"^ckeditor/upload/$","bx.manage.views.ck_upload"),  #ck upload
       (r'^ckeditor/', include('ckeditor_uploader.urls')),
       (r"^company/",include(company.site.urls)),
       (r"^app/",include(app.site.urls)),
       ("^news/",include(news.site.urls)),
        ("^study/",include(study.site.urls)),
       (r"^weixin_dingyuehao/",include(weixin_dingyuehao.site.urls)),



        # sitemap
        ("^sitemap.index$",views.sitemap_index),
        ("^sitemap.xml$",views.sitemap_index),
        ("^sitemap.index.xml$",views.sitemap_index),
        ("^zixun_sitemap(\d+).xml$",views.zixun_sitemap_xml),
        ("^product_sitemap(\d+).xml$",views.product_sitemap_xml),
        ("^ask_sitemap(\d+).xml$",views.ask_sitemap_xml),
        ("^news_sitemap(\d+).xml$",views.news_sitemap_xml),
                       ("top_roll_message_api",views.top_roll_message_api),
                       ("^hot_dailiren_api",views.hot_dailiren_api),
                       ("^",lambda request:\
                           HttpResponseRedirect((request.path+"/") ) if not  request.path.endswith("/") else HttpResponseNotFound()),
)
