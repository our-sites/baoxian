#coding:utf-8
from django.http import  HttpResponse
from django.shortcuts import  render_to_response
from django.template.context import  RequestContext
from ..myauth.models import *
from ..myauth.decorators import login_required,buyuser_login_required,proxyuser_login_required
from django.core.paginator import Paginator,EmptyPage,InvalidPage
from ..models import Ask,Answer,DingZhi,Consult,Product
from django.core.files.uploadedfile import InMemoryUploadedFile
from PIL import  Image
import  StringIO


@proxyuser_login_required
def index(request):
    hot_anli=Consult.objects.filter(type=2,status=1)[:7]
    hot_pro=Product.objects.all()[:7]
    hot_baike=Consult.objects.filter(type=6,status=1)[:7]
    hot_users=ProxyUserProfile.objects.filter(certifi_status=2)[:12]
    return render_to_response("work_proxy_index.html",locals(),context_instance=RequestContext(request))


@proxyuser_login_required
def all_msg(request):
    page=request.GET.get("page","1")
    request.myuser.send_message("test","fsdafdsafdsafdsafdsfddsf")
    try:
        page=int(page)
        assert page>0
    except:
        page=1
    all_msg=request.myuser.get_messages()

    all_msg.update(is_read=1)
    msg_paginator=Paginator(all_msg,10)
    allinfo_paginator=msg_paginator
    try:
        msg_info=msg_paginator.page(page)
    except (EmptyPage,InvalidPage):
        page=1
        msg_info=msg_paginator.page(1)

    return  render_to_response("work_proxy_allmsg.html",locals(),context_instance=RequestContext(request))





@proxyuser_login_required
def my_ans(request):
    page=request.GET.get("page","1")
    all_ans=Answer.objects.filter(uid=request.myuser.uid).values("askid").distinct().order_by("-askid")
    print all_ans.query
    try:
        page=int(page)
        assert page>0
    except:
        page=1

    allinfo_paginator=Paginator(all_ans,10)
    try:
        ans_info=allinfo_paginator.page(page)
    except (EmptyPage,InvalidPage):
        page=1
        ans_info=allinfo_paginator.page(1)
    def get_ask(askid):
        return Ask.objects.get(askid=askid)
    for i in ans_info:
        i["get_ask"]=get_ask(i["askid"])

    return  render_to_response("work_proxy_myans.html",locals(),context_instance=RequestContext(request))



@proxyuser_login_required
def change_pwd(request):
    error_msg=""
    success_msg=""
    if request.method=="POST":
        post_info=request.POST
        oldpwd=post_info.get("oldpwd","")
        newpwd=post_info.get("newpwd","")
        newpwd_again=post_info.get("newpwd_again","")
        if not oldpwd:
            error_msg=u"请输入旧密码"
        if not error_msg:
            if not request.myuser.check_password(oldpwd):
                error_msg=u"旧密码输入有误！请重新输入"
        if not error_msg:
            if len(newpwd)<=5:
                error_msg=u"新密码长度小于6位！"
        if not error_msg:
            if newpwd!=newpwd_again:
                error_msg=u"新密码两次输入不一致！"
        if not error_msg:
            request.myuser.password=request.myuser.reset_password(newpwd)
            success_msg=u"修改成功！"
            return  render_to_response("work_proxy_changepwd.html",locals(),context_instance=RequestContext(request))



    return  render_to_response("work_proxy_changepwd.html",locals(),context_instance=RequestContext(request))