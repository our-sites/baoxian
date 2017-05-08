# from newtest.items import DmozItem
# coding:utf-8
import scrapy
from zaobao.items import InfoItem
import re,time
import copy
import sys
import math
import MySQLdb.cursors
import MySQLdb as mdb

reload(sys)
sys.setdefaultencoding('utf-8')

###仅采集联合早报第一页中最新的内容###
class ZaoBaoSpider(scrapy.Spider):
    name = "ZaoBaoSpider"
    allowed_domains = ["zaobao.com"]
    start_urls = ["http://www.zaobao.com"]
    def parse(self, response):
        KW=['保险','社保','医保','工伤','公积金','养老','生育','养老金']
        for kw in KW :
            yield scrapy.Request('http://www.zaobao.com/search/site/%s'%kw, callback=self.page_list, dont_filter=True)
    def page_list(self, response):
        urls = response.xpath('//li[@class="search-result"]/a/@href').extract()
        Time = response.xpath('//li[@class="search-result"]/div[@class="search-snippet-info"]/span[@class="search-info"]/node()').extract()
        TIME=int(time.mktime(time.strptime(time.strftime('%Y%m%d',time.localtime(time.time())), "%Y%m%d")))
        for index,url in enumerate(urls):
            publishtime = int(time.mktime(time.strptime(' '.join(Time[index].split()), "%Y-%m-%d %H:%M")))
            Item = {}
            Item['url'] = 'http://www.zaobao.com/'+url
            Item['publishtime']=publishtime
            if publishtime > TIME :
                yield scrapy.Request(Item['url'], callback=self.page_desc, dont_filter=True,meta={'item': Item})
            else :
                yield scrapy.Request(Item['url'], callback=self.page_desc, dont_filter=True,meta={'item': Item})
                pass
    def page_desc(self, response):
        p_pattern = re.compile(r"<p.*</p>|.*<strong><span.*</span></strong>.*")
        item = response.meta['item']
        item['url'] = response.url
        title=response.xpath('//div[@class="body-content"]/h1/text()').extract()[0]
        Writer=response.xpath('//div[@class="body-content"]/aside/span[@class="contributor meta-byline"]/a/text()').extract()[0]
        item['keyword']=""
        info=response.xpath('//div[@id="FineDining" and @class="article-content-container"]/node()').extract()
        Info =[ i.replace("'",'"') for i in info if p_pattern.match(i) ]
        item['type'] = 0
        item['title'] = title
        item['content']=''.join([ I.replace("<p>",'<p>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;') for I in  Info ])
        item['writer']=Writer
        return item

