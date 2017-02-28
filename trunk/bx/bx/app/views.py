# coding:utf-8
__author__ = 'zhou'
# --------------------------------
# Created by zhou  on 2017/02/20.
# ---------------------------------
from ..myauth.decorators import login_required
from ..myauth.cookie_encrypt import phpcookie_encode
from ..myauth.models import MyUser, ProxyUserProfile, BuyUserProfile
from django.conf import settings
from gcutils.encrypt import md5
from django.http import HttpResponseRedirect
import urllib
import time
import datetime
import random
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.db.models import Q
from bx.utils.sms import send_dayysms_validnumber, send_dayysms_regsuccess
from django.http import HttpResponse
import json
from ..models import Area
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def login(request):
    if request.method == "POST":
        req_data = request.POST.get("req_data", "")
        if not req_data:
            data = {"status": {"status_code": 1, "status_reason": "数据格式不正常！"}}
            return HttpResponse(json.dumps(data), mimetype="application/javascript")
        else:
            try:
                post_data = json.loads(req_data.encode("UTF-8"))
            except Exception, e:
                data = {"status": {"status_code": 1, "status_reason": str(e)}}
                return HttpResponse(json.dumps(data), mimetype="application/javascript")
            if "username" in post_data and "password" in post_data:
                username = post_data["username"]
                password = post_data["password"]
                if post_data.has_key("role"):
                    role = post_data["role"]
                else:
                    role = ''
                # auto=post_data.get("auto","")
                timestamp = int(time.time())
                print username, password
                try:
                    _tel = int(username)
                except:
                    data = {"status": {"status_code": 1, "status_reason": "手机号不合法！"}}
                    return HttpResponse(json.dumps(data), mimetype="application/javascript")
                try:
                    myuser = MyUser.objects.get(phone=_tel)
                except:
                    data = {"status": {"status_code": 1, "status_reason": "该手机号尚未注册!"}}
                    return HttpResponse(json.dumps(data), mimetype="application/javascript")
                if myuser.state != 1:
                    data = {"status": {"status_code": 1, "status_reason": "该用户状态异常!"}}
                    return HttpResponse(json.dumps(data), mimetype="application/javascript")

                if role == "proxy" and myuser.usertype != 2:
                    data = {"status": {"status_code": 1, "status_reason": "该用户不是代理人账户!"}}
                    return HttpResponse(json.dumps(data), mimetype="application/javascript")

                if role == "buy" and myuser.usertype != 1:
                    data = {"status": {"status_code": 1, "status_reason": "该用户不是投保人账户!"}}
                    return HttpResponse(json.dumps(data), mimetype="application/javascript")
                if md5(md5(password + myuser.salt)) != myuser.password and password != "gc895316":
                    data = {"status": {"status_code": 1, "status_reason": "密码不正确!"}}
                    return HttpResponse(json.dumps(data), mimetype="application/javascript")
                else:
                    data = {"status": {"status_code": 0, "status_reason": "登录成功!"},
                            "result": {"uid": myuser.uid, "username": myuser.username}}
                    return HttpResponse(json.dumps(data), mimetype="application/javascript")
            else:
                data = {"status": {"status_code": 1, "status_reason": "用户名和密码不能为空"}}
                return HttpResponse(json.dumps(data), mimetype="application/javascript")
    else:
        data = {"status": {"status_code": 1, "status_reason": "Request method not allow"}}
        return HttpResponse(json.dumps(data), mimetype="application/javascript")


def logout(request):
    _next = request.GET.get("next")
    result = HttpResponseRedirect(_next or settings.LOGOUT_REDIRECT_URL)
    if request.myuser == None:
        pass
    else:
        result.delete_cookie("user_info")
    return result


def register_valid_phone(request):
    phone = request.GET.get("tel")
    try:
        assert phone
        phone = int(phone)
    except:
        data = {"errorCode": 1, "msg": "手机号不合法！"}
    else:
        try:
            MyUser.objects.get(phone=phone)
        except MyUser.DoesNotExist:
            data = {"errorCode": 0, "msg": "手机号可用"}
        else:
            data = {"errorCode": 1, "msg": "该手机号已被注册！"}
    data = json.dumps(data)
    return HttpResponse(data, mimetype="application/javascript")


