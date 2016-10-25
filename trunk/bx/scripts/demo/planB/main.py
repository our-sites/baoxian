#coding:utf-8
__author__ = 'admin'
# --------------------------------
# Created by admin  on 2016/10/12.
# ---------------------------------
from threadspider import *
from pyquery import  *
import  re
import  time

spider_init(8,2000000)
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
            content=PyQuery(content).html()
            print "【采集到的数据】：","标题："+title,"\t","内容："+content.replace("\r","").replace("\n","")
            alldata.append ([url ,title,content.replace("\r","").replace("\n","")])
        Spider(detail_url,code="utf-8",handle=detail_handle)
Spider("http://finance.sina.com.cn/money/insurance/",code="utf-8",handle=index_handle)
spider_join()
# for i in alldata:
#     print "标题:%s \t内容:%s"%(i[1],i[2])
