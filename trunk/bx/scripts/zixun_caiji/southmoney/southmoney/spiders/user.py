# -*- coding: utf-8 -*-
# from newtest.items import DmozItem
# coding:utf-8
import scrapy
from southmoney.items import InfoItem
import re,time
import copy
import sys
import math
import MySQLdb.cursors
import MySQLdb as mdb
import requests,json

reload(sys)
sys.setdefaultencoding('utf-8')

###采集社保网的数据###
class SouthmoneySpider(scrapy.Spider):
    name = "SouthmoneySpider"
    allowed_domains = ["southmoney.com"]
    start_urls = ["http://shebao.southmoney.com"]
    def parse(self, response):
        yield scrapy.Request('http://shebao.southmoney.com/', callback=self.homepage_list, dont_filter=True)
    def homepage_list(self, response):
        urls = response.xpath('//div[@class="column" or @class="center_col" or class="list2"]/ul/li/a/@href').extract()
        for url in urls:
            Url="http://shebao.southmoney.com"+url
            yield scrapy.Request(Url, callback=self.page_list, dont_filter=True)
    def page_list(self, response):
        url=response.url
        url_list=[url]
        R = requests.get(url)
        m=re.findall(r'(\d+_\d+\.html)+',R.text)
        item={'source':'社保网','keyword':'','type':0,'publishtime':int(time.time()),'title':'','writer':'','content':''}
        if m :
            _max=1
            for _m in m:
                _Max=int(_m.split('.html')[0].split('_')[-1])
                _max = _Max if _max < _Max else _max
            for page in range(2,_max+1):
                url_list.append(url.split('.html')[0]+'_'+str(page)+'.html')
            for _url in  url_list :
                yield scrapy.Request(_url, callback=self.page_desc, dont_filter=True,meta={'item': item})
        else :
            yield scrapy.Request(url, callback=self.page_desc, dont_filter=True,meta={'item': item})

    def page_desc(self, response):
        p_pattern = re.compile(r"<p.*</p>|<div.*<img\sclass.*>")
        P = re.compile(r"http://shebao.southmoney.com/.*/\d+_\d+.html")
        strinfo = re.compile('''<a.*\.southmoney\.com.*>|</a>|<p align="center"><b>.*</b></p>''')
        item = response.meta['item']
        item['url'] = response.url
        R = requests.get(item['url'])
        Title=response.xpath('//h1[@id="articleTitle"]/text()').extract()[0]
        Time=response.xpath('//span[@id="articleTime"]/text()').extract()[0]
        Writer=response.xpath('//span[@id="articleSource"]/text()').extract()[0]
        info= response.xpath('//div[@class="content" and @id="articleText"]/node()').extract_unquoted()
        Info = [i.replace("'",'"') for i in info if p_pattern.match(i) and "<script" not in i]
        item['content']="".join([ strinfo.sub('',I) for I in Info ])+item['content']
        item['title']=Title
        item['publishtime']=int(time.mktime(time.strptime(Time, "%Y-%m-%d %H:%M:%S")))
        item['writer']=Writer
        if not P.match(item['url']) :
            return item
        else :
            print item['url'],'~~1~~~~~~2~~~~~~3~~'


###采集社保网保险知识的数据###
class SouthMoneySpider(scrapy.Spider):
    name = "SouthMoneySpider"
    allowed_domains = ["southmoney.com"]
    start_urls = ["http://baoxian.southmoney.com"]
    def parse(self, response):
        """
        for i in range(2,68): 
            yield scrapy.Request('http://baoxian.southmoney.com/zhishi/index_%d.html'%i,callback=self.page_list,dont_filter=True)
        else :
            yield scrapy.Request('http://baoxian.southmoney.com/zhishi/index.html', callback=self.page_list, dont_filter=True)
        """
        yield scrapy.Request('http://baoxian.southmoney.com/zhishi/index.html', callback=self.page_list, dont_filter=True)

    def page_list(self, response):
        urls = response.xpath('//div[@class="col1 fn-left"]/ul[@class="newslist2"]/li/a/@href').extract()
        Time = response.xpath('//div[@class="col1 fn-left"]/ul[@class="newslist2"]/li/span[@class="time"]/text()').extract()
        for index,url in enumerate(urls):
            #if url == 'http://baoxian.southmoney.com/zhishi/4472.html' :
            item={'publishtime':int(time.mktime(time.strptime(Time[index], "%Y-%m-%d %H:%M:%S"))),'keyword':'','type':0,'source':'社保网'}
            yield scrapy.Request(url, callback=self.page_desc, dont_filter=True,meta={'item': item})

    def page_desc(self, response):
        p_pattern = re.compile(r"<p.*</p>|.*<img\s.*/></center>")
        strinfo = re.compile('''<a.*\.southmoney\.com.*>|</a>''')
        item = response.meta['item']
        item['url'] = response.url
        R = requests.get(item['url'])
        Title=response.xpath('//div[@class="article"]/h1[@class="artTitle"]/text()').extract()[0]
        Writer=response.xpath('//div[@class="article"]/p[@class="artDate"]/text()').extract()[0].split()[-2]
        info=response.xpath('//div[@class="article"]/div[@class="articleCon"]/node()').extract()
        Info = [i.replace("'",'"') for i in info if p_pattern.match(i) and "<script" not in i]
        item['content']="".join([ strinfo.sub('',I) for I in Info ])
        item['title']=Title
        item['writer']=Writer
        return item

