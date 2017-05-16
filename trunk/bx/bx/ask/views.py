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
import  sys
reload(sys)
sys.setdefaultencoding("utf-8")

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



def detail(request,ask_id):
    now_date=datetime.datetime.now().strftime("%Y-%m-%d")
    page=1
    ask_id=int(ask_id)
    try:
        page=re.match(r"^/ask/detail/\d+.html/(\d+)/",request.path).groups()[0]
        page=int(page)
    except:
        pass

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