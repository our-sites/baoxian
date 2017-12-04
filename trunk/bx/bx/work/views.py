#coding:utf-8
from django.http import  HttpResponse
from django.shortcuts import  render_to_response
from django.template.context import  RequestContext
from ..myauth.models import *
from ..myauth.decorators import login_required
from django.core.paginator import Paginator,EmptyPage,InvalidPage
from ..models import Ask,Answer,DingZhi,Consult,Product,Share,Add,AddDegree,AddMoney,AddPosition
from django.core.files.uploadedfile import InMemoryUploadedFile
from PIL import  Image
import  StringIO
from django.http import  HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.conf import  settings
import  os
from  threadspider.utils.encrypt import  md5
from ..utils.sms import send_dayysms_validnumber
import random

@login_required
def index(request):
    hot_anli=Consult.objects.filter(type=2,status=1)[:5]
    hot_pro=Product.objects.all()[:5]
    hot_baike=Consult.objects.filter(type=6,status=1)[:7]
    hot_users=MyUser.objects.filter(is_proxy=1,proxy_cid__gt=0)[:12]
    return render_to_response("work_index.html",locals(),context_instance=RequestContext(request))

@login_required
def phonevalid(request):
    go=request.GET.get("go")
    session=request.session
    post_info=request.POST
    if request.GET.get("remote_valid"):
        phone=request.GET.get("phone")
        try:
            MyUser.objects.get(phone=phone)
        except MyUser.DoesNotExist:
            return HttpResponse("true")
        else:
            return HttpResponse("false")
    if go:
        phone=go
        numer="".join(random.sample(["1","2","3","4","5","6","7","8","9"],6))
        result=send_dayysms_validnumber(phone,numer)
        session["work_phone_valid"]=numer
        return HttpResponse("true")
    if request.GET.get("code_valid"):
        code=request.GET.get("code")
        try:
            _numer=session.get("work_phone_valid")
            assert code==_numer

        except:
            return HttpResponse("false")
        else:
            return HttpResponse("true")
    if request.method=="POST":
        phone=post_info.get("phone")
        code=post_info.get("code")
        _numer=session.get("work_phone_valid")
        assert  code==_numer
        session.delete("work_phone_valid")
        request.myuser.phone=phone
        request.myuser.vphone=1
        request.myuser.save()
        return HttpResponseRedirect("/work/phonevalid/?have_post=1")

    return  render_to_response("work_phonevalid.html",locals(),
                               context_instance=RequestContext(request))


@login_required
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

    return  render_to_response("work_allmsg.html",locals(),context_instance=RequestContext(request))


@login_required
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

    return  render_to_response("work_myask.html",locals(),context_instance=RequestContext(request))

@login_required
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

    return  render_to_response("work_myans.html",locals(),context_instance=RequestContext(request))


@login_required
def startproxy(request):
    go=request.GET.get("go")
    if not go:
        return render_to_response("work_startproxy.html",locals(),context_instance=RequestContext(request))
    else:
        request.myuser.is_proxy=1
        request.myuser.save()
        return HttpResponseRedirect("/work/proxy/myinfo/")


