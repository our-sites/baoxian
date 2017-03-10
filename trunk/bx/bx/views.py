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
from myauth.models import  ProxyUserProfile
from models import Consult
import  datetime


def home(request):
    #return  HttpResponse(request.myuser.username+request.ip)
    hot_ask=Ask.objects.all().order_by("-ask_time")
    hot_proxy_profile=ProxyUserProfile.objects.filter(certifi_status=2).order_by("-id")
    friend_company=Company.objects.all().order_by("-product_weight")
    return render_to_response( "index.html",locals(),context_instance=RequestContext(request))

@login_required
def work(request):
    assert  request.myuser.usertype in (1,2)
    #request.myuser.send_message("test","testtesttest")
    if request.myuser.usertype==1:
        return HttpResponseRedirect(request.path.replace("work","work_buy"))
    else:
        return HttpResponseRedirect(request.path.replace("work","work_proxy"))


def sitemap_index(request):
    _=Consult.objects.all().order_by("-zid")[0]
    max_id=_.zid
    zixun_info=[i for  i in range(0,max_id/10000+1)]
    return render_to_response("sitemap_index.html", locals(),mimetype="text/xml")

def zixun_sitemap_xml(request,id):
    id=int(id)
    info=Consult.objects.filter(zid__gte=id*10000,zid__lt=(id+1)*10000).values("zid","addtime")
    info=[[i["zid"],datetime.datetime.fromtimestamp(i["addtime"]).strftime("%Y-%m-%d")]  for i in info ]
    return  render_to_response("zixun_sitemap_xml.html",locals(),mimetype="text/xml")

