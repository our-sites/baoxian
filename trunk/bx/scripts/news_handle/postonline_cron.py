#coding:utf-8

import  urllib2
from threadspider.utils.db import  MySQLMgr
import  time
import  random
import  urllib
import  json
import  sys
reload(sys)
sys.setdefaultencoding("utf-8")

import xmlrpclib
proxy=xmlrpclib.ServerProxy('http://127.0.0.1:8888')

def get_cate_id(title):
    data= proxy.auto_cate(title)
    print time.time()
    response=urllib2.urlopen("https://www.bao361.cn/news/get_cate_id?catename="+urllib.quote(str(data['predicted_y']))).read()
    print time.time()
    data=json.loads(response)
    if data["status"]:
        return tuple(data["data"])
    else:
        return False

mgr=MySQLMgr("127.0.0.1",3306,"bx_abc","root","123456")

def postBaiDu(filecontent):
    URL = "http://data.zz.baidu.com/urls?site=www.bao361.cn&token=MrHjCbljFlIJxYhk"
    send_headers = {'Content-Type': 'text/plain'}
    conn = urllib2.Request(URL,filecontent,send_headers)
    req=urllib2.urlopen(conn)
    return  req.read()

def add_to_online(title,content,_from,tags,keywords,description,abstract,cate1,cate2):
    url="https://www.bao361.cn/news/add_news"
    data={"title":title,"content":content,"from":_from,"tags":tags,"keywords":keywords,"description":description,
          "abstract":abstract,"cate1":cate1,"cate2":cate2,"secret":"gc7232275"}
    data=dict([(i,str(j)) for i,j in data.items()])
    print data
    data=urllib.urlencode(data)
    print data
    req=  urllib2.urlopen(url,data).read()
    req_data=json.loads(req)
    return req_data["status"],req_data["message"],req_data.get("nid",0)
result=mgr.runQuery('''select nid,kw,title,content,`from`,tags,keywords,description,abstract,cate1,cate2  from bx_news WHERE status=2   limit 25''',())

for info   in  result:
    info=list(info)
    info[-5]=info[1]
    info[5]=info[1]
    info=tuple(info)
    time.sleep(random.randrange(1,5))
    cate_info=get_cate_id(info[2])
    if cate_info:
        cate_info=cate_info[::-1]
        cate1,cate2=cate_info
        status,message,nid=add_to_online(*(info[2:-2]+cate_info))
        print status,message,cate1,cate2,info[2]
        if status:
            print postBaiDu("https://www.bao361.cn/news/detail/%s.html"%int(nid)) #提交百度
            mgr.runOperation("update bx_news  set status=1 ,cate1 = %s ,cate2 = %s  where nid=%s ",(cate1,cate2,int(info[0])))
        else:
            mgr.runOperation("update bx_news set status=4,cate1=%s,cate2=%s  where nid=%s  ",(cate1,cate2,int(info[0])))
    else:
        mgr.runOperation("update bx_news set status=4 where nid=%s  ",(int(info[0]),))


