#coding:utf-8
__author__ = 'admin'
# --------------------------------
# Created by admin  on 2016/10/19.
# ---------------------------------

from threadspider import  *
from pyquery import  *
import  datetime
from gcutils.db import  MySQLMgr
mgr=MySQLMgr("10.141.52.179",3306,"bx_abc","bx_user","gc895316")
spider_init(1,2000000)
alldata=[]
def list_handle(result):
    doc=PyQuery(result)
    for i in doc(".cont_tit"):
        title,date=PyQuery(i).find(".cont_tit03").html(),PyQuery(i).find(".cont_tit02").html()
        addtime=int(time.mktime(datetime.datetime.strptime(date,"%Y-%m-%d").timetuple()))
        url=PyQuery(i).parent().attr("href")
        if url[0:2]=="./":
            url="http://www.stats.gov.cn/tjsj/zxfb/"+url[2:]
        if url[0]=="/":
            url="http://www.stats.gov.cn"+url
        def detail_handle(result,title=title,addtime=addtime,fromurl=url):
            doc=PyQuery(result)
            content=doc(".TRS_PreAppend").html()
            alldata.append([title,content,addtime,fromurl])
            time.sleep(2)
        Spider(url,code="utf-8",response_handle=detail_handle,proxy=False,retry_times=3,timeout=30)

Spider("http://www.stats.gov.cn/tjsj/zxfb/index.html",code="utf-8",response_handle=list_handle,proxy=False,
       timeout=30
       )

spider_join()
for i,j,k,l   in alldata:
    mgr.runOperation(''' insert ignore    into bx_consult(title, type, writer, `from`, addtime, content, status, type_cate)
                          VALUES (%s,4,"国家统计局",%s,%s,%s,0,0)''',(i,l , k ,j))