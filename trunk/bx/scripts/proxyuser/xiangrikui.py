#coding:utf-8
__author__ = 'admin'
# --------------------------------
# Created by admin  on 2016/10/28.
# ---------------------------------

from threadspider import  *
import re
from gcutils.db import  MySQLMgr
import  json
from gcutils.encrypt import  md5
from pyquery import  *

cid_config={u"平安人寿":54,u"中国人寿":19,u"太平洋人寿":63,u"新华人寿":69,u"泰康人寿":62,u"友邦保险":77,u"阳光人寿":76,
            u"信诚人寿":70,u"民生保险":49,u"人保寿险":46,u"中德安联":85,u"合众人寿":27,u"安邦财险":2,u"安邦人寿":1,
            u"百年人寿":6,u"安诚保险":3,u"北大方正":7,u"渤海人寿":8,u"长城人寿":9,u"长生人寿":10,u"东吴人寿":11,
            u"大都会人寿":12,u"大地财险":13,u"德华安顾":14,u"福德生命":16,u"国华人寿":21,u"光大永明":22,u"国联人寿":24,
            u"华夏人寿":26,u"华泰人寿":28,u"恒大人寿":31,u"华康财险":33,u"宏康人寿":38,u"和谐健康":40,u"汇丰人寿":41,
            u"吉祥人寿":42,u"建信人寿":43,u"君龙人寿":45,u"昆仑健康":46,u"利安人寿":47,u"美亚财险":50,u"农银人寿":52,
            u"前海人寿":55,u"瑞泰人寿":58,u"瑞德康健康":59,u"天安人寿":64,u"同方全球":65,u"太阳联合":66,u"泰康养老":67,
            u"幸福人寿":71,u"英大人寿":78,u"永安财险":79,u"永诚财险":80,u"中意人寿":82,u"中英人寿":83,u"中荷人寿":84,
            u"珠江人寿":87,u"中华联合财险":88,u"中邮人寿":89,u"中银保险":90,u"中银三星":91,u"中融人寿":94}

mgr=MySQLMgr("113.10.195.169",3306,"bx_abc","bx_user","gc895316")
spider_init(2,1000000,proxy_list=[urllib2_get_httpproxy("192.168.8.%s"%i,890)   for i in range(40,46)+[33,34,35]])
def get_area_id(areaname):
    try:
        result=mgr.runQuery("select  id,parentid from area WHERE  shortname=%s and level=2",(areaname,))
        return  result[0]
    except:
        return [0,0]

alldata={}

def handle(result):
    result=json.loads(result)
    for i in result:
        province_id=i["id"]
        def citys_handle(result,province_id=province_id):
            for j in json.loads(result):
                city_id=j["id"]
                city_name=j["city_name"]
                def detail_handle(result,city_name=city_name):
                    doc=PyQuery(result)
                    for t  in doc("[data-imgid]"):
                        userid=PyQuery(t).attr("data-imgid")
                        if alldata.has_key(userid):
                            alldata[userid]["city_name"]=city_name
                        else:
                            alldata[userid]={"city_name":city_name}
                        def phone_handle(_ps,userid=userid):
                            a=json.loads(_ps)
                            if alldata.has_key(userid):
                                alldata[userid]["phone"]=a["phone"]
                            else:
                                alldata[userid]={"phone":a["phone"]}
                        Spider("http://common.xiangrikui.com/api/users/%s"%userid,handle=phone_handle,proxy=False)
                        def user_handle(_us,userid=userid):
                            doc=PyQuery(_us)
                            name=doc(".agent-name").html()
                            comname=doc(".agent-company").html()
                            img_url=doc(".agent-img").attr("src")
                            numer=doc(".right").text()
                            try:
                                numer=re.search(r"\d+",numer).group()
                            except:
                                numer=""
                            alldata[userid]["name"]=name
                            alldata[userid]["comname"]=comname
                            alldata[userid]["img_url"]=img_url
                            alldata[userid]["numer"]=numer
                            _ttt=doc(".agent-self").find("p.text-gray").html()
                            def jieshao_handle(_js,userid=userid):
                                doc=PyQuery(_js)
                                content=doc(".info-box").find("p").html()
                                if not content:
                                    content=""
                                else:
                                    content=content.strip()
                                alldata[userid]["content"]=content
                            Spider("http://pc."+_ttt+"/jieshao.html",handle=jieshao_handle,code="utf-8",retry_times=3,proxy=False)
                        Spider("http://pc.bxr.im/%s"%userid,handle=user_handle,code="utf-8",retry_times=3,proxy=False)
                    _next=doc("a[rel='next']").attr("href")
                    if _next:
                        Spider("http://a.xiangrikui.com"+_next,handle=detail_handle,code="utf-8",retry_times=3,proxy=False)
                Spider("http://a.xiangrikui.com/sf%s-cs%s/gs.html"%(province_id,city_id),handle=detail_handle,code="utf-8",retry_times=3,proxy=False)
        Spider("http://common.xiangrikui.com/api/v1/locate/provinces/%s/cities"%province_id,handle=citys_handle,
               retry_times=3,proxy=False)
Spider("http://common.xiangrikui.com/api/v1/locate/provinces",handle=handle,proxy=False)

spider_join()
for i,j in alldata.items():
    try:
        url=  j["img_url"]
        assert  url
    except:
        pass
    else:
        filename=md5(url)+"."+url.split(".")[-1]
        j["img_url"]="proxyuser_imgs/"+filename
        def img_handle(data,filename=filename):
            fl=open("./proxyuser_imgs/"+filename,"wb")
            fl.write(data)
            fl.close()
        Spider(url,handle=img_handle,retry_times=5,proxy=False)
spider_join()
for i,j in alldata.items():
    try:
        name=j["name"]
        comname=j["comname"].split("\xa0\xa0")[0]
        img_user=j["img_url"]
        numer=str(j["numer"])
        phone=j["phone"]
        jieshao=j["content"]
        cid=cid_config[comname]
        province,city=get_area_id(j["city_name"])
        assert  numer
        assert  province and city
    except Exception as e :
        print j
        print e.message
        pass
    else:
        print name,comname,img_user,numer,phone,jieshao
        mgr.runOperation('''insert ignore into bx_user(username, real_name, salt, state, phone, tel, email,
         qq, imgurl, sex, birthday, ip, province, city, "zone", usertype, addtime, password)
         VALUES (%s,%s,'',0,%s,'','',
         '',%s,0,"","",%s,%s,0,2,,''
         )''',(phone,name,phone,
               img_user,province,city) )
        uid=mgr.runQuery('''select uid from bx_user where username=%s''',(phone,))[0][0]
        mgr.runOperation('''insert ignore  into  bx_proxyuser_profile("position",cid,weixin,my_ad,uid,certifi_num)
 VALUES ('',%s,'',%s,%s,%s)''',(cid,jieshao,uid,numer))

