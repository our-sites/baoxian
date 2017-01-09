#coding:utf-8
from django.http import  HttpResponse
from django.shortcuts import  render_to_response
from django.template.context import  RequestContext
from ..myauth.models import *
from ..myauth.decorators import login_required,buyuser_login_required
from django.core.paginator import Paginator,EmptyPage,InvalidPage
from ..models import Ask,Answer,DingZhi,Consult,Product
from django.core.files.uploadedfile import InMemoryUploadedFile
from PIL import  Image
import  StringIO

@buyuser_login_required
def index(request):
    hot_anli=Consult.objects.filter(type=2,status=1)[:7]
    hot_pro=Product.objects.all()[:7]
    hot_baike=Consult.objects.filter(type=6,status=1)[:7]
    hot_users=ProxyUserProfile.objects.filter(certifi_status=2)[:12]
    return render_to_response("work_buy_index.html",locals(),context_instance=RequestContext(request))

@buyuser_login_required
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

    return  render_to_response("work_buy_allmsg.html",locals(),context_instance=RequestContext(request))


@buyuser_login_required
def my_ask(request):
    page=request.GET.get("page","1")
    all_ask=Ask.objects.filter(uid=request.myuser.uid).order_by("-ask_time")
    try:
        page=int(page)
        assert page>0
    except:
        page=1

    allinfo_paginator=Paginator(all_ask,10)
    try:
        ask_info=allinfo_paginator.page(page)
    except (EmptyPage,InvalidPage):
        page=1
        ask_info=allinfo_paginator.page(1)

    return  render_to_response("work_buy_myask.html",locals(),context_instance=RequestContext(request))

@buyuser_login_required
def my_dingzhi(request):
    all_dingzhi=DingZhi.objects.filter(uid=request.myuser.uid).order_by("-addtime")
    return  render_to_response("work_buy_mydingzhi.html",locals(),context_instance=RequestContext(request))

@buyuser_login_required
def contact(request):
    error_msg=""
    success_msg=""
    post_info=request.POST


    if request.method=="POST":
        name=post_info.get("name")
        birthday=post_info.get("birthday")
        qq=post_info.get("qq")
        tel=post_info.get("tel")
        sex=post_info.get("sex")
        married=post_info.get("married")
        sex=int(sex)
        married=int(married)
        assert  sex>=0 and  married>=0
        if qq:
            try:
                qq=int(qq.strip())
            except:
                error_msg="qq号必须为纯数字!"
        if not error_msg:
            if tel:
                _=tel.strip().replace("-","")
                try:
                    for _t in _:
                        int(_t)
                except:
                    error_msg="电话号中含有非法字符!"
        if not error_msg:
            if birthday:
                try:
                    datetime.datetime.strptime(birthday,"%Y-%m-%d")
                except:
                    error_msg="出生年月格式非法!"
        if not error_msg:
            request.myuser.real_name=name
            request.myuser.birthday=birthday
            request.myuser.qq=qq
            request.myuser.tel=tel
            request.myuser.sex=sex
            request.myuser.married=married
            request.myuser.save()
            success_msg="基本信息修改成功!"


    return  render_to_response("work_buy_contact.html",locals(),context_instance=RequestContext(request))

@buyuser_login_required
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

    return  render_to_response("work_buy_img.html",locals(),context_instance=RequestContext(request))

@buyuser_login_required
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
            return  render_to_response("work_buy_changepwd.html",locals(),context_instance=RequestContext(request))



    return  render_to_response("work_buy_changepwd.html",locals(),context_instance=RequestContext(request))