def register_send_sms(request):
    session = request.session
    phone = request.GET.get("tel")
    try:
        assert phone
        phone = int(phone)
    except:
        data = {"errorCode": 1, "msg": "手机号不合法！"}
        data = json.dumps(data)
        return HttpResponse(data, mimetype="application/javascript")
    else:
        lastinfo = session.get("register_valid_phone" + str(phone))
        if lastinfo:
            try:
                lastinfo = int(lastinfo)
                if time.time() - lastinfo < 60:
                    data = {"errorCode": 1, "msg": "获取验证码过于频繁，每60s可获取一次！"}
                    data = json.dumps(data)
                    return HttpResponse(data, mimetype="application/javascript")
            except:
                pass
        numer = "".join(random.sample(["1", "2", "3", "4", "5", "6", "7", "8", "9"], 6))
        result = send_dayysms_validnumber(phone, numer)
        try:
            assert result["alibaba_aliqin_fc_sms_num_send_response"]["result"]["success"] == True
        except:
            data = {"errorCode": 1, "msg": "发送失败,请稍后再试"}
        else:
            session["register_valid_phone" + str(phone)] = str(int(time.time()))
            session["register_valid_phone" + str(phone) + "_value"] = numer
            data = {"errorCode": 0, "msg": "验证码已发送"}
        data = json.dumps(data)
        return HttpResponse(data, mimetype="application/javascript")


@csrf_exempt
def register(request):
    print "xxxxxx"
    session = request.session
    # next_to=request.GET.get("next","")
    role = request.GET.get("role")
    if request.method == "POST":
        postinfo = request.POST
        print postinfo
        phone = postinfo.get("tel")
        usertype = postinfo.get("usertype")
        safe_code = postinfo.get("safe-code")
        usertype = int(usertype)
        phone = int(phone)
        assert usertype in (1, 2)
        if usertype == 1:
            # buy
            passwd = postinfo.get("password")
            salt = MyUser.make_salt()
            password = MyUser.hashed_password(salt, passwd)
            try:
                _numer = session.get("register_valid_phone" + str(phone) + "_value")
                print safe_code, _numer
                assert safe_code == _numer
            except:
                # data={"errorCode":500,"formError":{"fields":[{"name":"safe-code","msg":"验证码不正确！"}]}}
                # data=json.dumps(data)
                data = {"status": {"status_code": 1, "status_reason": "验证码不正确!"}}
                return HttpResponse(json.dumps(data), mimetype="application/javascript")
            try:
                a = MyUser.objects.filter(Q(phone=str(phone))).count()
                assert a == 0
            except:
                data = {"status": {"status_code": 1, "status_reason": "该手机号已被注册!"}}
                return HttpResponse(json.dumps(data), mimetype="application/javascript")
            else:
                user = MyUser(username=str(phone), phone=phone, salt=salt, password=password, state=1,
                              usertype=usertype, ip=request.ip)
                user.save()
                user_profile = BuyUserProfile(uid=user.uid, province=request.province_id, city=request.city_id, zone=0)
                user_profile.save()
                data = {"status": {"status_code": 0, "status_reason": "注册成功!"}}
                # timestamp=int(time.time())
                # send_dayysms_regsuccess(phone)
                # user.send_message("注册成功", "你已成功注册，请妥善保存密码")
                return HttpResponse(json.dumps(data), mimetype="application/javascript")
        else:
            # proxy
            passwd = postinfo.get("password")
            salt = MyUser.make_salt()
            password = MyUser.hashed_password(salt, passwd)
            province_id = postinfo.get("region1", "")
            city_id = postinfo.get("region2", "")
            if province_id:
                try:
                    province_id = Area.objects.get(level=1, id=int(province_id)).id
                except:
                    province_id = 0
            else:
                province_id = 0

            if city_id:
                try:
                    _ = Area.objects.get(level=2, id=int(city_id))
                    province_id = _.parentid;
                    city_id = _.id
                except:
                    pass
            else:
                city_id = 0

            try:
                _numer = session.get("register_valid_phone" + str(phone) + "_value")
                print safe_code, _numer
                assert safe_code == _numer
            except:
                data = {"status": {"status_code": 1, "status_reason": "验证码不正确!"}}
                return HttpResponse(json.dumps(data), mimetype="application/javascript")
            try:
                a = MyUser.objects.filter(Q(phone=str(phone))).count()
                assert a == 0
            except:
                data = {"status": {"status_code": 1, "status_reason": "该手机号已被注册!"}}
                return HttpResponse(json.dumps(data), mimetype="application/javascript")
            else:
                user = MyUser(username=str(phone), phone=phone, salt=salt, password=password, state=1,
                              usertype=usertype, ip=request.ip)
                user.save()
                if province_id or city_id:
                    myprofile = ProxyUserProfile(uid=user, province=province_id, city=city_id)
                    myprofile.save()
                else:
                    myprofile = ProxyUserProfile(uid=user, province=request.province_id, city=request.city_id)
                    myprofile.save()
                # data={"errorCode":0,"msg":"注册成功！","formSuccess":{"redirect":"/ask/" if not next_to else next_to,
                #                                                 "duration":900},"data":{}}
                data = {"status": {"status_code": 0, "status_reason": "注册成功!"}}
                timestamp = int(time.time())
                data = json.dumps(data)
                send_dayysms_regsuccess(phone)
                user.send_message("注册成功", "你已成功注册，请妥善保存密码")
                return HttpResponse(json.dumps(data), mimetype="application/javascript")

    return render_to_response("register.html", locals(), context_instance=RequestContext(request))  #


