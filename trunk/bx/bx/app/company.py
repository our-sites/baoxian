#! /usr/bin/env python
#coding=utf-8
__author__ = 'Administrator'
#this is bx 
#create by 2017/2/21 0021
from django.shortcuts import  render_to_response
from django.http import  HttpResponse
from ..models import Company
from django.template.context import  RequestContext
from django.views.decorators.csrf import csrf_exempt
import  json
from django.core import serializers


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
                friend_company=Company.objects.all().order_by("-product_weight")
                tmp_list=[]
                for i in friend_company:
                    tmp_dic=dict()
                    tmp_dic["cid"]=i.cid
                    tmp_dic["comname"]=i.comname
                    tmp_dic["shotname"]=i.shortname
                    tmp_dic["img"]=i.img.url
                    tmp_list.append(tmp_dic)
                data = {"status": {"status_code": 0, "status_reason": ""},"result":{"company_list":tmp_list}}
    else:
        data = {"status": {"status_code": 1, "status_reason": "Request method not allow"}}
    return HttpResponse(json.dumps(data,ensure_ascii=False,indent=2),mimetype="application/javascript")

