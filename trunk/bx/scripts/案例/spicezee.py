#coding:utf-8
__author__ = 'admin'
# --------------------------------
# Created by admin  on 2016/10/13.
# ---------------------------------
from gcutils.db import  MySQLMgr
from threadspider import *
from pyquery import  *
import  re
import  time
import  datetime
import  time
mgr=MySQLMgr("113.10.195.169",3306,"bx_abc","bx_user","gc895316")
spider_init(10,2000000)
alldata=[]
def index_handle(result):
    doc=PyQuery(result)
    detail_list=[]
    time_list=[]
    for i in doc(".clearfix.list_itemone").find("li").find("a"):
        detail_list.append(PyQuery(i).attr("href"))
    for i in doc(".clearfix.list_itemone").find("li").find("span"):
        time_list.append(int(time.mktime(datetime.datetime.strptime(
                PyQuery(i).find("font").html() or PyQuery(i).html() ,
                "%Y-%m-%d").timetuple()
                                         )))
    for detail_url,addtime in zip(detail_list,time_list):
        def detail_handle(result,url=detail_url,addtime=addtime):
            doc=PyQuery(result)
            title= doc(".pagetit").html()
            content=doc("#content_font").html()
            print url,title
            alldata.append ([url ,title,content,addtime])
        Spider("http://www.spicezee.com"+detail_url,code="gbk",handle=detail_handle)

for i in range(1,33):
    Spider("http://www.spicezee.com/anli/18_%s.html"%i,code="gbk",handle=index_handle)

spider_join()
for i,j,k,l   in alldata:
    mgr.runOperation(''' insert ignore   into bx_consult(title, type, writer, `from`, addtime, content, status, type_cate)
                          VALUES (%s,2,"网络",%s,%s,%s,0,0)''',(j,i,l ,k))