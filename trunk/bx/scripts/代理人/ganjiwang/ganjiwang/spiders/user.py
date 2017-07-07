# coding:utf-8
# from newtest.items import DmozItem
# coding:utf-8
import scrapy
from ganjiwang.items import InfoItem
import re,time
import copy
import sys
import math
import MySQLdb.cursors
import MySQLdb as mdb

reload(sys)
sys.setdefaultencoding('utf-8')

###采集赶集网保险招聘信息中的联系人###
class ganjiSpider(scrapy.Spider):
    name = "ganjiSpider"
    allowed_domains = ["ganji.com"]
    start_urls = ["https://3g.ganji.com/"]
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
        yield scrapy.Request('https://3g.ganji.com/hn/?a=c&ifid=shouye_chengshi&backURL=zpbaoxianjingjiren%2F',callback=self.city_list, dont_filter=True)
    def city_list(self, response):
        city_urls = response.xpath('//div[@class="wrap-char"]/ul/li/a/@href').extract()
        city_list = response.xpath('//div[@class="wrap-char"]/ul/li/a/text()').extract()
        for index,url in enumerate(city_urls):
            Item = {"city":city_list[index]}
            URL = "https://3g.ganji.com"+url+"o_%d/?ifid=gj3g_list_previous__list"
            #print URL
            for n in range(1,21):
                yield scrapy.Request(URL%n, callback=self.page_list, dont_filter=True, meta={'item': Item})

    def page_list(self, response):
        item = response.meta['item']
        urls = response.xpath('//div[@class="infor"]/div[@class="deliver-area"]/a/@href').extract()
        companys=response.xpath('//a[@class="infor"]/div[@class="i-else2"]/p[@class="i-company fl"]/text()').extract()
        for index,url in enumerate(urls):
            iTem = copy.copy(item)
            iTem['company']=companys[index].strip()
            iTem['url']="https://3g.ganji.com"+url
            SQL = "SELECT uid FROM agent_caiji_sj WHERE url='%s'"%iTem['url']
            My_cur.execute(SQL)
            result = My_cur.fetchall()
            if result:
                print result, u'该页面已爬过~~~'
            else:
                yield scrapy.Request(iTem['url'], callback=self.page_desc, dont_filter=True, meta={'item': iTem})

    def page_desc(self, response):
        pattern = re.compile(r'1[3,5,7,8]\d{9}|0\d{2,3}-\d{6,8}|0\d{10,11}|\d{7,8}')
        item = response.meta['item']
        item['url'] = response.url
        info_list = response.xpath('//tr/td/text()').extract()
        item['address']=info_list[-6].strip()
        item['name']=info_list[-7].strip()
        item['phone'] = info_list[-8].strip()
        if not item['company'] :
            com=response.xpath('//div[@id="company_info"]/div[@class="comm-area"]/div[@class="comm-name"]/a/text()').extract()
            item['company'] = com[0]
        for a in info_list:
            m = pattern.search(a)
            if m:
                item['phone']=m.group()
                break
        if len(item['name']) > 6 :
            for a in info_list:
                if len(a) < 5 :
                    item['name']=a
        if item['phone'].isdigit():
            return item
        else :
            info_list = response.xpath('//tr/td/text()').extract()
            i=0
            for a in info_list:
                print a,'~~~~~~~~~~',i
                i+=1
            print item['url'],'\r\n'

