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
    page=re.search(r"(\d)\.html",path)
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
    company_list=Company.objects.all()
    params={}
    if c_id:
        params["cid"]=c_id
    if city_id:
        params["city"]=int(city_id)
    objs=ProxyUserProfile.objects.filter(certifi_status=2,**params)
    paginator=Paginator(objs,9)
    info=paginator.page( page)
    allinfo=info
    return  render_to_response("dailiren_search.html",locals(),
                               context_instance=RequestContext(request))



def detail(request,id):
    user=MyUser.objects.get(uid=int(id))
    assert user.usertype==2
    user.profile=ProxyUserProfile.objects.get(uid__uid=id)
    try:
        user.city_info=Area.objects.get(id=user.city).shortname
    except:
        user.city_info=""
    try:
        user.comname=Company.objects.get(cid=user.profile.cid).comname
    except:
        user.comname=""
    products=Product.objects.filter(cid=user.profile.cid)[:10]
    return  render_to_response("dailiren_detail.html",locals(),
                               context_instance=RequestContext(request))