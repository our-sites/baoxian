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
    for i in doc("a[href]"):
        if re.match(r"^http://insurance\.hexun\.com/\d{4}-\d{2}-\d{2}/\d+\.html",doc(i).attr("href")):
            detail_list.append(doc(i).attr("href"))
    for detail_url in detail_list:
        def detail_handle(result,url=detail_url):
            doc=PyQuery(result)
            content=doc(".art_contextBox") or doc(".art_context")
            title=doc(".articleName").find("h1").html() or doc(".art_title").find("h1").html()
            print url,title
            alldata.append ([url ,title,PyQuery(content).html()])
        Spider(detail_url,code="gbk",response_handle=detail_handle)
Spider("http://insurance.hexun.com/",code="gbk",response_handle=index_handle)
spider_join()
for i,j,k  in alldata:
    print i,j ,k
    add_xinwen(i,"网络",j,k)
