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

for i in range(1,2):
    Spider("http://www.circ.gov.cn/web/site0/tab5207/",code="utf-8",handle=index_handle)


spider_join()

for i,j,k,l   in alldata:
    mgr.runOperation(''' insert ignore   into bx_consult(title, type, writer, `from`, addtime, content, status, type_cate)
                          VALUES (%s,5,"网络",%s,%s,%s,0,0)''',(j,i,l ,k))
