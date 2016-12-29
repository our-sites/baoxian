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
    for i in doc("a[href]"):
        if re.match(r"/anli/\d+/$",doc(i).attr("href")):
            detail_list.append("http://www.bxd365.com"+doc(i).attr("href"))
    for detail_url in detail_list:
        def detail_handle(result,url=detail_url):
            doc=PyQuery(result)
            title= doc(".fontcon_info").find("h1").html().strip().replace("\n","")

            addtime=int(time.mktime(datetime.datetime.strptime(doc(".time").html(),"%Y-%m-%d").timetuple()))
            content=doc(".anli_fontcon").html().strip()
            print url,title
            alldata.append ([url ,title,content,addtime])
        Spider(detail_url,code="utf-8",handle=detail_handle)
for i in range(1,100):
    Spider("http://www.bxd365.com/anli/%s.html"%i,code="utf-8",handle=index_handle)
spider_join()
for i,j,k,l   in alldata:
    mgr.runOperation(''' insert ignore   into bx_consult(title, type, writer, `from`, addtime, content, status, type_cate)
                          VALUES (%s,2,"网络",%s,%s,%s,0,0)''',(j,i,l ,k))
