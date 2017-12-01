# from newtest.items import DmozItem
# coding:utf-8
import scrapy
from scrapy.selector import HtmlXPathSelector
from toutiao.items import InfoItem
import re,time
import copy
import sys
import math
import MySQLdb.cursors
import MySQLdb as mdb
import requests,json
from selenium import webdriver
import urllib

reload(sys)
sys.setdefaultencoding('utf-8')

###采集头条搜索的数据###
class ToutiaoSpider(scrapy.Spider):
    name = "ToutiaoSpider"
    allowed_domains = ["eastday.com"]
    start_urls = ["https://s.eastday.com"]
    global Mysql_conf, My_cxn, My_cur
    Mysql_conf = {
        'host': '118.89.220.36',
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
        KW=['保险','社保','医保','工伤','公积金','养老','生育','养老金']
        for kw in KW :
            item={'source':'头条搜索','keyword':kw,'type':0,'publishtime':int(time.time()),'title':'','writer':'','content':''}
            driver = webdriver.PhantomJS("/usr/local/bin/phantomjs")
            #driver = webdriver.PhantomJS("D:\Program Files\phantomjs.exe")
            driver.get('http://s.eastday.com/?'+urllib.urlencode({"kw":kw}))
            data = driver.page_source
            url_pattern = re.findall(r'(<a class="fl" href="//mini.eastday.com/a/\d+.html|<a class="J-share-a" href="//mini.eastday.com/a/\d+.html)',data)
            if url_pattern :
                for url in list(set(url_pattern)):
                    url='http://'+url.split('href="//')[-1]
                    if self.check_url(url, My_cxn, My_cur):
                        print u'该页面已爬过~~~'
                        continue
                    print url,'~~~1~~~2~~~3~~~'
                    yield scrapy.Request(url, callback=self.page_list, dont_filter=True, meta={'item': item})
            else :
                pass
            #driver.quit()

    def page_list(self, response):
        item = response.meta['item']
        url_list=[response.url]
        urls = response.xpath('//div[@class="pagination"]/a/@href').extract()
        maxpage=1
        if urls:
            for url in urls:
                page=int(url.split('-')[-1].split('.')[0])
                if page > maxpage :
                    maxpage = page
            for n in xrange(2,maxpage+1):
                url_list.append(response.url.split('.html')[0]+'-'+str(n)+'.html')
            for url in  url_list :
                yield scrapy.Request(url, callback=self.page_desc, dont_filter=True,meta={'item': item})
        else :
            yield scrapy.Request(response.url, callback=self.page_desc, dont_filter=True,meta={'item': item})
    def page_desc(self, response):
        p_pattern = re.compile(r"<p.*</p>|<div.*<img\sclass.*>")
        P = re.compile(r"http://mini.eastday.com/a/\d+-\d+.html")
        item = response.meta['item']
        item['url'] = response.url
        info= response.xpath('//div[@class="J-contain_detail_cnt contain_detail_cnt"]/node()').extract_unquoted()
        Info = [i.replace("'",'"') for i in info if p_pattern.match(i) and "<script" not in i]
        item['content']="".join(Info)+item['content']
        title=response.xpath('//div[@class="J-title_detail title_detail"]/h1/span/text()').extract()[0].strip()
        TIME=response.xpath("""//div[@class='share_cnt_p clearfix']/div[@class="fl"]/i/text()""").extract()
        if TIME :
            Time=TIME[0].strip()
            Writer=TIME[-1].strip()
        else :
            TIME=response.xpath("""//div[@class='share_cnt_p']/i/text()""").extract()
            Time=TIME[0].strip()
            Writer=TIME[-1].strip()
        if title :
            item['title'] = title
        elif item['title']:
            pass
        else :
            item['title'] = 'unknow'
        item['writer'] = Writer
        try :
            item['publishtime']=int(time.mktime(time.strptime(Time, "%Y-%m-%d %H:%M")))
        except :
            try :
                item['publishtime'] = int(time.mktime(time.strptime(Time, "%Y-%m-%d %H:%M:%S")))
            except :
                print Time, 'EEEEE~~~~~~EEEEEEEEEEE~~~~~~~~EEEEEE'

        if P.match(item['url']) :
            print item['url'],'~~1~~~~~~2~~'
        else :
            return item

    ###检测url是否已经采集过,防止重复采集###
    def check_url(self, url, My_cxn, My_cur):
        try:
            My_cxn.ping()
        except:
            My_cxn = MySQLdb.connect(**Mysql_conf)
            My_cur = My_cxn.cursor()
        SQL = "SELECT id FROM zixun WHERE url='%s'"
        My_cur.execute(SQL % url)
        result = My_cur.fetchall()
        if result:
            return True
        else:
            return False

###采集今日头条的数据###
class TouTiaoSpider(scrapy.Spider):
    name = "TouTiaoSpider"
    allowed_domains = ["toutiao.com"]
    start_urls = ["http://www.toutiao.com"]

    global Mysql_conf, My_cxn, My_cur
    Mysql_conf = {
        'host': '118.89.220.36',
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
        KW=['保险','社保','医保','工伤','公积金','养老','生育','养老金']
        for kw in KW :
            URL="http://www.toutiao.com/search_content/?offset=0&format=json&autoload=true&count=100&cur_tab=1&"+urllib.urlencode({"keyword":kw})
            R = requests.get(URL)
            for d in json.loads(R.text).get('data'):
                if self.check_url(d.get('url'), My_cxn, My_cur) :
                    print u'该页面已爬过~~~',"URL:",d.get('url')
                    continue
                item={'source':'今日头条','keyword':d.get('keywords'),'type':0,'publishtime':d.get('publish_time',int(time.time())),'title':d.get('title',''),'writer':d.get('source','')}
                if d.get('url') and 'toutiao.com/' in d.get('url'):
                    yield scrapy.Request(d.get('url'), callback=self.toutiao_spider, dont_filter=True,meta={'item': item})
                elif d.get('url') and '.sctv.com/' in d.get('url'):
                    yield scrapy.Request(d.get('url'), callback=self.sctv_spider, dont_filter=True,meta={'item': item})
                elif d.get('url') and 'baic.qianlong.com/' in d.get('url'):
                    yield scrapy.Request(d.get('url'), callback=self.qianlong_spider, dont_filter=True,meta={'item': item})
                else :
                    pass

    def toutiao_spider(self, response):
        item = response.meta['item']
        item['url'] = response.url
        driver = webdriver.PhantomJS("/usr/local/bin/phantomjs")
        #driver = webdriver.PhantomJS("D:\Program Files\phantomjs.exe")
        driver.get(response.url)
        data = driver.page_source
        hxs = HtmlXPathSelector(text=data)
        #print response.url,'~~~~~~~',response,response.body
        #info=response.xpath('//div[@class="article-content"]/div')
        #info=response.xpath('//html/body/div/div/div/div/div[@class="article-content"]/div')
        info=hxs.select('//div[@class="article-box"]/div[@class="article-content"]/div/node()').extract()
        if not info:
            info=hxs.select('//div[@class="article-content"]/node()').extract()
        item['content'] = "".join(info)
        if info :
            return item
        else :
            print item['url'],'~~~Err~~~',item['title']

    def qianlong_spider(self, response):
        item = response.meta['item']
        item['url'] = response.url
        info=response.xpath('//div[@class="article-content"]/div/node()').extract()
        item['content'] = "".join(info)
        print item['url']
        #return item

    def sctv_spider(self, response):
        p_pattern = re.compile(r"<p.*</p>|<div.*<img\ssrc=.*/>")
        item = response.meta['item']
        item['url'] = response.url
        title=response.xpath('//div[@class="ep-cont"]/h1[@class="ep-h1"]/text()').extract()[0].strip()
        Time=response.xpath('//div[@class="ep-cont"]/div[@class="ep-info"]/div[@class="ep-time"]/text()').extract()[0].strip()
        item['publishtime']=int(time.mktime(time.strptime(Time, "%Y-%m-%d %H:%M")))
        Writer=response.xpath('//div[@class="ep-cont"]/div[@class="ep-info"]/div[@class="ep-source"]/a/text()').extract()[0].strip()
        info=response.xpath('//div[@id="end-text"]/div[@class="end-text-c"]/div/node()').extract()
        Info = [ i for i in info if p_pattern.match(i) ]
        item['content'] = "".join(Info)
        item['title'] = title
        item['writer'] = Writer
        return item

    ###检测url是否已经采集过,防止重复采集###
    def check_url(self, url, My_cxn, My_cur):
        if not url :
            return True
        try:
            My_cxn.ping()
        except:
            My_cxn = MySQLdb.connect(**Mysql_conf)
            My_cur = My_cxn.cursor()
        SQL = "SELECT id FROM zixun WHERE url='%s'"
        My_cur.execute(SQL % url)
        result = My_cur.fetchall()
        if result:
            return True
        else:
            return False
