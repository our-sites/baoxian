# coding:utf-8
# from newtest.items import DmozItem
# coding:utf-8
import scrapy
from weixinqun.items import InfoItem
import re,time
import copy
import sys
import math
import MySQLdb.cursors
import MySQLdb as mdb

from scrapy.spiders import Rule
from scrapy.spiders.init import InitSpider
from scrapy.http import Request, FormRequest
from scrapy.linkextractors.sgml import SgmlLinkExtractor

reload(sys)
sys.setdefaultencoding('utf-8')

##采集weixinqun.cn的资讯##
class wxqzxSpider(scrapy.Spider):
    name = "wxqzxSpider"
    allowed_domains = ["weixinqun.cn"]
    start_urls = ["http://www.weixinqun.cn"]
    global Mysql_conf, My_cxn, My_cur
    Mysql_conf = {
        'host': '113.10.195.169',
        'user': 'dba_user',
        'passwd': 'gc895316',
        'db': 'wechat',
        'charset': 'utf8',
        'init_command': 'set autocommit=0',
        'cursorclass': MySQLdb.cursors.DictCursor
    }
    My_cxn = MySQLdb.connect(**Mysql_conf)
    My_cur = My_cxn.cursor()
    def parse(self, response):
        cate_dic={'huodong':1,'wxyingxiao':2,'zixun':3,'pinpaizx':4}
        for url in ['huodong','wxyingxiao','zixun','pinpaizx']:
            ITem = {'cateid': cate_dic[url],'zixun':1}
            url = "http://www.weixinqun.cn/wenzhang/"+url
            yield scrapy.Request(url,callback=self.page_list, dont_filter=True,meta={'item':ITem})

    def page_list(self, response):
        item = response.meta['item']
        urls = response.xpath('//ul[@class="news-list"]/li[@class="item"]/a/@href').extract()
        imgs = response.xpath('//ul[@class="news-list"]/li[@class="item"]/a/img/@src').extract()
        titles = response.xpath('//div[@class="txt"]/p[@class="title ellipsis"]/a/text()').extract()
        abstracts = response.xpath('//div[@class="txt"]/p[@class="sub-title ellipsis"]/a/text()').extract()
        for index,url in enumerate(urls):
            iTem = item.copy()
            iTem['url'] = url
            iTem['title'] = titles[index]
            iTem['show_url'] = imgs[index]
            iTem['abstract'] = abstracts[index]
            if self.check_url(iTem['url'], My_cxn, My_cur):
                print u'该页面已爬过~~~'
                continue
            yield scrapy.Request(url, callback=self.page_desc, dont_filter=True, meta={'item':iTem})

    def page_desc(self, response):
        item = response.meta['item']
        item['url'] = response.url
        pubtime = response.xpath('//div[@class="news-details"]/div[@class="news-content"]/div[@class="state"]/p[@class="left"]/span/text()').extract()
        content = response.xpath('//div[@class="news-details"]/div[@class="news-content"]/div[@class="txt"]/node()').extract()
        try :
            item['addtime'] = int(time.time())
            item['pubtime'] = int(time.mktime(time.strptime(pubtime[0], "%Y-%m-%d %H:%M:%S")))
        except :
            item['pubtime'] = int(time.time())
        if content :
            item['content'] = ''.join(content).replace("'", '"')
        return item

    ###检测url是否已经采集过,防止重复采集###
    def check_url(self, url, My_cxn, My_cur):
        try:
            My_cxn.ping()
        except:
            My_cxn = MySQLdb.connect(**Mysql_conf)
            My_cur = My_cxn.cursor()
        SQL = "SELECT newid FROM wx_fb_news WHERE url='%s'"
        My_cur.execute(SQL % url)
        result = My_cur.fetchall()
        if result:
            return True
        else:
            return False
