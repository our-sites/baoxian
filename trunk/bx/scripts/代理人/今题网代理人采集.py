#coding:utf-8
__author__ = 'lgq'
# --------------------------------
# Created by lgq  on 16/12/2.
#  共计5040 条信息
# ---------------------------------
from pyquery import PyQuery as  pq
import re,requests
import MySQLdb
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

headers={
    'User-Agent' :'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:50.0) Gecko/20100101 Firefox/50.0'
}

def insert_mysql(shuju):
    conn=MySQLdb.connect(host='localhost',user='root',passwd='123456',db='bx_abc')
    cursor=conn.cursor()
    for da in shuju:
        sql="""insert into jinti (phone,city,zone,name,url) VALUES (%s,%s,%s,%s,%s)"""
        para=(da[0],da[2],da[3],da[4],da[5])
        # print para
        # cursor.execute(sql,para)
        try:
            print cursor.execute(sql,para)
            conn.commit()
        except Exception as e:
            print e
            # conn.rollback()
            pass
    cursor.close()

def get_chengshi():
    url='http://www.jinti.com/selectcity/?f=2'
    doc=pq(url=url)
    doc2= doc('#content')('.mBox')
    import re
    chengshi= re.findall(r'(http://.*jinti\.com/)',doc2.html())
    return set(chengshi)

def get_info():
    for chengshi in get_chengshi():
        i=1
        while 1:
            url=chengshi+"baoxian/p"+str(i)+"/"
            # url='http://zhengzhou.jinti.com/baoxian/p'+str(i)+'/'
            print url
            doc=requests.get(url=url,headers=headers)
            # print doc.content
            v_source=pq(doc.content)
            shuju=[]
            for a in  v_source('.fw_group') :
                hang=[]
                b= pq(a)
                try:
                    if b('p').filter('.f14').text():  #标题
                        tel= re.search(r"1\d{10}",b.html())
                        if tel:
                            hang.append(tel.group())
                            # print ">>>>>>"
                            # print b('p').filter('.f14').text()           #标题
                            # print b('p').eq(2).text().split("-")[0].strip().replace(u'保险服务','')
                            # print b('p').eq(2).text().split("-")[1].strip()
                            # print b('p').eq(3).text().split(" ")[0].strip()

                            hang.append(b('p').filter('.f14').text()   )
                            hang.append(b('p').eq(2).text().split("-")[0].strip().replace(u'保险服务',''))          #city
                            hang.append(b('p').eq(2).text().split("-")[1].strip())                      #zone
                            hang.append(b('p').eq(3).text().split(" ")[0].strip())                      #name
                            hang.append(url)
                            shuju.append(hang)
                    else:
                        break
                except:
                    pass
            # print len(shuju)
            for a in shuju:
                print a[0],a[1],a[2],a[3],a[4]
            # i+=1
            page=v_source('#Page_panel').text()
            print type(page)
            insert_mysql(shuju)
            if u'下一页' in page:
                i+=1
            else:
                break

if __name__ == '__main__':
    get_info()