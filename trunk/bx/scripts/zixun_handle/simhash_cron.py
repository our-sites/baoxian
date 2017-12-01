import re
from threadspider.utils.db import MySQLMgr
import HTMLParser
import  simhash
import  json

def filter_tags(htmlstr):
    s=re.sub("<[^<>]+>",'',htmlstr)
    return s

def replaceCharEntity(htmlstr):
    htmlstr=htmlstr.replace("&quot;",'"')
    htmlstr=htmlstr.replace("&amp;",'&')
    htmlstr=htmlstr.replace("&lt;",'<')
    htmlstr=htmlstr.replace("&gt;",'>')
    htmlstr=htmlstr.replace("&nbsp;",' ')
    return htmlstr

def prodesc_delsytle(prodesc):
    try:
        return  filter_tags(replaceCharEntity(prodesc))
    except:
        return  prodesc

def get_simple_content(self) :
    a = filter_tags(self)
    b = replaceCharEntity(a)
    _ = HTMLParser.HTMLParser()
    return _.unescape(b.strip())




def hash_obj_handle(zid,hash_obj):
    hash_a,hash_b,hash_c,hash_d=hash_obj.get_cut_value("a"),hash_obj.get_cut_value("b"), \
    hash_obj.get_cut_value("c"),hash_obj.get_cut_value("d")
    _={}
    print hash_a,hash_b,hash_c,hash_d
    result=[mgr.runQuery("select zids from bx_consult_simhash_a WHERE simhash_a=%s",(hash_a,)) or [] ,
        mgr.runQuery("select zids from bx_consult_simhash_b WHERE simhash_b=%s",(hash_b,)) or [] ,
        mgr.runQuery("select zids from bx_consult_simhash_c WHERE simhash_c=%s",(hash_c,)) or [] ,
        mgr.runQuery("select zids from bx_consult_simhash_d WHERE simhash_d=%s",(hash_d,)) or [] ]
    def _handle(x):
        if x and x[0]:
            return json.loads(x[0][0])
        return {}
    result=[_handle(i)  for i in result]
    print result
    for i in result:
        for j,k in i.items():
            _[int(j)]=k
    for j,k in _.items():
        if zid != j:
            distance=hash_obj.distance_by_value(k)
            if distance<=3:
                mgr.runOperation("update bx_consult set status=4 where zid=%s",(zid,))
                flag=False
                result[0].pop(str(zid),"")
                result[1].pop(str(zid),"")
                result[2].pop(str(zid),"")
                result[3].pop(str(zid),"")
                break
    else:
        flag=True
        result[0][zid]=hash_obj.value
        result[1][zid]=hash_obj.value
        result[2][zid]=hash_obj.value
        result[3][zid]=hash_obj.value
        mgr.runOperation("update bx_consult set status=2 where zid=%s",(zid,))

        mgr.runOperation('''INSERT INTO bx_consult_simhash_a(simhash_a ,  zids ) VALUES ( %s ,%s)
        ON DUPLICATE KEY UPDATE zids = %s  ''',(hash_a, json.dumps(result[0]),json.dumps(result[0])))


        mgr.runOperation('''INSERT INTO bx_consult_simhash_b(simhash_b  ,  zids ) VALUES ( %s ,%s)
        ON DUPLICATE KEY UPDATE zids = %s  ''',(hash_b,json.dumps(result[1]),json.dumps(result[1])))

        mgr.runOperation('''INSERT INTO bx_consult_simhash_c(simhash_c  ,  zids ) VALUES ( %s ,%s)
        ON DUPLICATE KEY UPDATE zids = %s  ''',(hash_c ,json.dumps(result[2]),json.dumps(result[2])))

        mgr.runOperation('''INSERT INTO bx_consult_simhash_d(simhash_d  ,  zids ) VALUES ( %s ,%s)
        ON DUPLICATE KEY UPDATE zids = %s  ''',(hash_d ,json.dumps(result[3]),json.dumps(result[3])))

    return flag





mgr=MySQLMgr("118.89.220.36",3306,"bx_abc","bx_user","gc895316")

def consult_handle(zid,content):
    assert  zid>0
    simple_content=get_simple_content(content)
    if not  simple_content:
        mgr.runOperation("update bx_consult set status=4 where zid=%s",(_zid,))
        return
    else:
        if not isinstance(simple_content,unicode):
            try:
                simple_content=simple_content.decode("utf-8")
            except:
                mgr.runOperation("update bx_consult set status=4 WHERE zid=%s",(_zid,))
                return
        hash_obj=simhash.Simhash(simple_content)
        hash_obj_handle(zid,hash_obj)



result=mgr.runQuery('''select zid,content  from bx_consult WHERE status=3   limit 50''',())

for _zid,content  in  result:
    print consult_handle(_zid,content)



