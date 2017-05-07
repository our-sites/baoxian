#coding:utf-8
__author__ = 'zhoukunpeng'
# --------------------------------
# Created by zhoukunpeng  on 2016/7/13.
# ---------------------------------
from django.http import  HttpResponse,HttpResponseRedirect
from django.conf import  settings
import urlparse
import  urllib
assert isinstance(settings.LOGIN_URL,str)

def _url_next(next):
    obj=urlparse.urlparse(settings.LOGIN_URL)
    _t=list(obj)
    if _t[4]=="":
        _t[4]+="next=%s"%urllib.quote(next)
    else:
        _t[4]+="&next=%s"%urllib.quote(next)
    return urlparse.urlunparse(_t)

def login_required(func):
    def fun(request):
        if request.myuser!=None:
            return func(request)
        else:
            return  HttpResponseRedirect(_url_next(next=request.get_full_path()))
    return fun

# def proxyuser_login_required(func):
#     def fun(request):
#         if request.myuser!=None and request.myuser.usertype==2:
#             return func(request)
#         else:
#             return  HttpResponseRedirect(_url_next(next=request.get_full_path())+"&role=proxy")
#     return fun
#
# def buyuser_login_required(func):
#     def fun(request):
#         if request.myuser!=None and request.myuser.usertype==1:
#             return func(request)
#         else:
#             return  HttpResponseRedirect(_url_next(next=request.get_full_path())+"&role=buy")
#     return fun
