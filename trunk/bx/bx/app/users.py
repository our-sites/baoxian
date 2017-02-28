#! /usr/bin/env python
#coding=utf-8
__author__ = 'Administrator'
#this is bx 
#create by 2017/2/21 0021

from django.shortcuts import  render_to_response
from django.http import  HttpResponse
from ..myauth.models import MyUser
from django.template.context import  RequestContext
from django.views.decorators.csrf import csrf_exempt
import  json

@csrf_exempt
def msg(request):
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
                if "uid" in post_data and post_data["uid"].isdigit():
                    try:
                        myuser=MyUser.objects.get(uid=post_data["uid"])
                        megs=myuser.get_unread_messages()
                    except MyUser.DoesNotExist:
                        data = {"status": {"status_code": 1, "status_reason": "uid不存在"}}
                    else:
                        data = {"status": {"status_code": 0, "status_reason": ""},
                                "result": {"messages": len(megs)}}
                else:
                    data = {"status": {"status_code": 1, "status_reason": "uid不能为空"}}
    else:
        data = {"status": {"status_code": 1, "status_reason": "Request method not allow"}}
    return HttpResponse(json.dumps(data,ensure_ascii=False,indent=2),mimetype="application/javascript")