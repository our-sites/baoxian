# coding:utf-8
# from newtest.items import DmozItem
# coding:utf-8
import scrapy
from baixingwang.items import InfoItem
import re,time
import copy
import sys
import math
import MySQLdb.cursors
import MySQLdb as mdb

reload(sys)
sys.setdefaultencoding('utf-8')

###采集百姓网中的保险招聘###
class baixingSpider(scrapy.Spider):
    name = "baixingSpider"
    allowed_domains = ["baixing.com"]
    start_urls = ["http://www.baixing.com/m/"]
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
        yield scrapy.Request('http://www.baixing.com/m/?changeLocation=yes&return=%2Fm%2Fbaoxianzhaopin%2F',callback=self.city_list, dont_filter=True)
    def city_list(self, response):
        info = response.xpath('//html/node()').extract()
        f=open('aaa.html','w')
        f.write(''.join(info))
        f.close()
        city_urls = response.xpath( '//div[@class="content cities"]/ul[@class="cm-grid-list cm-grid-list-flexible"]/li/a/@href').extract()
        city_list = response.xpath( '//div[@class="content cities"]/ul[@class="cm-grid-list cm-grid-list-flexible"]/li/a/text()').extract()
        for index,url in enumerate(city_urls):
            Item = {"city":city_list[index]}
            if url[:1] == 'm' :
                url="baixing.com"+url[1:]
            URL = "http:"+url
            for n in range(1,10):
                yield scrapy.Request(URL+"?page=%d"%n, callback=self.page_list, dont_filter=True, meta={'item': Item})
                #break
            #break

    def page_list(self, response):
        item = response.meta['item']
        urls = response.xpath('//ul[@class="list multiplex gongzuo-list"]/li[@class="item gongzuo"]/a/@href').extract()
        companys=response.xpath('//div[@class="gongzuo-content"]/div[@class="addr-tag"]/span[@class="addr"]/text()').extract()
        for index,url in enumerate(urls):
            iTem = copy.copy(item)
            area_com=companys[index]
            iTem['company']=area_com.split('-')[-1].strip()
            iTem['area'] = area_com.split('-')[0].strip()
            SQL = "SELECT uid FROM agent_caiji_sj WHERE url='%s'"%url
            My_cur.execute(SQL)
            result = My_cur.fetchall()
            if result:
                print result, u'该页面已爬过~~~'
            else:
                yield scrapy.Request(url, callback=self.page_desc, dont_filter=True, meta={'item':iTem})

    def page_desc(self, response):
        pattern = re.compile(r'1[3,5,7,8]\d{9}|0\d{2,3}-\d{6,8}|0\d{10,11}|\d{7,8}')
        item = response.meta['item']
        item['url'] = response.url
        name = response.xpath('//section[@class="user-info"]/a[@class="block gongzuo-block"]/span[@class="contactor"]/text()').extract()
        #company = response.xpath('//div[@class="com"]/div[@class="comWrap"]/h2[@class="c_tit"]/a/text()').extract()
        phone = response.xpath('//div[@class="contact-inner"]/div[@class="contact-container"]/a[@class="contact-btn main-btn"]/@href').extract()
        address = response.xpath('//section[@class="cm-section-content cm-section-content-with-padding content-meta"]/ul[@class="bx-meta-list"]/li[@class="meta-item"]/div/text()').extract()
        if name:
            item['name'] = name[-1].strip().split("：")[-1]
        else:
            name = response.xpath('//section[@class="user-info"]/div[@class="block gongzuo-block"]/span[@class="contactor"]/text()').extract()
            if name:
                item['name'] = name[-1].strip().split("：")[-1]
            else:
                item['name'] = ''

        item['phone'] = ''

        for a in phone:
            m = pattern.search(a)
            if m:
                item['phone'] = m.group()
                break
            else:
                if phone :
                    item['phone'] = phone[0]
                else :
                    item['phone'] = ''

        if address:
            item['address'] = address[-1]
        else:
            item['address'] = ''

        if item['phone']:
            return item
            print "name:",item['name'],"company:",item['company'],"phone:",item['phone'],"address:",item['address'],response.url
        else:
            print '\n\n', item['url'], '~~~~~~~~~~~~~~~~~\r\n\r\n'

