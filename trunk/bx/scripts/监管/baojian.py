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
import  datetime
import  time
mgr=MySQLMgr("113.10.195.169",3306,"bx_abc","bx_user","gc895316")
spider_init(10,2000000)
alldata=[]
def index_handle(result):
    doc=PyQuery(result)
    detail_list=[]
    title_list=[]
    for i in doc(".hui14").find("span").find("a"):
        detail_list.append(PyQuery(i).attr("href"))
        title_list.append(PyQuery(i).attr("title"))
    time_list=[]
    for i in doc(".hui14").next():
        time_list.append(int(time.mktime(datetime.datetime.strptime("20"+PyQuery(i).html()[1:-1],"%Y-%m-%d").timetuple())))
    for detail_url,addtime,title  in zip(detail_list,time_list,title_list):
        def detail_handle(result,url=detail_url,addtime=addtime,title=title ):
            doc=PyQuery(result)
            content=doc(".xilanwb").html()
            print url,title
            alldata.append ([url ,title,content,addtime])
        if detail_url.startswith("/"):
            Spider("http://www.circ.gov.cn"+detail_url,code="utf-8",handle=detail_handle)

for i in range(1,70):
    Spider("http://www.circ.gov.cn/web/site0/tab5207/module14337/page%s.htm"%i,code="utf-8",handle=index_handle)
for i in range(1,104):
    Spider("http://www.circ.gov.cn/web/site0/tab5209/module14341/page%s.htm"%i,code="utf-8",handle=index_handle)
for i in range(1,6):
    Spider("http://www.circ.gov.cn/web/site0/tab5212/module14345/page%s.htm"%i,code="utf-8",handle=index_handle)
for i in range(1,7):
    Spider("http://www.circ.gov.cn/web/site0/tab5218/module14348/page%s.htm"%i,code="utf-8",handle=index_handle)
for i in range(1,17):
    Spider("http://www.circ.gov.cn/web/site0/tab5214/module14351/page%s.htm"%i,code="utf-8",handle=index_handle)
for i in range(1,28):
    Spider("http://www.circ.gov.cn/web/site0/tab5216/module14349/page%s.htm"%i,code="utf-8",handle=index_handle)
for i in range(1,7):
    Spider("http://www.circ.gov.cn/web/site0/tab5218/module14348/page%s.htm"%i,code="utf-8",handle=index_handle)
for i in range(1,4):
    Spider("http://www.circ.gov.cn/web/site0/tab5220/module14355/page%s.htm"%i,code="utf-8",handle=index_handle)
for i in range(1,15):
    Spider("http://www.circ.gov.cn/web/site0/tab5221/module14357/page%s.htm"%i,code="utf-8",handle=index_handle)
for i in range(1,6):
    Spider("http://www.circ.gov.cn/web/site0/tab6762/module17199/page%s.htm"%i,code="utf-8",handle=index_handle)
for i in range(1,9):
    Spider("http://www.circ.gov.cn/web/site0/tab5208/module14343/page%s.htm"%i,code="utf-8",handle=index_handle)
for i in range(1,28):
    Spider("http://www.circ.gov.cn/web/site0/tab5210/module14342/page%s.htm"%i,code="utf-8",handle=index_handle)

spider_join()

for i,j,k,l   in alldata:
    mgr.runOperation(''' insert ignore   into bx_consult(title, type, writer, `from`, addtime, content, status, type_cate)
                          VALUES (%s,5,"网络",%s,%s,%s,0,0)''',(j,i,l ,k))
