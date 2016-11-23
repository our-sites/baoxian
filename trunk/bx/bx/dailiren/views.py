#coding:utf-8
__author__ = 'admin'
# --------------------------------
# Created by admin  on 2016/11/15.
# ---------------------------------
from django.shortcuts import  render_to_response
from django.template.context import  RequestContext
from django.http import  HttpResponseRedirect
from bx.models import *
from django.core.paginator import  Paginator

def index(request):
    return HttpResponseRedirect("/dailiren/search/")

def search(request):
    company_list=Company.objects.all()
    path=request.path
    page=re.search(r"(\d)\.html",path)
    if page:
        page=int(page.groups()[0])
    else:
        page=1
    _info=re.search(r"/(\d+)-(\d+)-(\d+)/",path)
    if _info:
        people_id,cate_id,c_id=tuple(_info.groups())
        people_id=int(people_id)
        cate_id=int(cate_id)
        c_id=int(c_id)
    else:
        people_id=0
        cate_id=0
        c_id=0


    user_type_list=UserType.objects.all()
    cate_type_list=CateType.objects.all()
    company_list=Company.objects.all()

    return  render_to_response("dailiren_search.html",locals(),
                               context_instance=RequestContext(request))



def detail(request,id):
    return  render_to_response("dailiren_detail.html",locals(),
                               context_instance=RequestContext(request))