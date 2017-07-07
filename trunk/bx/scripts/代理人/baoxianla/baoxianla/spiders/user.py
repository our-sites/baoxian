# coding:utf-8
# from newtest.items import DmozItem
# coding:utf-8
import scrapy
from baoxianla.items import InfoItem
import re,time
import copy
import sys
import math
import MySQLdb.cursors
import MySQLdb as mdb

reload(sys)
sys.setdefaultencoding('utf-8')

###采集保险啦中的保险人信息###
class baoxianlaSpider(scrapy.Spider):
    name = "baoxianlaSpider"
    allowed_domains = ["baoxianla.com"]
    start_urls = ["http://www.baoxianla.com/dailiren"]
    def parse(self, response):
        for n in xrange(1,133):
            yield scrapy.Request('http://www.baoxianla.com/dailiren/?page=%d'%n,callback=self.page_list, dont_filter=True)

    def page_list(self, response):
        pattern = re.compile(r'\d{5,11}')
        Pattern = re.compile(r"\d")
        info = response.xpath('//div[@class="bx_agenlist"]/div[@class="bx_aglist"]/div')
        user_list=[]
        for i in info :
            item={}
            item['name'] = i.xpath('div/h4/a/text()').extract()[0]
            QQ=i.xpath('div/ul/li/a[@class="contact_qq"]/@href').extract()

            m = pattern.search(QQ[0])
            if m :
                item['qq']=m.group()
            else :
                item['qq']=0
            phone = i.xpath('div/ul/li/a/@title').extract()
            item['phone'] = phone[0]
            url = i.xpath('div/ul/li/a/@href').extract()
            item['url']=url[0]
            INFO = i.xpath('div[@class="bx_psimg"]/p/text()').extract()
            M = Pattern.search(INFO[0])
            if M :
                item['work'] = M.group()
            else :
                item['work']=0
            item['city'] = INFO[0].split()[0]
            item['company'] = INFO[0].split()[1].split()[0]
            item['zige'] = INFO[1][5:]
            yield scrapy.Request('http://www.baoxianla.com/',callback=self.page_desc, dont_filter=True,meta={'item':item})
    def page_desc(self, response):
            item = response.meta['item']
            return item
