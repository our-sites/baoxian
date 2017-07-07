
#!/usr/bin/env python
# coding=utf-8
import MySQLdb.cursors
import MySQLdb
import requests
from lxml import etree
from bs4 import BeautifulSoup

import sys
reload(sys)
sys.setdefaultencoding('utf8')

my_conn= MySQLdb.connect(
        host='172.16.13.165',
        port = 3306,
        user='root',
        passwd='123456',
        db ='bx_caiji',charset="utf8",cursorclass=MySQLdb.cursors.DictCursor)
my_cur = my_conn.cursor()
my_cur.execute("SELECT uid,phone,url  FROM agent_caiji_shejiao LIMIT 1000")
allData = my_cur.fetchall()

url="https://3g.ganji.com/zz_zpbaoxianjingjiren/2621627814x?pos=9&page=26&tg=1001&url=zpbaoxianjingjiren&d=o_26/&pageSize=40&gjchver=A&ifid=gj3g_wclick_co_32_103_9_0"
def get_info(url):
    headers = {'user-agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.110 Safari/537.36 CoolNovo/2.0.9.20",
               'Referer': "https://3g.ganji.com/"}
    DATA = requests.get(url,headers=headers)
    html = DATA.content
    soup = BeautifulSoup(html, 'lxml')
    selector = etree.HTML(html)
    #Value = selector.xpath('//table/tbody/tr/td')
    Value = selector.xpath('//tr/td')
    print Value[3].text,'~~~~~~~~~~~~~~',Value[5].text
    n=0
    for v in Value:
        if v.text.isdigit() :
            phone=v.text
    #    print v.text,n
    #    n+=1

for D in allData :
    if D['phone'].isdigit() :
        continue
    else :
        get_info(D['url'])