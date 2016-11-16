#coding:utf-8
__author__ = 'admin'
# --------------------------------
# Created by admin  on 2016/11/14.
# ---------------------------------
from django.shortcuts import  render_to_response
from django.template.context import  RequestContext
from ..models import  UserType,CateType,Company,Product
from django.core.paginator import  Paginator
import  re

#
def search(request):
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

    querystring=""
    if people_id:
        end_age=UserType.objects.get(id=people_id).end_age
        querystring+=" end_age>=%s"%end_age
    else:
        end_age=0
    if cate_id:
        if  querystring!="":
            querystring+= " and "
        querystring+=" FIND_IN_SET(  '%s',bx_type )  "%cate_id
    if c_id:
        if querystring!="":
            querystring+=  " and "
        querystring+=" cid = %s "%c_id

    user_type_list=UserType.objects.all()
    cate_type_list=CateType.objects.all()
    company_list=Company.objects.all()

    if querystring:
        _u=Product.objects.raw("select  * from bx_product WHERE "+querystring)
        _u=[i for i in _u]
        product_paginator=Paginator(_u,9)
    else:
        product_paginator=Paginator(Product.objects.all(),9)
    allinfo=product_paginator.page(page)
    allinfo.previous_page_number()
    cid_list=[i.cid  for i in allinfo]
    cid_objs=Company.objects.filter(cid__in=cid_list).values("cid","comname")
    cid_dict=dict([(i["cid"],i["comname"])  for i in cid_objs])
    for i in allinfo:
        i.comname=cid_dict.get(i.cid,"")
    return  render_to_response("product_search.html",locals(),
                               context_instance=RequestContext(request))

def detail(request,pid):
    product=Product.objects.get(pid=int(pid))
    company=Company.objects.get(cid=product.cid)
    return   render_to_response("product_detail.html",locals(),
                                context_instance=RequestContext(request))