#coding:utf-8
from gcutils.encrypt import md5
from django.http import HttpResponseRedirect
import urllib
import time
import datetime
import random
from ...models import Area
from django.views.decorators.csrf import csrf_exempt
from ...myauth.models import MyUser
JsonResponse=lambda x:HttpResponse(json.dumps(x),mimetype="application/javascript")
from bx.utils.aes import *
from bx.decorators import *
from bx.utils.sms import *


@app_api()
def findpwd_sendsms(request):
    '''
    功能说明:
    找回密码-发送验证码

    参数说明:
    phone  手机号

    返回数据说明:
    发送失败:
    {"errorCode":0,"formError":{"phone":"该手机号尚未被注册!"},"data":null,"message":"该手机号尚未被注册!"}

    发送成功:
    {"errorCode":0,"formError":{},"data":true,"message":""}
    '''
    post_info=request.POST
    phone=post_info.get("phone","")
    assert phone,FieldError("phone",u"请输入手机号!")
    try:
        phone=int(phone)
        assert len(str(phone))==11
    except:
        raise FieldError("phone",u"手机号不合法!")
    try:
        user=MyUser.objects.get(phone=phone)
    except:
        raise FieldError("phone",u"该手机号尚未被注册!")
    assert user.is_proxy==1,FieldError("phone",u"该账户类型不是保险代理人!")
    numer="".join(random.sample(["1","2","3","4","5","6","7","8","9"],6))
    send_dayysms_validnumber(phone,numer)
    request.appsession["app_validnumber"]=numer
    return True

@app_api()
def findpwd_validsms(request):
    '''
    功能说明:
    找回密码-验证验证码是否正确

    参数说明:
    numer  验证码

    返回数据说明:
    验证成功:
    {"errorCode":0,"formError":{},"data":true,"message":""}
    验证失败
    {"errorCode":0,"formError":{},"data":false,"message":""}
    '''
    post_info=request.POST
    numer=post_info.get("numer","")
    print request.appsession.items()
    if numer==request.appsession.get("app_validnumber"):
        return True
    else:
        return False


@app_api()
def findpwd_resetpwd(request):
    '''
    功能说明:
    找回密码-重置密码, 注意: 密码重置后,该终端应该重新进入登录逻辑, 服务器端不会自动把此用户在此终端置为登录状态!!

    参数说明:
    phone    手机号
    numer    验证码
    password 新密码

    返回数据说明:
    重置成功:
    {"errorCode":0,"formError":{},"data":true,"message":""}
    重置失败:
    a.
    {"errorCode":0,"formError":{"phone":"手机号不合法!"},"data":null,"message":"手机号不合法!"}
    b.
    {"errorCode":0,"formError":{"numer":"验证码不正确"},"data":null,"message":"验证码不正确"}
    c.
    {"errorCode":0,"formError":{"password":"密码长度不能小于6位"},"data":null,"message":"密码长度不能小于6位"}
    ...

    '''
    post_info=request.POST
    phone=post_info.get("phone","")
    numer=post_info.get("numer","")
    password=post_info.get("password","")
    assert phone,FieldError("phone",u"请输入手机号!")
    try:
        phone=int(phone)
        assert len(str(phone))==11
    except:
        raise FieldError("phone",u"手机号不合法!")
    try:
        user=MyUser.objects.get(phone=phone)
    except:
        raise FieldError("phone",u"该手机号尚未被注册!")
    assert user.is_proxy==1,FieldError("phone",u"该账户类型不是保险代理人!")
    if numer==request.appsession.get("app_validnumber"):
        pass
    else:
        raise FieldError("numer",u"验证码不正确!")
    if len(password)<6:
        raise FieldError("password",u"密码长度不能小于6位")
    try:
        del request.appsession["app_validnumber"]
    except:
        pass
    user.reset_password(password)
    return True

