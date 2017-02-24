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
                request.myuser_profile=None
            else:
                request.myuser=user
                if request.myuser.usertype==1:
                    try:
                        request.myuser_profile=BuyUserProfile.objects.get(uid=request.myuser.uid)
                    except:
                        _=BuyUserProfile(uid=request.myuser, province=request.province_id, city=request.city_id)
                        _.save()
                        request.myuser_profile=_

                else:
                    try:
                        request.myuser_profile=ProxyUserProfile.objects.get(uid=request.myuser.uid)
                    except:
                        _=ProxyUserProfile(uid=request.myuser,province=request.province_id, city=request.city_id)
                        _.save()
                        request.myuser_profile=_
        else:
            request.myuser=None
            request.myuser_profile=None


    def process_response(self, request, response):
        return  response