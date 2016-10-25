#coding:utf-8
__author__ = 'admin'
# --------------------------------
# Created by admin  on 2016/10/11.
# ---------------------------------
import MySQLdb
import MySQLdb.cursors
import re
import sys
import redis
import  urllib2
import  urllib
import requests
import shutil
import json
reload(sys)
sys.setdefaultencoding('utf-8')
host='113.10.195.169'
global info_conn
def get_sql_data(cur, sql):
    info = cur.execute(sql)
    sql_data = cur.fetchmany(info)
    return sql_data


def update_data(cur, sql):
    global info_conn
    try:
        cur.execute(sql)
    except Exception,e:
        print e
        info_conn=MySQLdb.connect(host='113.10.195.169',user='dba_user',passwd='gc895316',port=3306,charset='utf8',\
                       db="bx_abc",cursorclass = MySQLdb.cursors.DictCursor)
        cur.execute(sql)
        info_conn.commit()
    else:
        info_conn.commit()


def download_image(url):
    path="/dev/shm/tmp."+url.split('.')[-1]
    headers = { 'User-Agent': 'Mozilla/5.0 (Windows NT 6.0; WOW64; rv:24.0) Gecko/20100101 Firefox/24.0' }
    try:
        req = requests.get(url, stream=True,headers=headers)
    except Exception,e:
        print e,url
        return False
    else:
        if req.status_code == 200:
            with open(path, 'wb') as f:
                req.raw.decode_content = True
                shutil.copyfileobj(req.raw, f)
            return path
        else:
            return False


if __name__ == '__main__':
    res="(http.*?\.(jpg|png|jpeg))"
    res="(http:\/\/[a-z0-9./]+\.(jpg|png|jpeg))"
    sql="select zid,content from bx_consult limit 20"
    mark="mark_id"
    mark_url="mark_url"
    try:
        info_conn=MySQLdb.connect(host='113.10.195.169',user='dba_user',passwd='gc895316',port=3306,charset='utf8',\
                       db="bx_abc",cursorclass = MySQLdb.cursors.DictCursor)
        r=redis.Redis(host='172.16.13.177',port=6379,db=0)
    except Exception,e:
        print e
    else:
        mark_id=r.get(mark)
        if mark_id:
            print mark_id
            sql="select zid,content from bx_consult where zid>"+str(mark_id)+" limit 20"
        cur = info_conn.cursor(cursorclass=MySQLdb.cursors.DictCursor)
        while True:
            data=get_sql_data(cur,sql)
            if data:
                for i in data:
                    re_result=re.findall(res,i["content"],re.IGNORECASE)
                    if re_result:
                        for result in re_result:
                            url=re_result[0][0]
                            print url
                            if "www.baoxiangj.com" in url:
                                print "New image url"
                            else:
                                if r.hget("image_old_new",url):
                                    #新图片
                                    new_url=r.hget("image_old_new",url)
                                    print "old image",re_result[0][0],i["zid"]
                                    #print "update bx_consult set content="+i["content"].replace(url, new_url)+" where zid="+str(i["zid"])
                                    i["content"]=MySQLdb.escape_string(i["content"].replace(url, new_url))
                                    update_data(cur,"update bx_consult set content="+"'"+i["content"]+"'"+" where zid="+str(i["zid"]))
                                else:
                                    download_data=download_image(url)
                                    if download_data:
                                        img_content=open(download_data,"rb").read()
                                        a=urllib2.urlopen("http://img.baoxiangj.com/api/upload_img",data=urllib.urlencode({"extname":"."+url.split('.')[-1],"file":img_content}))
                                        urldata=a.read()
                                        urldata=json.loads(urldata)
                                        new_url="http://www.baoxiangj.com"+urldata["imgurl"]
                                        print "new image",url,new_url,i["zid"]
                                        r.hset("image_old_new",url,new_url)
                                        #print "update bx_consult set content="+i["content"].replace(url, new_url)+" where zid="+str(i["zid"])
                                        i["content"]=MySQLdb.escape_string(i["content"].replace(url, new_url))
                                        update_data(cur,"update bx_consult set content="+"'"+i["content"]+"'"+" where zid="+str(i["zid"]))
                                        #break
                                    else:
                                        print "Download image error........"

                print i["zid"]
                r.set(mark,i["zid"])
                sql="select zid,content from bx_consult where zid>"+str(i["zid"])+" limit 20"
            else:
                cur.close()
                info_conn.close()
                break


# img_content=open("./baidu.png","rb").read()
#
# a=open("baidu1.png","wb")
# a.write(img_content)
# a.close()
#
# a=urllib2.urlopen("http://img.baoxiangj.com/api/upload_img",data=urllib.urlencode({"extname":".png","file":img_content}) )
# #使用说明：
# # 地址：  http://img.baoxiangj.com/api/upload_img
# # 传参形式： post
# # 参数： file  文件内容
# # 参数： extname 文件的扩展名
# # 返回数据如下：
# #  {"status": true, "imgurl": "/media/img/2885cdb57f913ed832df4a0731bdc765.png", "filename": "2885cdb57f913ed832df4a0731bdc765.png"}
# #  imgurl 为这个文件的访问地址
# #  filename 为这个文件在服务器中的文件名
# print a.read()
