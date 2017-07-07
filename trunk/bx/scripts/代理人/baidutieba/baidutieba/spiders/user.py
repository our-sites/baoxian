# coding:utf-8
# from newtest.items import DmozItem
# coding:utf-8
import scrapy
from baidutieba.items import InfoItem
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

##采集百度贴吧保险吧(移动端)的代理人手机号码###
class BaiDuSpider(scrapy.Spider):
    name = "BaiDuSpider"
    allowed_domains = ["baidu.com"]
    start_urls = ["http://tieba.baidu.com"]
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
        for page in range(0,1000,10) :
            url = "http://tieba.baidu.com/mo/q---1FA20802A0552AE533AA25681DDB1480%3AFG%3D1--1-3-0--2--wapp_1498211779765_111/m?kw=%E4%BF%9D%E9%99%A9&lp=5011&lm=&pn="+str(page)
            print page,'~~~~~~',url
            #yield scrapy.Request(url,callback=self.city_list, dont_filter=True)
    def city_list(self, response):
        info = response.xpath('//html/node()').extract()
        f=open('aaa.html','w')
        f.write(''.join(info))
        f.close()
        city_urls = response.xpath( '//div[@class="content cities"]/ul[@class="cm-grid-list cm-grid-list-flexible"]/li/a/@href').extract()
        city_list = response.xpath( '//div[@class="content cities"]/ul[@class="cm-grid-list cm-grid-list-flexible"]/li/a/text()').extract()
        for index,url in enumerate(city_urls):
            Item = {"city":city_list[index]}
            if url[:1] == 'm' :
                url="baixing.com"+url[1:]
            URL = "http:"+url
            for n in range(1,10):
                yield scrapy.Request(URL+"?page=%d"%n, callback=self.page_list, dont_filter=True, meta={'item': Item})
                #break
            #break

    def page_list(self, response):
        item = response.meta['item']
        urls = response.xpath('//ul[@class="list multiplex gongzuo-list"]/li[@class="item gongzuo"]/a/@href').extract()
        companys=response.xpath('//div[@class="gongzuo-content"]/div[@class="addr-tag"]/span[@class="addr"]/text()').extract()
        for index,url in enumerate(urls):
            iTem = copy.copy(item)
            area_com=companys[index]
            iTem['company']=area_com.split('-')[-1].strip()
            iTem['area'] = area_com.split('-')[0].strip()
            SQL = "SELECT uid FROM agent_caiji_sj WHERE url='%s'"%url
            My_cur.execute(SQL)
            result = My_cur.fetchall()
            if result:
                print result, u'该页面已爬过~~~'
            else:
                yield scrapy.Request(url, callback=self.page_desc, dont_filter=True, meta={'item':iTem})

    def page_desc(self, response):
        pattern = re.compile(r'1[3,5,7,8]\d{9}|0\d{2,3}-\d{6,8}|0\d{10,11}|\d{7,8}')
        item = response.meta['item']
        item['url'] = response.url
        name = response.xpath('//section[@class="user-info"]/a[@class="block gongzuo-block"]/span[@class="contactor"]/text()').extract()
        #company = response.xpath('//div[@class="com"]/div[@class="comWrap"]/h2[@class="c_tit"]/a/text()').extract()
        phone = response.xpath('//div[@class="contact-inner"]/div[@class="contact-container"]/a[@class="contact-btn main-btn"]/@href').extract()
        address = response.xpath('//section[@class="cm-section-content cm-section-content-with-padding content-meta"]/ul[@class="bx-meta-list"]/li[@class="meta-item"]/div/text()').extract()
        if name:
            item['name'] = name[-1].strip().split("：")[-1]
        else:
            name = response.xpath('//section[@class="user-info"]/div[@class="block gongzuo-block"]/span[@class="contactor"]/text()').extract()
            if name:
                item['name'] = name[-1].strip().split("：")[-1]
            else:
                item['name'] = ''

        item['phone'] = ''

        for a in phone:
            m = pattern.search(a)
            if m:
                item['phone'] = m.group()
                break
            else:
                if phone :
                    item['phone'] = phone[0]
                else :
                    item['phone'] = ''

        if address:
            item['address'] = address[-1]
        else:
            item['address'] = ''

        if item['phone']:
            return item
            print "name:",item['name'],"company:",item['company'],"phone:",item['phone'],"address:",item['address'],response.url
        else:
            print '\n\n', item['url'], '~~~~~~~~~~~~~~~~~\r\n\r\n'

