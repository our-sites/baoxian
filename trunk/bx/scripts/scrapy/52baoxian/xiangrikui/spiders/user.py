#from newtest.items import DmozItem
#coding:utf-8
import scrapy
import redis
from xiangrikui.items import  UserItem
import re
import copy
import sys
import math
reload(sys)
sys.setdefaultencoding('utf-8')
r=redis.Redis(host='172.16.13.177')
class XiangrikuiSpider(scrapy.Spider):
    name = "XiangrikuiSpider"
    allowed_domains = ["www.52baoxian.com"]
    start_urls=[]
    for i in range(1,133):
        start_urls.append("http://www.52baoxian.com/agent.php?page="+str(i))
    #start_urls=["http://www.52baoxian.com/agent.php?page=1"]
    def parse(self, response):
        items=[]
        item={}
        for sel in response.xpath('//td/div[@class="bx_yxdy"]/ul'):
            item=copy.copy(item)
            item["info_url"]="http://www.52baoxian.com"+sel.xpath('li[@style="width:100px;text-align:center"]/a/@href').extract()[0]
            tmp_info=sel.xpath('li[@style="width:100px;text-align:center"]/a/img').extract()[0].split('"')
            item["img_url"]="http://www.52baoxian.com"+tmp_info[1]
            item["name"]=tmp_info[5]
            item["phone"]=sel.xpath('li/div/ul/li[@style="color:#444444"]/text()').extract()[0]
            item["company_name"]=sel.xpath('li/div[@class="bx_yxdyhp"]/span/text()').extract()[0]
            items.append(item)
        for tmp_item in items:
            #print tmp_item["info_url"]
            #tmp_item["info_url"]="http://www.52baoxian.com/company-286.html"
            yield scrapy.Request(tmp_item["info_url"], meta={'item':tmp_item},callback=self.people_info,dont_filter=True)


    def people_info(self,response):
        item = response.meta['item']
        #print response.url
        item["des_url"]="http://www.52baoxian.com/"+response.xpath('//dl[@class="infoIntro"]/dd/a/@href').extract()[0]
        for sel in response.xpath('//dl[@class="infoContact"]/dd'):
            info_key=sel.xpath('span/text()').extract()[0]
            info_value=sel.xpath('text()').extract()
            if info_key==u"Mail：":
                if info_value:
                    item["mail"]=info_value[0]
                else:
                    item["mail"]=''
            elif info_key==u"资格证书号码：":
                if info_value:
                    item["certificate_code"]=info_value[0]
                else:
                    item["certificate_code"]=''
            elif info_key==u"执业证编号：":
                if info_value:
                    item["evelop_code"]=info_value[0]
                else:
                    item["evelop_code"]=''
            elif info_key==u"服务地区：":
                if info_value:
                    item["city_name"]=info_value[0].replace(u'市','')
                else:
                    item["city_name"]=''
        #print item.values()
        item["province_name"]=''
        item["tag"]=''
        yield scrapy.Request(item["des_url"], meta={'item':item},callback=self.parse_detail,dont_filter=True)


    def parse_detail(self,response):
        item = response.meta['item']
        try:
            item["introduce"]=response.xpath('//div[@class="mainContent"]/p/text()').extract()[0]
        except Exception,e:
            print e
            item["introduce"]=''
        finally:
            return item
