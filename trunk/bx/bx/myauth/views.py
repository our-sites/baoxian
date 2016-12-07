#coding:utf-8
__author__ = 'zhoukunpeng'
# --------------------------------
# Created by zhoukunpeng  on 2016/7/13.
# ---------------------------------
from decorators import  login_required
from django.conf import  settings
from gcutils.encrypt import  md5
from django.http import  HttpResponseRedirect
from cookie_encrypt import  phpcookie_encode
import  urllib
import time
import  datetime
import  random
from django.shortcuts import  render_to_response
from models import  MyUser,ProxyUserProfile,BuyUserProfile
from django.template.context import  RequestContext
from django.db.models import  Q
from bx.utils.sms import send_dayysms_validnumber
from django.http import  HttpResponse
import  json
import  random
from ..models import Area

def login(request):
    post_data=request.POST
    next_to=request.GET.get("next","")
    next_to=next_to or  settings.LOGIN_REDIRECT_URL
    if request.method=="POST":
        username=post_data["username"]
        password=post_data["password"]
        auto=post_data.get("auto","")
        timestamp=int(time.time())

        try:
            _tel=int(username)
        except:
            data={"errorCode":500,"formError":{"fields":[{"name":"username","msg":"手机号不合法！"}]}}
            return HttpResponse(json.dumps(data),mimetype="application/javascript")

        try:
            myuser=MyUser.objects.get(phone=_tel)
        except:
            data={"errorCode":500,"formError":{"fields":[{"name":"username","msg":"该手机号尚未注册！"}]}}
            return HttpResponse(json.dumps(data),mimetype="application/javascript")
        if myuser.state!=1:
            data={"errorCode":500,"formError":{"fields":[{"name":"username","msg":"该用户状态异常！"}]}}
            return HttpResponse(json.dumps(data),mimetype="application/javascript")
        if md5(md5(password+myuser.salt))!=myuser.password:
            data={"errorCode":500,"formError":{"fields":[{"name":"password","msg":"密码不正确！"}]}}
            return HttpResponse(json.dumps(data),mimetype="application/javascript")
        else:
            data={"errorCode":0,"msg":"登录成功！","formSuccess":{"redirect":"/" if not next_to else next_to,
                                                                 "duration":500},"data":{}}
            response=HttpResponse(json.dumps(data),mimetype="application/javascript")
            response.set_cookie("user_info",urllib.quote(
                        phpcookie_encode("\t".join([str(myuser.uid), myuser.username,request.ip,str(timestamp)]),'gc895316')),
                                  )
            return  response
    return render_to_response(settings.LOGIN_TEMPLATE_NAME,locals(),context_instance=RequestContext(request))


def logout(request):
    result=  HttpResponseRedirect(settings.LOGOUT_REDIRECT_URL)
    if request.myuser==None:
        pass
    else:
        result.delete_cookie("user_info",domain=".baoxiangj.com")
    return  result


def register_valid_phone(request):
    phone=request.GET.get("tel")
    try:
        assert  phone
        phone=int(phone)
    except:
        data={"errorCode":1,"msg":"手机号不合法！"}
    else:
        try:
            MyUser.objects.get(phone=phone)
        except MyUser.DoesNotExist:
            data={"errorCode":0,"msg":"手机号可用"}
        else:
            data={"errorCode":1,"msg":"该手机号已被注册！"}
    data=json.dumps(data)
    return HttpResponse(data ,mimetype="application/javascript")




def register_send_sms(request):
    session=request.session
    phone=request.GET.get("tel")
    try:
        assert  phone
        phone=int(phone)
    except:
        data={"errorCode":1,"msg":"手机号不合法！"}
        data=json.dumps(data)
        return HttpResponse(data ,mimetype="application/javascript")
    else:
        lastinfo= session.get("register_valid_phone"+str(phone))
        if lastinfo:
            try:
                lastinfo=int(lastinfo)
                if time.time()-lastinfo<60:
                    data={"errorCode":1,"msg":"获取验证码过于频繁，每60s可获取一次！"}
                    data=json.dumps(data)
                    return HttpResponse(data ,mimetype="application/javascript")
            except:
                pass
        numer="".join(random.sample(["1","2","3","4","5","6","7","8","9"],6))
        result=send_dayysms_validnumber(phone,numer)
        try:
            assert  result["alibaba_aliqin_fc_sms_num_send_response"]["result"]["success"]==True
        except:
            data={"errorCode":1,"msg":"发送失败,请稍后再试"}
        else:
            session["register_valid_phone"+str(phone)]=str(int(time.time()))
            session["register_valid_phone"+str(phone)+"_value"]=numer
            data={"errorCode":0,"msg":"验证码已发送"}
        data=json.dumps(data)
        return  HttpResponse(data ,mimetype="application/javascript")


