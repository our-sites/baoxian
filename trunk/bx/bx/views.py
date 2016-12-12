#coding:utf-8
__author__ = 'admin'
# --------------------------------
# Created by admin  on 2016/10/27.
# ---------------------------------
from django.shortcuts import  render_to_response
from django.http import  HttpResponse
from django.template.context import  RequestContext

def home(request):
    #return  HttpResponse(request.myuser.username+request.ip)
    return render_to_response( "index.html",locals(),context_instance=RequestContext(request))