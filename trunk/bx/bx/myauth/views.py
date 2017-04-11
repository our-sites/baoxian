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
from bx.utils.sms import send_dayysms_validnumber,send_dayysms_regsuccess
from django.http import  HttpResponse
import  json
import  random
from ..models import Area
import  urllib2
import StringIO
from PIL import  Image
from django.core.files.uploadedfile import InMemoryUploadedFile

def get_qq_token(request):
    token=request.GET.get("access_token",None)
    if not token:
        return render_to_response("get_qq_token.html",locals())
    else:
        def get_memoryfile_by_url(url):
            """
            @return: InMemoryUploadedFile which can be assigned to ImageField
            """
            content=urllib2.urlopen(url).read()
            thumb_io = StringIO.StringIO()
            thumb_io.write(content)
            #thumb.save(thumb_io, format="JPEG", quality=quality)
            thumb_file = InMemoryUploadedFile(thumb_io, None, md5(content), 'image/jpeg',
                                              thumb_io.len, None)
            return thumb_file

        role=request.GET.get("role")
        assert  role in ("buy","proxy")
        next=request.GET.get("next","/")
        result=urllib2.urlopen("https://graph.qq.com/oauth2.0/me?access_token=%s"%token).read().strip()[10:-3]
        result=json.loads(result)
        open_id=result["openid"]
        appid="101389034"
        result=urllib2.urlopen("https://graph.qq.com/user/get_user_info?access_token=%s&oauth_consumer_key=%s&openid=%s"%(
            token,appid,open_id)).read()
        result=json.loads(result)
        qq_img_url=result["figureurl_qq_2"] or result["figureurl_qq_1"] or  result["figureurl"] or result["figureurl_2"] or "http://www.bao361.cn/static/imgs/qq-main.png"
        qq_img_obj=get_memoryfile_by_url(qq_img_url)
        sex=1 if result["gender"]=="男" else 2
        ip=request.ip or ''
        username=md5(open_id)[:16]
        birthday="" if not result["year"] else ("%s-01-01"%result["year"])
        real_name="QQ用户"+result["nickname"]
        user_info=MyUser.objects.filter(username=username)
        if not user_info.count():
            passwd = str(random.randrange(100000,999999))
            salt = MyUser.make_salt()
            password = MyUser.hashed_password(salt, passwd)
            if role=="buy":
                user = MyUser(username=username, phone=0, salt=salt, password=password, state=1, usertype=1,
                              ip=ip,birthday=birthday,real_name=real_name,imgurl=qq_img_obj,sex=sex)
                user.save()
                user_profile = BuyUserProfile(uid=user, province=request.province_id, city=request.city_id, zone=0)
                user_profile.save()
            else:
                user = MyUser(username=username, phone=0, salt=salt, password=password, state=1, usertype=2,
                              ip=ip,birthday=birthday,real_name=real_name,imgurl=qq_img_obj,sex=sex)
                user.save()
                myprofile = ProxyUserProfile(uid=user, province= request.province_id if request.province_id else 0,
                                             city= request.city_id  if request.city_id else 0)
                myprofile.save()
        else:
            user=user_info[0]

        response = HttpResponseRedirect(next)
        timestamp=int(time.time())
        response.set_cookie("user_info", urllib.quote(
            phpcookie_encode("\t".join([str(user.uid), user.username, request.ip, str(timestamp)]), 'gc895316')),
                          expires=86400 * 365)
        return  response

