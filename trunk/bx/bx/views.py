#coding:utf-8
__author__ = 'admin'
# --------------------------------
# Created by admin  on 2016/10/27.
# ---------------------------------
from django.shortcuts import  render_to_response
from django.http import  HttpResponse,HttpResponseRedirect
from django.template.context import  RequestContext
from myauth.decorators import  login_required
from models import Ask
from myauth.models import  ProxyUserProfile


def home(request):
    #return  HttpResponse(request.myuser.username+request.ip)
    hot_ask=Ask.objects.all().order_by("-ask_time")
    hot_proxy_profile=ProxyUserProfile.objects.filter(certifi_status=2).order_by("-id")
    return render_to_response( "index.html",locals(),context_instance=RequestContext(request))

@login_required
def work(request):
    assert  request.myuser.usertype in (1,2)
    request.myuser.send_message("test","testtesttest")
    if request.myuser.usertype==1:
        return HttpResponseRedirect("/work_buy/")
    else:
        return HttpResponseRedirect("/work_proxy/")
