#coding:utf-8
__author__ = 'admin'
# --------------------------------
# Created by admin  on 2016/10/12.
# ---------------------------------
import  sys
reload(sys)
sys.setdefaultencoding("utf-8")
from threadspider import *
from pyquery import  *
import  re
import  time
from threadspider.utils.db import MySQLMgr
import urllib
from urlparse import *
from posixpath import  normpath

def myjoin(base, url):
    url1 = urljoin(base, url)
    arr = urlparse(url1)
    path = normpath(arr[2])
    return urlunparse((arr.scheme, arr.netloc, path, arr.params, arr.query, arr.fragment))

mgr=MySQLMgr("118.89.220.36",3306,"bx_abc","bx_user","gc895316")
spider_init(10,2000000)
alldata=[]
def index_handle(result):
    doc=PyQuery(result)
    detail_list=[]
    for i in doc("#listAll").find("a")[:50]:
        _=i
        detail_list.append(PyQuery(_).attr("href"))

    for detail_url in detail_list:
        def detail_handle(result,url=detail_url):
            doc=PyQuery(result)
            doc("script").remove()
            doc(".blank10").remove()
            doc(".page").remove()
            doc(".list_fj").remove()
            for  _ in doc("#mainCon").find("a"):
                if PyQuery(_).attr("href"):
                    PyQuery(_).remove()
            content=doc("#mainCon").html()
            title=doc("#4g_title").text()
            print url,title
            if title and content:
                alldata.append ([url ,title,PyQuery(content).html()])
        Spider(detail_url,code="utf-8",response_handle=detail_handle)

Spider("http://news.dahe.cn/sz/",code="utf-8",response_handle=index_handle)
spider_join()

for i,j,k  in alldata:
    print i,j ,k
    mgr.runOperation(''' insert ignore   into bx_consult(title, type, writer, `from`, addtime, content, status, type_cate)
                        VALUES (%s,4,"网络",%s,%s,%s,0,0)''',(j,i,int(time.time()),k))
