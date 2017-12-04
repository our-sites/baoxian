#:coding:utf-8
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
from bx.utils.sms import send_dayysms_validnumber,send_dayysms_regsuccess

@app_api()
def register_sendsms(request):
    '''
    功能说明:
    用户注册-发送验证码

    参数说明:
    phone  手机号

    返回数据说明:
    发送失败:
    {"errorCode":0,"formError":{"phone":"手机号不合法!"},"data":null,"message":"手机号不合法!"}
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
        MyUser.objects.get(phone=phone)
        raise FieldError("phone",u"该手机号已被注册!")
    except:
        pass
    numer="".join(random.sample(["1","2","3","4","5","6","7","8","9"],6))
    send_dayysms_validnumber(phone,numer)
    request.appsession["app_validnumber"]=numer
    return True

@app_api()
def register_validsms(request):
    '''
    功能说明:
    用户注册-验证验证码是否正确

    参数说明:
    numer  验证码

    返回数据说明:
    验证成功:
    {"errorCode":0,"formError":{},"data":true,"message":""}
    验证失败
    {"errorCode":0,"formError":{},"data":false,"message":""}
    '''
    post_info=request.POST
    print request.appsession.items()
    numer=post_info.get("numer","")
    if numer==request.appsession.get("app_validnumber"):
        return True
    else:
        return False




@app_api()
def register(request):
    '''
    功能说明:
    用户注册-提交注册,如果注册成功,服务端自动将此客户端置为登录状态,客户端无需再次调用登录逻辑.(注册成功后会自动发送注册成功短信提示)

    参数说明:
    phone 手机号
    numer 验证码
    password 密码
    invitenumer 邀请码,非必填项,主要为了配合进行用户邀请注册机制

    返回数据说明:
    注册成功:
    {"errorCode":0,"formError":{},"data":true,"message":""}
    注册失败:
    a.
    {"errorCode":0,"formError":{"phone":"手机号不合法!"},"data":null,"message":"手机号不合法!"}
    b.
    {"errorCode":0,"formError":{"numer":"验证码不正确"},"data":null,"message":"验证码不正确"}
    c.
    {"errorCode":0,"formError":{"password":"密码长度不能小于6位"},"data":null,"message":"密码长度不能小于6位"}
    ...

    '''
    post_info=request.POST
    print request.body
    print request.appsession.items()
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
        MyUser.objects.get(phone=phone)
    except:
        pass
    else:
       raise FieldError("phone",u"该手机号已被注册!")
    assert numer,FieldError("numer",u"请输入验证码")
    assert password,FieldError("password",u"请输入您的密码")
    if numer!=request.appsession.get("app_validnumber",""):
        raise FieldError("numer",u"验证码不正确")
    if len(password)<6:
        raise FieldError("password",u"密码长度不能小于6位")
    try:
        del request.appsession["app_validnumber"]
    except:
        pass
    salt=MyUser.make_salt()
    password=MyUser.hashed_password(salt,password)
    user=MyUser(username=str(phone),phone=phone,salt=salt,
                            password=password,state=1,is_proxy=1,ip=request.ip,
                            province_id=request.province_id,city_id=request.city_id,
                vphone=1)
    user.save()
    #send_dayysms_regsuccess(phone)#发送注册成功短信
    user.send_success_reged_sms()
    user.app_login(request)
    return True

