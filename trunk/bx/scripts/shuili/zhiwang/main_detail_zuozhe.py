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
    result=mgr.runQuery("select id, from_url from zhiwang_article_huangtugaoyuan where id>%s order by id asc limit 500",(id,))
    if len(result)==0:
        break
    _list+=result
    id=max([i[0] for i in result])

for i,j in _list:
    def handle(data,from_url=j,_id=i):
        doc=PyQuery(data)
        for _ in doc(u"p:contains('【作者】')").find("a"):
            print PyQuery(_).html()

        lock.acquire()
        pass
        # try:
        #     mgr.runOperation(''' update shuili.zhiwang_article_huangtugaoyuan set teacher=%s,author_info=%s,abstract=%s,abstract_en=%s,
        #                        keyword=%s,keyword_en=%s,network_publisher=%s,network_publish_date=%s,cate_num=%s
        #                         where from_url=%s''',(teacher,author_info,abstract,abstract_en,keyword,keyword_en,
        #                                               network_publisher,network_publish_date,cate_num,from_url))
        # except:
        #     pass
        lock.release()
    Spider(j,code="utf-8",response_handle=handle,timeout=30,retry_times=5)
spider_join()