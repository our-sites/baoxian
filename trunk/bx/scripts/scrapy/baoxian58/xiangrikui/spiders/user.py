#from newtest.items import DmozItem
#coding:utf-8
import scrapy
import urllib2
import json
from xiangrikui.items import  UserItem
import re
import copy
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
class XiangrikuiSpider(scrapy.Spider):
    name = "XiangrikuiSpider"
    allowed_domains = ["bx58.com"]
    start_urls=[]
    for i in range(1,3855):
            start_urls.append("http://www.bx58.com/agentPepole.html?gsid=0&cityid="+str(i))
    #start_urls=start_urls[0:1]
    #start_urls=["http://www.bx58.com/agentPepole.html?gsid=0&cityid=328"]
    def parse(self, response):
        tmp_total_page=response.xpath('//span[@class="total_count"]/text()').extract()[0]
        max_page=re.findall(r"\d+\.?\d*",tmp_total_page.split('/')[1])[0]
        if int(max_page)>=1:
            for i in range(1,int(max_page)+1):
            #for i in range(1,2):
                yield scrapy.Request(response.url+"&page="+str(i),callback=self.parse_page)

    def parse_page(self,response):
        urls=[]
        for sel in response.xpath('//div[@class="txt"]/span[@class="a color"]'):
            tmp_info_url=sel.xpath('a/@href').extract()[0]
            urls.append(tmp_info_url)
            print response.url,tmp_info_url
        #urls=urls[0:1]
        for url in urls:
            item={}
            item["info_url"]=url
            yield scrapy.Request(item["info_url"], meta={'item':item},callback=self.people_info)
    def people_info(self,response):
        item = response.meta['item']
        tmp_image_url=response.xpath('//div[@class="fw1"]/span/img').extract()[0].split("src=")[1].split(' ')[0].split('"')[1]
        item["img_url"]="http://images.bx58.com"+tmp_image_url
        #print response.xpath('//div[@class="com_tp fw2"]/h2[@class="tp cbg"]/text()').extract()[0]
        item["company_name"]=response.xpath('//div[@class="com_tp fw2"]/h2[@class="tp cbg"]/text()').extract()[0]
        for sel in response.xpath('//div[@class="index1 cline"]/div[@class="w1"]'):
            tmp_str="".join(sel.xpath('h2/text()').extract()[0].split())
            item["name"]=tmp_str
            try:
                item["qq"]=sel.xpath('h2/a/img').extract()[0].split("title=")[-1].split('"')[1].split("：")[-1]
            except:
                item["qq"]=''
            item["mail"]=sel.xpath('p/text()').extract()[0].split("：")[-1]
            item["phone"]=sel.xpath('span/b/text()').extract()[0]
            area_info=sel.xpath('span/em/text()').extract()[0].split('·')
            item["province_name"]=area_info[0]
            item["city_name"]=area_info[1]
            item["tag"]=",".join(sel.xpath('p/em/text()').extract())
        for sel in response.xpath('//div[@class="index1 cline"]/div[@class="w3"]/ul[@class="list"]'):
            renzheng_info=sel.xpath('li/p/text()').extract()
            if u"资格证号：" in renzheng_info:
                if len(renzheng_info[renzheng_info.index(u"资格证号：")+1])>1:
                    item["certificate_code"]=renzheng_info[renzheng_info.index(u"资格证号：")+1]
                else:
                    item["certificate_code"]=''
            else:
                item["certificate_code"]=''
            if u"身份证号：" in renzheng_info:
                if len(renzheng_info[renzheng_info.index(u"身份证号：")+1])>1:
                    item["shenfen_code"]=renzheng_info[renzheng_info.index(u"身份证号：")+1]
                else:
                    item["shenfen_code"]=''
            else:
                item["shenfen_code"]=''
        item["des_url"]=response.url+"/presence.html"
        yield scrapy.Request(item["des_url"], meta={'item':item},callback=self.parse_detail)
    def parse_detail(self,response):
        item = response.meta['item']
        try:
            item["introduce"]=response.xpath('//div[@class="about1"]/div[@class="txt"]/text()').extract()[0]
        except:
            item["introduce"]=None
        return item
        # for sel in response.xpath('//dev[@class="about1"]/div[@class="txt'):
        #     try:
        #         content=sel.xpath('p/text()').extract()[0]
        #     except:
        #         pass
        #     else:
        #         item["introduce"]=content
        #     return item