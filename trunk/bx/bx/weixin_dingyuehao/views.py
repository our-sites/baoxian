#coding:utf-8


from django.http import  HttpResponse,HttpResponseRedirect
from ..utils.weixin import *

def weixin_test_token(request):
    getinfo=request.GET
    sign=getinfo.get("signature","")
    timestamp=getinfo.get("timestamp","")
    random_num=getinfo.get("nonce","")
    random_str=getinfo.get("echostr","")
    result=weixin_check_signature("zhou",sign,timestamp,random_num)
    if result:
        return HttpResponse(random_str)
    else:
        return HttpResponse("error!")






