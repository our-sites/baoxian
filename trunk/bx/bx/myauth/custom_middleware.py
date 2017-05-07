#coding:utf-8
__author__ = 'zhoukunpeng'
# --------------------------------
# Created by zhoukunpeng  on 2016/7/13.
# ---------------------------------
from cookie_encrypt import  phpcookie_decode,phpcookie_encode
from models import *
import urllib

class self_auth_middleware(object):

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


        print "process_request"


    def process_response(self, request, response):
        print "process_response"
        timestamp=int(time.time())

        if getattr(request,"myuser",None):
            myuser=request.myuser
            if not  request.COOKIES.get("user_info"):
                response.set_cookie("user_info",urllib.quote(
                        phpcookie_encode("\t".join([str(myuser.uid), myuser.username,request.ip,str(timestamp)]),'gc895316')),
                                  expires=86400*365)
            else:
                response.set_cookie("user_info",request.COOKIES.get("user_info"),
                                    expires=86400*365)

            response.set_cookie("user_status","1",expires=86400*365)

        else:

            response.delete_cookie("user_info")
            response.delete_cookie("user_status")
        return  response