# from newtest.items import DmozItem
# coding:utf-8
import scrapy
from zhongmin.items import InfoItem
import re,time
import copy
import sys
import math
import MySQLdb.cursors
import MySQLdb as mdb

reload(sys)
sys.setdefaultencoding('utf-8')
###采集所有内容###
class zhongminSpider(scrapy.Spider):
    name = "zhongminSpider"
    allowed_domains = ["zhongmin.cn"]
    start_urls = ["http://www.zhongmin.cn"]
    def parse(self, response):
        types = [{'type':1010,'url':'http://www.zhongmin.cn/news/newslist.aspx?bid=5','name':'意外保险'},{'type':1011,'url':'http://www.zhongmin.cn/news/newslist.aspx?bid=7','name':'旅游保险'},{'type':1012,'url':'http://www.zhongmin.cn/news/newslist.aspx?bid=8','name':'健康保险'},{'type':1012,'url':'http://www.zhongmin.cn/news/newslist.aspx?bid=9','name':'人寿保险'},{'type':1013,'url':'http://www.zhongmin.cn/news/newslist.aspx?bid=10','name':'家财保险'},{'type':1014,'url':'http://www.zhongmin.cn/news/newslist.aspx?bid=12','name':'保险常识'},{'type':1015,'url':'http://www.zhongmin.cn/news/newslist.aspx?bid=13','name':'媒体中民'},{'type':1016,'url':'http://www.zhongmin.cn/news/newslist.aspx?bid=16','name':'保险观点'},{'type':1017,'url':'http://www.zhongmin.cn/news/newslist.aspx?bid=17','name':'理赔知识'},{'type':1018,'url':'http://www.zhongmin.cn/news/newslist.aspx?bid=18','name':'保险案例'},{'type':1019,'url':'http://www.zhongmin.cn/news/newslist.aspx?bid=19','name':'保险知识'},{'type':1020,'url':'http://www.zhongmin.cn/news/newslist.aspx?bid=20','name':'保险新闻'},{'type':1021,'url':'http://www.zhongmin.cn/news/newslist.aspx?bid=21','name':'保险理财'}]
        for item in types :
            yield scrapy.Request('%s'%item['url'], callback=self.type_list, dont_filter=True,meta={'item': item})
    def type_list(self, response):
        item = response.meta['item']
        maxpage = int(response.xpath('//span[@id="CustomInfoClass"]/font[@color="blue"]/b/text()').extract()[-1])
        for n in range(2,maxpage+1):
            item['page']=n
            yield scrapy.Request(item['url']+'&page=%s'%n, callback=self.page_list, dont_filter=True,meta={'item': item})
        else :
            yield scrapy.Request(item['url'], callback=self.page_list, dont_filter=True,meta={'item': item})
    def page_list(self, response):
        item = response.meta['item']
        urls = response.xpath('//div[@class="tjyd_li"]/table/tr/td/a/@href').extract()
        #for url in ['newsinfor14500.html','newsinfor11585.html','newsinfor11587.html','newsinfor11260.html','newsinfor11351.html']:
        for index,url in enumerate(urls):
            Item = item.copy()
            Item['url'] = 'http://www.zhongmin.cn/news/'+url
            yield scrapy.Request(Item['url'], callback=self.page_desc, dont_filter=True,meta={'item': Item})
    def page_desc(self, response):
        p_pattern = re.compile(r"<p.*</p>|<div.*</div>|<FONT .*</FONT>")
        #P = re.compile(r"http://mini.eastday.com/a/\d+-\d+.html")
        strinfo = re.compile('''<a href="http://.*\.zhongmin\.cn/.*\.html">|<a href="http://.*\.zhongmin\.cn/.*\.aspx">|</a>''')
        item = response.meta['item']
        item['url'] = response.url
        site=response.xpath('//div[@class="lby_l"]/div[@class="acticle_k"]')
        title=site.select('h1/span/text()').extract()
        Time=site.select('div[@class="acticle_ly"]/ul/li/span[@id="labinfortime"]/text()').extract()[0]
        keyword=site.select('div[@class="acticle_ly"]/ul/li/text()').extract()[-1].split('：')[-1]
        Writer=site.select('div[@class="acticle_ly"]/ul/li/span[@id="labfrom"]/text()').extract()[0]
        item['keyword']=",".join(keyword.strip().split())
        item['publishtime']=int(time.mktime(time.strptime(Time, "%Y-%m-%d %H:%M")))
        info= response.xpath('//div[@class="acticle_nr"]/div/span[@id="labContents"]/node()').extract_unquoted()
        if not info :
            info="".join(response.xpath('//div[@class="acticle_nr"]/div/span[@id="labContents"]/div/node()').extract_unquoted())
        Info = [strinfo.sub('',i).replace("'",'"') for i in info if p_pattern.match(i.strip().replace("\n", "").replace("\t", "")) and "<script" not in i]
        if title :
            item['title'] = title[0]
        else:
            item['title'] = 'unknow'
        item['content']="".join(Info)
        item['writer']=Writer
        if len(item['content']) < 200 :
            print Info,item['url']
        else :
            return item
