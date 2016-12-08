#coding:utf-8
__author__ = 'admin'
# --------------------------------
# Created by admin  on 2016/10/18.
# ---------------------------------
from django.shortcuts import  render_to_response
from django.template.context import  RequestContext
from ..models import  Ask,Answer,Product
from django.core.paginator import Paginator,InvalidPage
from django.http import  HttpResponseRedirect
import  re
from django.db.models import  Q
from ..myauth.models import ProxyUserProfile

def home(request):
    page=1
    try:
        page=re.match(r"^/ask/(\d+)/",request.path).groups()[0]
        page=int(page)
    except:
        pass

    if request.method=="POST":
        page=1
        content=request.POST.get("content")
        assert  content
        if request.myuser and request.myuser.usertype==1:
            _=Ask(ask_content=content,uid=request.myuser.uid,province=request.province_id,
                city=request.city_id)
            _.save()
            try:
                del request.session["last_ask_info"]
            except:
                pass
        else:
            request.session["last_ask_info"]=content
            return  HttpResponseRedirect("/register/?next=/ask/")

    ask_all=Ask.objects.all().order_by("-ask_time")
    ask_paginator=Paginator(ask_all,5)
    try:
        allinfo=ask_paginator.page(page)
    except InvalidPage:
        allinfo=ask_paginator.page(1)
    #ask_paginator.num_pages
    last_ask_info=request.session.get("last_ask_info","")
    return  render_to_response("ask.html",locals(),context_instance=RequestContext(request))



def detail(request,ask_id):
    page=1
    ask_id=int(ask_id)
    try:
        page=re.match(r"^/ask/detail/\d+.html/(\d+)/",request.path).groups()[0]
        page=int(page)
    except:
        pass

    if request.method=="POST":
        page=1
        content=request.POST.get("content")
        assert  content
        if request.myuser and request.myuser.usertype==2:
            _=Answer(askid=int(ask_id),ans_content=content,uid=request.myuser.uid,parent_ansid=0)
            _.save()
            profile=request.myuser.get_profile()
            # if not  profile:
            #     profile=ProxyUserProfile(uid=request.myuser,ans_num=1)
            #     profile.save()
            if profile:
                profile.ans_num+=1
                profile.save()
            try:
                del request.session["last_answer_info"]
            except:
                pass
        else:
            request.session["last_answer_info"]=content
            return  HttpResponseRedirect("/register/?next=/ask/detail/%s.html&role=proxy"%ask_id)

    ask_obj=Ask.objects.get(askid=int(ask_id))
    answer_all=Answer.objects.filter(askid=int(ask_id)).order_by("ans_time")
    answer_paginator=Paginator(answer_all,5)
    try:
        allinfo=answer_paginator.page(page)
    except InvalidPage:
        allinfo=answer_paginator.page(1)
    other_info=Ask.objects.filter(Q(askid__gt=ask_id)|Q(askid__lt=ask_id))[:3]
    other_proinfo=Product.objects.all()[:4]
    last_answer_info=request.session.get("last_answer_info","")
    return  render_to_response("ask_detail.html",locals(),context_instance=RequestContext(request))