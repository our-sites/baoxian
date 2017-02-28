#! /usr/bin/env python
#coding=utf-8
__author__ = 'Administrator'
#this is bx 
#create by 2017/2/21 0021

from django.shortcuts import  render_to_response
from django.http import  HttpResponse
from django.template.context import  RequestContext
import  json


def lunbo(request):
    data={"errorCode":0,"msg":""}
    return HttpResponse(json.dumps(data),mimetype="application/javascript")

def yuanchuang(request):
    data={"errorCode":0,"msg":""}
    return HttpResponse(json.dumps(data),mimetype="application/javascript")

def duanzi(request):
    data={"errorCode":0,"msg":""}
    return HttpResponse(json.dumps(data),mimetype="application/javascript")

def shequ(request):
    data={"errorCode":0,"msg":""}
    return HttpResponse(json.dumps(data),mimetype="application/javascript")

def pinglun(request):
    data={"errorCode":0,"msg":""}
    return HttpResponse(json.dumps(data),mimetype="application/javascript")


