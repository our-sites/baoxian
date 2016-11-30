#from newtest.items import DmozItem
#coding:utf-8

import time
import scrapy
import MySQLdb
import MySQLdb.cursors
import sys
import json
reload(sys)
sys.setdefaultencoding('utf-8')
info_conn=MySQLdb.connect(host='172.16.13.177',user='root',passwd='123456',port=3306,charset='utf8',\
                       db="bx_abc",cursorclass = MySQLdb.cursors.DictCursor)

def get_sql_data(conn, sql):
    cur = conn.cursor(cursorclass=MySQLdb.cursors.DictCursor)
    info = cur.execute(sql)
    sql_data = cur.fetchmany(info)
    cur.close()
    return sql_data

def update_data(conn, sql):
    cur = conn.cursor()
    cur.execute(sql)
    conn.commit()
    cur.close()


class MobileSpider(scrapy.Spider):
    name = "MobileSpider"
    allowed_domains = ["bxr.im"]
    start_urls =[]
    website_possible_httpstatus_list=[302,301,200]
    sql="select info_url from bx_vipuser where info_mark=0 limit 200"
    sql_data=get_sql_data(info_conn,sql)
    for i in sql_data:
        start_urls.append(i["info_url"])
    #start_urls = ["http://bxr.im/2137769","http://bxr.im/1423255"]
    #start_urls = ["http://bxr.im:9099/1423255"]
    def parse(self, response):
            print request.meta
            request.meta["change_proxy"] = True
            sql_tmp=[]
            try:
                response_data=response.xpath('//textarea[@id="profile"]/text()').extract()[0]
            except:
                print "begin"
                header_url=response.xpath('//img[@id="share-img"]').extract()[0].split('"')[-2]
                tags=",".join(response.xpath('//div[@class="tag"]/ul/li/text()').extract())
                phone=response.xpath('//div[@class="nav-contact-list"]/a/@href').extract()[0].split(':')[-1]
                print header_url,tags,phone
                sql="update bx_vipuser set img_url='%s',bx_type='%s',phone='%s',info_mark=1 where info_url='%s'" %(header_url,tags,phone,response.url)
                #sql_tmp.append(sql)
                print sql
                update_data(info_conn, sql)
            else:
                data=json.loads(response_data)
                username=data["username"]
                weixin=data["profile"]["wx_no"]
                qq=data["profile"]["qq"]
                phone=data["profile"]["phone"]
                header_url=data["profile"]["small_header_image"]
                point=data["growing"]["point"]
                grade=data["growing"]["grade"]
                tags=",".join(data["tags"])
                if not weixin:
                    weixin='0'
                if not qq:
                    qq="0"
                if not phone:
                    phone="0"
                sql="update bx_vipuser set img_url='%s',bx_type='%s',phone='%s',username='%s',weixin='%s',qq='%s',phone='%s',score='%s',stars='%s',info_mark=1 where info_url='%s'" \
                    %(header_url,tags,phone,username,weixin,qq,phone,point,grade,response.url)
                print sql
                update_data(info_conn, sql)