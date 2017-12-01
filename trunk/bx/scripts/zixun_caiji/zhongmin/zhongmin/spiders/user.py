# from newtest.items import DmozItem
# coding:utf-8
import scrapy
from zhongmin.items import InfoItem
import re,time
import copy
import sys
import math
from selenium import webdriver
from scrapy.selector import HtmlXPathSelector
import MySQLdb.cursors
import MySQLdb as mdb

reload(sys)
sys.setdefaultencoding('utf-8')
###采集所有内容###
class zhongminSpider(scrapy.Spider):
    name = "zhongminSpider"
    allowed_domains = ["zhongmin.cn"]
    start_urls = ["http://www.zhongmin.cn"]
    global Mysql_conf, My_cxn, My_cur
    Mysql_conf = {
        'host': '172.16.13.164',
        'user': 'mha_user',
        'passwd': 'gc895316',
        'db': 'bx_abc',
        'charset': 'utf8',
        'init_command': 'set autocommit=0',
        'cursorclass': MySQLdb.cursors.DictCursor
    }
    My_cxn = MySQLdb.connect(**Mysql_conf)
    My_cur = My_cxn.cursor()
    def parse(self, response):
        types = [{'type':1010,'url':'http://www.zhongmin.cn/news/newslist.aspx?bid=5','name':'意外保险','cate1':2,'cate2':33},
                 {'type':1011,'url':'http://www.zhongmin.cn/news/newslist.aspx?bid=7','name':'旅游保险','cate1':2,'cate2':34},
                 {'type':1012,'url':'http://www.zhongmin.cn/news/newslist.aspx?bid=8','name':'健康保险','cate1':2,'cate2':35},
                 {'type':1012,'url':'http://www.zhongmin.cn/news/newslist.aspx?bid=9','name':'人寿保险','cate1':2,'cate2':36},
                 {'type':1013,'url':'http://www.zhongmin.cn/news/newslist.aspx?bid=10','name':'家财保险','cate1':2,'cate2':37},
                 {'type':1014,'url':'http://www.zhongmin.cn/news/newslist.aspx?bid=12','name':'保险常识','cate1':5,'cate2':38},
                 {'type':1015,'url':'http://www.zhongmin.cn/news/newslist.aspx?bid=13','name':'媒体中民'},
                 {'type':1016,'url':'http://www.zhongmin.cn/news/newslist.aspx?bid=16','name':'保险观点','cate1':1,'cate2':40},
                 {'type':1017,'url':'http://www.zhongmin.cn/news/newslist.aspx?bid=17','name':'理赔知识','cate1':5,'cate2':39},
                 {'type':1018,'url':'http://www.zhongmin.cn/news/newslist.aspx?bid=18','name':'保险案例','cate1':5,'cate2':28},
                 {'type':1019,'url':'http://www.zhongmin.cn/news/newslist.aspx?bid=19','name':'保险知识','cate1':5,'cate2':0},
                 {'type':1020,'url':'http://www.zhongmin.cn/news/newslist.aspx?bid=20','name':'保险新闻','cate1':1,'cate2':41},
                 {'type':1021,'url':'http://www.zhongmin.cn/news/newslist.aspx?bid=21','name':'保险理财','cate1':1,'cate2':8}]
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
            if self.check_url(Item['url'], My_cxn, My_cur) :
                continue
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
        Writer=site.select('div[@class="acticle_ly"]/ul/li/span[@id="labfrom"]/text()').extract()
        item['keyword']=",".join(keyword.strip().split())
        item['publishtime']=int(time.mktime(time.strptime(Time, "%Y-%m-%d %H:%M")))
        info = response.xpath('//div[@class="acticle_nr"]/div/span[@id="labContents"]/node()').extract_unquoted()
        info = response.xpath('//div[@class="acticle_nr"]/div/span[@id="labContents"]/node()').extract_unquoted()
        if not info :
            driver = webdriver.PhantomJS("/usr/local/bin/phantomjs")
            #driver = webdriver.PhantomJS("D:\Program Files\phantomjs.exe")
            driver.get(item['url'])
            data = driver.page_source
            hxs = HtmlXPathSelector(text=data)
            info = hxs.select('//div[@class="acticle_nr"]/div/span[@id="labContents"]/node()').extract_unquoted()
        Info = [strinfo.sub('',i).replace("'",'"') for i in info if p_pattern.match(i.strip().replace("\n", "").replace("\t", "")) and "<script" not in i]
        if title :
            item['title'] = title[0]
        else:
            item['title'] = 'unknow'
        item['content']="".join(Info)
        if Writer :
            item['writer']=Writer[0]
        else :
            item['writer'] = ''
        if len(item['content']) < 2 :
            print 'Info:',Info,item['url']
        else :
            #print item['url']
            #return item
            self.insert_data(item, My_cxn, My_cur)

    ###检测url是否已经采集过,防止重复采集###
    def check_url(self, url, My_cxn, My_cur):
        try:
            My_cxn.ping()
        except:
            My_cxn = MySQLdb.connect(**Mysql_conf)
            My_cur = My_cxn.cursor()
        SQL = "SELECT nid FROM bx_news WHERE `from`='%s'"
        My_cur.execute(SQL % url)
        result = My_cur.fetchall()
        if result:
            return True
        else:
            return False

    ###将采集到的数据插入数据库###
    def insert_data(self, data, My_cxn, My_cur):
        try:
            My_cxn.ping()
        except:
            My_cxn = MySQLdb.connect(**Mysql_conf)
            My_cur = My_cxn.cursor()
        SQL = """INSERT INTO bx_news(nid,title,cate1,cate2,writer,`from`,addtime,caijitime,content,keywords)
                              VALUES(NULL,'%s',%s,%s,'%s','%s',%s,%s,'%s','%s')"""
        try:
            My_cur.execute(SQL % (data.get('title',''), data.get('cate1',0), data.get('cate2',0), data.get('writer',''),data.get('url',''), data.get('publishtime',0),data.get('addtime',0),data.get('content',''),data.get('keyword','')))
            id = int(My_cur.lastrowid)
        except Exception,e:
            print e
            id = 0
        if id:
            My_cxn.commit()
            return True
        else:
            return False

