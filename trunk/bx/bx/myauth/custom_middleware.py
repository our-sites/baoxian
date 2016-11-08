#coding:utf-8
__author__ = 'zhoukunpeng'
# --------------------------------
# Created by zhoukunpeng  on 2016/7/13.
# ---------------------------------
from cookie_encrypt import  phpcookie_decode
from models import *

class SelfAuthMiddleware(object):
    def process_request(self, request):
        login_cookie=request.COOKIES.get("user_info","")
        request.ip=request.META.get("HTTP_X_REAL_IP","0.0.0.0")
        if login_cookie:
            suplier_login_cookie=phpcookie_decode(login_cookie,'gc895316')
            try:
                uid,username,ip,timestamp=suplier_login_cookie.split("\t")
                user=MyUser.objects.get(uid=int(uid),state=1)
            except Exception as e :
                print "Exception",e.message
                request.myuser=None
            else:
                request.myuser=user
        else:
            request.myuser=None


    def process_response(self, request, response):
        return  response