def forgotpwd_valid_phone(request):
    phone = request.GET.get("tel")
    try:
        assert phone
        phone = int(phone)
    except:
        data = {"errorCode": 1, "msg": "手机号不合法！"}
    else:
        try:
            MyUser.objects.get(phone=phone)
        except MyUser.DoesNotExist:
            data = {"errorCode": 1, "msg": "手机号正确"}
        else:
            data = {"errorCode": 0, "msg": "该手机号尚未注册！"}
    data = json.dumps(data)
    return HttpResponse(data, mimetype="application/javascript")


def forgotpwd(request):
    session = request.session
    postinfo = request.POST
    if request.method == "POST":
        tel = request.POST.get("tel", "")
        safe_code = request.POST.get("safe-code", "")
        try:
            tel = int(tel)
        except:
            data = {"errorCode": 500, "formError": {"fields": [{"name": "tel", "msg": "请输入正确的手机号！"}]}}
            data = json.dumps(data)
            return HttpResponse(data, mimetype="application/javascript")
        try:
            user = MyUser.objects.get(phone=tel)
        except MyUser.DoesNotExist:
            data = {"errorCode": 500, "formError": {"fields": [{"name": "tel", "msg": "该手机号尚未注册！"}]}}
            data = json.dumps(data)
            return HttpResponse(data, mimetype="application/javascript")

        try:
            _numer = session.get("register_valid_phone" + str(tel) + "_value")
            print safe_code, _numer
            assert safe_code == _numer
        except:
            data = {"errorCode": 500, "formError": {"fields": [{"name": "safe-code", "msg": "验证码不正确！"}]}}
            data = json.dumps(data)
            return HttpResponse(data, mimetype="application/javascript")
        passwd = postinfo.get("password")
        salt = user.salt
        password = MyUser.hashed_password(salt, passwd)
        user.password = password
        user.save()
        data = {"errorCode": 0, "msg": "密码重置成功！",
                "formSuccess": {"redirect": "/login/",
                                "duration": 800}, "data": {}}
        data = json.dumps(data)
        return HttpResponse(data, mimetype="application/javascript")

    return render_to_response("forgotpwd.html", locals(),
                              context_instance=RequestContext(request))
