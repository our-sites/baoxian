# coding:utf-8
# from newtest.items import DmozItem
# coding:utf-8
import scrapy
from soku.items import InfoItem
import copy
import sys
import MySQLdb.cursors
import MySQLdb as mdb


reload(sys)
sys.setdefaultencoding('utf-8')

##搜库视频采集###
class sokuSpider(scrapy.Spider):
    name = "sokuSpider"
    allowed_domains = ["soku.com"]
    start_urls = ["http://www.soku.com"]
    global Mysql_conf, My_cxn, My_cur
    Mysql_conf = {
        'host': '172.16.13.165',
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
        kws=[u'保险销售话术',u'保险销售技巧']
        URL="http://www.soku.com/search_video/q_%s_orderby_2_limitdate_0?spm=a2h0k.8191407.0.0&site=14&_lg=10&page=%d"
        for kw in kws:
            for page in range(1,115,1) :
                url = URL%(kw,page)
                yield scrapy.Request(url,callback=self.page_list, dont_filter=True,meta={'item':{"kw":kw}})

    def page_list(self, response):
        item = response.meta['item']
        titles= response.xpath('//div[@class="v-meta va"]/div[@class="v-meta-title"]/a/@title').extract()
        urls = response.xpath('//div[@class="v-meta va"]/div[@class="v-meta-title"]/a/@href').extract()
        for index,url in enumerate(urls):
            iTem = copy.copy(item)
            iTem['url']=url
            iTem['title'] = titles[index]
            SQL = "SELECT id FROM bx_shipin WHERE url='%s'"%url
            My_cur.execute(SQL)
            result = My_cur.fetchall()
            if result:
                print result, u'该页面已爬过~~~'
            else:
                self.insert_data(iTem,My_cxn,My_cur)


    ###将采集到的数据插入数据库###
    def insert_data(self,data,My_cxn,My_cur):
        try :
            My_cxn.ping()
        except :
            My_cxn = MySQLdb.connect(**Mysql_conf)
            My_cur = My_cxn.cursor()
        SQL = """INSERT INTO bx_shipin(id,title,url,kw,pubtime)
                                      VALUES(NULL,'%s','%s','%s',%s)"""
        try :
            My_cur.execute(SQL%(data.get('title',''),data.get('url',''),data.get('kw',''),0))
            id = int(My_cur.lastrowid)
        except :
            id = 0
        if id :
            My_cxn.commit()
            return True
        else :
            return False
