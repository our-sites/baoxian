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

import  urllib
import  json
import  sys
reload(sys)
sys.setdefaultencoding("utf-8")

def add_xinwen(_from,writer,title,content):
    result=urllib2.urlopen("http://www.bao361.cn/zixun/add_xinwen",urllib.urlencode({"secret":"gc7232275",
                                                                        "from":str(_from),
                                                                        "writer":str(writer),
                                                                        "title":str(title),
                                                                        "content":str(content)})).read()
    return  json.loads(result)

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
    print add_xinwen(i,"网络",j,k)
