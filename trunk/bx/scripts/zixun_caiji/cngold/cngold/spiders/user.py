# from newtest.items import DmozItem
# coding:utf-8
import scrapy
from cngold.items import InfoItem
import re,time
import copy
import sys
import math
import MySQLdb.cursors
import MySQLdb as mdb

reload(sys)
sys.setdefaultencoding('utf-8')

###采集金投网行业资讯###
class CNgoldSpider(scrapy.Spider):
    name = "CNgoldSpider"
    allowed_domains = ["cngold.org"]
    start_urls = ["https://insurance.cngold.org/hyxw/"]
    def parse(self, response):
            yield scrapy.Request("https://insurance.cngold.org/"+'hyxw/', callback=self.page_list, dont_filter=True)
    def page_list(self, response):
        dic,L={"[生育保险]":1101,"[车险动态]":1102,"[公司动态]":1103,"[失业保险]":1104,"[监管动态]":1105,"[保险案例]":1106,"[公积金新闻]":1107,"[医疗保险]":1108,"[政策法规]":1109,"[养老险]":1110,"[行业资讯]":1111,"[其他险]":1112,"[公积金知识]":1113,"[养老保险]":1114,"[意外险]":1115,"[财产险]":1116,"[养老金]":1117,"[投保指南]":1118,"[基础知识]":1119,"[健康险]":1120,"[汽车险]":1121,'保险热点':1122},[]
        urls = response.xpath('//ul/li[@class="clearfix"]/p[@class="clearfix"]/a[@class="list_news_a"]/@href').extract()
        Title = response.xpath('//ul/li[@class="clearfix"]/p[@class="clearfix"]/a[@class="list_news_a"]/text()').extract()
        Type = response.xpath('//ul/li[@class="clearfix"]/p[@class="clearfix"]/a[@class="list_channel"]/text()').extract()
        for index,url in enumerate(urls):
            Item = {'url':url,'title':Title[index],'type':dic.get(Type[index].encode("utf-8"),0)}
            yield scrapy.Request(Item['url'], callback=self.page_desc, dont_filter=True,meta={'item': Item})
    def page_desc(self, response):
        strinfo = re.compile('''<a href="http://.*\.cngold\.org/.* target="_blank">|<a href="https://.*\.cngold\.org/.* target="_blank">|</a>|http://insurance.cngold.org/''') 
        Strinfo = re.compile('''<p.*</p>''') 
        item = response.meta['item']
        item['url'] = response.url
        Time=response.xpath('//div[@class="aricleInfo clearfix"]/span[@class="time"]/text()').extract()[0]
        Writer='保险管家'
        item['keyword']=' '
        item['writer']=Writer
        item['publishtime']=int(time.mktime(time.strptime(Time, "%Y-%m-%d %H:%M:%S")))
        info=[strinfo.sub('',i).replace("金投保险网",'') for i in response.xpath('//div[@class="art_content"]/node()').extract_unquoted()]
        item['content']="".join([ strinfo.sub('',i).strip().replace("'",'"') for i in info if Strinfo.match(i) ])
        return item


