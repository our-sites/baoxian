#coding:utf-8
__author__ = 'admin'
# --------------------------------
# Created by admin  on 2016/10/14.
# ---------------------------------



import  datetime
import  time
import  MySQLdb
import json

conn=MySQLdb.connect(host="118.89.220.36",port=3306,user="bx_user",passwd="gc895316")

zid=0
while 1:
    cursor=conn.cursor()
    cursor.execute("select zid,content from bx_abc.bx_consult WHERE zid>%s  ORDER by zid asc limit 30",(zid,))
    data= cursor.fetchall()
    cursor.close()
    zid=max([i[0] for i in data])
    for i,j in data:
        if "W020170314314894491800_r75.gif" in j :
            print i,j
            exit(0)

    print zid









