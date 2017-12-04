#coding:utf-8
__author__ = 'admin'
# --------------------------------
# Created by admin  on 2016/10/10.
# ---------------------------------

from gcutils.encrypt import  md5
from django.conf import  settings
import os
from django.http import  HttpResponse
import  json
from django.views.decorators.csrf import csrf_exempt
import  urllib
import urlparse
from models import Area
from bx.utils.sms import send_dayysms_validnumber
import random
from gcutils.encrypt import  md5
import  time
import  traceback
import upyun

@csrf_exempt
def upload_img(request):
    print request.method,len(request.body)
    try:
        _file = urlparse.parse_qs(request.body).get("file")[0]
        extname = request.POST["extname"]
        extname = extname.split("?")[0]
        def up_to_upyum(key, value):
            up_conn = upyun.UpYun(settings.UPYUN_BUCKETNAME, settings.UPYUN_USERNAME, settings.UPYUN_PASSWORD)
            up_headers = {}
            up_conn.put(key, value, checksum=True, headers=up_headers)
            return settings.UPYUN_BASE_URL + key
        filename = md5(str(time.time())+str(random.random()))+extname
        image_key = "/image_upload_api/"+filename
        url = up_to_upyum(image_key,_file)
        return HttpResponse(json.dumps({"status":True,"filename":filename,"imgurl":url}),
                            mimetype="application/javascript")
    except Exception as e :
        traceback.print_exc()
        print e.message
        return HttpResponse(json.dumps({"status":False,"message":e.message}),mimetype="application/javascript")

def area_list(request):
    getinfo=request.GET
    areaid=getinfo.get("areaid",None)
    callback=getinfo.get("callback")
    if areaid==None:
        info=Area.objects.filter(level=1)
    else:
        areaid=int(areaid)
        info=Area.objects.filter(parentid=areaid)
    info=info.order_by("id")
    data=[(i.id,i.shortname)  for i in info]
    result=json.dumps({"status":True,"data":data},ensure_ascii=True)
    if callback:
        result="%s(%s)"%(callback,result)
    return  HttpResponse(result,mimetype="application/javascript")

def send_sms_validnumer(request):
    getinfo=request.GET
    tel=getinfo.get("tel")
    tel=int(tel)
    numer="".join(random.sample(["1","2","3","4","5","6","7","8","9"],6))
    calback=getinfo.get("callback")
    try:
        result=send_dayysms_validnumber(phone=tel,content=numer)
        assert  result["alibaba_aliqin_fc_sms_num_send_response"]["result"]["success"]==True
        request.session.setdefault("sms_validnumer",numer)
        request.session.setdefault("sms_validtime",str(int(time.time())))
        _result={"status":True,"message":"success!","md5":md5(numer+"gc895316")}
    except:
        message="发送失败！稍后再试"
        _result={"status":False,"message":message}
    _result=json.dumps(_result,ensure_ascii=True)
    if calback:
        _result="%s(%s)"%(calback,_result)
    response=HttpResponse(_result,mimetype="application/javascript")
    return  response

def valid_sms_validnumer(request):
    getinfo=request.GET
    numer=getinfo.get("numer")
    md=getinfo.get("md5")
    callback=getinfo.get("callback")
    assert  numer and md
    if md5(numer+"gc895316")==md:
        result={"status":True}
    else:
        result={"status":False}
    result=json.dumps(result,ensure_ascii=True)
    if callback:
        result="%s(%s)"%(callback,result)
    return HttpResponse(result,mimetype="application/javascript")




