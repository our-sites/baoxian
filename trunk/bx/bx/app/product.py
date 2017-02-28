#! /usr/bin/env python
#coding=utf-8
__author__ = 'Administrator'
#this is bx
#create by 2017/2/21 0021
from django.shortcuts import  render_to_response
from django.http import  HttpResponse
from ..models import Product
from django.template.context import  RequestContext
from django.views.decorators.csrf import csrf_exempt

import  json
@csrf_exempt
def list(request):
    if request.method == "POST":
        req_data = request.POST.get("req_data", "")
        if not req_data:
            data = {"status": {"status_code": 1, "status_reason": "数据格式不正常！"}}
        else:
            try:
                post_data = json.loads(req_data.encode("UTF-8"))
            except Exception, e:
                data = {"status": {"status_code": 1, "status_reason": str(e)}}
            else:
                products=Product.objects.all()[0:10]
                tmp_list=[]
                for i in products:
                    tmp_dic=dict()
                    tmp_dic["cid"]=i.pid
                    tmp_dic["comname"]=i.pro_name
                    tmp_dic["img"]=i.img.url
                    tmp_list.append(tmp_dic)
                data = {"status": {"status_code": 0, "status_reason": ""},"result":{"company_list":tmp_list}}
    else:
        data = {"status": {"status_code": 1, "status_reason": "Request method not allow"}}
    return HttpResponse(json.dumps(data,ensure_ascii=False,indent=2),mimetype="application/javascript")

def lunbo(request):
    data={"errorCode":0,"msg":""}
    return HttpResponse(json.dumps(data),mimetype="application/javascript")