#coding:utf-8
__author__ = 'admin'
# --------------------------------
# Created by admin  on 2016/11/1.
# ---------------------------------

from django.contrib.admin.views.decorators import  staff_member_required
from django.http import  HttpResponse,HttpResponseRedirect
from django.shortcuts import  render_to_response
from django.template.context import RequestContext
from  bx.myauth.models import *
from bx.models import Area
import  datetime
from django.core.paginator import Paginator,EmptyPage
from ..models import Consult,Company


@staff_member_required
def home(request):
    return  HttpResponseRedirect('/manage/user/buy/')

@staff_member_required
def user_buy(request):
    if request.method=="POST" and  request.POST.get("input") :
        _type=request.POST.get("type","")
        input=request.POST.get("input","")
        if _type=="phone":
            try:
                input=int(input)
            except:
                allinfo=[]
            else:
                allinfo=MyUser.objects.filter(usertype=1,phone=input)
        else:
            allinfo=MyUser.objects.filter(usertype=1,username=input)
        for i in allinfo:
            i.profile=i.get_profile()
        area_config=dict([(i["id"],i["shortname"]) for i in  Area.objects.filter(id__in=[i.profile.province  for i in allinfo  if i.profile]+[i.profile.city for i in allinfo if i.profile ]).values("id","shortname") ])
        for i in allinfo:
            i.province_info=area_config.get(i.profile.province  if  i.profile else None  ,"")
            i.city_info=area_config.get(  i.profile.city  if i.profile else None ,"")
            i.datetime=datetime.datetime.fromtimestamp(i.addtime).strftime("%Y-%m-%d %H:%M:%S")
        return  render_to_response("manage_user_buy.html",locals(),context_instance=RequestContext(request))
    else:
        page=request.GET.get("page","1")
        page=int(page)
        allinfo_paginator=Paginator(MyUser.objects.filter(usertype=1),15)
        try:
            allinfo=allinfo_paginator.page(page)
        except EmptyPage:
            allinfo=allinfo_paginator.page(1)
            page=1
        allinfo.next_page_number()
        allinfo.has_next()
        for i in allinfo:
            i.profile=i.get_profile()
        area_config=dict([(i["id"],i["shortname"]) for i in  Area.objects.filter(id__in=[i.profile.province  for i in allinfo  if i.profile]+[i.profile.city for i in allinfo if i.profile ]).values("id","shortname") ])
        for i in allinfo:
            i.province_info=area_config.get(i.profile.province  if  i.profile else None  ,"")
            i.city_info=area_config.get(  i.profile.city  if i.profile else None ,"")
            i.datetime=datetime.datetime.fromtimestamp(i.addtime).strftime("%Y-%m-%d %H:%M:%S")
        return  render_to_response("manage_user_buy.html",locals(),context_instance=RequestContext(request))

@staff_member_required
def user_buy_detail(request,_id):
    myuser=MyUser.objects.get(usertype=1,uid=int(_id))
    if request.method=="POST":
        img=request.FILES.get("img")
        real_name=request.POST.get("real_name")
        state=request.POST.get("state")
        state=int(state)
        tel=request.POST.get("tel")
        email=request.POST.get("email")
        qq=request.POST.get("qq")
        sex=request.POST.get("sex")
        sex=int(sex)
        if img:
            myuser.imgurl=img
        myuser.real_name=real_name
        myuser.state=state
        myuser.tel=tel
        myuser.email=email
        myuser.qq=qq
        myuser.sex=sex
        myuser.save()
        return  HttpResponseRedirect(request.get_full_path())
    else:
        profile=myuser.get_profile()
        if profile:
            try:
                _t=Area.objects.get(level=1,id=profile.province)
            except Area.DoesNotExist:
                myuser.province_info=""
            else:
                myuser.province_info=_t.areaname
            try:
                _t=Area.objects.get(level=2,id=profile.city)
            except Area.DoesNotExist:
                myuser.city_info=""
            else:
                myuser.city_info=_t.areaname
        else:
            myuser.province_info="";myuser.city_info=""
        myuser.datetime=datetime.datetime.fromtimestamp(myuser.addtime).strftime("%Y-%m-%d %H:%M:%S")
        return  render_to_response("manage_user_buy_detail.html",locals(),context_instance=RequestContext(request))

