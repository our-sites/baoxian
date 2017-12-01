#coding:utf-8
__author__ = 'admin'
# --------------------------------
# Created by admin  on 2016/12/6.
# ---------------------------------
from bx.myauth.models import MyUser

def dailiren(request):
    class Test:
        def get_hot(self):
            if request.city_id:
                return MyUser.objects.filter(is_proxy=1,city_id=request.city_id).order_by("-ans_num")
            else:
                return MyUser.objects.filter(is_proxy=1).order_by("-ans_num")

    return {"dailiren_common":Test()}

