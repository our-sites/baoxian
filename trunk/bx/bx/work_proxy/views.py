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
def get_baojianju_info(request):
    pass


@proxyuser_login_required
def renzheng(request):
    com_info=Company.objects.all().order_by("-product_weight")
    success_mgs=error_msg=""
    post_info=request.POST
    if request.method=="POST":
        cid=post_info.get("cid","0")
        cid=int(cid)
        position=post_info.get("position","")
        name=post_info.get("name","")
        qq=post_info.get("qq","")
        weixin=post_info.get("weixin","")
        certifi_num=post_info.get("certifi_num","")
        practice_num=post_info.get("practice_num","")
        sex=post_info.get("sex","0")
        sex=int(sex)
        my_ad=post_info.get("my_ad","")
        year=post_info.get("year","1")
        year=int(year)
        request.myuser_profile.year=year
        request.myuser_profile.save()
        if cid==0:
            error_msg="请选择保险企业！"
        else:
            request.myuser_profile.cid=cid
            request.myuser_profile.save()
        if  not name:
            error_msg="请输入您的姓名"
        else:
            request.myuser.real_name=name
            request.myuser.save()
        if not certifi_num :
            error_msg="请输入资格证编号"
        elif len(certifi_num)!=20:
            error_msg="资格证编号长度不合法！"
        else:
            request.myuser_profile.certifi_num=certifi_num
            request.myuser_profile.save()

        if practice_num:
            if len(practice_num)>26:
                error_msg="长度过长"
            else:
                request.myuser_profile.practice_num=practice_num
                request.myuser_profile.save()


        if not error_msg:
            request.myuser_profile.cid=cid
            request.myuser.sex=sex
            request.myuser_profile.position=position
            request.myuser.real_name=name
            request.myuser.qq=qq
            request.myuser_profile.weixin=weixin
            request.myuser_profile.certifi_num=certifi_num
            request.myuser_profile.my_ad=my_ad
            request.myuser_profile.certifi_status=2
            request.myuser.save()
            request.myuser_profile.save()
            success_mgs="实名认证成功！"

    return render_to_response("work_proxy_renzheng.html",locals(),context_instance=RequestContext(request))

@proxyuser_login_required
def all_msg(request):
    page=request.GET.get("page","1")
    #request.myuser.send_message("test","fsdafdsafdsafdsafdsfddsf")
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

@proxyuser_login_required
def img(request):
    post_info=request.POST


    def get_thumbnail(orig, width=200, height=200):
        """get the thumbnail of orig
        @return: InMemoryUploadedFile which can be assigned to ImageField
        """
        quality = "keep"
        file_suffix = orig.name.split(".")[-1]
        filename = orig.name
        if file_suffix not in ["jpg", "jpeg"]:
            filename = "%s.jpg" % orig.name[:-(len(file_suffix)+1)]
            quality = 95
        im = Image.open(orig)
        size = (width, height)
        thumb = im
        thumb.thumbnail(size, Image.ANTIALIAS)
        thumb_io = StringIO.StringIO()
        thumb.save(thumb_io, format="JPEG", quality=quality)
        thumb_file = InMemoryUploadedFile(thumb_io, None, filename, 'image/jpeg',
                                          thumb_io.len, None)
        return thumb_file
    error_msg=""
    success_msg=""
    if request.method=="POST":
        img_file=request.FILES["img"]
        try:
            assert img_file.name.split(".")[-1] in ["jpg","png","gif"]
        except:
            error_msg="文件格式必须位jpg png gif之一！"
        if not error_msg:
            if img_file.size>2000000:
                error_msg="文件过大，文件大小必须在2M以内！"
        if not error_msg:
            img_file=get_thumbnail(img_file,125,145)
            request.myuser.imgurl=img_file
            request.myuser.save()
            success_msg="头像修改成功"

    return  render_to_response("work_proxy_img.html",locals(),context_instance=RequestContext(request))