###仅采集第一页中最新的内容###
class ZhongMinSpider(scrapy.Spider):
    name = "ZhongMinSpider"
    allowed_domains = ["zhongmin.cn"]
    start_urls = ["http://www.zhongmin.cn"]
    def parse(self, response):
        types = [{'type':1010,'url':'http://www.zhongmin.cn/news/newslist.aspx?bid=5','name':'意外保险'},{'type':1011,'url':'http://www.zhongmin.cn/news/newslist.aspx?bid=7','name':'旅游保险'},{'type':1012,'url':'http://www.zhongmin.cn/news/newslist.aspx?bid=8','name':'健康保险'},{'type':1012,'url':'http://www.zhongmin.cn/news/newslist.aspx?bid=9','name':'人寿保险'},{'type':1013,'url':'http://www.zhongmin.cn/news/newslist.aspx?bid=10','name':'家财保险'},{'type':1014,'url':'http://www.zhongmin.cn/news/newslist.aspx?bid=12','name':'保险常识'},{'type':1015,'url':'http://www.zhongmin.cn/news/newslist.aspx?bid=13','name':'媒体中民'},{'type':1016,'url':'http://www.zhongmin.cn/news/newslist.aspx?bid=16','name':'保险观点'},{'type':1017,'url':'http://www.zhongmin.cn/news/newslist.aspx?bid=17','name':'理赔知识'},{'type':1018,'url':'http://www.zhongmin.cn/news/newslist.aspx?bid=18','name':'保险案例'},{'type':1019,'url':'http://www.zhongmin.cn/news/newslist.aspx?bid=19','name':'保险知识'},{'type':1020,'url':'http://www.zhongmin.cn/news/newslist.aspx?bid=20','name':'保险新闻'},{'type':1021,'url':'http://www.zhongmin.cn/news/newslist.aspx?bid=21','name':'保险理财'}]
        for item in types :
            yield scrapy.Request('%s'%item['url'], callback=self.page_list, dont_filter=True,meta={'item': item})
    def page_list(self, response):
        item = response.meta['item']
        urls = response.xpath('//div[@class="tjyd_li"]/table/tr/td/a/@href').extract()
        Time = response.xpath('//div[@class="tjyd_li"]/table/tr/td/text()').extract()
        TIME=int(time.mktime(time.strptime(time.strftime('%Y%m%d',time.localtime(time.time())), "%Y%m%d")))
        for index,url in enumerate(urls):
            #print url , '&&&&&&&&&&&&%%%%%%%%%%%%%%%',Time[index].split(),type(Time[index].split())
            publishtime = int(time.mktime(time.strptime(' '.join(Time[index].split()), "%Y-%m-%d %H:%M:%S")))
            #print url , '&&%%%%%%%%%%%%%12312312313123123123123123'
            Item = item.copy()
            Item['url'] = 'http://www.zhongmin.cn/news/'+url
            if publishtime > TIME :
                yield scrapy.Request(Item['url'], callback=self.page_desc, dont_filter=True,meta={'item': Item})
            else :
                pass
    def page_desc(self, response):
        p_pattern = re.compile(r"<p.*</p>|<div.*</div>|<FONT .*</FONT>")
        #P = re.compile(r"http://mini.eastday.com/a/\d+-\d+.html")
        strinfo = re.compile('''<a href="http://.*\.zhongmin\.cn/.*\.html">|<a href="http://.*\.zhongmin\.cn/.*\.aspx">|</a>''')
        item = response.meta['item']
        item['url'] = response.url
        site=response.xpath('//div[@class="lby_l"]/div[@class="acticle_k"]')
        title=site.select('h1/span/text()').extract()
        Time=site.select('div[@class="acticle_ly"]/ul/li/span[@id="labinfortime"]/text()').extract()[0]
        keyword=site.select('div[@class="acticle_ly"]/ul/li/text()').extract()[-1].split('：')[-1]
        Writer=site.select('div[@class="acticle_ly"]/ul/li/span[@id="labfrom"]/text()').extract()[0]
        item['keyword']=",".join(keyword.strip().split())
        item['publishtime']=int(time.mktime(time.strptime(Time, "%Y-%m-%d %H:%M")))
        info= response.xpath('//div[@class="acticle_nr"]/div/span[@id="labContents"]/node()').extract_unquoted()
        if not info :
            info="".join(response.xpath('//div[@class="acticle_nr"]/div/span[@id="labContents"]/div/node()').extract_unquoted())
        Info = [strinfo.sub('',i).replace("'",'"') for i in info if p_pattern.match(i.strip().replace("\n", "").replace("\t", "")) and "<script" not in i]
        if title :
            item['title'] = title[0]
        else:
            item['title'] = 'unknow'
        item['content']="".join(Info)
        item['writer']=Writer
        if len(item['content']) < 200 :
            print Info,item['url']
        else :
            return item
