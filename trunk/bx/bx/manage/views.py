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
from ..models import Consult,Company,Product,CateType
from itertools import  groupby
import  json


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

@staff_member_required
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


@staff_member_required
def product_all(request):
    "所有产品"
    getinfo=request.GET
    page=getinfo.get("page","1")
    if page:
        page=int(page)
    else:
        page=1
    objs=Product.objects.all()
    allinfo_paginator=Paginator(objs,15)
    allinfo=allinfo_paginator.page(page)

    return render_to_response("manage_product_all.html",locals(),context_instance=RequestContext(request))


@staff_member_required
def product_add(request):
    "新增产品"
    all_company=Company.objects.all()
    all_cate_type=CateType.objects.all()
    error_msg=""
    if request.method=="POST":
        post_info=request.POST
        pro_name=post_info.get("pro_name")
        img=request.FILES.get("img")
        cid=post_info.get("cid")
        type_list=post_info.getlist("type")
        if type_list:
            type_list=[ int(i) for  i in type_list if  i ]
        feature=post_info.get("feature")
        star_age=post_info.get("star_age")
        star_age_type=post_info.get("star_age_type")
        end_age=post_info.get("end_age")
        end_age_type=post_info.get("end_age_type")
        timelimit=post_info.get("timelimit")
        paytype=post_info.get("paytype")
        agelimit=post_info.get("agelimit")
        minprice=post_info.get("minprice")

        a_0,a_1,a_2,a_3,a_4,a_5,a_6,a_7,a_8,a_9=tuple([post_info.get("a_%s"%i)   for i in range(0,10)])
        b_0,b_1,b_2,b_3,b_4,b_5,b_6,b_7,b_8,b_9=tuple([post_info.get("b_%s"%i)   for i in range(0,10)])
        c_0,c_1,c_2,c_3,c_4,c_5,c_6,c_7,c_7,c_9=tuple([post_info.get("c_%s"%i)   for i in range(0,10)])
        _local=locals()
        content=[[_local.get("a_%s"%i),_local.get("b_%s"%i),_local.get("c_%s"%i)] for i in range(10)]
        content=[i for i in content if i[0]]
        content.sort(key=lambda x:x[0])
        content_list=[]
        for i,j in groupby(content,key=lambda x:x[0]):
            _=[]
            for k in j :
                _.append(k[1:])
            if len(_)>0:
                content_list.append([i]+_)

        case=post_info.get("case")
        reason=post_info.get("reason")
        duty=post_info.get("duty")
        if not pro_name:
            error_msg="请输入产品名！"
        if not  img:
            error_msg="请选择产品图片！"
        if not cid:
            error_msg="请选择企业名！"
        else:
            _=Company.objects.get(cid=int(cid))
        if not type_list:
            error_msg="请选择类型！"
        if not feature:
            error_msg="请填写产品特色！"
        if not star_age:
            error_msg="请填写开始年龄！"
        else:
            try:
                star_age=int(star_age)
            except:
                error_msg="开始年龄信息必须为整数"

        if not end_age:
            error_msg="请填写结束年龄！"
            try:
                end_age=int(end_age)
            except:
                error_msg="结束年龄信息必须为整数"
        if not timelimit:
            error_msg="请填写保障年限信息！"
        if not paytype:
            error_msg="请填写缴费方式信息！"
        if not agelimit:
            error_msg="请填写参保年龄信息！"
        if not  minprice:
            minprice="请填写最低价格信息！"
        else:
            try:
                minprice=int(minprice)
            except:
                error_msg="最低价格信息必须为整数！"
        if not error_msg:
            pro_obj=Product(pro_name=pro_name,
                            cid=int(cid),
                            bx_type=",".join([str(i) for i in type_list]) if type_list else "",
                            bx_feature=feature,
                            star_age=star_age if star_age_type=="0" else -star_age,
                            end_age=end_age if end_age_type=="0" else  -end_age,
                            pro_desc_content=json.dumps(content_list),
                            pro_desc_case=case,
                            pro_desc_reason=reason,
                            pro_desc_duty=duty,
                            from_url=str(time.time()),
                            img=img,
                            meta="",
                            min_price=minprice,
                            addtime=int(time.time()),
                            insurance_timelimit=timelimit,
                            insurance_paytype=paytype,
                            insurance_agelimit=agelimit)
            pro_obj.save()
            return  render_to_response("manage_product_add_success.html",locals(),
                                       context_instance=RequestContext(request))


    return  render_to_response("manage_product_add.html",locals(),
                              context_instance=RequestContext(request))


