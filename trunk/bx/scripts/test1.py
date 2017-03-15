#coding:utf-8
__author__ = 'admin'
# --------------------------------
# Created by admin  on 2016/10/14.
# ---------------------------------
from threadspider.utils.db import MySQLMgr

mgr=MySQLMgr("118.89.220.36",3306,"bx_abc","bx_user","gc895316")
result=mgr.runQuery("SELECT  askid,count(*) from bx_answer GROUP BY askid",())

for askid,num in result:
    askid=int(askid)
    num=int(num)
    mgr.runOperation("update bx_ask set ans_num=%s where askid=%s",(num,askid))