#coding:utf-8
__author__ = 'admin'
# --------------------------------
# Created by admin  on 2016/10/18.
# ---------------------------------
from django.shortcuts import  render_to_response
from django.template.context import  RequestContext
from ..models import  Ask,Answer,Product
from django.core.paginator import Paginator,InvalidPage
from django.http import  HttpResponseRedirect,HttpResponse
import  re
from django.db.models import  Q
import  json
import  datetime
from bx.utils.template import get_template_string
from ..myauth.models import MyUser
from django.views.decorators.csrf import csrf_exempt
import  sys
from ..utils.seo import postBaiDu
from bx.decorators import  mobile_browser_adaptor_by_host
import bx.settings as settings
import  traceback
reload(sys)
sys.setdefaultencoding("utf-8")

@mobile_browser_adaptor_by_host(settings.M_HOST_FUN,{"ask.html":"m_ask.html"})
def home(request):
    now_date=datetime.datetime.now().strftime("%Y-%m-%d")
    page=1
    try:
        page=re.match(r"^/ask/(\d+)/",request.path).groups()[0]
        page=int(page)
    except:
        pass

    if request.method=="POST":
        page=1
        content=request.POST.get("content")
        _next=request.POST.get("next")
        if not content:
            data={"errorCode":500,"formError":{"fields":[{'name':"content","msg":"问题内容不能为空!","content":"问题内容不能为空!"}]}}
        if  not request.myuser :
            data={"errorCode":800,"data":{"html":get_template_string(request,"buy_login_pop.html",{"next":_next})}}
        else:
            _=Ask(ask_content=content,uid=request.myuser.uid,province=request.province_id,
                city=request.city_id)
            _.save()
            try:
                del request.session["last_ask_info"]
            except:
                pass
            data={"errorCode":0,"msg":"问题已提交！","formSuccess":{"redirect":"/ask/" ,
                                                                 "duration":1000},"data":{}}

            request.send_allsite_msg('''来自%s%s 的用户提交了一条新的提问"%s" '''%( request.province,request.city,content),"/ask/detail/%s.html"%_.askid)
        data=json.dumps(data)
        return  HttpResponse(data,mimetype="application/javascript")
    ask_all=Ask.objects.filter(state=0).order_by("-ask_time")
    ask_no_reply_all=Ask.objects.filter(state=0,ans_num=0).order_by("-ask_time")[:5]
    ask_has_reply_all=Ask.objects.filter(state=0,ans_num__gt=0).order_by("-ask_time")[:5]
    ask_paginator=Paginator(ask_all,5)
    try:
        allinfo=ask_paginator.page(page)
    except InvalidPage:
        allinfo=ask_paginator.page(1)
    #ask_paginator.num_pages
    last_ask_info=request.session.get("last_ask_info","")
    return  render_to_response("ask.html",locals(),context_instance=RequestContext(request))