@login_required
def proxy_myinfo(request):
    if request.myuser.is_proxy!=1:
        return HttpResponseRedirect("/work/startproxy/")
    success_msg=""
    error_msg=""
    com_info=Company.objects.all().order_by("-product_weight")
    get_info=request.GET
    post_info=request.POST
    if request.method=="POST":
        name=post_info.get("name")
        sex=post_info.get("sex")
        cid=post_info.get("cid")
        work_year=post_info.get("workyear")
        position=post_info.get("position")
        qq=post_info.get("qq")
        weixin=post_info.get("weixin")
        #phone=post_info.get("phone")
        certifi_num=post_info.get("certifi_num")
        practice_num=post_info.get("practice_num")
        my_ad=post_info.get("my_ad")
        sex=int(sex)
        assert  sex>=0
        cid=int(cid)
        if cid:
            _=Company.objects.get(cid=cid)
        request.myuser.sex=sex
        request.myuser.proxy_cid=cid
        work_year=int(work_year)
        request.myuser.proxy_workyear=work_year
        if qq:
            try:
                qq=int(qq.strip())
                request.myuser.qq=qq
            except:
                error_msg="qq号必须为纯数字!"
        if not error_msg:
            if weixin:
                if len(weixin)>50:
                    error_msg="微信号长度过长！"
                else:
                    request.myuser.weixin=weixin
        # if not error_msg:
        #     if phone and request.myuser.is_3login:
        #         try:
        #             phone=int(phone.strip())
        #         except:
        #             error_msg="手机号中含有非法字符!"
        #         else:
        #             try:
        #                 assert len(str(phone))==11
        #             except:
        #                 error_msg="手机号长度不正确！"
        #             else:
        #                 if len(MyUser.objects.filter(is_3login=0,phone=phone))>0:
        #                     error_msg="该手机号已被占用！"
        #                 else:
        #                     request.myuser.phone=phone
        position=unicode(position)
        request.myuser.proxy_position=position

        if   certifi_num:
            if len(certifi_num)!=20:
                error_msg="资格证编号长度不合法！长度必须为20！"
            else:
                request.myuser.proxy_certifinum=certifi_num

        if practice_num:
            if len(practice_num)>26:
                error_msg="执业证编号长度过长！长度一般不超过26！"
            else:
                request.myuser.proxy_practicenum=practice_num
        request.myuser.proxy_myad=my_ad
        request.myuser.save()
        if not error_msg:
            success_msg="Success！信息更新成功。"
    return  render_to_response("work_proxy_myinfo.html",locals(),context_instance=RequestContext(request))


@login_required
def proxy_myshare(request):

    if request.myuser.is_proxy!=1:
        return  HttpResponseRedirect("/work/startproxy/")

    error_msg=""
    success_msg=""
    sid=request.GET.get("sid")
    com_info=Company.objects.all().order_by("-product_weight")
    title,cid,pro_name,price,content='',0,'',0,''
    if sid:
        sid=int(sid)
        s_obj=Share.objects.get(sid=sid,uid=request.myuser.uid)
        title,cid,pro_name,price,content=s_obj.title,s_obj.cid,s_obj.other_proname,s_obj.price,s_obj.content

    if request.method=="POST"  :
        title=request.POST.get("title")
        cid=request.POST.get("cid")
        cid=int(cid)
        pro_name=request.POST.get("pro_name")
        price=request.POST.get("price")
        content=request.POST.get("content")
        if len(title)==0:
            error_msg="分享标题不能为空！"
        if not error_msg:
            if len(pro_name)==0:
                error_msg="保险产品名不能为空！"
        if not error_msg:
            try:
                price=int(price)
            except:
                error_msg="保费必须为整数！"
        if not error_msg:
            if len(content)==0:
                error_msg="分享详情不能为空！"
        if not error_msg:
            if not sid:
                if  Share.objects.filter(uid=request.myuser.uid).count()>=100:
                    error_msg="您的签单分享数目已达上限100条！不可再添加！"
                else:
                    _=Share(title=title,cid=cid,other_proname=pro_name,price=price,content=content,uid=request.myuser.uid)
                    _.save()
                    success_msg="签单分享提交成功！"
            else:
                s_obj.title=title
                s_obj.cid=cid
                s_obj.other_proname=pro_name
                s_obj.price=price
                s_obj.content=content
                s_obj.uptime=int(time.time())
                s_obj.save()
                success_msg="签单分享修改成功！"
    if (not request.GET.get("add")) or success_msg:

        my_shares=Share.objects.filter(uid=request.myuser.uid).order_by("-uptime")
        page=request.GET.get("page","1")
        page=int(page)
        allinfo_paginator=Paginator(my_shares,10)
        try:
            allinfo=allinfo_paginator.page(page)
        except (EmptyPage,InvalidPage):
            page=1
            allinfo=allinfo_paginator.page(page)
        cid_s=[ i.cid for  i in allinfo]
        cid_s_info=Company.objects.filter(cid__in=cid_s).values("cid","comname")
        cid_s_info=dict([(i["cid"],i["comname"]) for i in cid_s_info])
        for i in allinfo:
            i.comname=cid_s_info[i.cid]

    return  render_to_response("work_proxy_myshare.html",locals(),context_instance=RequestContext(request))


