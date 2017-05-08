# from newtest.items import DmozItem
# coding:utf-8
import scrapy
from ifeng.items import InfoItem
import re,time
import copy
import sys
import math
import MySQLdb.cursors
import MySQLdb as mdb

reload(sys)
sys.setdefaultencoding('utf-8')

###从凤凰网搜索并采集###
class IfengSpider(scrapy.Spider):
    name = "IfengSpider"
    allowed_domains = ["ifeng.com"]
    start_urls = ["http://search.ifeng.com/sofeng/search.action?q=%E4%BF%9D%E9%99%A9&c=1"]
    def parse(self, response):
        yield scrapy.Request("http://search.ifeng.com/sofeng/search.action?q=%E4%BF%9D%E9%99%A9&c=1", callback=self.page_list, dont_filter=True)
    def page_list(self, response):
        urls = response.xpath('//div[@class="searchResults"]/p/a/@href').extract()
        for index,url in enumerate(urls):
            Item = {'url':url}
            yield scrapy.Request(Item['url'], callback=self.page_desc, dont_filter=True,meta={'item': Item})
    def page_desc(self, response):
        strinfo = re.compile('''<span class="ifengLogo">.*</span>''') 
        item = response.meta['item']
        item['url'] = response.url
        site=response.xpath('//div[@class="left"]/div[@id="artical"]')
        title=site.select('h1[@id="artical_topic"]/text()').extract()[0].strip()
        Time=site.select('div[@class="clearfix"]/p[@class="p_time"]/span[@class="ss01"]/text()').extract()[0]
        Writer=site.select('div[@class="clearfix"]/p[@class="p_time"]/span/span[@class="ss03"]/text()').extract()
        if Writer :
            writer=Writer[0]
        else :
            writer=site.select('div[@class="clearfix"]/p[@class="p_time"]/span/span[@class="ss03"]/a/text()').extract()[0]
        item['keyword']=' '
        item['type']=0
        item['writer']=writer
        try :
            item['publishtime']=int(time.mktime(time.strptime(Time.encode("utf-8"), "%Y年%m月%d日 %H:%M:%S")))
        except :
            item['publishtime']=int(time.mktime(time.strptime(Time.encode("utf-8"), "%Y-%m-%d %H:%M:%S")))
        info= response.xpath('//div[@class="js_img_share_area"]/div[@id="main_content" and @class="js_selection_area"]/node()').extract_unquoted()
        item['title'] = title
        item['content']="".join([strinfo.sub('',i).strip() for i in info])
        return item

