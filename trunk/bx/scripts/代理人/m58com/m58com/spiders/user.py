# coding:utf-8
# from newtest.items import DmozItem
# coding:utf-8
import scrapy
from m58com.items import InfoItem
import re,time
import copy
import sys
import math
import MySQLdb.cursors
import MySQLdb as mdb

reload(sys)
sys.setdefaultencoding('utf-8')

###采集58同城网中的保险招聘###
class m58comSpider(scrapy.Spider):
    name = "m58comSpider"
    allowed_domains = ["58.com"]
    start_urls = ["http://m.58.com/bz/baoxian/"]
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
        yield scrapy.Request('http://m.58.com/city.html?from=click_city_new',callback=self.city_list, dont_filter=True)
    def city_list(self, response):
        city_urls = response.xpath( '//div[@class="city_box"]/ul[@class="city_lst"]/li/a/@href').extract()
        city_list = response.xpath( '//div[@class="city_box"]/ul[@class="city_lst"]/li/a/text()').extract()
        for index,url in enumerate(city_urls):
            Item = {"city":city_list[index]}
            URL = url+"baoxian/pn%d/"
            for n in range(1,11):
                yield scrapy.Request(URL%n, callback=self.page_list, dont_filter=True, meta={'item': Item})
                #break
            #break

    def page_list(self, response):
        item = response.meta['item']
        urls = response.xpath('//div[@class="infolst_w"]/ul[@class="infoList"]/li[@class="item"]/a[@class="item-content"]/@href').extract()
        #companys=response.xpath('//a[@class="infor"]/div[@class="i-else2"]/p[@class="i-company fl"]/text()').extract()
        for index,url in enumerate(urls):
            iTem = copy.copy(item)
            # iTem['company']=companys[index].strip()
            SQL = "SELECT uid FROM agent_caiji_sj WHERE url='%s'" % url
            My_cur.execute(SQL)
            result = My_cur.fetchall()
            if result:
                print result, u'该页面已爬过~~~'
            else:
                yield scrapy.Request(url, callback=self.page_desc, dont_filter=True, meta={'item': iTem})

    def page_desc(self, response):
        pattern = re.compile(r'1[3,5,7,8]\d{9}|0\d{2,3}-\d{6,8}|0\d{10,11}|\d{7,8}')
        item = response.meta['item']
        item['url'] = response.url

        name=response.xpath('//div[@class="com"]/div[@class="comWrap"]/div[@class="contact"]/span/text()').extract()
        company = response.xpath('//div[@class="com"]/div[@class="comWrap"]/h2[@class="c_tit"]/a/text()').extract()
        phone = response.xpath('//div[@class="com"]/div[@class="phoneWrap"]/a/@phoneno').extract()
        address = response.xpath('//ul/li/span[@class="attrValue dizhiValue"]/a/text()').extract()
        if name :
            item['name'] =name[-1].strip()
        else :
            item['name'] = ''
        if company :
            item['company'] = company[0].strip()
        else:
            item['company'] = ''
        for a in phone:
            m = pattern.search(a)
            if m:
                item['phone']=m.group().strip()
                break
            else :
                item['phone'] =phone[0].strip()
        if address :
            item['address'] = '-'.join(address)
        else:
            item['address'] = ''
        if item['phone'] :
            return item
        else :
            print '\n\n',item['url'],'\r\n\r\n'


##采集58同城网租房频道联系人###
class M58COMSpider(scrapy.Spider):
    name = "M58COMSpider"
    allowed_domains = ["58.com"]
    start_urls = ["http://m.58.com/"]
    global Mysql_conf,My_cxn,My_cur
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
        yield scrapy.Request('http://m.58.com/city.html?from=click_city_new',callback=self.city_list, dont_filter=True)

    def city_list(self, response):
        city_urls = response.xpath('//ul[@class="city_lst"]/li/a/@href').extract()
        city_list = response.xpath('//ul[@class="city_lst"]/li/a/text()').extract()
        city_list.reverse()
        city_urls.reverse()

        for index, url in enumerate(city_urls):
            Item = {"city": city_list[index]}
            URL =url+"zufang/pn%d/?58ihm=m_house_index_zufang_zhengzu&58cid=342&PGTID=0d200001-0015-6ccc-8249-10df5490d5e5&ClickID=1"
            for n in range(11, 1, -1):
                yield scrapy.Request(URL% n, callback=self.page_list, dont_filter=True,meta={'item': Item})
                #break
            #break

    def page_list(self, response):
        item = response.meta['item']
        urls = response.xpath('//ul[@class="infoList infoL"]/li[@class="item"]/a/@href').extract()
        for index,url in enumerate(urls):
            iTem = copy.copy(item)
            SQL="SELECT id FROM bx_toubao_caiji WHERE url='%s'"%url
            My_cur.execute(SQL)
            result=My_cur.fetchall()
            if result :
                print result,u'该页面已爬过~~~'
            else :
                yield scrapy.Request(url, callback=self.page_desc, dont_filter=True, meta={'item':iTem})

    def page_desc(self, response):
        if "callback.58.com/firewall/valid" in response.url:
            My_cxn = MySQLdb.connect(**Mysql_conf)
            My_cur = My_cxn.cursor()
            print  '~~~1~~~2~~~3~~~4~~~',response.url
        else :
            pattern = re.compile(r'1[3,5,7,8]\d{9}|0\d{2,3}-\d{6,8}|0\d{10,11}|\d{7,8}')
            item = response.meta['item']
            item['url'] = response.url
            item['toubao'] = 1

            phone = response.xpath('//ul[@class="user-contact"]/li/a[@class="icon-tel phoneNumber"]/@phone').extract()
            area_name = response.xpath('//div[@class="body-content"]/ul[@class="houseInfo-meta bbOnepx"]/li/span/text()').extract()
            if not area_name :
                print item['url'],'\n\n~~~~~~~~~~~~~\n\n'
            item['area_name'] = area_name[0].split('小区:')[-1].strip()
            name = response.xpath('//div[@class="user"]/ul[@class="user-profile"]/li[@class="profile"]/span/text()').extract()
            if name :
                item['name'] = name[0].strip()
            else :
                name = response.xpath('//div[@class="card_top"]/div[@class="personal_des"]/p[@class="name"]/text()').extract()
                try :
                    item['name'] = name[0].strip()
                except :
                    item['name'] = ''
            if not phone :
                phone = response.xpath('//div[@class ="linkManMsg"]/div[@class="IconBottom"]/a[@class="LinkPhone"]/@phone').extract()
            if not phone :
                phone = response.xpath('//div[@class="user"]/ul[@class="user-profile"]/li[@class="meta"]/span/text()').extract()

            item['phone'] = ''
            for a in phone:
                m = pattern.search(a)
                if m:
                    item['phone'] = m.group().strip()
            info = response.xpath('//div[@class="body-content"]/div[@class="body-content"]/ul[@class="houseInfo-detail bbOnepx"]/li/i/text()').extract()
            if info :
                item['address'] = info[-1]
                item['area']=item['address'].split('-')[0] if item['address'] else ''
            else :
                item['address']=''
                item['area']=''
            if  u'经纪人' not in name :
                return item

