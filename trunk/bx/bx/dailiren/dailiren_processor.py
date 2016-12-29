#coding:utf-8
__author__ = 'admin'
# --------------------------------
# Created by admin  on 2016/12/6.
# ---------------------------------
from bx.myauth.models import MyUser,ProxyUserProfile

def dailiren(request):
    class Test:
        def get_hot(self):
            return ProxyUserProfile.objects.all().order_by("-ans_num")

    return {"dailiren_common":Test()}

