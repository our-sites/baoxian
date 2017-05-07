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
from  bx.myauth.models import *


def index(request):
    return HttpResponseRedirect("/dailiren/search/")

def search(request):
    company_list=Company.objects.all()
    path=request.path
    page=re.search(r"/(\d+)\.html",path)
    if page:
        page=int(page.groups()[0])
    else:
        page=1
    _info=re.search(r"/(\d+)-(\d+)/",path)
    if _info:
        city_id,c_id=tuple(_info.groups())
        city_id=int(city_id)
        c_id=int(c_id)
    else:
        city_id=0
        c_id=0
    if c_id:
        c_obj=Company.objects.get(cid=c_id)
    else:
        c_obj=None
    company_list=Company.objects.all().order_by("-dailiren_weight")[:25]
    params={}

    if c_id:
        params["proxy_cid"]=c_id

    if city_id:
        params["city_id"]=int(city_id)

    objs=MyUser.objects.filter(is_proxy=1, proxy_cid__gt=0,**params).order_by("-ans_num","uid")
    paginator=Paginator(objs,9)
    info=paginator.page( page)
    allinfo=info
    area_ids=[ i.province_id  for i in allinfo  if i.province_id  ]+[i.city_id for i in allinfo if i.city_id]
    area_info=dict([(i["id"],i["areaname"]) for i in  Area.objects.filter(id__in=area_ids).values("id","areaname")])
    for i in allinfo:
        i.province_city_info=''
        if i.province_id:
            i.province_city_info+=area_info[i.province_id]
        if i.city_id:
            i.province_city_info+=area_info[i.city_id]

    return  render_to_response("dailiren_search.html",locals(),
                               context_instance=RequestContext(request))



def detail(request,id):
    user=MyUser.objects.get(uid=int(id))
    assert user.is_proxy==1

    try:
        _=Company.objects.get(cid=user.proxy_cid)
        user.comname=_.comname
        user.comcontent=_.content
    except:
        user.comname=""
        user.comcontent=""

    products=Product.objects.filter(cid=user.proxy_cid)[:10]

    my_ans=Answer.objects.filter(uid=user.uid)
    _dict = dict([(_.askid,_.ans_content) for _ in my_ans])
    my_ans_ask=Ask.objects.filter(askid__in=[ i.askid for i in my_ans]).order_by("-ask_time")[:10]
    for _ in my_ans_ask:
        _.self_content=_dict[_.askid]

    degree_info=dict(AddDegree.objects.all().values_list("adid","info"))
    money_info=dict(AddMoney.objects.all().values_list("amid","info"))
    position_info=dict(AddPosition.objects.all().values_list("apid","info"))
    company_info=dict(Company.objects.all().values_list("cid","comname"))

    my_adds=Add.objects.filter(uid=user.uid).order_by("-uptime")
    for i in my_adds:
        i.degree_info=degree_info[i.adid]
        i.money_info=money_info[i.amid]
        i.position_info=position_info[i.apid]
        i.company_info=company_info[i.cid]

    my_shares=Share.objects.filter(uid=user.uid).order_by("-uptime")
    for i in my_shares:
        i.company_info=company_info[i.cid]

    return  render_to_response("dailiren_detail.html",locals(),
                               context_instance=RequestContext(request))