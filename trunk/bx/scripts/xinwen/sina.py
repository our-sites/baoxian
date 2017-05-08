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

import  urllib
import  json


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
        if re.match(r"^http://finance\.sina\.com\.cn.+?/\d{4}-\d{2}-\d{2}/doc-.+?.shtml",doc(i).attr("href")):
            detail_list.append(doc(i).attr("href"))
    for detail_url in detail_list:
        def detail_handle(result,url=detail_url):
            doc=PyQuery(result)
            doc("blockquote").remove()
            doc("[data-sudaclick]").remove()
            title,content= doc("#artibodyTitle").html(),doc("#artibody").html()
            print url,title
            alldata.append ([url ,title,content])
        Spider(detail_url,code="utf-8",response_handle=detail_handle,retry_times=3)
Spider("http://finance.sina.com.cn/money/insurance/",code="utf-8",response_handle=index_handle)
spider_join()
for i,j,k  in alldata:
    print i,j,k
    print add_xinwen(i,"网络",j,k)
