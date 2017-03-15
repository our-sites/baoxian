#coding:utf-8
__author__ = 'admin'
# --------------------------------
# Created by admin  on 2016/10/18.
# ---------------------------------
from django.http import  HttpResponse
from django.shortcuts import  render_to_response
from ..models import *
from django.template.context import  RequestContext
from django.core.paginator import  Paginator,InvalidPage,EmptyPage

def index(request):
    baike_info=Consult.objects.filter(type=1,status=1).order_by("-addtime")[:6]
    anli_info=Consult.objects.filter(type=2,status=1).order_by("-addtime")[:6]
    guahua_info=Consult.objects.filter(type=3,status=1).order_by("-addtime")[:6]
    xinwen_info=Consult.objects.filter(type=4,status=1).order_by("-addtime")[:6]
    dongtai_info=Consult.objects.filter(type=5,status=1).order_by("-addtime")[:6]
    citiao_info=Consult.objects.filter(type=6,status=1).order_by("-addtime")[:6]
    return  render_to_response("zixun_index.html",locals(),context_instance=RequestContext(request))

def index_index(request,name):
    try:
        page=re.search(r"/(\d+)/",request.path).groups()[0]
        page=int(page)
    except:
        page=1
    config={"baike":"保险百科","anli":"保险案例","dongtai":"监管动态","guahua":"保险规划","citiao":"保险词条",
            "xinwen":'保险新闻'}
    name_ch=config[name]
    baike_info=Consult.objects.filter(type=1,status=1).order_by("-addtime")
    anli_info=Consult.objects.filter(type=2,status=1).order_by("-addtime")
    guahua_info=Consult.objects.filter(type=3,status=1).order_by("-addtime")
    xinwen_info=Consult.objects.filter(type=4,status=1).order_by("-addtime")
    dongtai_info=Consult.objects.filter(type=5,status=1).order_by("-addtime")
    citiao_info=Consult.objects.filter(type=6,status=1).order_by("-addtime")
    info=locals()[name+"_info"]
    assert  name in config
    allinfo_paginator=Paginator(info,10)
    try:
        allinfo=allinfo_paginator.page(page)
    except (EmptyPage,InvalidPage):
        page=1
        allinfo=allinfo_paginator.page(1)

    return  render_to_response("zixun_index_index.html",locals(),context_instance=RequestContext(request))


def detail(request,zid):
    info=Consult.objects.get(zid=int(zid))
    try:
        next_id=Consult.objects.filter(zid__gt=zid,status=1).order_by("zid")[0].zid
    except:
        next_id=0
    try:
        last_id=Consult.objects.filter(zid__lt=zid,status=1).order_by("-zid")[0].zid
    except:
        last_id=0
    _infos=Consult.objects.filter(type=info.type,status=1).order_by("-addtime")[:16]
    hot_infos=_infos[:8]
    relate_infos=_infos[8:]
    return  render_to_response("zixun_detail.html",locals(),context_instance=RequestContext(request))