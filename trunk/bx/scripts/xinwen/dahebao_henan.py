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
import  json

def myjoin(base, url):
    url1 = urljoin(base, url)
    arr = urlparse(url1)
    path = normpath(arr[2])
    return urlunparse((arr.scheme, arr.netloc, path, arr.params, arr.query, arr.fragment))

def add_xinwen(_from,writer,title,content):
    result=urllib2.urlopen("http://www.bao361.cn/zixun/add_xinwen",urllib.urlencode({"secret":"gc7232275",
                                                                        "from":str(_from),
                                                                        "writer":str(writer),
                                                                        "title":str(title),
                                                                        "content":str(content)})).read()
    return  json.loads(result)

mgr=MySQLMgr("118.89.220.36",3306,"bx_abc","bx_user","gc895316")
spider_init(10,2000000)
alldata=[]
def index_handle(result):
    doc=PyQuery(result)
    detail_list=[]
    for i in PyQuery(doc(".borderR")[0]).find("a")[:50]:
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

Spider("http://www.dahe.cn/",code="utf-8",response_handle=index_handle)
spider_join()

for i,j,k  in alldata:
    print i,j ,k
    print add_xinwen(i,"大河新闻",j,k)
    break
