#coding:utf-8
__author__ = 'admin'
# --------------------------------
# Created by admin  on 2016/12/8.
# ---------------------------------

from threadspider import  *
import  pyquery
from threading import  Lock
from gcutils.db import  MySQLMgr
mgr=MySQLMgr("113.10.195.169",3306,"bx_abc","bx_user","gc895316")
lock=Lock()
spider_init(10,1000000)
def run(typeid,allpage,totypeid):
    for page_num in range(1,allpage+1):
        url="http://www.bxd365.com/chanpin/0-%st-0/%s.html"%(typeid,page_num)
        def handle(data,totypeid=str(totypeid)):
            doc=pyquery.PyQuery(data)
            products=[pyquery.PyQuery(i).attr("href") for i in doc("h3").find("a")]
            lock.acquire()
            for i in products:
                _old=mgr.runQuery("select bx_type from bx_product WHERE from_url=%s",(i,))
                if _old :
                    _old_type=_old[0][0]
                    _old_type_list=_old_type.split(",")
                    if _old_type:
                        _new_type=",".join(list(set(_old_type_list+[totypeid])))
                    else:
                        _new_type=totypeid
                    print [_old_type,_new_type,i]
                    mgr.runOperation("update bx_product set bx_type=%s where from_url=%s ",(_new_type,i))
            lock.release()
        Spider(url,code="utf-8",response_handle=handle)
run(101,26,25)
run(102,16,26)
run(104,5,27)
run(3,26,28)
run(105,8,29)
run(106,10,30)
run(107,53,31)
run(143,14,32)
run(142,49,33)
run(41,41,34)
run(121,65,35)
run(144,21,36)
run(21,6,37)
run(145,17,38)
run(146,7,39)
run(147,17,40)
spider_join()
