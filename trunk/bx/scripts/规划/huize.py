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
    for i in doc("a.red_b3"):
        #print i
        detail_list.append(PyQuery(i).attr("href"))
    time_list=[]
    for i in doc("td.gray.st_27[align]"):
        #print PyQuery(i).html()
        time_list.append(int(time.mktime(datetime.datetime.strptime(PyQuery(i).html(),"%Y/%m/%d %H:%M:%S").timetuple())))
    for detail_url,addtime in zip(detail_list,time_list):
        def detail_handle(result,url=detail_url,addtime=addtime ):
            doc=PyQuery(result)
            title= doc(".study_center_l2_2").find("h1").html().strip().replace("\n","")
            #addtime=int(time.mktime(datetime.datetime.strptime(doc(".time").html(),"%Y-%m-%d").timetuple()))
            content=doc(".tppp").html().strip()
            print url,title
            alldata.append ([url ,title,content,addtime])
        Spider("http://xuexi.huize.com"+detail_url,code="utf-8",handle=detail_handle)

for i in range(1,280):
    Spider("http://xuexi.huize.com/study/list-2-%s.html"%i,code="utf-8",handle=index_handle)
spider_join()

for i,j,k,l   in alldata:
    mgr.runOperation(''' insert ignore   into bx_consult(title, type, writer, `from`, addtime, content, status, type_cate)
                          VALUES (%s,3,"网络",%s,%s,%s,0,0)''',(j,i,l ,k))
