#from newtest.items import DmozItem
#coding:utf-8
import scrapy
import MySQLdb
import MySQLdb.cursors
import urllib2
import json
from xiangrikui.items import  UserItem
import re
import copy
from scrapy.http import FormRequest
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
info_conn=MySQLdb.connect(host='172.16.13.177',user='root',passwd='123456',port=3306,charset='utf8',\
                       db="bx_abc",cursorclass = MySQLdb.cursors.DictCursor)
cur = info_conn.cursor()
class XiangrikuiSpider(scrapy.Spider):
    name = "XiangrikuiSpider"
    allowed_domains = ["www.baoxian360.net"]
    start_urls=[]
    for i in range(1,901):
            start_urls.append("http://www.baoxian360.net/index.asp?page="+str(i))
    #start_urls=start_urls[0:1]
    start_urls=["http://www.baoxian360.net"]
    def parse(self, response):
        for i in range(1,901):
            yield FormRequest(url="http://www.baoxian360.net/index.asp?page="+str(i),
                                                formdata={'age1':'18','age2':'65','sex':'0','education':'0','atplace':'0','type':'0'},
                                                callback=self.people_info)
    def people_info(self,response):
        urls,count=[],0
        for sel in response.xpath('//table/tr/td[@class="f"]'):
            url_info=sel.xpath('font[@size="-1"]/a[@class="m"]/@href').extract()
            for url in url_info:
                if "http" in url:
                    urls.append(url)
            item={}
            for index,data in enumerate(sel.xpath('font[@size="-1"]/text()').extract()):
                ans=''.join(re.findall(u'[\u2E80-\u9FFF\u3002\uff1b\uff0c\uff1a\u201c\u201d\uff08\uff09\u3001\uff1f\u300a\uff01\u300ba-zA-Z0-9\[\]\{\}%]+',data))
                if ans and len(data)>10:
                    if (u"男" in data or u"女" in data ) and u"岁" in data:
                        tt=data.split('　')
                        item["name"]=tt[0]
                        if tt[1]==u"女":
                            item["sex"]=0
                        else:
                            item["sex"]=1
                        age=tt[2].split('岁')[0]
                        item["age"]=age
                        item["xueli"]=tt[3]
                        item["tttcity"]=tt[4]
                        item["company_name"]=tt[5]
                    else:
                        if u"执业证号:" in data:
                            t2=data.split('，')[1:]
                            item["evelop_code"]=None
                            item["tel"]=None
                            item["phone"]=None
                            item["email"]=None
                            item["info_url"]=urls[count]
                            count=count+1
                            for i in t2:
                                if u"执业证号" in i:
                                    if len(i.split(":"))>1:
                                        item["evelop_code"]=str(i.split(":")[-1])
                                    else:
                                        item["evelop_code"]=None
                                elif 'Tel:' in i:
                                    if len(i.split(":"))>1:
                                        item["tel"]=i.split(":")[-1]
                                    else:
                                        item["tel"]=None
                                elif 'MP:' in i:
                                    if len(i.split(":"))>1:
                                        item["phone"]=i.split(":")[-1]
                                    else:
                                        item["phone"]=None
                                elif 'Email:' in i:
                                    if len(i.split(":"))>1:
                                        item["email"]=i.split(":")[-1]
                                    else:
                                        item["email"]=None
                            item["weizhi"]=t2[-1]
                            item["city"]=item["tttcity"].split('省')[-1].split('市')[0]
                            try:
                                cur.execute("insert into bx_vipuser_360baoxian(uid,bx_com,sex ,age,xueli,city,info_url,phone,email,evelop_code,tel,real_name) \
                values(NULL ,'%s','%s','%s','%s','%s', '%s','%s', '%s','%s','%s','%s')" %(item['company_name'], item['sex'],item['age'],item["xueli"], \
                                                                     item['city'],item['info_url'],\
                                                                     item['phone'],item["email"],item["evelop_code"],item["tel"],item["name"]))
                            except Exception,e:
                                #print e
                                pass
                            finally:
                                info_conn.commit()