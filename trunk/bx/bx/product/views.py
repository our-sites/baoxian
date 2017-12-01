#coding:utf-8
__author__ = 'admin'
# --------------------------------
# Created by admin  on 2016/11/14.
# ---------------------------------
from django.shortcuts import  render_to_response
from django.template.context import  RequestContext
from ..models import  UserType,CateType,Company,Product
from django.core.paginator import  Paginator,EmptyPage
import  re
from django.http import  HttpResponse
import  json
from django.conf import  settings
from bx.decorators import  mobile_browser_adaptor_by_host
#
def search_redirect(request):
    keyword=request.POST.get("keyword")
    data={"errorCode":0,"formSuccess":{"redirect":"/product/search/?keyword="+keyword,
                                                                 "duration":50},"data":{}}

    return  HttpResponse(json.dumps(data),mimetype="application/javascript")

@mobile_browser_adaptor_by_host(settings.M_HOST_FUN,{"product_search.html":"m_product_search.html"})
def search(request):
    path=request.path
    page=re.search(r"/(\d+)\.html",path)
    keyword=request.GET.get("keyword","")
    if page:
        page=int(page.groups()[0])
    else:
        page=1
    _info=re.search(r"/(\d+)-(\d+)-(\d+)",path)
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
        _usertype=UserType.objects.get(id=people_id)
        end_age=_usertype.end_age
        querystring+=" end_age>=%s"%end_age
        user_type_info=_usertype.type_name
    else:
        end_age=0
    if cate_id:
        if  querystring!="":
            querystring+= " and "
        querystring+=" FIND_IN_SET(  '%s',bx_type )  "%cate_id
        cate_type_info=CateType.objects.get(id=cate_id).type_name
    if c_id:
        if querystring!="":
            querystring+=  " and "
        querystring+=" cid = %s "%c_id
        c_info=Company.objects.get(cid=c_id).shortname

    user_type_list=UserType.objects.all()
    if not people_id:
        cate_type_list=CateType.objects.all()[:6]
    else:
        cate_type_list=CateType.objects.filter(usertype_id=int(people_id))
    company_list=Company.objects.filter(product_weight__gt=0).order_by("-product_weight")
    if not  keyword:
        if querystring:
            _u=Product.objects.raw("select  * from bx_product WHERE "+querystring)
            _u=[i for i in _u]
            product_paginator=Paginator(_u,9)
        else:
            product_paginator=Paginator(Product.objects.all(),9)
    else:
        product_paginator=Paginator(Product.objects.filter(pro_name__contains=keyword),9)

    try:
        allinfo=product_paginator.page(page)
    except EmptyPage:
        page=1
        allinfo=product_paginator.page(page)
    allinfo.previous_page_number()
    cid_list=[i.cid  for i in allinfo]
    cid_objs=Company.objects.filter(cid__in=cid_list).values("cid","comname")
    cid_dict=dict([(i["cid"],i["comname"])  for i in cid_objs])
    for i in allinfo:
        i.comname=cid_dict.get(i.cid,"")
    return  render_to_response("product_search.html",locals(),
                               context_instance=RequestContext(request))

@mobile_browser_adaptor_by_host(settings.M_HOST_FUN,{"product_detail.html":"m_product_detail.html"})
def detail(request,pid):
    product=Product.objects.get(pid=int(pid))
    company=Company.objects.get(cid=product.cid)
    jsoninfo=product.get_pro_desc_json()
    desc_json_info=[]
    for i in jsoninfo:
        name=i[0]
        for j in i[1:]:
            if not desc_json_info:
                desc_json_info.append([[name,len(i[1:])],j[0],j[1]])
            else:
                if desc_json_info[-1][0][0]==name:
                    desc_json_info.append([[name,0],j[0],j[1]])
                else:
                    desc_json_info.append([[name,len(i[1:])],j[0],j[1]])
    product.desc_json_info=desc_json_info
    other_products=Product.objects.filter(pid__gt=int(pid))[:4]
    if len(other_products)<4:
        other_products=Product.objects.filter(pid__lt=int(pid))[:4]
    return   render_to_response("product_detail.html",locals(),
                                context_instance=RequestContext(request))