###采集百姓网保险频道联系人###
class BaixingSpider(scrapy.Spider):
    name = "BaixingSpider"
    allowed_domains = ["baixing.com"]
    start_urls = ["http://www.baixing.com/"]

    def parse(self, response):
        yield scrapy.Request('http://www.baixing.com/m/?changeLocation=yes&return=%2Fm%2Fzhengzu%2F',
                             callback=self.city_list, dont_filter=True)

    def city_list(self, response):
        # print response.url
        # city_urls = response.xpath('//div[@class="content cities"]/ul[@class="cm-grid-list cm-grid-list-flexible"]/li/a/@href').extract()
        # city_list = response.xpath('//div[@class="content cities"]/ul[@class="cm-grid-list cm-grid-list-flexible"]/li/a/text()').extract()
        city_urls = response.xpath('//div/ul/li/a/@href').extract()
        city_list = response.xpath('//div/ul/li/a/text()').extract()
        for index, url in enumerate(city_urls):
            Item = {"city": city_list[index]}
            URL = "http:" + url
            print URL, city_list[index], '\n'
            for n in range(1, 101):
                print URL + "?page=%d" % n
                yield scrapy.Request(URL + "?page=%d" % n, callback=self.page_list, dont_filter=True,
                                     meta={'item': Item})
                break
            break

    def page_list(self, response):
        item = response.meta['item']
        urls = response.xpath('//div[@class="server fuwu-list-quick"]/a[@class="infor"]/@href').extract()
        companys=response.xpath('//a[@class="infor"]/div[@class="iName"]/span[@class="name"]/text()').extract()
        for index,url in enumerate(urls):
            iTem = copy.copy(item)
            iTem['company']=companys[index].strip()
            yield scrapy.Request("https:"+url, callback=self.page_desc, dont_filter=True, meta={'item':iTem})

    def page_desc(self, response):
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
        item['phone'] = phone[0]
        return item

##采集百姓网租房频道联系人###
class BaiXingSpider(scrapy.Spider):
    name = "BaiXingSpider"
    allowed_domains = ["baixing.com"]
    start_urls = ["http://www.baixing.com/"]
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
        yield scrapy.Request('http://www.baixing.com/m/?changeLocation=yes&return=%2Fm%2Fzhengzu%2F',callback=self.city_list, dont_filter=True)

    def city_list(self, response):
        city_urls = response.xpath('//div/ul/li/a/@href').extract()
        city_list = response.xpath('//div/ul/li/a/text()').extract()
        for index, url in enumerate(city_urls):
            Item = {"city": city_list[index]}
            URL = "http:" + url
            for n in range(1, 11):
                yield scrapy.Request(URL + "?page=%d" % n, callback=self.page_list, dont_filter=True,meta={'item': Item})
                #break
            #break

    def page_list(self, response):
        item = response.meta['item']
        urls = response.xpath('//ul[@class="list show-image multiplex"]/li[@class="item special"]/a/@href').extract()
        address_list = response.xpath('//ul[@class="list show-image multiplex"]/li[@class="item special"]/a/div/div/div/span[@class="addr"]/text()').extract()
        for index,url in enumerate(urls):
            iTem = copy.copy(item)
            iTem['address']=address_list[index]
            SQL = "SELECT id FROM bx_toubao_caiji WHERE url='%s'" % url
            My_cur.execute(SQL)
            result = My_cur.fetchall()
            if result :
                print result, u'该页面已爬过~~~'
            else :
                yield scrapy.Request(url, callback=self.page_desc, dont_filter=True, meta={'item':iTem})

    def page_desc(self, response):
        pattern = re.compile(r'1[3,5,7,8]\d{9}|0\d{2,3}-\d{6,8}|0\d{10,11}|\d{7,8}')
        item = response.meta['item']
        item['url'] = response.url
        item['toubao'] = 1
        info = response.xpath('//div[@class="content-meta"]/ul[@class="bx-meta-list"]/li[@class="meta-item"]/div/text()').extract()
        if info :
            item['nametype'] = info[1]
            item['area_name'] = info[0]
            item['address'] = info[-1]
            item['area']=item['address'].split('-')[0] if item['address'] else ''
        #phone = response.xpath('//div[@class="contact-container"]/a/div[@class="contact-btn-wrapper"]/span[@class="contact-main-txt"]/text()').extract()
        phone = response.xpath( '//div[@class="contact-inner"]/div[@class="contact-container"]/a/@href').extract()
        item['phone']=''
        for a in phone :
            m = pattern.search(a)
            if m:
                item['phone'] = m.group()
        item['name'] = ''
        if item.get('nametype','') and u'经纪人' not in item.get('nametype','') :
            item['name'] = item['nametype']
            return item