@login_required
def proxy_myadd(request):
    if request.myuser.is_proxy!=1:
        return  HttpResponseRedirect("/work/startproxy/")
    error_msg=""
    success_msg=''
    aid=request.GET.get("aid")
    get_info=request.GET
    post_info=request.POST
    com_info=Company.objects.all().order_by("-product_weight")
    add_degree_info=AddDegree.objects.all()
    add_money_info=AddMoney.objects.all()
    add_position_info=AddPosition.objects.all()

    apid,amid,adid,cid,work_year,num,need_content,work_content,phone,address,title=\
       0,   0,   0,  0,        0,  1,          '',          '',   '',request.province+request.city,''

    phone=request.myuser.phone

    if aid :
        aid=int(aid)
        a_obj=Add.objects.get(aid=aid,uid=request.myuser.uid)
        apid,amid,adid,cid,work_year,num,need_content,work_content,phone,address,title=\
        a_obj.apid,   a_obj.amid,   a_obj.adid,  a_obj.cid,a_obj.work_year,  a_obj.num, a_obj.need_content,\
        a_obj.work_content,   a_obj.phone,a_obj.address,a_obj.title

    if request.method=="POST"  :
        title=request.POST.get("title")
        apid=post_info.get("apid")
        apid=int(apid)
        amid=int(post_info.get("amid"))
        adid=int(post_info.get("adid"))
        cid=request.POST.get("cid")
        cid=int(cid)
        work_year=int(post_info.get("work_year"))
        num=post_info.get("num")
        need_content=post_info.get("need_content")
        work_content=post_info.get("work_content")
        phone=post_info.get("phone")
        address=post_info.get("address") or (request.province+request.city)

        title=request.POST.get("title")
        if len(title)==0:
            error_msg="职位标题不能为空！"

        if not error_msg:
            try:
                num=int(num)
            except:
                error_msg="保费必须为整数！"
        if not error_msg:
            if len(need_content)==0:
                error_msg="职位要求不能为空！"
        # if not error_msg:
        #     if len(work_content)==0:
        #         error_msg="职位描述不能为空！"

        if not phone:
            if len(phone)==0:
                error_msg="联系方式不能为空!"
        if not address:
            error_msg="工作地址不能为空!"



        if not error_msg:
            if not aid:
                if Add.objects.filter(uid=request.myuser.uid).count()>=100:
                    error_msg="您的提交数目已达上限100条！不可再添加！"
                else:
                    _=\
                    Add(uid=request.myuser.uid,apid=apid,amid=amid,adid=adid,cid=cid,
                        work_year=work_year,num=num,need_content=need_content,
                        work_content=work_content,phone=phone,address=address,
                        title=title)
                    _.save()
                    success_msg="提交成功！"
            else:
                a_obj.title=title
                a_obj.apid=apid;a_obj.amid=amid;a_obj.adid=adid;a_obj.cid=cid
                a_obj.work_year=work_year;a_obj.num=num
                a_obj.need_content=need_content
                a_obj.work_content=work_content
                a_obj.phone=phone
                a_obj.address=address
                a_obj.uptime=int(time.time())
                a_obj.save()
                success_msg="修改成功！"
    if (not request.GET.get("add")) or success_msg:

        my_adds=Add.objects.filter(uid=request.myuser.uid).order_by("-uptime")
        page=request.GET.get("page","1")
        page=int(page)
        allinfo_paginator=Paginator(my_adds,10)
        try:
            allinfo=allinfo_paginator.page(page)
        except (EmptyPage,InvalidPage):
            page=1
            allinfo=allinfo_paginator.page(page)
        cid_s=[ i.cid for  i in allinfo]
        cid_s_info=Company.objects.filter(cid__in=cid_s).values("cid","comname")
        cid_s_info=dict([(i["cid"],i["comname"]) for i in cid_s_info])
        for i in allinfo:
            i.comname=cid_s_info[i.cid]

        amid_s=[i.amid  for i in allinfo]
        amid_s_info=dict([(i.amid,i.info  )   for i in add_money_info])
        for i in allinfo:
            i.amidinfo=amid_s_info[i.amid]


    return  render_to_response("work_proxy_myadd.html",locals(),context_instance=RequestContext(request))

