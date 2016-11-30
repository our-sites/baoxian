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
    allowed_domains = ["fangxinbao.com"]
    start_urls=["http://www.fangxinbao.com/city-all.html"]
    def parse(self, response):
        items=[]
        for sel in response.xpath('//table/tr'):
            province_name=sel.xpath('td[@style="vertical-align:top"]/strong/text()').extract()
            if province_name:
                province_name=''.join(re.findall(u'[\u4e00-\u9fa5a-zA-Z0-9]+',province_name[0]))
                #print province_name
                for city_url in sel.xpath('td/ul/li/a/@href').extract():
                    citycode=city_url.split('-')[-1].split('.')[0]
                    items.append({"province_name":province_name,"city_url":city_url,"city_code":citycode})
        for sel in response.xpath('//ul[@class="zxs clearfix"]/li'):
            tmp_city_url=sel.xpath('a/@href').extract()
            if tmp_city_url:
                for i in tmp_city_url:
                    if "www.fangxinbao.com" in i:
                        citycode=city_url.split('-')[-1].split('.')[0]
                        items.append({"province_name":sel.xpath('a/text()').extract()[0],"city_url":i,"city_code":citycode})
                    else:
                        citycode=city_url.split('-')[-1].split('.')[0]
                        items.append({"province_name":sel.xpath('a/text()').extract()[0],"city_url":"http://www.fangxinbao.com"+i,"city_code":citycode,})
        if r.get('mark'):
            mark=int(r.get('mark'))
        else:
            mark=0

        if mark>=0:
            item=items[mark]
            print "---------------------------------------------------"
            print mark,len(items),item["city_url"]
            #for item in items:
                #item["list_url"]="http://www.fangxinbao.com/yingxiaoyuan"
            yield scrapy.Request(item["city_url"], meta={'item':item},cookies={'cityCode':item["city_code"]},callback=self.cookie_info,dont_filter=True)
            if mark+1<len(items):
               r.set('mark',mark+1)
            else:
               r.set('mark',-1)

    def cookie_info(self,response):
        item = response.meta['item']
        item["list_url"]="http://www.fangxinbao.com/yingxiaoyuan"
        yield scrapy.Request(item["list_url"], meta={'item':item},cookies={'cityCode':item["city_code"]},callback=self.page_info,dont_filter=True)


    def page_info(self,response):
        item = response.meta['item']
        tmp_pop=response.xpath('//div[@class="l"]/span/text()').extract()
        print tmp_pop
        try:
            total_people=int(tmp_pop[0])
        except Exception,e:
            print tmp_pop,item["city_url"]
            total_people=1
        max_page=int(math.ceil(total_people/6.0))
        if max_page>=1:
             for i in range(1,int(max_page)+1):
                yield scrapy.Request(response.url+"/list-"+str(i)+".html",cookies={'cityCode':item["city_code"]}, meta={'item':item},callback=self.city_info,dont_filter=True)
        #print response.xpath('//div[@class="l"]/span/text()').extract(),item["city_code"]

    def city_info(self,response):
        item = response.meta['item']
        items=[]
        #print response.url
        for sel in response.xpath('//div[@class="content"]/div[@class="b_line clearfix"]'):
            tt=copy.copy(item)
            tt["info_url"]=sel.xpath('div/a/@href').extract()[0].replace('www.fangxinbao.com','m.fangxinbao.com')
            tt["img_url"]=sel.xpath('div[@class="floatleft img"]/a/img').extract()[0].split('"')[1]
            tmp_zige=sel.xpath('div[@class="floatleft x2"]/div[@class="y2"]/span/text()').extract()
            if len(tmp_zige)>1:
                tt["certificate_code"]=tmp_zige[1]
            else:
                tt["certificate_code"]=''
            tt["name"]=sel.xpath('div[@class="floatleft x2"]/div[@class="y1"]/a/text()').extract()[0]
            tmp_area_company=sel.xpath('div[@class="floatleft x2"]/div[@class="y1"]/span/text()').extract()[0].split('  ')
            tt["city_name"]=tmp_area_company[1].replace(u"市",'')
            tt["company_name"]=tmp_area_company[0]
            items.append(tt)
        #items=items[0:2]
        for item in items:
            #item["people_url"]="http://m.fangxinbao.com/yingxiaoyuan/118188.html"
            yield scrapy.Request(item["info_url"], meta={'item':item},cookies={'cityCode':item["city_code"]},callback=self.parse_detail,dont_filter=True)


    def parse_detail(self,response):
        item = response.meta['item']
        for sel in response.xpath('//div[@class="contanctbox pdg ryzs"]/div[@class="cardname"]'):
            mail=sel.xpath('p/i[@id="mail"]/text()').extract()
            if mail:
                item["mail"]=mail[0]
            else:
                item["mail"]=''
            phone_info=sel.xpath('p/i/a/text()').extract()
            if phone_info:
                if phone_info[0].isdigit():
                    item["phone"]=phone_info[0]
                else:
                    item["phone"]=''
            else:
                item["phone"]=''
        item["tag"]=','.join(response.xpath('//div[@class="cardname"]/div[@class="grjjcont"]/div/label/text()').extract())
        item["introduce"]=(''.join(re.findall(u'[\u2E80-\u9FFFa-zA-Z0-9]+',response.xpath('//div[@class="cardname"]/div[@class="grjjcont"]/dl/text()').extract()[0])))
        return item