@staff_member_required
def product_detail(request,_id):
    "产品详情"
    all_company=Company.objects.all()
    all_cate_type=CateType.objects.all()
    pid=int(_id)
    pro_obj=Product.objects.get(pid=pid)
    pro_name=pro_obj.pro_name
    cid=pro_obj.cid
    img=pro_obj.img
    type_list=pro_obj.get_type_id_list()
    feature=pro_obj.bx_feature
    star_age=int(pro_obj.star_age);star_age_type="1" if pro_obj.star_age<0 else "0"
    end_age=int(pro_obj.end_age);end_age_type="1" if pro_obj.end_age<0 else "0"
    timelimit=pro_obj.insurance_timelimit
    paytype=pro_obj.insurance_paytype
    agelimit=pro_obj.insurance_agelimit
    minprice=pro_obj.min_price
    a_0,a_1,a_2,a_3,a_4,a_5,a_6,a_7,a_8,a_9=("",)*10
    b_0,b_1,b_2,b_3,b_4,b_5,b_6,b_7,b_8,b_9=("",)*10
    c_0,c_1,c_2,c_3,c_4,c_5,c_6,c_7,c_7,c_9=("",)*10
    _json=pro_obj.get_pro_desc_json()
    _content_list=[]
    for i in _json:
        _=i[0]
        _content_list+=[[_]+ j for j in i[1:] if len(j)==2]
    for i in range(0,10):
        try:
            assert  len(_content_list[i])==3
            _str='''a_%s,b_%s,c_%s=tuple(_content_list[i])'''%(i,i,i)
            exec(_str)
        except Exception as e :
            print e
            pass
    case=pro_obj.pro_desc_case
    reason=pro_obj.pro_desc_reason
    duty=pro_obj.pro_desc_duty
    error_msg=""
    if request.method=="POST":
        post_info=request.POST
        _pro_name=post_info.get("pro_name")
        _img=request.FILES.get("img")
        _cid=post_info.get("cid")
        _type_list=post_info.getlist("type")
        if _type_list:
            _type_list=[ int(i) for  i in _type_list if  i ]
        _feature=post_info.get("feature")
        _star_age=post_info.get("star_age")
        _star_age_type=post_info.get("star_age_type")
        _end_age=post_info.get("end_age")
        _end_age_type=post_info.get("end_age_type")
        _timelimit=post_info.get("timelimit")
        _paytype=post_info.get("paytype")
        _agelimit=post_info.get("agelimit")
        _minprice=post_info.get("minprice")

        _a_0,_a_1,_a_2,_a_3,_a_4,_a_5,_a_6,_a_7,_a_8,_a_9=tuple([post_info.get("a_%s"%i)   for i in range(0,10)])
        _b_0,_b_1,_b_2,_b_3,_b_4,_b_5,_b_6,_b_7,_b_8,_b_9=tuple([post_info.get("b_%s"%i)   for i in range(0,10)])
        _c_0,_c_1,_c_2,_c_3,_c_4,_c_5,_c_6,_c_7,_c_7,_c_9=tuple([post_info.get("c_%s"%i)   for i in range(0,10)])
        _local=locals()
        content=[[_local.get("_a_%s"%i),_local.get("_b_%s"%i),_local.get("_c_%s"%i)] for i in range(10)]
        content=[i for i in content if i[0]]
        content.sort(key=lambda x:x[0])
        content_list=[]
        for i,j in groupby(content,key=lambda x:x[0]):
            _=[]
            for k in j :
                _.append(k[1:])
            if len(_)>0:
                content_list.append([i]+_)

        _case=post_info.get("case")
        _reason=post_info.get("reason")
        _duty=post_info.get("duty")
        if not _pro_name:
            error_msg="请输入产品名！"
        if not  _img and not img :
            error_msg="请选择产品图片！"
        if not _cid:
            error_msg="请选择企业名！"
        else:
            _=Company.objects.get(cid=int(cid))
        if not _type_list:
            error_msg="请选择类型！"
        if not _feature:
            error_msg="请填写产品特色！"
        if not _star_age:
            error_msg="请填写开始年龄！"
        else:
            try:
                _star_age=int(_star_age)
            except:
                error_msg="开始年龄信息必须为整数"

        if not _end_age:
            error_msg="请填写结束年龄！"
            try:
                _end_age=int(_end_age)
            except:
                error_msg="结束年龄信息必须为整数"
        if not _timelimit:
            error_msg="请填写保障年限信息！"
        if not _paytype:
            error_msg="请填写缴费方式信息！"
        if not _agelimit:
            error_msg="请填写参保年龄信息！"
        if not  _minprice:
            error_msg="请填写最低价格信息！"
        else:
            try:
                _minprice=int(_minprice)
            except:
                error_msg="最低价格信息必须为整数！"
        if not error_msg:
            _t=",".join([str(i) for i in _type_list]) if _type_list else ""
            _star_age=_star_age if _star_age_type=="0" else -_star_age
            pro_obj.pro_name=_pro_name
            pro_obj.cid=int(_cid)
            pro_obj.bx_type=_t
            pro_obj.bx_feature=_feature
            pro_obj.star_age=_star_age
            pro_obj.end_age=_end_age if _end_age_type=="0" else  -_end_age
            pro_obj.pro_desc_content=json.dumps(_content_list)
            pro_obj.pro_desc_case=_case
            pro_obj.pro_desc_reason=_reason
            pro_obj.pro_desc_duty=_duty
            pro_obj.from_url=str(time.time())
            pro_obj.img=_img or img
            pro_obj.meta=""
            pro_obj.min_price=_minprice
            pro_obj.insurance_timelimit=_timelimit
            pro_obj.insurance_paytype=_paytype
            pro_obj.insurance_agelimit=_agelimit
            pro_obj.save()
            return  render_to_response("manage_product_detail_success.html",locals(),
                                       context_instance=RequestContext(request))


    return  render_to_response("manage_product_detail.html",locals(),
                              context_instance=RequestContext(request))