###仅采集第一页中最新的内容###
class ZhongMinSpider(scrapy.Spider):
    name = "ZhongMinSpider"
    allowed_domains = ["zhongmin.cn"]
    start_urls = ["http://www.zhongmin.cn"]
    global Mysql_conf, My_cxn, My_cur
    Mysql_conf = {
        'host': '172.16.13.164',
        'user': 'mha_user',
        'passwd': 'gc895316',
        'db': 'bx_abc',
        'charset': 'utf8',
        'init_command': 'set autocommit=0',
        'cursorclass': MySQLdb.cursors.DictCursor
    }
    My_cxn = MySQLdb.connect(**Mysql_conf)
    My_cur = My_cxn.cursor()
    def parse(self, response):
        types = [{'type':1010,'url':'http://www.zhongmin.cn/news/newslist.aspx?bid=5','name':'意外保险','cate1':2,'cate2':33},
                 {'type':1011,'url':'http://www.zhongmin.cn/news/newslist.aspx?bid=7','name':'旅游保险','cate1':2,'cate2':34},
                 {'type':1012,'url':'http://www.zhongmin.cn/news/newslist.aspx?bid=8','name':'健康保险','cate1':2,'cate2':35},
                 {'type':1012,'url':'http://www.zhongmin.cn/news/newslist.aspx?bid=9','name':'人寿保险','cate1':2,'cate2':36},
                 {'type':1013,'url':'http://www.zhongmin.cn/news/newslist.aspx?bid=10','name':'家财保险','cate1':2,'cate2':37},
                 {'type':1014,'url':'http://www.zhongmin.cn/news/newslist.aspx?bid=12','name':'保险常识','cate1':5,'cate2':38},
                 {'type':1015,'url':'http://www.zhongmin.cn/news/newslist.aspx?bid=13','name':'媒体中民'},
                 {'type':1016,'url':'http://www.zhongmin.cn/news/newslist.aspx?bid=16','name':'保险观点','cate1':1,'cate2':40},
                 {'type':1017,'url':'http://www.zhongmin.cn/news/newslist.aspx?bid=17','name':'理赔知识','cate1':5,'cate2':39},
                 {'type':1018,'url':'http://www.zhongmin.cn/news/newslist.aspx?bid=18','name':'保险案例','cate1':5,'cate2':28},
                 {'type':1019,'url':'http://www.zhongmin.cn/news/newslist.aspx?bid=19','name':'保险知识','cate1':5,'cate2':0},
                 {'type':1020,'url':'http://www.zhongmin.cn/news/newslist.aspx?bid=20','name':'保险新闻','cate1':1,'cate2':41},
                 {'type':1021,'url':'http://www.zhongmin.cn/news/newslist.aspx?bid=21','name':'保险理财','cate1':1,'cate2':8}]
        for item in types :
            yield scrapy.Request('%s'%item['url'], callback=self.page_list, dont_filter=True,meta={'item': item})

    def page_list(self, response):
        item = response.meta['item']
        urls = response.xpath('//div[@class="tjyd_li"]/table/tr/td/a/@href').extract()
        Time = response.xpath('//div[@class="tjyd_li"]/table/tr/td/text()').extract()
        TIME=int(time.mktime(time.strptime(time.strftime('%Y%m%d',time.localtime(time.time())), "%Y%m%d")))
        for index,url in enumerate(urls):
            publishtime = int(time.mktime(time.strptime(' '.join(Time[index].split()).replace('/','-'), "%Y-%m-%d %H:%M:%S")))
            Item = item.copy()
            Item['url'] = 'http://www.zhongmin.cn/news/'+url
            if self.check_url(Item['url'], My_cxn, My_cur) :
                continue
            if publishtime > TIME :
                yield scrapy.Request(Item['url'], callback=self.page_desc, dont_filter=True,meta={'item': Item})
            else :
                yield scrapy.Request(Item['url'], callback=self.page_desc, dont_filter=True,meta={'item': Item})
                pass

    def page_desc(self, response):
        p_pattern = re.compile(r"<p.*</p>|<div.*</div>|<FONT .*</FONT>")
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
            self.insert_data(item, My_cxn, My_cur)
            return item

    ###检测url是否已经采集过,防止重复采集###
    def check_url(self, url, My_cxn, My_cur):
        try:
            My_cxn.ping()
        except:
            My_cxn = MySQLdb.connect(**Mysql_conf)
            My_cur = My_cxn.cursor()
        SQL = "SELECT nid FROM bx_news WHERE `from`='%s'"
        My_cur.execute(SQL % url)
        result = My_cur.fetchall()
        if result:
            return True
        else:
            return False

    ###将采集到的数据插入数据库###
    def insert_data(self, data, My_cxn, My_cur):
        try:
            My_cxn.ping()
        except:
            My_cxn = MySQLdb.connect(**Mysql_conf)
            My_cur = My_cxn.cursor()
        SQL = """INSERT INTO bx_news(nid,title,cate1,cate2,writer,`from`,addtime,caijitime,content,keywords)
                              VALUES(NULL,'%s',%s,%s,'%s','%s',%s,%s,'%s','%s')"""
        try:
            My_cur.execute(SQL % (data.get('title',''), data.get('cate1',0), data.get('cate2',0), data.get('writer',''),data.get('url',''), data.get('publishtime',0),data.get('addtime',0),data.get('content',''),data.get('keyword','')))
            id = int(My_cur.lastrowid)
        except Exception,e:
            print e
            id = 0
        if id:
            My_cxn.commit()
            return True
        else:
            return False