##采集百度贴吧保险吧(PC端)的代理人手机号码###
class baiduSpider(scrapy.Spider):
    name = "baiduSpider"
    allowed_domains = ["baidu.com"]
    start_urls = ["http://tieba.baidu.com"]

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

    rules = (Rule(SgmlLinkExtractor(allow=r'http://tieba.baidu.com/.*'), callback='parse', follow=True),)

    def init_request(self):
        """This function is called before crawling starts."""
        return Request(url=self.login_page, callback=self.login)

    def login(self, response):
        """Generate a login request."""
        return FormRequest.from_response(response,
                                         formdata={'name': 'shoringchow@foxmail.com', 'password': 'Lovelan6958'},
                                         callback=self.check_login_response)

    def check_login_response(self, response):
        """Check the response returned by a login request to see if we are
        successfully logged in.
        """
        if "shoringchow" in response.body:
            self.log("Successfully logged in. Let's start crawling!")
            # Now the crawling can begin..
            self.initialized()
        else:
            self.log("Bad times :(")
            # Something went wrong, we couldn't log in, so nothing happens.

    def parse(self, response):
        kw_list=[u'保险',u'保险公司',u'新华保险',u'太平洋保险',u'社保',u'平安保险',u'车险',u'意外险',
                 u'定期寿险',u'终身寿险',u'旅游保险',u'健康保险',u'投连险',u'万能保险',u'分红保险',u'重疾险',
                 u'养老保险',u'医疗保险',u'儿童保险',u'女性保险',u'两全保险',u'理财保险',u'年金保险']
        for kw in kw_list:
            for num in range(0, 750, 50):
                item = {'flag':kw}
                url = "https://tieba.baidu.com/f?kw=%s=utf-8&pn=%s"%(kw,num)
                yield scrapy.Request(url,callback=self.page_list, dont_filter=True, meta={'item':item})

    def page_list(self, response):
        item = response.meta['item']
        urls = response.xpath('//div/div/div[@class="threadlist_lz clearfix"]/div/a/@href').extract()
        for url in urls:
            url = 'http://tieba.baidu.com' + url
            #if self.check_url(url,My_cxn,My_cur):
            #    print u'该页面已爬过~~~'
            #    continue
            iTem = item.copy()
            if 'fid=' not in url :
                yield scrapy.Request(url, callback=self.page_Desc, dont_filter=True, meta={'item':iTem})
            else :
                continue

    def page_Desc(self, response):
        item = response.meta['item']
        item['url'] = response.url
        item['addtime'] = int(time.time())
        pagenum = response.xpath('//div[@class="l_thread_info"]/ul/li[@class="l_reply_num"]/span[@class="red"]/text()').extract()
        maxpage=pagenum[-1]
        ITEM=copy.copy(item)
        if int(maxpage) < 2 :
            yield scrapy.Request(item['url'], callback=self.page_desc, dont_filter=True, meta={'item': ITEM})
        else :
            for page in range(1,int(maxpage)+1) :
                item['url'] = response.url + "?pn=%d"%page
                if self.check_url(item['url'],My_cxn,My_cur):
                    print u'该页面已爬过~~~'
                    continue
                yield scrapy.Request(item['url'], callback=self.page_desc, dont_filter=True, meta={'item': ITEM})

    def page_desc(self, response):
        #pattern = re.compile(r'1[3,5,7,8]\d{9}|0\d{2,3}-\d{6,8}|0\d{10,11}|\d{7,8}')
        pattern_phone = re.compile(r'1[3,5,7,8]\d{9}')
        pattern_weixin = re.compile(r'\w{5,20}')
        iteM = response.meta['item']
        iteM['url'] = response.url
        iteM['toubao'] = 0

        mark_list = [u'微信',u'加v',u'v信',u'加微','vx','v:',u'v：',u'威信',u'加我',u'微同']
        Body = response.body

        ###对正文中的信息过滤###
        info = response.xpath('//div/div/cc/div/text()').extract()
        pattern_time = re.compile(r'20\d{2}-[0-1]\d-[0-3]\d [0-2]\d:[0-5]\d')
        timeinfo = pattern_time.findall(Body)
        for index, i in enumerate(info):
            i = i.lower().replace(' ', '').replace('\t', '')
            item = iteM.copy()
            try :
                item = self.check_com(i,item)
            except Exception,e:
                print e
            mark = 0
            for m in mark_list :
                if m in i :
                    mark+=1

            if mark :
                w = pattern_weixin.search(i)
                if w :
                    item['weixin'] = w.group()
                    item['weixin'] = re.sub('^vx','', item['weixin'])
                    try :
                        item['pubtime'] = time.mktime(time.strptime(timeinfo[index], "%Y-%m-%d %H:%M"))
                    except :
                        if timeinfo :
                            item['pubtime'] = time.mktime(time.strptime(timeinfo[-1], "%Y-%m-%d %H:%M"))
                    if not item.get('cid',0):
                        item = self.get_com(item,My_cxn,My_cur)
                else :
                    item['weixin'] = ''

            m = pattern_phone.findall(i)
            if m:
                for phone in m:
                    item['phone'] = phone
                    try :
                        item['pubtime'] = time.mktime(time.strptime(timeinfo[index], "%Y-%m-%d %H:%M"))
                    except :
                        if timeinfo :
                            item['pubtime'] = time.mktime(time.strptime(timeinfo[-1], "%Y-%m-%d %H:%M"))
                    if not item.get('cid',0):
                        item = self.get_com(item,My_cxn,My_cur)
                    self.insert_data(item, My_cxn, My_cur)
            else:
                if item.get('weixin','') :
                    self.insert_data(item, My_cxn, My_cur)

        ###帖子回复中的信息过滤###
        _pattern_time = re.compile(r'\"now_time\":(\d+?),\"\w+\"\:')
        _pattern_info = re.compile(r'\"content\":(.*?),\"\w+\"\:')
        _timeinfo = _pattern_time.findall(Body)
        _info = _pattern_info.findall(Body)
        for index, _i in enumerate(_info):
            ###将unicode字符串进行转码处理###
            i = _i.decode('unicode_escape')
            ###转小写并去空格tab键###
            i = i.lower().replace(' ', '').replace('\t', '')
            ###去掉无用的超链接###
            i = re.sub('\<ahref\=.*?\<\\\/a\>', '', i)
            i = re.sub('\<imgclass\=.*?"\>', '', i)
            ###去用贴吧中的户名###
            i = re.sub(u'回复.*?:','',i)
            i = re.sub(u'回复.*?：', '', i)

            item = iteM.copy()
            try :
                item = self.check_com(i,item)
            except Exception,e:
                print e
            mark = 0
            for m in mark_list:
                if m in i:
                    mark += 1

            if mark:
                w = pattern_weixin.search(i)
                if w:
                    item['weixin'] = w.group()
                    item['weixin'] = re.sub('^vx','', item['weixin'])
                    try:
                        item['pubtime'] = _timeinfo[index]
                    except:
                        if timeinfo:
                            item['pubtime'] = _timeinfo[-1]
                    if not item.get('cid',0):
                        item = self.get_com(item,My_cxn,My_cur)
                else:
                    item['weixin'] = ''

            m = pattern_phone.findall(i)
            if m:
                for phone in m:
                    item['phone'] = phone
                    try:
                        item['pubtime'] = _timeinfo[index]
                    except:
                        if timeinfo:
                            item['pubtime'] = _timeinfo[-1]
                    if not item.get('cid',0):
                        item = self.get_com(item,My_cxn,My_cur)
                    self.insert_data(item, My_cxn, My_cur)
            else:
                if item.get('weixin', ''):
                    self.insert_data(item, My_cxn, My_cur)

    ###检测url是否已经采集过,防止重复采集###
    def check_url(self,url,My_cxn,My_cur):
        try :
            My_cxn.ping()
        except :
            My_cxn = MySQLdb.connect(**Mysql_conf)
            My_cur = My_cxn.cursor()
        SQL = "SELECT uid FROM agent_caiji_tieba WHERE url='%s'"
        My_cur.execute(SQL%url)
        result = My_cur.fetchall()
        if result :
            return True
        else :
            return False

    ###利用已有的数据,判断当前信息中不含公司信息的进行公司信息补全处理###
    def get_com(self,item,My_cxn,My_cur):
        try :
            My_cxn.ping()
        except :
            My_cxn = MySQLdb.connect(**Mysql_conf)
            My_cur = My_cxn.cursor()
        if item.get('phone',0) :
            SQL="SELECT	company,cid FROM agent_caiji_tieba WHERE phone='%s' AND cid>0 ORDER BY pubtime LIMIT 1"
            My_cur.execute(SQL%item.get('phone',0))
        elif item.get('weixin','') :
            SQL="SELECT	company,cid FROM agent_caiji_tieba WHERE weixin='%s' AND cid>0 ORDER BY pubtime LIMIT 1"
            My_cur.execute(SQL%item.get('weixin',''))
        else :
            return item

        result = My_cur.fetchall()
        if result :
            item['company']=result[0]['company']
            item['cid']=result[0]['cid']
            #print item['url'],item.get('weixin'),'~~~',item.get('phone')
            return item
        else :
            return item

    ###根据采集的内容使用关键词判断该发帖人属于哪家保险公司###
    def check_com(self,i,item):
        if u'太平洋' in i:
            item['cid'] = 99
            item['company'] = u'中国太平洋保险（集团）股份有限公司'
            return item
        if u'太平' in i:
            item['cid']=63
            item['company'] = u'中国太平保险集团有限责任公司'
            return item
        if u'中国人寿' in i or u'国寿' in i:
            item['cid'] = 19
            item['company'] = u'中国人寿保险（集团）公司'
            return item
        if u'泰康' in i:
            item['cid'] = 62
            item['company'] = u'泰康人寿保险股份有限公司'
            return item
        if u'平安' in i:
            item['cid'] = 54
            item['company'] = u'中国平安保险（集团）股份有限公司'
            return item
        if u'中国人民' in i or 'picc' in i or u'人保寿险' in i or u'中国人保' in i:
            item['cid'] = 56
            item['company'] = u'中国人民人寿保险股份有限公司'
            return item
        if u'新华' in i:
            item['cid'] = 69
            item['company'] = u'新华人寿保险股份有限公司'
            return item
        if u'华夏' in i:
            item['cid'] = 26
            item['company'] = u'华夏人寿保险股份有限公司'
        if u'安邦' in i:
            item['cid'] = 1
            item['company'] = u'安邦人寿保险股份有限公司'
        if u'富德' in i:
            item['cid'] = 16
            item['company'] = u'富德生命人寿保险股份有限公司'
        return item

    ###将采集到的数据插入数据库###
    def insert_data(self,data,My_cxn,My_cur):
        try :
            My_cxn.ping()
        except :
            My_cxn = MySQLdb.connect(**Mysql_conf)
            My_cur = My_cxn.cursor()
        SQL = """INSERT INTO agent_caiji_tieba(uid,weixin,phone,company,cid,pubtime,addtime,url,flag)
                                      VALUES(NULL,'%s',%s,'%s',%s,%s,%s,'%s','%s')"""
        try :
            My_cur.execute(SQL%(data.get('weixin',''),data.get('phone',0),data.get('company',''),data.get('cid',0),data.get('pubtime',0),data.get('addtime',0),data.get('url',''),data.get('flag','')))
            uid = int(My_cur.lastrowid)
        except :
            uid = 0
        if uid :
            My_cxn.commit()
            return True
        else :
            return False
