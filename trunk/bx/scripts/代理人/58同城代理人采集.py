#coding:utf-8
__author__ = 'lgq'
# --------------------------------
# Created by lgq  on 16/12/2.
# ---------------------------------
import requests
import re,MySQLdb,time
from pyquery import PyQuery as pq
from collections import defaultdict

headers={
    'User-Agent' :'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:50.0) Gecko/20100101 Firefox/50.0'
}

def insert_mysql(shuju):
    conn=MySQLdb.connect(host='localhost',user='root',passwd='123456',db='bx_abc')
    cursor=conn.cursor()
    for da in shuju:
        sql="""insert into dailiren_58 (phone,city,name,url,title) VALUES (%s,%s,%s,%s,%s)"""
        para=(da['phone'],da['city'],da['name'],da['url'],da['title'])
        # print para
        try:
            print cursor.execute(sql,para)
            conn.commit()
        except Exception as e:
            print e
            pass
    cursor.close()

def get_chengshi():
    url="http://m.58.com/city.html?from=click_city_new&58hm=m_changecity_new&58cid=18"
    doc=pq(url=url)
    chengshi=[]
    print ">>>>>>>>>>>>>>"
    for c in doc('.city_box').find('a'):
        d=pq(c).attr('href')
        if 'http' in d:chengshi.append(d)
    print chengshi
    return chengshi

def search_data():
    for cs in get_chengshi():
        page=1
        while 1:
            url=cs+'baoxianfuwu/pn'+str(page)+'/?key=保险&cmcskey=保险&final=1&jump=1&sqa_type=0&newkey=保险&formatsource=sou&from=home_sou&keyfrom=sou'
            print  url
            # doc_r=requests.get(url=url,headers=headers)
            time.sleep(5)
            doc=pq(url=url)
            shuju=[]
            city= doc('.dl_nav')('h1').text().replace(u'保险','')

            for a in  doc('.list-info').find('li') :
                try:
                    sj=defaultdict(unicode)
                    c=pq(a)('a')('.call').children()
                    tel= re.match(r"1\d{10}",c.attr('telnumber'))
                    if tel:
                        print ">>>>>>>>>>>>>>>>>>>>>"
                        # # print pq(a)('.wlt_ico_o').text()
                        # # print pq(a).html()
                        # print c.attr('telnumber')
                        # print c.attr('username')
                        # print c.attr('title')
                        # print c.attr('url')

                        sj['title']=c.attr('title')
                        sj['url']=c.attr('url')
                        sj['name']=c.attr('username')
                        sj['phone']=c.attr('telnumber')
                        sj['city'] = city
                        # sj['vip'] = pq(a)('.wlt_ico_o').text()
                        shuju.append(sj)
                        print sj
                except Exception as e:
                    print e
                     #判断有无下一页
            insert_mysql(shuju)
            print doc('.pager').text()
            try:
                num=len( doc('.pager')('a') .eq(4).attr('href') )
            except Exception as e:
                print e
                break
            abc=doc('.page').text()
            print abc,type(abc)
            print num
            if num>20:
                page+=1
            else:
                break
if __name__ == '__main__':
    search_data()