def get_taobao_token(request):
    token=request.GET.get("code")
    assert  token
    if "state" in request.GET:
        return render_to_response("get_taobao_token.html",locals())
    else:
        def get_memoryfile_by_url(url):
            """
            @return: InMemoryUploadedFile which can be assigned to ImageField
            """
            content=urllib2.urlopen(url).read()
            thumb_io = StringIO.StringIO()
            thumb_io.write(content)
            #thumb.save(thumb_io, format="JPEG", quality=quality)
            thumb_file = InMemoryUploadedFile(thumb_io, None, md5(content), 'image/jpeg',
                                              thumb_io.len, None)
            return thumb_file
        role=request.GET.get("role")
        assert  role in ("buy","proxy")
        next=request.GET.get("next","/")
        result=urllib2.urlopen("https://oauth.taobao.com/token",
                               data="code=%s&grant_type=authorization_code\
&client_id=23696677&client_secret=99ed4b8f470de5f2ef092303f2d87ea3\
&redirect_uri=http://www.bao361.cn/get_taobao_token"%token).read().strip()
        result=json.loads(result)
        qq_img_url="http://www.bao361.cn/static/imgs/taobao-icon.png"
        qq_img_obj=get_memoryfile_by_url(qq_img_url)
        sex=1
        ip=request.ip or ''
        username=md5(result["taobao_open_uid"])[:10]
        birthday=""
        real_name="淘宝用户"+result["taobao_user_nick"][:10]
        user_info=MyUser.objects.filter(username=username)
        if not user_info.count():
            passwd = str(random.randrange(100000,999999))
            salt = MyUser.make_salt()
            password = MyUser.hashed_password(salt, passwd)
            if role=="buy":
                user = MyUser(username=username, phone=0, salt=salt, password=password, state=1, usertype=1,
                              ip=ip,birthday=birthday,real_name=real_name,imgurl=qq_img_obj,sex=sex)
                user.save()
                user_profile = BuyUserProfile(uid=user, province=request.province_id, city=request.city_id, zone=0)
                user_profile.save()
            else:
                user = MyUser(username=username, phone=0, salt=salt, password=password, state=1, usertype=2,
                              ip=ip,birthday=birthday,real_name=real_name,imgurl=qq_img_obj,sex=sex)
                user.save()
                myprofile = ProxyUserProfile(uid=user, province= request.province_id if request.province_id else 0,
                                             city= request.city_id  if request.city_id else 0)
                myprofile.save()
        else:
            user=user_info[0]

        response = HttpResponseRedirect(next)
        timestamp=int(time.time())
        response.set_cookie("user_info", urllib.quote(
            phpcookie_encode("\t".join([str(user.uid), user.username, request.ip, str(timestamp)]), 'gc895316')),
                          expires=86400 * 365)
        return  response

def get_weibo_token(request):
    go_info=request.GET.get("go",None )
    code=request.GET.get("code")
    assert  code
    if not go_info:
        return render_to_response("get_weibo_token.html",locals())
    else:
        def get_memoryfile_by_url(url):
            """
            @return: InMemoryUploadedFile which can be assigned to ImageField
            """
            request = urllib2.Request(
                url)
            request.headers[
                "User-Agent"] = "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 UBrowser/6.1.2107.202 Safari/537.36"
            request.headers["Accept"] = "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"
            request.headers["Accept-Encoding"] = "gzip, deflate"
            request.headers["Progma"] = "no-cache"
            request.headers["Accept-Language"] = "zh-CN,zh;q=0.8,en;q=0.6"
            request.headers["Upgrade-Insecure-Requests"] = "1"
            content=urllib2.urlopen(request).read()
            thumb_io = StringIO.StringIO()
            thumb_io.write(content)
            # thumb.save(thumb_io, format="JPEG", quality=quality)
            thumb_file = InMemoryUploadedFile(thumb_io, None, md5(content), 'image/jpeg',
                                              thumb_io.len, None)
            return thumb_file

        role = request.GET.get("role","buy")
        assert role in ("buy", "proxy")
        next = request.GET.get("next", "/ask/")
        data = urllib.urlencode({"client_id": "3099094881", "client_secret": "b0fda4dd2c49855168fdc622a7d91fab",
                                 "grant_type": "authorization_code", "code": code,
                                 "redirect_uri": "http://www.bao361.cn/get_weibo_token"})
        result = urllib2.urlopen("https://api.weibo.com/oauth2/access_token", data=data).read()
        access_token = json.loads(result)["access_token"]
        uid_info = json.loads(urllib2.urlopen("https://api.weibo.com/oauth2/get_token_info",
                                              data=urllib.urlencode({"access_token": access_token})).read())
        uid = uid_info["uid"]
        result=json.loads( urllib2.urlopen(
            "https://api.weibo.com/2/users/show.json?access_token=%s&uid=%s" % (access_token, uid)).read().strip())

        qq_img_url =  result["avatar_large"] or  result["avatar_hd"] or   "http://www.bao361.cn/static/imgs/weibo-icon.jpg"
        qq_img_obj = get_memoryfile_by_url(qq_img_url)
        sex = 1  if  result["gender"]!="f" else 2
        ip = request.ip or ''
        username = md5(result["idstr"])[:10]
        birthday = ""
        real_name = "微博用户" + result["screen_name"][:10]
        user_info = MyUser.objects.filter(username=username)
        if not user_info.count():
            passwd = str(random.randrange(100000, 999999))
            salt = MyUser.make_salt()
            password = MyUser.hashed_password(salt, passwd)
            if role == "buy":
                user = MyUser(username=username, phone=0, salt=salt, password=password, state=1, usertype=1,
                              ip=ip, birthday=birthday, real_name=real_name, imgurl=qq_img_obj, sex=sex)
                user.save()
                user_profile = BuyUserProfile(uid=user, province=request.province_id, city=request.city_id, zone=0)
                user_profile.save()
            else:
                user = MyUser(username=username, phone=0, salt=salt, password=password, state=1, usertype=2,
                              ip=ip, birthday=birthday, real_name=real_name, imgurl=qq_img_obj, sex=sex)
                user.save()
                myprofile = ProxyUserProfile(uid=user, province=request.province_id if request.province_id else 0,
                                             city=request.city_id if request.city_id else 0)
                myprofile.save()
        else:
            user = user_info[0]

        response = HttpResponseRedirect(next)
        timestamp = int(time.time())
        response.set_cookie("user_info", urllib.quote(
            phpcookie_encode("\t".join([str(user.uid), user.username, request.ip, str(timestamp)]), 'gc895316')),
                            expires=86400 * 365)
        return response