###采集赶集网保险频道联系人###
class GanjiSpider(scrapy.Spider):
    name = "GanjiSpider"
    allowed_domains = ["ganji.com"]
    start_urls = ["https://3g.ganji.com/"]
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
        yield scrapy.Request('https://3g.ganji.com/hn/?a=c&ifid=shouye_chengshi&backURL=baoxian',callback=self.city_list, dont_filter=True)
    def city_list(self, response):
        city_urls = response.xpath('//div[@class="wrap-char"]/ul/li/a/@href').extract()
        city_list = response.xpath('//div[@class="wrap-char"]/ul/li/a/text()').extract()
        for index,url in enumerate(city_urls):
            Item = {"city":city_list[index]}
            URL = "https://3g.ganji.com"+url+"/o%d/?ifid=gj3g_list_next_huangye"
            for n in range(1,21):
                yield scrapy.Request(URL%n, callback=self.page_list, dont_filter=True, meta={'item': Item})

    def page_list(self, response):
        item = response.meta['item']
        urls = response.xpath('//div[@class="server fuwu-list-quick"]/a[@class="infor"]/@href').extract()
        companys=response.xpath('//a[@class="infor"]/div[@class="iName"]/span[@class="name"]/text()').extract()
        for index,url in enumerate(urls):
            iTem = copy.copy(item)
            iTem['company']=companys[index].strip()
            iTem['url']="https:"+url
            SQL = "SELECT uid FROM agent_caiji_sj WHERE url='%s'"%iTem['url']
            My_cur.execute(SQL)
            result = My_cur.fetchall()
            if result:
                print result, u'该页面已爬过~~~'
            else:
                yield scrapy.Request(iTem['url'], callback=self.page_desc, dont_filter=True, meta={'item':iTem})

    def page_desc(self, response):
        Pattern = re.compile(r'1[3|5|7|8]\d{9}')
        pattern = re.compile(r'1[3,5,7,8]\d{9}|0\d{2,3}-\d{6,8}|0\d{10,11}|\d{7,8}')
        item = response.meta['item']
        item['url'] = response.url
        info_list = response.xpath('//tr/td/text()').extract()
        item['name']=info_list[1].strip()
        if len(info_list) == 4:
            item['name'] = info_list[2].strip()
        address = response.xpath('//div[@class="detail-p01"]/p[@class="address"]/text()').extract()
        item['address'] = address[0]
        phone = response.xpath('//div[@class="tel-area radius"]/a[@class="tel-area-phone"]/span[@class="f15 fc-red"]/text()').extract()
        for a in phone:
            m = Pattern.search(a)
            if m:
                item['phone']=m.group()
                break
            else :
                item['phone'] = phone[0]
        if item['phone'].isdigit():
            return item
        else :
            info_list = response.xpath('//tr/td/text()').extract()
            for a in info_list:
                m = Pattern.search(a)
                if m:
                    item['phone'] = m.group()
                    break
                else:
                    item['phone'] = phone[0]

            #print item['url'],phone,'\r\n'
            return item

##采集赶集网租房频道联系人###
class GanJiSpider(scrapy.Spider):
    name = "GanJiSpider"
    allowed_domains = ["ganji.com"]
    start_urls = ["https://3g.ganji.com/"]
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
        yield scrapy.Request('https://3g.ganji.com/bj/?a=c&ifid=shouye_chengshi',callback=self.city_list, dont_filter=True)
    def city_list(self, response):
        city_urls = response.xpath('//div[@class="wrap-char"]/ul/li/a/@href').extract()
        city_list = response.xpath('//div[@class="wrap-char"]/ul/li/a/text()').extract()
        for index,url in enumerate(city_urls):
            Item = {"city":city_list[index]}
            URL = "https://3g.ganji.com"+url[:-1]+"_fang1/m%d/"
            for n in range(1,300):
                yield scrapy.Request(URL%n, callback=self.page_list, dont_filter=True, meta={'item': Item})

    def page_list(self, response):
        item = response.meta['item']
        urls = response.xpath('//div[@class="list-items"]/a[@class="enter-house"]/@href').extract()
        for index,url in enumerate(urls):
            iTem = copy.copy(item)
            iTem['company']=''
            iTem['url'] = "https://3g.ganji.com"+url
            SQL = "SELECT id FROM bx_toubao_caiji WHERE url='%s'"%iTem['url']
            My_cur.execute(SQL)
            result = My_cur.fetchall()
            if result:
                print result, u'该页面已爬过~~~'
            else:
                yield scrapy.Request(iTem['url'], callback=self.page_desc, dont_filter=True, meta={'item':iTem})

    def page_desc(self, response):
        pattern = re.compile(r'1[3,5,7,8]\d{9}|0\d{2,3}-\d{6,8}|0\d{10,11}|\d{7,8}')
        item = response.meta['item']
        item['url'] = response.url
        item['toubao'] = 1

        name= response.xpath('//div[@class="broker fl-l"]/div/span/text()').extract()
        item['name'] = name[0].strip() if name else ''

        nametype = response.xpath('//div[@class="broker fl-l"]/div/span/em/text()').extract()
        item['nametype'] = nametype[0].strip() if nametype else ''

        area_name = response.xpath('//div[@class="house-xiaoqu"]/a/h2/span[@class="orange"]/text()').extract()
        item['area_name'] = area_name[0].strip() if area_name else ''

        address = response.xpath('//div[@class="house-xiaoqu"]/div[@class="xq-addr cont-padding"]/div[@class="area"]/text()').extract()
        item['address'] = address[0].strip() if address else ''
        item['area']=item['address'].split(':')[1].split('-')[0] if item['address'] else ''

        phone = response.xpath('//div[@class="house-broker js-fixed clear"]/a[@class="tel fl-l"]/@href').extract()
        item['phone']=''
        for a in phone :
            m = pattern.search(a)
            if m:
                item['phone'] = m.group()

        if u'个人' in item['nametype'] :
            return item
        #print item['phone'],item['url'],'~~~~~~~~~~~~~~~~'
