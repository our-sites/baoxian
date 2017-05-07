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
    for i in doc(".box740").find("dt").find("a"):
        _=myjoin("http://www.cs.com.cn/ssgs/hyzx/index.shtml",PyQuery(i).attr("href"))
        detail_list.append(_)
    for detail_url in detail_list:
        def detail_handle(result,url=detail_url):
            doc=PyQuery(result)
            doc("script").remove()
            doc(".blank10").remove()
            doc(".page").remove()
            doc(".list_fj").remove()
            content=doc(".artical_c").html()
            title=doc(".artical_t").find("h1").text()
            print url,title
            alldata.append ([url ,title,PyQuery(content).html()])
        Spider(detail_url,code="gbk",response_handle=detail_handle)

Spider("http://www.cs.com.cn/ssgs/hyzx/index.shtml",code="gbk",response_handle=index_handle)
spider_join()

for i,j,k  in alldata:
    print i,j ,k
    mgr.runOperation(''' insert ignore   into bx_consult(title, type, writer, `from`, addtime, content, status, type_cate)
                        VALUES (%s,4,"网络",%s,%s,%s,0,0)''',(j,i,int(time.time()),k))
