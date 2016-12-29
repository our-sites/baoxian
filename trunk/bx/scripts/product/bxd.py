#coding:utf-8
__author__ = 'admin'
# --------------------------------
# Created by admin  on 2016/10/26.
# ---------------------------------
from threadspider import *
import  re
from pyquery import    *
from gcutils.db import  MySQLMgr
import  json
from threading import  Lock
from itertools import  groupby
from gcutils.encrypt import  md5
import  time

mgr=MySQLMgr("113.10.195.169",3306,"bx_abc","bx_user","gc895316")
spider_init(10,1000000,[urllib2_get_httpproxy("192.168.8.%s"%i,890) for i  in range(40,46)])
lock=Lock()
def get_cid(comname):
    lock.acquire()
    try:
        result= mgr.runQuery("select cid from bx_company WHERE comname=%s",(comname,))[0][0]
    except:
        result=  None
    lock.release()
    return  result

def get_type(typename):
    lock.acquire()
    try:
        result=  mgr.runQuery("select id from bx_catetype_tab WHERE  type_name=%s",(typename,))[0][0]
    except:
        result= None
    lock.release()
    return result
results=[]
def handle(result):
    doc=PyQuery(result)
    for urlobj,priceobj  in zip(doc(".productlist-ul").find("h3").find("a"),doc(".money")):
        price=PyQuery(priceobj).html()
        if not price:
            price=0
        else:
            price=int(float(price))
        url=PyQuery(urlobj).attr("href")
        def detail_handle(result,price=price,url=url):
            doc=PyQuery(result)
            from_url=url
            pro_name=doc("h1").html()
            comname=doc(".lab").find("label").html()
            bx_type_info="|".join([PyQuery(i).html() for i in doc(".lab").find("label")])
            bx_type=[get_type(PyQuery(i).html())   for i in    doc(".lab").find("label")[1:]]
            min_price=price
            bx_type=",".join([str(i) for i in bx_type if i!=None])
            bx_feature=doc(".a-pro-mess").find("h5").text()[2:]
            insurance_agelimit,insurance_timelimit,insurance_paytype=[  PyQuery(i).html() for i in  doc(".pro-d").find("font") ]
            if not insurance_agelimit:
                insurance_agelimit=""
            if not insurance_timelimit:
                insurance_timelimit=""
            if not insurance_paytype:
                insurance_paytype=""
            insurance_agelimit=insurance_agelimit.replace("---","-")
            insurance_agelimit=insurance_agelimit.replace("--","-")
            if "-" in insurance_agelimit:
                start_info,end_info=insurance_agelimit.split("-")[:2]
                if u"天" in start_info:
                    stat_age=-int(re.search("\d+",start_info).group())
                else:
                    stat_age=int(re.search("\d+",start_info).group())
                end_age=int(re.search("\d+",end_info).group())
            else:
                stat_age=0
                end_age=75
            _tt=[PyQuery(i).html()  for i in  doc(".product-fontmess")]
            if len(_tt)==2:
                _tt=[""]+_tt
            pro_desc_case,pro_desc_reason,pro_desc_duty =_tt
            pro_desc_content=[]
            for i in doc(".table-bao").find("tr:not([bgcolor])"):
                for j in PyQuery(i).find("td"):
                    _u= PyQuery(j).attr("rowspan")
                    if len(pro_desc_content)==0 or len(pro_desc_content[-1])==3:
                        pro_desc_content.append([])
                    info=PyQuery(j).html()
                    if not info:
                        info=""
                    if not _u:
                        for _t in pro_desc_content:
                            if len(_t)<3:
                                _t.append(info)
                                break
                    else:
                        pro_desc_content[-1].append(info)
                        for _k in range(2,int(_u)+1):
                            pro_desc_content.append([info])
            content=[]
            for i,j in groupby(pro_desc_content,lambda x:x[0]):
                _u=[i]
                for k in j :
                    _u.append(k[1:])
                content.append(_u)
            pro_desc_content=json.dumps(content,indent=True)
            img_style=doc(".a-pro-img").find("span").attr("style")
            img=""
            if img_style:
                _ttt=re.search(r"url\((.+)\)",img_style)
                if _ttt:
                    img=_ttt.groups()[0]
            if img:
                img_url="pro_imgs/"+md5(img)+"."+img.split(".")[-1]
                def img_handle(result,name=md5(img)+"."+img.split(".")[-1]):
                    info=result
                    fl=open("./pro_imgs/"+name,"wb")
                    fl.write(info)
                    fl.close()
                if not  img.startswith("http") and not img.startswith("//"):
                    img="http://www.bxd365.com"+img
                Spider(img,handle=img_handle,proxy=False,retry_times=5)
            else:
                img_url=""
            if comname:
                cid=get_cid(comname)
                if cid:
                    results.append([pro_name,cid,bx_type,bx_feature,stat_age,end_age,
                                    pro_desc_case,pro_desc_reason, pro_desc_content,pro_desc_duty,from_url,
                                    img_url,min_price,insurance_timelimit,insurance_paytype,insurance_agelimit])

        Spider("http://www.bxd365.com"+url, handle=detail_handle,code="utf-8",proxy=False)
for  i in range(1,385):
    Spider("http://www.bxd365.com/chanpin/%s.html"%i ,handle=handle,code="utf-8",proxy=False)
spider_join()
results.reverse()
for i in results:
    mgr.runOperation('''insert ignore  into  bx_product( pro_name, cid, bx_type, bx_feature, star_age, end_age,
 pro_desc_case, pro_desc_reason, pro_desc_content, pro_desc_duty, from_url,
 img, meta, min_price, addtime, insurance_timelimit, insurance_paytype, insurance_agelimit) VALUES
 (%s,%s,%s,%s,%s,%s,
 %s,%s,%s,%s,%s,
 %s,%s,%s,%s,%s,%s,%s)''',
                     (i[0],i[1],i[2],i[3],i[4],i[5],
                      i[6],i[7],i[8],i[9],i[10],
                      i[11],"",i[12],int(time.time()),i[13],i[14],i[15]))