@staff_member_required
def user_buy_resetpwd(request,_id):
    myuser=MyUser.objects.get(usertype=1,uid=int(_id))
    if request.method=="POST":
        newpwd=request.POST.get("newpwd")
        salt=MyUser.make_salt()
        password=MyUser.hashed_password(salt,newpwd)
        myuser.salt=salt
        myuser.password=password
        myuser.save()
        message=u"success! 新密码是%s"%newpwd
        return  render_to_response("manage_user_buy_resetpwd.html",locals(),context_instance=RequestContext(request))
    return  render_to_response("manage_user_buy_resetpwd.html",locals(),context_instance=RequestContext(request))

@staff_member_required
def user_proxy(request):
    if request.method=="POST" and  request.POST.get("input") :
        _type=request.POST.get("type","")
        input=request.POST.get("input","")
        if _type=="phone":
            try:
                input=int(input)
            except:
                allinfo=[]
            else:
                allinfo=MyUser.objects.filter(usertype=2,phone=input)
        else:
            allinfo=MyUser.objects.filter(usertype=2,username=input)

        allprofile=ProxyUserProfile.objects.filter(uid__uid__in=[i.uid for i in allinfo])
        print [i.uid  for i in allinfo],allprofile

        allprofile_config=dict([(i.uid.uid,[i.province,i.city])  for i in allprofile])
        area_config=dict([(i["id"],i["shortname"]) for i in  Area.objects.filter(id__in=[i.province  for i in allprofile ]+[i.city for i in allprofile]).values("id","shortname") ])
        for i in allinfo:
            i.province_info=area_config.get(allprofile_config.get(i.uid,[None,None])[0]  ,"")
            i.city_info=area_config.get(allprofile_config.get(i.uid,[None,None])[1],"")
            i.datetime=datetime.datetime.fromtimestamp(i.addtime).strftime("%Y-%m-%d %H:%M:%S")
        return  render_to_response("manage_user_proxy.html",locals(),context_instance=RequestContext(request))
    else:
        page=request.GET.get("page","1")
        page=int(page)
        allinfo_paginator=Paginator(MyUser.objects.filter(usertype=2),15)
        try:
            allinfo=allinfo_paginator.page(page)
        except EmptyPage:
            allinfo=allinfo_paginator.page(1)
            page=1
        allinfo.next_page_number()
        allinfo.has_next()

        allprofile=ProxyUserProfile.objects.filter(uid__uid__in=[i.uid for i in allinfo])
        print [i.uid  for i in allinfo],allprofile

        allprofile_config=dict([(i.uid.uid,[i.province,i.city])  for i in allprofile])
        area_config=dict([(i["id"],i["shortname"]) for i in  Area.objects.filter(id__in=[i.province  for i in allprofile ]+[i.city for i in allprofile]).values("id","shortname") ])
        for i in allinfo:
            i.province_info=area_config.get(allprofile_config.get(i.uid,[None,None])[0]  ,"")
            i.city_info=area_config.get(allprofile_config.get(i.uid,[None,None])[1],"")
            i.datetime=datetime.datetime.fromtimestamp(i.addtime).strftime("%Y-%m-%d %H:%M:%S")
        return  render_to_response("manage_user_proxy.html",locals(),context_instance=RequestContext(request))

@staff_member_required
def user_proxy_detail(request,_id):
    myuser=MyUser.objects.get(usertype=2,uid=int(_id))
    status_range=[1,2,3]
    try:
        myprofile=ProxyUserProfile.objects.get(uid__uid=myuser.uid)
    except ProxyUserProfile.DoesNotExist:
        myprofile=None
    allcompany=Company.objects.all()
    if request.method=="POST":
        if not myprofile:
            myprofile=ProxyUserProfile(uid=myuser)
            myprofile.save()
        img=request.FILES.get("img")
        real_name=request.POST.get("real_name")
        state=request.POST.get("state")
        state=int(state)
        tel=request.POST.get("tel")
        email=request.POST.get("email")
        qq=request.POST.get("qq")
        sex=request.POST.get("sex")
        sex=int(sex)
        if img:
            myuser.imgurl=img
        myuser.real_name=real_name
        myuser.state=state
        myuser.tel=tel
        myuser.email=email
        myuser.qq=qq
        myuser.sex=sex
        myuser.save()
        cid=int(request.POST.get("cid","0"))
        myprofile.cid=cid
        myprofile.my_ad=request.POST.get("my_ad","")
        myprofile.certifi_num=request.POST.get("certifi_num","")
        myprofile.practice_num=request.POST.get("practice_num","")
        if request.POST.has_key("certifi_status"):
            myprofile.certifi_status=int(request.POST.get("certifi_status"))
            myprofile.certifi_message=request.POST["certifi_message"]
        myprofile.weixin=request.POST["weixin"]
        myprofile.save()
        return  HttpResponseRedirect(request.get_full_path())
    else:
        if myprofile:
            try:
                _t=Area.objects.get(level=1,id=myprofile.province)
            except Area.DoesNotExist:
                myuser.province_info=""
            else:
                myuser.province_info=_t.areaname
            try:
                _t=Area.objects.get(level=2,id=myprofile.city)
            except Area.DoesNotExist:
                myuser.city_info=""
            else:
                myuser.city_info=_t.areaname
        else:
            myuser.province_info="";myuser.city_info=""
        myuser.datetime=datetime.datetime.fromtimestamp(myuser.addtime).strftime("%Y-%m-%d %H:%M:%S")
        return  render_to_response("manage_user_proxy_detail.html",locals(),context_instance=RequestContext(request))

