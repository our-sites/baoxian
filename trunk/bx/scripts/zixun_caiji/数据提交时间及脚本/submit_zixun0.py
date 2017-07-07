#! /usr/bin/env python
# coding:utf8
# Create your views here.
#Write By Chou
import MySQLdb
import MySQLdb.cursors
import time
import urllib
import urllib2
import json
import sys

reload(sys)
sys.setdefaultencoding('utf8')

def post(url, data):
    req = urllib2.Request(url)
    data = urllib.urlencode(data)
    # enable cookie
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor())
    response = opener.open(req,data)
    return response.read()


def today_first_time():
    return int(time.time() - (time.time() % 86400) + time.timezone)


def get_info(info_conn,sql):
    cur = info_conn.cursor()
    info = cur.execute(sql)
    sql_data = cur.fetchmany(info)
    cur.close()
    return sql_data


if __name__ == '__main__':
    posturl = "https://www.bao361.cn/zixun/add_xinwen/"
    try:
        info_conn = MySQLdb.connect(host='118.89.220.36', user='mha_user', passwd='gc895316', port=3306, charset='utf8', \
                                    db="bx_caiji", cursorclass=MySQLdb.cursors.DictCursor)
        tmp_curl = info_conn.cursor()
    except Exception, e:
        print e
    else:
        assert_data= get_info(info_conn, "SELECT id FROM zixun WHERE publishtime > " + str(today_first_time()) + " AND online_id>0")
        if len(assert_data) < 300 and time.localtime(time.time()).tm_hour > 18 :
               SQL="SELECT id,writer,url,title,content FROM zixun WHERE online_id=0 AND LENGTH(content)>100 ORDER BY id DESC LIMIT 50"
        else :
               SQL="SELECT id,writer,url,title,content FROM zixun WHERE publishtime>="+ str(today_first_time()) + " AND online_id=0" 
        sql_data = get_info(info_conn, SQL)
        for data in sql_data:
            data["from"] = data["url"]
            data['secret'] = 'gc7232275'
            return_data = post(posturl, data)
            try:
                return_data = json.loads(return_data)
                #print return_data
                if return_data["status"] == True:
                    #print ("update zixun set online_id =%s where id='%s'" % (return_data["zid"], data["id"]))
                    tmp_curl.execute("update zixun set online_id =%s where id='%s'" % (return_data["zid"], data["id"]))
                    info_conn.commit()
                else:
                    if return_data["status"]==False and "has exists" in return_data["message"]:
                        #print ("update zixun set online_id =%s where id='%s'" % ("-111", data["id"]))
                        #此时表示该url由于其他原因已经被采集了但是未修改online_id
                        tmp_curl.execute("update zixun set online_id =%s where id='%s'" % ("-111", data["id"]))
                        info_conn.commit()
                    else:
                        print return_data, data["id"]
            except Exception, e:
                print e
                break
        tmp_curl.close()
        info_conn.close()
