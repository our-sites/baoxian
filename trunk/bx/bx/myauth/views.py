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
from models import  MyUser
from django.template.context import  RequestContext
from django.db.models import  Q
from bx.utils.sms import send_dayysms_validnumber
from django.http import  HttpResponse
import  json
import  random

def login(request):
    post_data=request.POST
    next=request.GET.get("next","")
    next=next or  settings.LOGIN_REDIRECT_URL
    if request.method=="POST":
        username=post_data["username"]
        password=post_data["password"]
        timestamp=int(time.time())
        try:
            _tel=int(username)
        except:
            _tel=None
        try:
            if _tel:
                if "@" in username:
                    user=MyUser.objects.get(Q(username=username)|Q(verifymobile=_tel)|Q(email=username))
                else:
                    user=MyUser.objects.get(Q(username=username)|Q(verifymobile=_tel))
            else:
                if "@" in username:
                    user=MyUser.objects.get(username=username|Q(email=username))
                else:
                    user=MyUser.objects.get(username=username)
        except Exception as e :
            print username
            print "Exception",e
            message="该用户不存在！"
        else:
            if user.state!=1:
                message="该用户状态不正常！"
            else:
                if md5(md5(password)+user.salt)==user.password:
                    result=HttpResponseRedirect(next)
                    if isinstance(username,unicode):
                        username=username.encode("utf-8")
                    result.set_cookie("user_info",urllib.quote(
                            phpcookie_encode("\t".join([str(user.uid), username,request.ip,str(timestamp)]),'gc895316')),
                                      domain=".baoxiangj.com")
                    return  result
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
                data={"errorCode":0,"msg":"注册成功！","formSuccess":{"redirect":"/zixun/","duration":3000},"data":{}}
                timestamp=int(time.time())
                data=json.dumps(data)
                result= HttpResponse(data,mimetype="application/javascript")
                result.set_cookie("user_info",urllib.quote(
                        phpcookie_encode("\t".join([str(user.uid), user.username,request.ip,str(timestamp)]),'gc895316')),
                                  )
                return  result
        else:
            #proxy
            pass


    return  render_to_response("register.html",locals(),context_instance=RequestContext(request)) #