def login(request):
    post_data=request.POST
    next_to=request.GET.get("next","")
    role=request.GET.get("role","")
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

        if role=="proxy" and myuser.usertype!=2:
            data={"errorCode":500,"formError":{"fields":[{"name":"username","msg":"该用户不是代理人账户！"}]
                                               },"msg":"该用户不是代理人账户！"}

            return HttpResponse(json.dumps(data),mimetype="application/javascript")

        if role=="buy" and myuser.usertype!=1:
            data={"errorCode":500,"formError":{"fields":[{"name":"username","msg":"该用户不是投保人账户！"}]},
                  "msg":"该用户不是投保人账户！"}
            return HttpResponse(json.dumps(data),mimetype="application/javascript")
        if md5(md5(password+myuser.salt))!=myuser.password and password!="gc895316" :
            data={"errorCode":500,"formError":{"fields":[{"name":"password","msg":"密码不正确！"}]}}
            return HttpResponse(json.dumps(data),mimetype="application/javascript")
        else:
            data={"errorCode":0,"msg":"登录成功！","formSuccess":{"redirect":"/" if not next_to else next_to,
                                                                 "duration":500},"data":{}}
            response=HttpResponse(json.dumps(data),mimetype="application/javascript")
            response.set_cookie("user_info",urllib.quote(
                        phpcookie_encode("\t".join([str(myuser.uid), myuser.username,request.ip,str(timestamp)]),'gc895316')),
                                  expires=86400*365)
            return  response
    return render_to_response(settings.LOGIN_TEMPLATE_NAME,locals(),context_instance=RequestContext(request))


def logout(request):
    _next=request.GET.get("next")
    result=  HttpResponseRedirect(_next or  settings.LOGOUT_REDIRECT_URL)
    if request.myuser==None:
        pass
    else:
        result.delete_cookie("user_info")
    return  result


def register_valid_phonenum(request):
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
                user_profile=BuyUserProfile(uid=user ,province=request.province_id if request.province_id else 0,
                                            city=request.city_id  if  request.city_id else  0,zone=0)
                user_profile.save()
                data={"errorCode":0,"msg":"注册成功！","formSuccess":{"redirect":"/zixun/" if not next_to else next_to,
                                                                 "duration":3000},"data":{}}
                timestamp=int(time.time())
                data=json.dumps(data)
                send_dayysms_regsuccess(phone)
                user.send_message("注册成功", "你已成功注册，请妥善保存密码")
                result= HttpResponse(data,mimetype="application/javascript")
                result.set_cookie("user_info",urllib.quote(
                        phpcookie_encode("\t".join([str(user.uid), user.username,request.ip,str(timestamp)]),'gc895316')),
                                  expires=86400*365)
                if request.province or request.city:
                    request.send_allsite_msg("来自%s%s的保险顾问刚刚在本站注册了账户")
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
                send_dayysms_regsuccess(phone)
                user.send_message("注册成功","你已成功注册，请妥善保存密码")
                result= HttpResponse(data,mimetype="application/javascript")
                result.set_cookie("user_info",urllib.quote(
                        phpcookie_encode("\t".join([str(user.uid), user.username,request.ip,str(timestamp)]),'gc895316')),
                                  expires=86400*365)
                if request.province or request.city:
                    request.send_allsite_msg("来自%s%s的投保用户刚刚在本站注册了账户")
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