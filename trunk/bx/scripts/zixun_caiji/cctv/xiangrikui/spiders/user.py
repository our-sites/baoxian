#from newtest.items import DmozItem
#coding:utf-8
import scrapy
import redis
from xiangrikui.items import  UserItem
import re
import copy
import sys
import math
import time
reload(sys)
sys.setdefaultencoding('utf-8')
script_pattern = re.compile(r'<script.*<\/script>')
p_pattern = re.compile(r'<p.*</p>')


def today_first_time():
    return int(time.time() - (time.time() % 86400) + time.timezone)


class XiangrikuiSpider(scrapy.Spider):
    name = "XiangrikuiSpider"
    allowed_domains = ["cctv.com"]
    start_urls=["http://search.cctv.com/search.php?qtext=保险&type=web&page=1&datepid=1&vtime=-1&sort=date&channel=新闻",
                "http://search.cctv.com/search.php?qtext=保险&type=web&page=1&datepid=1&vtime=-1&sort=date&channel=经济"]
    #start_urls=["http://search.cctv.com/search.php?qtext=保险&type=web&page=1&datepid=1&vtime=-1&sort=date&channel=经济"]
    def parse(self, response):
        for sel in response.xpath('//ul[@id="ccd"]/li'):
            des_url=sel.xpath('h3/a/@href').extract()[0]
            time_info=sel.xpath('span[@style="float:right"]/text()').extract()[0]
            print int(time.mktime(time.strptime(time_info.split("发布时间：")[-1], "%Y-%m-%d %H:%M:%S")))
            item={}
            item["title"]="".join(sel.xpath('h3/a/text()').extract())
            item["url"]=des_url
            item["publishtime"]=int(time.mktime(time.strptime(time_info.split("发布时间：")[-1], "%Y-%m-%d %H:%M:%S")))
            item["addtime"]=int(time.time())
            if "%E7%BB%8F%E6%B5%8E" in response.url:
                item["type"]="经济"
            else:
                item["type"]="新闻"
            if int(item["publishtime"]) > today_first_time():
                yield scrapy.Request(des_url,meta={'item':item},callback=self.desc,dont_filter=True)
            else:
                pass


    def desc(self,response):
        item = response.meta['item']
        if response.xpath('//div[@class="col_w660"]/div[@class="cnt_bd"]/div[@class="function"]/span/i/a/text()').extract():
            item["writer"]=response.xpath('//div[@class="col_w660"]/div[@class="cnt_bd"]/div[@class="function"]/span/i/a/text()').extract()[0]
        else:
            item["writer"]=response.xpath('//div[@class="col_w660"]/div[@class="cnt_bd"]/div[@class="function"]/span/i/text()').extract()[0].split("来源：")[1].split()[0]
        tmp_list=[i for i in response.xpath('//div[@class="col_w660"]/div[@class="cnt_bd"]//node()').extract() if p_pattern.match(i) and  not script_pattern.match(i) and "player.cntv.cn" not in i]
        str_neirong="".join(tmp_list)
        #print str_neirong
        item["content"]=str_neirong
        return item