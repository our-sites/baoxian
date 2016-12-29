#coding:utf-8
__author__ = 'admin'
# --------------------------------
# Created by admin  on 2016/10/24.
# ---------------------------------
from gcutils.db import  MySQLMgr
import  sys
conn=MySQLMgr("172.17.19.102",3306,"gcproinfo","tj","jf(w#r82_MHf")
def get_url(pid,cate3):
    if pid>900000000:
        return  "http://product.gongchang.com/s%s/CNS2%s.html"%(cate3,pid)
    else:
        return "http://product.gongchang.com/c%s/CNC1%s.html"%(cate3,pid)

for i in sys.stdin:
    i=i.strip()
    info=i.split("\t")
    try:
        info=[j.decode("utf-8") for j in info ]
        pid,key=info
        pid=int(pid)
    except:
        pass
    else:
        if pid<900000000:
            for i in range(0,100):
                result=conn.runQuery("select pid,lastcate from pd_info_%s WHERE state =1 and pid=%%s"%i,(pid,))
                if len(result)>0:
                    print (get_url(*result[0])+"\t"+key).encode("utf-8")
                    break
        else:
            result=conn.runQuery("select pid,lastcate from pd_specialpro WHERE  state=1 and pid=%s",(pid,))
            if len(result)>0:
                print (get_url(*result[0])+"\t"+key).encode("utf-8")