@staff_member_required
def user_proxy_resetpwd(request,_id):
    myuser=MyUser.objects.get(usertype=2,uid=int(_id))
    if request.method=="POST":
        newpwd=request.POST.get("newpwd")
        salt=MyUser.make_salt()
        password=MyUser.hashed_password(salt,newpwd)
        myuser.salt=salt
        myuser.password=password
        myuser.save()
        message=u"success! 新密码是%s"%newpwd
        return  render_to_response("manage_user_proxy_resetpwd.html",locals(),context_instance=RequestContext(request))
    return  render_to_response("manage_user_proxy_resetpwd.html",locals(),context_instance=RequestContext(request))


@staff_member_required
def zixun_add(request):
    if request.method=="POST":
        title=request.POST.get("title")
        _type=request.POST.get("type")
        _type=int(_type)
        writer=request.POST.get("writer")
        content=request.POST.get("content")
        keywords=request.POST.get("keywords")
        description=request.POST.get("description")
        obj=Consult(title=title,type=_type,writer=writer,_from=str(time.time()),addtime=int(time.time()),
                content=content,status=1,keywords=keywords,description=description,
                imghandle_tag=1)
        obj.save()
        return render_to_response("manage_zixun_add_success.html",locals(),context_instance=RequestContext(request))
    else:
        return  render_to_response("manage_zixun_add.html",locals(),context_instance=RequestContext(request))

@staff_member_required
def zixun_all(request):
    if request.method=="POST":
        _id=request.POST.get("input")
        try:
            _id=int(_id)
        except:
            allinfo=[]
        else:
            allinfo=Consult.objects.filter(zid=_id)
        return  render_to_response("manage_zixun_all.html",locals(),
                                   context_instance=RequestContext(request))
    else:
        page=request.GET.get("page","1")
        page=int(page)
        allinfo_paginator=Paginator(Consult.objects.filter(type__in=[1,2,3,4,5,6]).order_by("-addtime"),15)
        try:
            allinfo=allinfo_paginator.page(page)
        except EmptyPage:
            allinfo=allinfo_paginator.page(1)
            page=1
        allinfo.next_page_number()
        allinfo.has_next()
        #area_config=dict([(i["id"],i["shortname"]) for i in  Area.objects.filter(id__in=[i.province  for i in allinfo ]+[i.city for i in allinfo]).values("id","shortname") ])
        for i in allinfo:
            #i.province_info=area_config.get(i.province,"")
            #i.city_info=area_config.get(i.city,"")
            i.datetime=datetime.datetime.fromtimestamp(i.addtime).strftime("%Y-%m-%d %H:%M:%S")
    return  render_to_response("manage_zixun_all.html",locals(),context_instance=RequestContext(request))


def zixun_detail(request,zid):
    obj=Consult.objects.get(zid=int(zid))
    if request.method=="POST":
        title=request.POST.get("title")
        _type=request.POST.get("type")
        _type=int(_type)
        writer=request.POST.get("writer")
        content=request.POST.get("content")
        keywords=request.POST.get("keywords")
        description=request.POST.get("description")
        obj=Consult(title=title,type=_type,writer=writer,_from=str(time.time()),addtime=int(time.time()),
                content=content,status=1,keywords=keywords,description=description,
                imghandle_tag=1)
        obj.save()
        return render_to_response("manage_zixun_add_success.html",locals(),context_instance=RequestContext(request))
    else:
        return  render_to_response("manage_zixun_detail.html",locals(),
                                   context_instance=RequestContext(request))


def logout(request):
    try:
        assert  request.user.is_staff
        result= HttpResponseRedirect("/manage/logout/")
        result.delete_cookie("sessionid")
        return  result
    except:
        return HttpResponseRedirect("/manage/")
