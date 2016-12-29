#coding:utf-8
__author__ = 'admin'
# --------------------------------
# Created by admin  on 2016/10/12.
# ---------------------------------
from gcutils.db import  MySQLMgr
from threadspider import *
from pyquery import  *
import  re
import  time
mgr=MySQLMgr("113.10.195.169",3306,"bx_abc","bx_user","gc895316")
spider_init(10,2000000)
alldata=[]
def index_handle(result):
    doc=PyQuery(result)
    detail_list=[]
    for i in doc("a[href]"):
        if re.match(r"^http://finance\.sina\.com\.cn.+?/\d{4}-\d{2}-\d{2}/doc-.+?.shtml",doc(i).attr("href")):
            detail_list.append(doc(i).attr("href"))
    for detail_url in detail_list:
        def detail_handle(result,url=detail_url):
            doc=PyQuery(result)
            doc("blockquote").remove()
            doc("[data-sudaclick]").remove()
            title,content= doc("#artibodyTitle").html(),doc("#artibody").html()
            print url,title
            alldata.append ([url ,title,content])
        Spider(detail_url,code="utf-8",handle=detail_handle)
Spider("http://finance.sina.com.cn/money/insurance/",code="utf-8",handle=index_handle)
spider_join()
for i,j,k  in alldata:
    mgr.runOperation(''' insert ignore   into bx_consult(title, type, writer, `from`, addtime, content, status, type_cate)
                          VALUES (%s,4,"网络",%s,%s,%s,0,0)''',(j,i,int(time.time()),k))
