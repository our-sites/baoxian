# coding:utf-8
# from newtest.items import DmozItem
# coding:utf-8
import scrapy
from xmly.items import InfoItem
import copy
import time
import sys
import MySQLdb.cursors
import MySQLdb as mdb


reload(sys)
sys.setdefaultencoding('utf-8')

##搜库视频采集###
class xmlySpider(scrapy.Spider):
    name = "xmlySpider"
    allowed_domains = ["soku.com"]
    start_urls = ["http://www.soku.com"]
    global Mysql_conf, My_cxn, My_cur
    Mysql_conf = {
        'host': '172.16.13.165',
        'user': 'mha_user',
        'passwd': 'gc895316',
        'db': 'bx_caiji',
        'charset': 'utf8',
        'init_command': 'set autocommit=0',
        'cursorclass': MySQLdb.cursors.DictCursor
    }
    My_cxn = MySQLdb.connect(**Mysql_conf)
    My_cur = My_cxn.cursor()
    def parse(self, response):
        kws=[u'保险']
        URL="http://www.ximalaya.com/search/%s/t3p%d"
        for kw in kws:
            for page in range(1,51,1) :
                url = URL%(kw,page)
                yield scrapy.Request(url,callback=self.page_list, dont_filter=True,meta={'item':{"kw":kw}})

    def page_list(self, response):
        item = response.meta['item']
        albums= response.xpath('//li[@class="item"]/div[@class="content_wrap2"]/div[@class="info title"]/a/text()').extract()
        urls = response.xpath('//li[@class="item"]/div[@class="content_wrap2"]/div[@class="info title"]/a/@href').extract()
        writers=response.xpath('//li[@class="item"]/div[@class="content_wrap2"]/div[@class="info last"]/a/text()').extract()
        for index,url in enumerate(urls):
            iTem = copy.copy(item)
            iTem['url']="http://www.ximalaya.com"+url
            iTem['album'] = albums[index].strip()
            iTem['writer'] = writers[index].strip()
            yield scrapy.Request(iTem['url'], callback=self.page_desc, dont_filter=True, meta={'item': iTem})

    def page_desc(self, response):
        item = response.meta['item']
        titles= response.xpath('//ul/li/div[@class="miniPlayer3"]/a[@class="title"]/text()').extract()
        urls = response.xpath('//ul/li/div[@class="miniPlayer3"]/a[@class="title"]/@href').extract()
        times = response.xpath('//ul/li/div[@class="miniPlayer3"]/div[@class="operate"]/span/text()').extract()
        for index,url in enumerate(urls):
            ITem = copy.copy(item)
            ITem['url']="http://www.ximalaya.com"+url
            ITem['title'] = titles[index].strip()
            ITem['pubtime'] = time.mktime(time.strptime(times[index], "%Y-%m-%d"))
            SQL = "SELECT id FROM bx_yinpin WHERE url='%s'"%ITem['url']
            My_cur.execute(SQL)
            result = My_cur.fetchall()
            if result:
                print result, u'~~~该页面已爬过~~~'
            else:
                self.insert_data(ITem,My_cxn,My_cur)


    ###将采集到的数据插入数据库###
    def insert_data(self,data,My_cxn,My_cur):
        try :
            My_cxn.ping()
        except :
            My_cxn = MySQLdb.connect(**Mysql_conf)
            My_cur = My_cxn.cursor()
        SQL = """INSERT INTO bx_yinpin(id,title,url,kw,pubtime,writer,album)
                              VALUES(NULL,'%s','%s','%s',%s,'%s','%s')"""
        try :
            My_cur.execute(SQL%(data.get('title',''),data.get('url',''),data.get('kw',''),data.get('pubtime',0),data.get('writer',''),data.get('album','')))
            id = int(My_cur.lastrowid)
        except :
            id = 0
        if id :
            My_cxn.commit()
            return True
        else :
            return False