def register(request):
    session=request.session
    next_to=request.GET.get("next","")
    role=request.GET.get("role")
    if request.method=="POST":
        postinfo=request.POST
        phone=postinfo.get("tel")
        usertype=postinfo.get("usertype")
        safe_code=postinfo.get("safe-code")
        usertype=int(usertype)
        phone=int(phone)
        assert  usertype in (1,2)
        if usertype==1:
            #buy
            passwd=postinfo.get("password")
            salt=MyUser.make_salt()
            password=MyUser.hashed_password(salt,passwd)
            try:
                _numer=session.get("register_valid_phone"+str(phone)+"_value")
                print safe_code,_numer
                assert safe_code==_numer
            except:
                data={"errorCode":500,"formError":{"fields":[{"name":"safe-code","msg":"验证码不正确！"}]}}
                data=json.dumps(data)
                return HttpResponse(data,mimetype="application/javascript")
            try:
                a=MyUser.objects.filter(Q(phone=str(phone))).count()
                assert a==0
            except:
                data={"errorCode":500,"formError":{"fields":[{"name":"tel","msg":"该手机号已被注册！"}]}}
                data=json.dumps(data)
                return HttpResponse(data,mimetype="application/javascript")
            else:
                user=MyUser(username=str(phone),phone=phone,salt=salt,password=password,state=1,usertype=usertype,ip=request.ip)
                user.save()
                user_profile=BuyUserProfile(uid=user.uid,province=request.province_id,city=request.city_id,zone=0)
                user_profile.save()
                data={"errorCode":0,"msg":"注册成功！","formSuccess":{"redirect":"/zixun/" if not next_to else next_to,
                                                                 "duration":3000},"data":{}}
                timestamp=int(time.time())
                data=json.dumps(data)
                result= HttpResponse(data,mimetype="application/javascript")
                result.set_cookie("user_info",urllib.quote(
                        phpcookie_encode("\t".join([str(user.uid), user.username,request.ip,str(timestamp)]),'gc895316')),
                                  )
                return  result
        else:
            #proxy
            passwd=postinfo.get("password")
            salt=MyUser.make_salt()
            password=MyUser.hashed_password(salt,passwd)
            province_id=postinfo.get("region1","")
            city_id=postinfo.get("region2","")
            if province_id:
                try:
                    province_id=Area.objects.get(level=1,id=int(province_id)).id
                except:
                    province_id=0
            else:
                province_id=0

            if city_id:
                try:
                    _=Area.objects.get(level=2,id=int(city_id))
                    province_id=_.parentid;city_id=_.id
                except:
                    pass
            else:
                city_id=0

            try:
                _numer=session.get("register_valid_phone"+str(phone)+"_value")
                print safe_code,_numer
                assert safe_code==_numer
            except:
                data={"errorCode":500,"formError":{"fields":[{"name":"safe-code","msg":"验证码不正确！"}]}}
                data=json.dumps(data)
                return HttpResponse(data,mimetype="application/javascript")
            try:
                a=MyUser.objects.filter(Q(phone=str(phone))).count()
                assert a==0
            except:
                data={"errorCode":500,"formError":{"fields":[{"name":"tel","msg":"该手机号已被注册！"}]}}
                data=json.dumps(data)
                return HttpResponse(data,mimetype="application/javascript")
            else:
                user=MyUser(username=str(phone),phone=phone,salt=salt,password=password,state=1,usertype=usertype,ip=request.ip)
                user.save()
                if province_id or city_id:
                    myprofile=ProxyUserProfile(uid=user,province=province_id,city=city_id)
                    myprofile.save()
                else:
                    myprofile=ProxyUserProfile(uid=user,province=request.province_id,city=request.city_id)
                    myprofile.save()
                data={"errorCode":0,"msg":"注册成功！","formSuccess":{"redirect":"/ask/" if not next_to else next_to,
                                                                 "duration":900},"data":{}}
                timestamp=int(time.time())
                data=json.dumps(data)
                result= HttpResponse(data,mimetype="application/javascript")
                result.set_cookie("user_info",urllib.quote(
                        phpcookie_encode("\t".join([str(user.uid), user.username,request.ip,str(timestamp)]),'gc895316')),
                                  )
                return  result


    return  render_to_response("register.html",locals(),context_instance=RequestContext(request)) #

def forgotpwd_valid_phone(request):
    phone=request.GET.get("tel")
    try:
        assert  phone
        phone=int(phone)
    except:
        data={"errorCode":1,"msg":"手机号不合法！"}
    else:
        try:
            MyUser.objects.get(phone=phone)
        except MyUser.DoesNotExist:
            data={"errorCode":1,"msg":"手机号正确"}
        else:
            data={"errorCode":0,"msg":"该手机号尚未注册！"}
    data=json.dumps(data)
    return HttpResponse(data ,mimetype="application/javascript")

def forgotpwd(request):
    session=request.session
    postinfo=request.POST
    if request.method=="POST":
        tel=request.POST.get("tel","")
        safe_code=request.POST.get("safe-code","")
        try:
            tel=int(tel)
        except:
            data={"errorCode":500,"formError":{"fields":[{"name":"tel","msg":"请输入正确的手机号！"}]}}
            data=json.dumps(data)
            return HttpResponse(data,mimetype="application/javascript")
        try:
            user=MyUser.objects.get(phone=tel)
        except MyUser.DoesNotExist:
            data={"errorCode":500,"formError":{"fields":[{"name":"tel","msg":"该手机号尚未注册！"}]}}
            data=json.dumps(data)
            return HttpResponse(data,mimetype="application/javascript")

        try:
            _numer=session.get("register_valid_phone"+str(tel)+"_value")
            print safe_code,_numer
            assert safe_code==_numer
        except:
            data={"errorCode":500,"formError":{"fields":[{"name":"safe-code","msg":"验证码不正确！"}]}}
            data=json.dumps(data)
            return HttpResponse(data,mimetype="application/javascript")
        passwd=postinfo.get("password")
        salt=user.salt
        password=MyUser.hashed_password(salt,passwd)
        user.password=password
        user.save()
        data={"errorCode":0,"msg":"密码重置成功！",
              "formSuccess":{"redirect":"/login/" ,
                            "duration":800},"data":{}}
        data=json.dumps(data)
        return HttpResponse(data,mimetype="application/javascript")

    return  render_to_response("forgotpwd.html",locals(),
                               context_instance=RequestContext(request))