###采集金投网保险热点###
class CnGoldSpider(scrapy.Spider):
    name = "CnGoldSpider"
    allowed_domains = ["cngold.org"]
    start_urls = ["https://insurance.cngold.org/"]
    def parse(self, response):
        for u in ['hot/','jgdt/','gsdt/','bxlc/','bxal/','zcfg/','jczs/','tzzn/','shebaofa/']:
            yield scrapy.Request("https://insurance.cngold.org/"+u, callback=self.page_list, dont_filter=True)
    def page_list(self, response):
        dic,L={"[生育保险]":1101,"[车险动态]":1102,"[公司动态]":1103,"[失业保险]":1104,"[监管动态]":1105,"[保险案例]":1106,"[公积金新闻]":1107,"[医疗保险]":1108,"[政策法规]":1109,"[养老险]":1110,"[行业资讯]":1111,"[其他险]":1112,"[公积金知识]":1113,"[养老保险]":1114,"[意外险]":1115,"[财产险]":1116,"[养老金]":1117,"[投保指南]":1118,"[基础知识]":1119,"[健康险]":1120,"[汽车险]":1121,'保险热点':1122,'hot':1122,'监管动态':1123,'jgdt':1123,'公司动态':1124,'gsdt':1124,'保险理财':1125,'bxlc':1125,'保险案例':1126,'bxal':1126,'政策法规':1127,'zcfg':1127,'基础知识':1128,'jczs':1128,'投保指南':1129,'tzzn':1129,'社会保险法':1130,'shebaofa':1130},[]
        urls = response.xpath('//ul[@class="clearfix"]/li[@class="clearfix" or @class="clearfix mt10"]/a[@class="fl red3" or @class="fl"]/@href').extract()
        Title = response.xpath('//ul[@class="clearfix"]/li[@class="clearfix" or @class="clearfix mt10"]/a[@class="fl red3" or @class="fl"]/text()').extract()
        if not urls :
            urls = response.xpath('//div[@class="clearfix mb20"]/div[@class="mainLeft fl"]/div[@class="jianguandt mb20"]/ul/li/a/@href').extract()
            Title = response.xpath('//div[@class="clearfix mb20"]/div[@class="mainLeft fl"]/div[@class="jianguandt mb20"]/ul/li/a/text()').extract()
        for index,url in enumerate(urls):
            Item = {'url':url,'title':Title[index],'type':dic.get(response.url.split('/')[-2],0),'content':''}
            yield scrapy.Request(Item['url'], callback=self.page_Desc, dont_filter=True,meta={'item': Item})
    def page_Desc(self, response):
        Item = response.meta['item']
        max_page=response.xpath('//div[@class="listPage"]/a/@href').extract()
        url_list=[response.url]
        if max_page :
            Max_page=max_page[-1]
            for n in range(2,int(Max_page.split('_')[1].split('.html')[0])+1):
                url_list.append(Max_page.split('_')[0]+'_'+str(n)+'.html')
            for url in url_list:
                yield scrapy.Request(url, callback=self.page_desc, dont_filter=True,meta={'item': Item})
        else :
            yield scrapy.Request(Item['url'], callback=self.page_desc, dont_filter=True,meta={'item': Item})
    def page_desc(self, response):
        strinfo = re.compile('''<a href="http://.*\.cngold\.org/.* target="_blank">|<a href="https://.*\.cngold\.org/.* target="_blank">|</a>|http://insurance.cngold.org/''') 
        Strinfo = re.compile('''<p.*</p>''') 
        P = re.compile(r"http://insurance\.cngold\.org/.*/c\d+_\d+\.html|https://insurance\.cngold\.org/.*/c\d+_\d+\.html")
        item = response.meta['item']
        item['url'] = response.url
        Time=response.xpath('//div[@class="aricleInfo clearfix"]/span[@class="time"]/text()').extract()
        if Time :
            item['publishtime']=int(time.mktime(time.strptime(Time[0], "%Y-%m-%d %H:%M:%S")))
            WRITER=response.xpath('//div[@class="aricleInfo clearfix"]/span/text()').extract()
            Writer=WRITER[1].split('：')[-1]
        else :
            Time=response.xpath('//div[@class="art_tit"]/p/span/text()').extract()
            item['publishtime']=int(time.mktime(time.strptime(Time[0], "%Y-%m-%d"))) 
            Writer=Time[1].split('：')[-1]
        item['keyword']=' '
        item['writer']=Writer if '金投保险网' not in Writer else '保险管家'
        item['writer']=item['writer'] if '沃保网' not in item['writer'] else '保险管家'
        info=[strinfo.sub('',i).replace("金投保险网",'') for i in response.xpath('//div[@class="art_content"]/node()').extract_unquoted()]
        item['content']="".join([ strinfo.sub('',i).strip().replace("'",'"') for i in info if Strinfo.match(i) ])+item['content']
        if P.match(item['url']) :
            print item['url'],'~~~1~~~1~~~1~~~'
        else :
            return item
