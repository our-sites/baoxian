#coding:utf-8
__author__ = 'admin'
# --------------------------------
# Created by admin  on 2016/11/25.
# ---------------------------------
from threadspider import   *
from pyquery import  PyQuery
import  re
from threading import  Lock
from gcutils.db  import  MySQLMgr

lock=Lock()
spider_init(80,500000)
mgr=MySQLMgr("192.168.8.94",3306,"shuili","root","gc895316")
id=0
_list=[]
while 1:
    result=mgr.runQuery("select id,from_url,abstract,abstract_en,keyword,keyword_en,cate_num from zhiwang_article_huangtugaoyuan where cate_num='' and id>%s order by id asc limit 500",(id,))
    if len(result)==0:
        break
    _list+=[(i,j)   for i,j,k,l,m,n,t in   result if not k   and not l  and not m  and not n and not t ]
    id=max([i[0] for i in result])

for i,j in _list:
    def handle(data,from_url=j,_id=i):
        doc=PyQuery(data)
        teacher=doc(u"p:contains('【导师】')").text()
        if teacher:
            teacher=teacher.replace(u"【导师】","").strip()
        else:
            teacher=""
        author_info=doc(u"p:contains('【作者基本信息】')").text()
        if author_info:
            author_info=author_info.replace(u"【作者基本信息】","").strip()
        else:
            author_info=""
        abstract=doc(u"#ChDivSummary").html()
        if not abstract:
            abstract=""
        abstract_en=doc(u"#EnChDivSummary").html()
        if not abstract_en:
            abstract_en=""
        keyword="";keyword_en=""
        try:
            keyword=PyQuery(doc(u"#ChDivKeyWord")[0]).text()
            keyword_en=PyQuery(doc(u"#ChDivKeyWord")[1]).text()
        except:
            pass
        network_publisher=doc(u"li:contains('【网络出版投稿人】')").text().split(u"【网络出版投稿人】")[-1].replace("\r\n","").replace(" ","")
        network_publish_date=doc(u"ul:contains('【网络出版年期】')").text().split(u"【网络出版年期】")[-1].replace("\r\n","").replace(" ","")
        def _handle(info):
            return  info.replace("\r\n","").replace("\n","").replace(" ","")
        teacher=_handle(teacher)
        author_info=_handle(author_info)
        network_publisher=_handle(network_publisher)
        cate_num=doc(u"li:contains('【分类号】')").text().split(u"【分类号】")[-1].replace("\r\n","").replace(" ","")
        print _id,teacher,author_info,network_publisher,network_publish_date,cate_num
        lock.acquire()
        try:
            mgr.runOperation(''' update shuili.zhiwang_article_huangtugaoyuan set teacher=%s,author_info=%s,abstract=%s,abstract_en=%s,
                               keyword=%s,keyword_en=%s,network_publisher=%s,network_publish_date=%s,cate_num=%s
                                where from_url=%s''',(teacher,author_info,abstract,abstract_en,keyword,keyword_en,
                                                      network_publisher,network_publish_date,cate_num,from_url))
        except:
            pass
        lock.release()
    Spider(j,code="utf-8",handle=handle,timeout=30,retry_times=5,cookie="ASP.NET_SessionId=p4kapeuvrolqx4552vbk1455; LID=")
spider_join()