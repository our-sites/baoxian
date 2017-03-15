#! /usr/bin/env python
#coding=utf-8
__author__ = 'Administrator'
#this is bx 
#create by 2017/2/21 0021

from django.shortcuts import  render_to_response
from django.http import  HttpResponse
from django.template.context import  RequestContext
import json
from django.views.decorators.csrf import csrf_exempt

import MySQLdb.cursors
import MySQLdb

from ..models import  Ask,Answer,Product,Area
#from django.core.paginator import Paginator,InvalidPage
#from django.db.models import Q

@csrf_exempt
def huifu(request):
    post_data = request.POST.get('req_data','')
    DATA = {"status": {"status_code": 0, "status_reason": ""}}
    if post_data :
        try:
            data =json.loads(post_data)
        except :
            DATA["status"]["status_reason"] = 'POST参数格式错误'
        else :
            ask_stat=data['body'].get('ask_stat','')
            _data,_DATA=[],[]

            if ask_stat == 'unanswer':
                _data=Ask.objects.filter(ans_num=0).order_by("-ask_time")[:50]

            elif ask_stat == 'answer':
                _data=Ask.objects.filter(ans_num__gt=0).order_by("-ask_time")[:50]

            else :
                DATA["status"]["status_reason"] = 'POST参数未知'

            if _data :
                for _d in _data:
                    Dic={}
                    Dic['area']=_d.get_area_info()
                    Dic['ask_content'] = _d.ask_content
                    Dic['askid'] = _d.askid
                    #Dic['user'] = _d.get_user()
                    _DATA.append(Dic)
            DATA['result'] = {'ask_list': _DATA}
    else :
        DATA["status"]["status_reason"]='POST参数不能为空'
    #return HttpResponse(json.dumps(DATA), mimetype="application/javascript")
    return HttpResponse(json.dumps(DATA, ensure_ascii=False, indent=2), mimetype="application/javascript")
