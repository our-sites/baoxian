#coding:utf-8

from urlparse import urljoin
from urlparse import urlparse
from urlparse import urlunparse
from posixpath import normpath
from threadspider.utils.db import   MySQLMgr
from snownlp import SnowNLP
import jieba.posseg as pseg
import json
import requests
from pyquery import  PyQuery
import  urllib
import  urllib2
import  traceback
import  HTMLParser
import  re
import  sys
import  time
import  random
reload(sys)
sys.setdefaultencoding("utf-8")


def myjoin(base, url):
    url1 = urljoin(base, url)
    arr = urlparse(url1)
    path = normpath(arr[2])
    return urlunparse((arr.scheme, arr.netloc, path, arr.params, arr.query, arr.fragment))

def save_img(content,extname):
    img_content=content
    a=urllib2.urlopen("http://www.bao361.cn/api/upload_img",data=urllib.urlencode({"extname":extname,"file":img_content}) ).read()
    return  json.loads(a)["imgurl"]


mgr=MySQLMgr("118.89.220.36",3306,"bx_abc","bx_user","gc895316")

zid=0

while 1:
    result=mgr.runQuery('''select zid,title,content,`from`  from bx_consult WHERE writer="国家统计局" and zid>%s   order by zid asc  limit 10''',(zid,))
    for _zid,title,content,_from  in  result:
        if not content:
            pass
        else:
            doc=PyQuery("<div>"+ content+"</div>")
            for j in doc("img"):
                src=PyQuery(j).attr("src")
                if not src.startswith("/media/img"):
                    if _from.startswith("http://") or _from.startswith("https://"):
                        try:
                            _url=myjoin(_from,src)
                            print _url
                            request=urllib2.Request(_url)
                            request.headers["Upgrade-Insecure-Requests"]=1
                            request.headers["User-Agent"]="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.98 Safari/537.36 QQBrowser/4.2.4718.400"
                            request.headers["Accept"]="text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"
                            _imgdata=urllib2.urlopen(request,timeout=3).read()
                            extname="."+ _url.split(".")[-1]
                            if "/" in extname:
                                extname=".jpg"
                            new_name=save_img(_imgdata,extname)
                            print new_name
                        except Exception as e :
                            traceback.print_exc()
                        else:
                            pass
                            j.set("src",new_name)

            content= doc.html()
            mgr.runOperation('''update bx_consult  set content=%s  where zid=%s''',(content,_zid))
            print _zid
    zid=max([ i[0]  for i in result])
    if len(result)<10:
        exit(0)