@mobile_browser_adaptor_by_host(settings.M_HOST_FUN,{"ask_detail.html":"m_ask_detail.html"})
def detail(request,ask_id):
    now_date=datetime.datetime.now().strftime("%Y-%m-%d")
    page=1
    ask_id=int(ask_id)
    get_info=request.GET
    try:
        page=re.match(r"^/ask/detail/\d+.html/(\d+)/",request.path).groups()[0]
        page=int(page)
    except:
        pass

    if get_info.has_key("ansid")  and get_info.has_key("good"):
        ansid=get_info.get("ansid")
        ansid=int(ansid)
        _ans=Answer.objects.get(ansid=ansid)
        _ans.good_num+=1
        _ans.save()
        _ans_user=_ans.get_user()
        _ans_user.good_num+=1
        _ans_user.save()
        return HttpResponse(json.dumps({"status":True,"message":_ans.good_num}),mimetype="application/javascript")

    if request.method=="POST":
        content=request.POST.get("content")
        _next = request.POST.get("next")
        if not content:
            data={"errorCode":500,"formError":{"fields":[{"name":"content","msg":"内容不能为空!","content":"内容不能为空!"}]}}

        if  not request.myuser:
            data = {"errorCode": 800, "data": {"html": get_template_string(request,"proxy_login_pop.html", {"next": _next})}}
        else:
            ask_obj=Ask.objects.get(askid=int(ask_id),state=0)
            ans_obj=ask_obj.add_answer(request.myuser,content=content)

            try:
                del request.session["last_answer_info"]
            except:
                pass
            request.send_allsite_msg(u'''来自%s%s 的用户提交了一条新的回答"%s" ''' %(request.province,request.city,content), "/ask/detail/%s.html"%ask_id)
            data={"errorCode":0,"msg":"回答已提交！","formSuccess":{"redirect":"/ask/detail/%s.html?end=1"%ask_id ,
                                                                 "duration":1000},"data":{}}
        data=json.dumps(data)
        return  HttpResponse(data,mimetype="application/javascript")
    ask_obj=Ask.objects.get(askid=int(ask_id),state=0)
    answer_all=Answer.objects.filter(askid=int(ask_id)).order_by("ans_time")
    answer_paginator=Paginator(answer_all,10)
    if not  request.GET.get("end"):
        pass
    else:
        page=answer_paginator.num_pages
    try:
        allinfo=answer_paginator.page(page)
    except InvalidPage:
        allinfo=answer_paginator.page(1)
    other_info=Ask.objects.filter(Q(askid__lt=ask_id)).order_by("-askid")[:3]
    if len(other_info)<3:
        other_info=Ask.objects.filter(Q(askid__gt=ask_id)).order_by("askid")[:3]

    other_proinfo=Product.objects.all()[:4]
    last_answer_info=request.session.get("last_answer_info","")
    return  render_to_response("ask_detail.html",locals(),context_instance=RequestContext(request))


@csrf_exempt
def auto_add_ask(request):
    get_info=request.GET
    post_info=request.POST
    try:
        secret=post_info.get("secret")
        assert  secret=="gc7232275"
        uid=post_info.get("uid")
        content=post_info.get("content")
        uid=int(uid)
        user=MyUser.objects.get(uid=uid)
        assert user.state==1
        _ = Ask(ask_content=content, uid= uid, province=user.province_id,
                city=user.city_id)
        _.save()
        area_info=user.get_province_city_info()
        if area_info:
            request.send_allsite_msg('''来自%s 的用户提交了一条新的提问"%s" ''' % (area_info, content),
                                 "/ask/detail/%s.html" % _.askid)
        ask_id=_.askid
        try:
            postBaiDu("https://www.bao361.cn/ask/detail/%s.html"%_.askid)
        except:
            pass
        data={"status":True,"message":"success","askid":ask_id}
    except Exception as e :
        data={"status":False,"message":str(e)}
        traceback.print_exc()
    print data

    return  HttpResponse(json.dumps(data),mimetype="application/javascript")



@csrf_exempt
def auto_add_answer(request):
    get_info=request.GET
    post_info=request.POST
    try:
        secret=post_info.get("secret")
        assert  secret=="gc7232275"
        uid=post_info.get("uid")
        askid=post_info.get("askid")
        ask_id=int(askid)
        content=post_info.get("content")
        uid=int(uid)
        user=MyUser.objects.get(uid=uid)
        ask_obj=Ask.objects.get(askid=ask_id)
        assert user.state==1
        ans_obj = ask_obj.add_answer(user, content=content)
        area_info=user.get_province_city_info()
        if area_info:
            request.send_allsite_msg('''来自%s 的用户提交了一条新的回答"%s" ''' % (area_info, content),
                                 "/ask/detail/%s.html" % ask_obj.askid)
        ans_id=ans_obj.ansid
        try:
            postBaiDu("https://www.bao361.cn/ask/detail/%s.html"%ask_obj.askid)
        except:
            pass
        data={"status":True,"message":"success","ansid":ans_id}
    except Exception as e :
        data={"status":False,"message":str(e)}
        traceback.print_exc()
    return  HttpResponse(json.dumps(data),mimetype="application/javascript")