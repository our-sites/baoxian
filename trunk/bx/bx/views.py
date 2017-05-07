#coding:utf-8
__author__ = 'admin'
# --------------------------------
# Created by admin  on 2016/10/27.
# ---------------------------------
from django.shortcuts import  render_to_response
from django.http import  HttpResponse,HttpResponseRedirect
from django.template.context import  RequestContext
from myauth.decorators import  login_required
from models import Ask,Company
from models import Consult,Product,Ask
import  datetime
from myauth.models import  MyUser


def home(request):
    #return  HttpResponse(request.myuser.username+request.ip)
    hot_ask=Ask.objects.all().order_by("-ask_time")
    hot_user_proxy=MyUser.objects.filter(is_proxy=1).order_by("-ans_num","uid")[:20]
    cids=[i.proxy_cid for i in hot_user_proxy]
    cid_objs=Company.objects.filter(cid__in=cids)
    cid_info=dict([(i.cid,i.shortname) for i in cid_objs])
    for i in hot_user_proxy:
        #if i.proxy_cid:
        i.short_comname=cid_info.get(i.proxy_cid,"")

    # friend_company=Company.objects.all().order_by("-product_weight")
    hot_zixun_news=Consult.objects.filter(type=4,status=1).order_by("-addtime")[:5]
    hot_zixun_baike=Consult.objects.filter(type=1,status=1).order_by("-addtime")[:5]
    hot_zixun_anli=Consult.objects.filter(type=2,status=1).order_by("-addtime")[:5]


    return render_to_response( "index.html",locals(),context_instance=RequestContext(request))



def about(request):
    if request.path=="/about":
        return  HttpResponseRedirect("/about/")
    return render_to_response("about/about.html",locals(),
                              context_instance=RequestContext(request))




def sitemap_index(request):
    _=Consult.objects.all().order_by("-zid")[0]
    max_id=_.zid
    zixun_info=[i for  i in range(0,max_id/10000+1)]

    _=Product.objects.all().order_by("-pid")[0]
    max_id=_.pid
    product_info=[i for  i in range(0,max_id/10000+1)]

    _=Ask.objects.all().order_by("-askid")[0]
    max_id=_.askid
    ask_info=[i for  i in range(0,max_id/10000+1)]

    return render_to_response("sitemap/sitemap_index.html", locals(),mimetype="text/xml")

def zixun_sitemap_xml(request,id):
    id=int(id)
    info=Consult.objects.filter(zid__gte=id*10000,zid__lt=(id+1)*10000).values("zid","addtime")
    info=[[i["zid"],datetime.datetime.fromtimestamp(i["addtime"]).strftime("%Y-%m-%d")]  for i in info ]
    return  render_to_response("sitemap/zixun_sitemap_xml.html",locals(),mimetype="text/xml")

def product_sitemap_xml(request,id):
    id=int(id)
    info=Product.objects.filter(pid__gte=id*10000,pid__lt=(id+1)*10000).values("pid","addtime")
    info=[[i["pid"],datetime.datetime.fromtimestamp(i["addtime"]).strftime("%Y-%m-%d")]  for i in info ]
    return  render_to_response("sitemap/product_sitemap_xml.html",locals(),mimetype="text/xml")

def ask_sitemap_xml(request,id):
    id=int(id)
    info=Ask.objects.filter(askid__gte=id*10000,askid__lt=(id+1)*10000).values("askid","ask_time")
    info=[[i["askid"],datetime.datetime.fromtimestamp(i["ask_time"]).strftime("%Y-%m-%d")]  for i in info ]
    return  render_to_response("sitemap/ask_sitemap_xml.html",locals(),mimetype="text/xml")