@csrf_exempt
@login_required
def simple_upload(request):
    assert  request.method=="POST"
    _file=request.FILES["upload"]
    _file_content=_file.read()
    _fil_name=_file.name
    finger=md5(_file_content)
    filename=finger+"."+str(_fil_name.split(".")[-1])
    _flag=int(finger,16)
    try:
        os.mkdir(os.path.join(settings.MEDIA_ROOT,"img",str(_flag%100)))
    except:
        pass
    path=os.path.join(settings.MEDIA_ROOT,"img",str(_flag%100),filename)
    real_path="/media/img/%s/%s"%(str(_flag%100),filename)
    _u=open(path,"wb")
    _u.write(_file_content)
    _u.flush()
    _u.close()
    return  render_to_response("work_simple_upload.html",locals(),context_instance=RequestContext(request))






@login_required
def contact(request):
    error_msg=""
    success_msg=""
    post_info=request.POST


    if request.method=="POST":
        name=post_info.get("name")
        birthday=post_info.get("birthday")
        qq=post_info.get("qq")
        #phone=post_info.get("phone")
        sex=post_info.get("sex")
        province_id=post_info.get("province_id")
        city_id=post_info.get("city_id")
        if province_id:
            province_id=int(province_id)
        if city_id:
            city_id=int(city_id)
        weixin=post_info.get("weixin")
        sex=int(sex)

        assert  sex>=0
        if qq:
            try:
                qq=int(qq.strip())
            except:
                error_msg="qq号必须为纯数字!"
        if not error_msg:
            if weixin:
                if len(weixin)>50:
                    error_msg="微信号长度过长！"
        # if not error_msg:
        #     if phone and request.myuser.is_3login:
        #
        #         try:
        #             phone=int(phone.strip())
        #         except:
        #             error_msg="手机号中含有非法字符!"
        #         else:
        #             try:
        #                 assert len(str(phone))==11
        #             except:
        #                 error_msg="手机号长度不正确！"
        #             else:
        #                 if len(MyUser.objects.filter(is_3login=0,phone=phone))>0:
        #                     error_msg="该手机号已被占用！"
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
            # if  request.myuser.is_3login:
            #     request.myuser.phone=phone
            request.myuser.sex=sex

            request.myuser.weixin=weixin
            if province_id:
                request.myuser.province_id=province_id
            if province_id and  city_id:
                request.myuser.city_id=city_id
            request.myuser.save()
            success_msg="基本信息修改成功!"


    return  render_to_response("work_contact.html",locals(),context_instance=RequestContext(request))

@login_required
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
            request.myuser.imgurl=img_file
            request.myuser.save()
            success_msg="头像修改成功"

    return  render_to_response("work_img.html",locals(),context_instance=RequestContext(request))

@login_required
def change_pwd(request):
    success_msg=''
    get_info=request.GET
    go=get_info.get("go")
    session=request.session
    post_info=request.POST
    if go:
        phone=request.myuser.phone
        numer="".join(random.sample(["1","2","3","4","5","6","7","8","9"],6))
        result=send_dayysms_validnumber(phone,numer)
        session["work_phone_valid"]=numer
        return HttpResponse("true")

    if request.GET.get("code_valid"):
        code=request.GET.get("code")
        try:
            _numer=session.get("work_phone_valid")
            assert code==_numer
        except:
            return HttpResponse("false")
        else:
            return HttpResponse("true")
    if request.method=="POST":
        code=post_info.get("code")
        pwd=post_info.get("pwd")
        pwd_again=post_info.get("pwd_again")
        _numer=session.get("work_phone_valid")
        assert  code==_numer
        session.delete("work_phone_valid")
        assert pwd==pwd_again
        request.myuser.reset_password(pwd)
        success_msg="Success! 您的密码已成功重置，请妥善保管！"

        return render_to_response("work_changepwd.html",locals(),context_instance=RequestContext(request))



    return  render_to_response("work_changepwd.html",locals(),context_instance=RequestContext(request))

@login_required
def my_advice(request):
    from ..models import Advice
    my_advice=Advice.objects.filter(touid=request.myuser.uid).order_by("-addtime")
    return  render_to_response("work_myadvice.html",locals(),context_instance=RequestContext(request))



@login_required
def invite(request):
    my_invite=UserInvite.objects.filter(parentuid=request.myuser.uid)
    my_invite_url=UserInvite.get_user_invite_url(request.myuser)
    return render_to_response("work_invite.html",locals(),context_instance=RequestContext(request))