#coding:utf-8
from __future__ import  unicode_literals
__author__ = 'lgq'
# --------------------------------
# Created by lgq  on 16/12/7.
# 共计  1038 条有电话的不重复记录
# ---------------------------------
from pyquery import PyQuery as pq
import  MySQLdb

headers={
    'User-Agent' :'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:50.0) Gecko/20100101 Firefox/50.0'
}

def insert_mysql(shuju):
    conn=MySQLdb.connect(host='localhost',user='root',passwd='123456',db='bx_abc')
    cursor=conn.cursor()
    for da in shuju:
        sql="""insert into changan (phone,city,name,url,company) VALUES (%s,%s,%s,%s,%s)"""
        para=(da['phone'],da['city'],da['name'],da['url'],da['company'])
        # print para
        try:
            print cursor.execute(sql,para)
            conn.commit()
        except Exception as e:
            print e
            pass
    cursor.close()

for i in range(1,118):
    url='http://www.changan.com/dailiren/0_0_a?p='+ str(i)
    print url
    doc=pq(url=url,headers=headers)
    # print doc('.bx_aglist')
    import  re
    shuju=[]
    for one in doc('.bx_aglist'):
        # print pq(one).html()
        dlr={}
        dlr['name']= pq(one)('h4').text()
        dlr['url']= pq(one)('.name')('a').attr('href')
        dlr['city']= pq(one)('em').eq(1).text()
        dlr['company']= pq(one)('em').eq(2).text()
        print dlr
        try:
            dlr['phone']= re.search(r'1\d{10}',pq(one)('.btn').html()).group()
            shuju.append(dlr)
        except Exception as e:
            print e
        print ">>>>>>>>>>>>>>>>"
    insert_mysql(shuju)
