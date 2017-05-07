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
cursor=conn.cursor(MySQLdb.cursors.DictCursor)
cursor.execute("select id,areaname,shortname,level,lng,lat,parentid from bx_abc.area  where level<=2")
data= cursor.fetchall()
print len(data)
from itertools import  groupby

for i ,j in groupby(data,key=lambda x:x["areaname"]):
    print i,j








