#coding:utf-8
__author__ = 'admin'
# --------------------------------
# Created by admin  on 2016/10/31.
# ---------------------------------

from ipip import  IP
IP.load("ipdb.dat")
from models import Area
from django.db.models import Q
import  urllib


def get_ip_info(ip):
    if ip and ip !="0.0.0.0" and ip!="127.0.0.1":
        result=IP.find(ip).split("\t")
        print ip,result
        country_info=result[0]
        province_info=result[1]
        city_info=result[2]
        if province_info and city_info:
            _objs= Area.objects.filter(Q(shortname=city_info)|Q(areaname=city_info) ,level=2)
            if len(_objs)>0:
                city_info=_objs[0].areaname
                city_id=_objs[0].id
                province_obj=Area.objects.get(id=_objs[0].parentid)
                province_info=province_obj.areaname
                province_id=province_obj.id
                return   province_info,province_id,city_info,city_id
    return '',0,'',0

class IpMiddleware(object):
    def process_request(self, request):
        ip_cookie=request.COOKIES.get("ip_info","")
        ip_cookie=urllib.unquote(ip_cookie)
        #print request.META
        _ip=request.META.get("HTTP_X_REAL_IP","")
        request.ip= _ip   if _ip else None
        if ip_cookie:
            province_info,city_info=ip_cookie.split("|")
            province,province_id=province_info.split(",")
            city,city_id=city_info.split(",")
            try:
                province_id=int(province_id)
            except:
                province_id=0
                province=''
                city_id=0
                city=''
            else:
                try:
                    city_id=int(city_id)
                except:
                    city_id=0
            request.province = province
            request.province_id=province_id
            request.city=city
            request.city_id=city_id
        else:
            request.province,request.province_id,request.city,request.city_id=get_ip_info(_ip)


    def process_response(self, request, response):
        ip_cookie=request.COOKIES.get("ip_info","")
        if response["Content-Type"]!="text/xml":

            if not ip_cookie:
                response.set_cookie("ip_info",urllib.quote(("%s,%s|%s,%s"%(request.province,request.province_id,
                                                                          request.city,request.city_id)).encode("utf-8")),
                                    max_age=86400*365)

        return  response