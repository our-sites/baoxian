#coding:utf-8
__author__ = 'admin'
# --------------------------------
# Created by admin  on 2016/10/18.
# ---------------------------------
from django.http import  HttpResponse
from django.shortcuts import  render_to_response
from ..models import *
from django.template.context import  RequestContext

def index(request):
    info=Consult.objects.all().order_by("-addtime")[:300]

    return  render_to_response("zixun_index.html",locals(),context_instance=RequestContext(request))


def detail(request,zid):
    info=Consult.objects.get(zid=int(zid))
    return  render_to_response("zixun_detail.html",locals(),context_instance=RequestContext(request))