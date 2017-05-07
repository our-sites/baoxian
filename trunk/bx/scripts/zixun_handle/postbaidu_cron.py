#coding:utf-8

import  urllib2
from threadspider.utils.db import  MySQLMgr

mgr=MySQLMgr("118.89.220.36",3306,"bx_abc","bx_user","gc895316")

def postBaiDu(filecontent):
    URL = "http://data.zz.baidu.com/urls?site=www.bao361.cn&token=MrHjCbljFlIJxYhk&type=original"
    send_headers = {'Content-Type': 'text/plain'}
    conn = urllib2.Request(URL,filecontent,send_headers)
    req=urllib2.urlopen(conn)
    return  req.read()

result=mgr.runQuery('''select zid  from bx_consult WHERE status=2   limit 10''',())

for _zid  in  result:
    print postBaiDu("http://www.bao361.cn/zixun/detail/%s.html"%_zid)
    mgr.runOperation("update bx_consult set status=1 where zid=%s ",(_zid,))


