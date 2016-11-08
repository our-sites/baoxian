#coding:utf-8
__author__ = 'admin'
# --------------------------------
# Created by admin  on 2016/10/29.
# ---------------------------------
import re
from gcutils.db import  MySQLMgr
import  json
from gcutils.encrypt import  md5
from pyquery import  *
import urllib2
import urllib
import  urlparse
import  traceback

mgr=MySQLMgr("113.10.195.169",3306,"bx_abc","bx_user","gc895316")
zid=0
def save_img(content,extname):
    img_content=content
    a=urllib2.urlopen("http://img.baoxiangj.com/api/upload_img",data=urllib.urlencode({"extname":".png","file":img_content}) ).read()
    return  json.loads(a)["imgurl"]

while 1:
    result=mgr.runQuery('''select zid,content,`from`  from bx_consult WHERE imghandle_tag=0 and zid>%s  ORDER by zid asc  limit 50''',(zid,))
    if len( result)==0:
        break
    else:
        zid=max([i[0] for i in result])
        for _zid,content,_from  in  result:
            print _zid
            doc=PyQuery("<div>"+ content+"</div>")
            host=urlparse.urlparse(_from).hostname
            for j in doc("img"):
                src=PyQuery(j).attr("src")
                if src and src[:2]!="//"  and (not src.startswith("http://")):
                    if src[0]=="/":
                        _tt=urlparse.urlparse(_from)
                        _tt=list(_tt)
                        _tt[2]=src
                        _url=urlparse.urlunparse(_tt)
                    elif src[:2]=="./"  :
                        _tt=urlparse.urlparse(_from)
                        _tt=list(_tt)
                        _tt[2]="/".join(_tt[2].split("/")[:-1])+src[1:]
                        _url=urlparse.urlunparse(_tt)
                    else:
                        _url=src
                    #print _url
                else:
                    _url=src
                print _url
                try:
                    _imgdata=urllib.urlopen(_url).read()
                    extname="."+ _url.split(".")[-1]
                    new_name=save_img(_imgdata,extname)
                    print new_name
                except Exception as e :
                    traceback.print_exc()
                    j.set("src",_url)
                else:
                    j.set("src",new_name)
            content=doc.html()
            mgr.runOperation('''update bx_consult  set content=%s,imghandle_tag=1 where zid=%s''',(content,_zid))
            print _zid






