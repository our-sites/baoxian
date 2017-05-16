# from newtest.items import DmozItem
# coding:utf-8
import scrapy
from bx58.items import InfoItem
import re,time
import copy
import sys
import math
import MySQLdb.cursors
import MySQLdb as mdb

reload(sys)
sys.setdefaultencoding('utf-8')
###采集签单分享所有内容###
class bx58Spider(scrapy.Spider):
    name = "bx58Spider"
    allowed_domains = ["bx58.cn"]
    start_urls = ["http://www.bx58.com"]
    def parse(self, response):
        for i in range(1,2322) :
            yield scrapy.Request('http://www.bx58.com/share/%s.html'%i, callback=self.page_list, dont_filter=True)
    def page_list(self, response):
        Title_list = response.xpath('//ul[@class="list clearfix"]/li/div[@class="txt"]/div[@class="tat"]/a/text()').extract()
        Url_list = response.xpath('//ul[@class="list clearfix"]/li/div[@class="txt"]/div[@class="tat"]/a/@href').extract()
        Info_list = response.xpath('//ul[@class="list clearfix"]/li/div[@class="txt"]/p[@class="tat1"]/i/text()').extract()
        LIST=[]
        for index,url in enumerate(Url_list):
            LIST=Info_list[index*4:(index+1)*4]
            item={'url':url,'title':Title_list[index],'province':LIST[1],'company':LIST[2],'name':LIST[0],'flag':1}
            yield scrapy.Request(item['url'], callback=self.page_desc, dont_filter=True,meta={'item': item})
    def page_desc(self, response):
        item = response.meta['item']
        item['url'] = response.url
        info= response.xpath('//div[@class="txt4"]/div[@class="tb"]/p/text()').extract_unquoted()
        if not info :
            info= response.xpath('//div[@class="txt4"]/div[@class="tb"]/node()').extract_unquoted()
        Info = [i.replace(item['name'],'').replace('保险同城','保险管家').strip() for i in info]
        item['info']=''.join(Info)
        return item
        #print item['info']


###采集增员分享所有内容###
class BX58Spider(scrapy.Spider):
    name = "BX58Spider"
    allowed_domains = ["bx58.com"]
    start_urls = ["http://www.bx58.com"]
    def parse(self, response):
        for i in range(1,459) :
            yield scrapy.Request('http://www.bx58.com/share/%s.html?chk=1'%i, callback=self.page_list, dont_filter=True)
    def page_list(self, response):
        Title_list = response.xpath('//li/div[@class="txt"]/div[@class="tat"]/a/text()').extract()
        Url_list = response.xpath('//li/div[@class="txt"]/div[@class="tat"]/a/@href').extract()
        Info_list = response.xpath('//li/div[@class="txt"]/p[@class="tat1"]/i/i/text()').extract()
        LIST=[]
        for index,url in enumerate(Url_list):
            LIST=Info_list[index*4:(index+1)*4]
            item={'url':'http://www.bx58.com'+url,'title':Title_list[index],'province':LIST[1],'company':LIST[2],'name':LIST[0],'flag':2}
            yield scrapy.Request(item['url'], callback=self.page_desc, dont_filter=True,meta={'item': item})
    def page_desc(self, response):
        item = response.meta['item']
        item['url'] = response.url
        info= response.xpath('//div[@class="com_antxt"]/div[@class="txt4"]/div[@class="tb"]/span/text()').extract_unquoted()
        if not info :
            info= response.xpath('//div[@class="com_antxt"]/div[@class="txt4"]/div[@class="tb"]/node()').extract_unquoted()
        Info = [i.replace(item['name'],'').replace('保险同城','保险管家').strip() for i in info]
        item['info']=''.join(Info)
        return item
        #print item['info'],item['url']



###采集案例分析所有内容###
class Bx58Spider(scrapy.Spider):
    name = "Bx58Spider"
    allowed_domains = ["bx58.com"]
    start_urls = ["http://www.bx58.com"]
    def parse(self, response):
        conn = MySQLdb.connect(
        host='172.16.13.165',
        port = 3306,
        user='root',
        passwd='123456',
        db ='bx_caiji',charset="utf8" )
        cur = conn.cursor(cursorclass = MySQLdb.cursors.DictCursor)
        cur.execute("SELECT province,province_id,company,cid,url FROM fenxiang WHERE flag=1")
        for item in cur.fetchall() :
            item['flag']=3
            url=item['url']
            yield scrapy.Request('http://'+url.split('/')[2]+'/mycase.html', callback=self.page_list, dont_filter=True,meta={'item': item})
    def page_list(self, response):
        item = response.meta['item']
        Url_list = response.xpath('//div[@class="com_ant"]/div[@class="page"]/a/@href').extract()
        for url in Url_list[:-1]:
            yield scrapy.Request(url, callback=self.page_desc, dont_filter=True,meta={'item': item})
        else :
            yield scrapy.Request(response.url, callback=self.page_desc, dont_filter=True,meta={'item': item})
            
    def page_desc(self, response):
        item = response.meta['item']
        item['url'] = response.url
        URL_list=response.xpath('//div[@class="com_ant"]/ul[@class="list clearfix"]/li/div[@class="txt"]/a/@href').extract()
        if not URL_list :
            print response.url,'~~~ERR~~~~~ERR~~~~~~ERR~~~123~~~'
            #info= response.xpath('//div[@class="com_antxt"]/div[@class="txt4"]/div[@class="tb"]/node()').extract_unquoted()
        for url in URL_list:
            yield scrapy.Request(url, callback=self.page_Desc, dont_filter=True,meta={'item': item})
    def page_Desc(self, response):
        item = response.meta['item']
        item['url'] = response.url
        Title = response.xpath('//div[@class="index_conl index_conla"]/div[@class="com_antxt"]/div[@class="txt1"]/text()').extract()
        info = response.xpath('//div[@class="com_antxt"]/div[@class="txt4"]/node()').extract_unquoted()
        if not Title :
            print response.url,'~~~ERR~~~~~ERR~~~~~~ERR~~~'
            #info= response.xpath('//div[@class="com_antxt"]/div[@class="txt4"]/div[@class="tb"]/node()').extract_unquoted()
        Info = [i.replace('保险同城','保险管家').strip().replace("'",'"') for i in info]
        item['info']=''.join(Info)
        item['title']=''.join(Title)
        return item
        #print item['info'],item['url']