def product_delete(request,_id):
    pro_obj=Product.objects.get(pid=int(_id))
    return render_to_response("manage_product_delete.html",locals(),context_instance=RequestContext(request))

def product_delete_do(request):
    pid=request.GET.get("pid")
    pid=int(pid)
    error_msg=""
    try:
        pro_obj=Product.objects.get(pid=pid)
        pro_name=pro_obj.pro_name
    except Product.DoesNotExist:
        error_msg="产品不存在!"
    else:
        pro_obj.delete()
    return  render_to_response("manage_product_delete_success.html",locals(),context_instance=RequestContext(request)
                               )

@staff_member_required
def company_all(request):
    "所有企业"
    getinfo=request.GET
    page=getinfo.get("page","1")
    if page:
        page=int(page)
    else:
        page=1
    objs=Company.objects.all().order_by("-cid")
    allinfo_paginator=Paginator(objs,15)
    allinfo=allinfo_paginator.page(page)
    return render_to_response("manage_company_all.html",locals(),context_instance=RequestContext(request))


@staff_member_required
def company_add(request):
    "新增企业"
    error_msg=""
    post_info=request.POST
    if request.method=="POST":
        comname=post_info.get("comname")
        img=request.FILES.get("img")
        shortname=post_info.get("shortname")
        product_weight=post_info.get("product_weight")
        dailiren_weight=post_info.get("dailiren_weight")
        content=post_info.get("content")
        if not comname:
            error_msg="企业名不能为空！"
        if not  img:
            error_msg="企业主图不能为空！"
        if not shortname:
            error_msg="企业缩写不能为空！"
        if not product_weight:
            error_msg="产品权重不能为空"
        else:
            try:
                product_weight=int(product_weight)
            except:
                error_msg="产品权重必须为整数"
        if not  dailiren_weight:
            error_msg="代理人权重不能为空"
        else:
            try:
                dailiren_weight=int(dailiren_weight)
            except:
                error_msg="代理人权重必须为整数"
        if not content:
            content=""
        if not error_msg:
            company=Company(comname=comname,img=img,shortname=shortname,dailiren_weight=dailiren_weight,
                            product_weight=product_weight,content=content)
            company.save()
            com_obj=company
            return  render_to_response("manage_company_add_success.html",locals(),
                                       context_instance=RequestContext(request))


    return render_to_response("manage_company_add.html",locals(),context_instance=RequestContext(request))


@staff_member_required
def company_detail(request,_id):
    "企业详情"

    cid=int(_id)
    com_obj=Company.objects.get(cid=cid)
    comname=com_obj.comname
    img=com_obj.img
    shortname=com_obj.shortname
    product_weight=com_obj.product_weight
    dailiren_weight=com_obj.dailiren_weight
    content=com_obj.content
    post_info=request.POST
    error_msg=""
    if request.method=="POST":
        _comname=post_info.get("comname")
        _img=request.FILES.get("img")
        _shortname=post_info.get("shortname")
        _product_weight=post_info.get("product_weight")
        _dailiren_weight=post_info.get("dailiren_weight")
        _content=post_info.get("content")
        if not _comname:
            error_msg="企业名不能为空！"
        if not  _img:
            _img=img
        if not _shortname:
            error_msg="企业缩写不能为空！"
        if not _product_weight:
            error_msg="产品权重不能为空"
        else:
            try:
                _product_weight=int(_product_weight)
            except:
                error_msg="产品权重必须为整数"
        if not  _dailiren_weight:
            error_msg="代理人权重不能为空"
        else:
            try:
                _dailiren_weight=int(_dailiren_weight)
            except:
                error_msg="代理人权重必须为整数"
        if not _content:
            _content=""
        if not error_msg:
            com_obj.comname=_comname
            com_obj.img=_img
            com_obj.shortname=_shortname
            com_obj.product_weight=_product_weight
            com_obj.dailiren_weight=_dailiren_weight
            com_obj.content=_content
            com_obj.save()
            return render_to_response("manage_company_detail_success.html",locals(),
                                      context_instance=RequestContext(request))


    return render_to_response("manage_company_detail.html",locals(),context_instance=RequestContext(request))


def company_delete(request):
    pass


def company_delete_do(request):
    pass