#coding:utf-8
__author__ = 'admin'
# --------------------------------
# Created by admin  on 2016/10/14.
# ---------------------------------



import  datetime
import  time
import  MySQLdb
import json
from pyquery import  *
import  urllib2
from urlparse import  *
from posixpath import  *
import  urllib
import traceback
from threadspider.utils.db import  MySQLMgr

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


pid=0
while 1:
    conn=MySQLdb.connect(host="118.89.220.36",port=3306,user="bx_user",passwd="gc895316")
    cursor=conn.cursor()
    cursor.execute("select pid,pro_desc_content from bx_abc.bx_product  WHERE pid>%s  ORDER by pid asc limit 30",(pid,))
    data= cursor.fetchall()
    cursor.close()
    conn.close()

    for _pid,_reason  in  data:
        print _pid
        if not _reason:
            pass
        else:
            doc=PyQuery("<div>"+ _reason+"</div>")
            for j in doc("img"):
                src=PyQuery(j).attr("src")
                if src:
                    if src.startswith("//"):
                        src="http"+src
                    if src.startswith("http"):
                        pass

                if src and src.startswith("http"):
                    try:
                        _url=src
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
                        doc(j).remove()
                    else:
                        pass
                        j.set("src",new_name)

            content= doc.html()
            #print mgr.runOperation('''update bx_product  set  pro_desc_content=%s  where pid =%s''',(content,_pid))
    if not data or len(data)<30 :
        break
    else:
        pid=max([i[0] for i in data])









