# from newtest.items import DmozItem
# coding:utf-8
import scrapy
from chinanews.items import InfoItem
import re,time
import copy
import sys
import math
import MySQLdb.cursors
import MySQLdb as mdb

reload(sys)
sys.setdefaultencoding('utf-8')

###从中新网搜索并采集###
class ChinanewsSpider(scrapy.Spider):
    name = "ChinanewsSpider"
    allowed_domains = ["chinanews.com.cn"]
    start_urls = ["http://sou.chinanews.com.cn"]
    def parse(self, response):
        KW=['保险','社保','医保','工伤','公积金','养老','生育','养老金']
        for kw in KW :
            yield scrapy.Request('http://sou.chinanews.com.cn/search.do?q=%s'%kw, callback=self.page_list, dont_filter=True)
    def page_list(self, response):
        urls = response.xpath('//ul[@class="news_item"]/li[@class="news_title"]/a/@href').extract()
        for index,url in enumerate(urls):
            Item = {}
            Item['url'] = url
            yield scrapy.Request(Item['url'], callback=self.page_desc, dont_filter=True,meta={'item': Item})
    def page_desc(self, response):
        p_pattern = re.compile(r"<p.*</p>|<div.*<img\s.*>")
        item = response.meta['item']
        item['url'] = response.url
        site=response.xpath('//div[@id="cont_1_1_2"]')
        title=site.select('h1/text()').extract()[0].strip()
        Time=site.select('div[@id="BaiduSpider"]/span[@id="pubtime_baidu"]/text()').extract()[0]
        Writer=site.select('div[@id="BaiduSpider"]/span[@id="source_baidu"]/a/text()').extract()[0]
        item['keyword']=' '
        item['writer']=Writer
        item['type']=0
        item['publishtime']=int(time.mktime(time.strptime(Time, "%Y-%m-%d %H:%M:%S")))
        info= response.xpath('//div[@class="left_zw" and @style="position:relative"]/node()').extract_unquoted()
        INFO = "".join([i.replace("'",'"') for i in info if p_pattern.match(i) and "<script" not in i])
        if title :
            item['title'] = title
        else:
            item['title'] = 'unknow'
        item['content']=INFO
        return item

