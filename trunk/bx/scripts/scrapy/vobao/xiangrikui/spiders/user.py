# from newtest.items import DmozItem
# coding:utf-8
import scrapy
from xiangrikui.items import UserItem
import re
import copy
import sys
import math

reload(sys)
sys.setdefaultencoding('utf-8')

class XiangrikuiSpider(scrapy.Spider):
    name = "XiangrikuiSpider"
    allowed_domains = ["vobao.com"]
    start_urls = ["http://member.vobao.com/"]

    def parse(self, response):
        for sel in response.xpath('//div[@class="me-area21"]'):
            tmp_urls = sel.xpath('a/@href').extract()
            tmp_names = sel.xpath('a/text()').extract()
        names = [name for name in tmp_names if u"全国" not in name]
        urls = [url for url in tmp_urls if url != "http://member.vobao.com/"]
        # urls=urls[0:1]
        for index, url in enumerate(urls):
            item = {"area_kw": names[index]}
            yield scrapy.Request(url, meta={'item': item}, callback=self.page_list_info, dont_filter=True)

    def page_list_info(self, response):
        item = response.meta['item']
        items = []
        for i in response.xpath('//div[@class="page_change"]/a[@class="page_link"]'):
            if u"尾" in i.xpath('text()').extract()[0]:
                max_url = i.xpath('@href').extract()[0]
                int_url = max_url.split('0_0')[0] + '0_0_'
                max_page = int(max_url.replace("/", "").split('_')[-1])
        for page in range(1, max_page + 1):
            print int_url + str(page)
            ttt = copy.copy(item)
            ttt["url"] = int_url + str(page)
            items.append(ttt)
        for info in items:
            yield scrapy.Request(info["url"], meta={'item': info}, callback=self.area_list_info, dont_filter=True)

    def area_list_info(self, response):
        items = []
        item = response.meta['item']
        for sel in response.xpath(
                '//ul/li[@class="me-hyxx2"]/div[@class="me-hyxx21"]/div[@class="me-hyxx111"]/div[@class="me-hyxx1111"]'):
            ttt = copy.copy(item)
            ttt["geren_url"] = sel.xpath('span[@class="me-hyxx1112"]/span[@class="me-hyxx1123"]/a/@href').extract()[0]
            ttt["info_url"] = sel.xpath('span[@class="me-hyxx1112"]/span[@class="me-hyxx11111"]/a/@href').extract()[0]
            ttt["name"] = sel.xpath('span[@class="me-hyxx11112"]/ul/li/span/a/text()').extract()[0]
            ttt["phone"] = sel.xpath('span[@class="me-hyxx11112"]/ul/li/span[@class="me-hyxx1121"]/text()').extract()[1]
            ttt["company_name"] = ''.join(
                re.findall(u'[\u4e00-\u9fa5]+', sel.xpath('span[@class="me-hyxx11112"]/ul/li/a/text()').extract()[0]))
            # print sel.xpath('span[@class="me-hyxx11112"]/ul/li/a/text()').extract()[3]
            ttt["province_name"] = item["area_kw"]
            ttt["city_name"] = \
                sel.xpath('span[@class="me-hyxx11112"]/ul/li/a/text()').extract()[2].replace("市", "").split(
                    item["area_kw"],
                    1)[-1]
            # ttt["img_url"] = None
            ttt["tag"] = None
            ss = sel.xpath('span[@class="me-hyxx11112"]/ul/li/span/a').extract()
            for i in ss:
                if "qqhits" in i:
                    qq = i.split("qqhits")[-1].split(')')[0].split("'")[1]
                    if qq:
                        ttt["qq"] = qq
                    else:
                        ttt["qq"] = None
            items.append(ttt)
        for info in items:
            yield scrapy.Request(info["info_url"], meta={'item': info}, callback=self.people_info, dont_filter=True)

    def people_info(self, response):
        print response.url
        item = response.meta['item']
        for sel in response.xpath('//div[@class="c_rightbottom"]'):
            if sel.xpath('div[@class="c_rightone"]/ul/li/text()').extract()[-1].split("：") > 1:
                item["mail"] = sel.xpath('div[@class="c_rightone"]/ul/li/text()').extract()[-1].split("：")[-1]
            else:
                item["mail"] = None
            tem = sel.xpath('div[@class="c_rightthree"]/ul/li/text()').extract()
            if tem[-1].split("：") > 1:
                item["evelop_code"] = tem[-1].split("：")[-1]
            else:
                item["evelop_code"] = None
            if tem[-2].split("：") > 1:
                item["certificate_code"] = tem[-2].split("：")[-1]
            else:
                item["certificate_code"] = None
        ques = response.xpath('//div[@class="sign"]/ul/li/text()').extract()[-1]
        item["img_url"] = response.xpath('//div[@class="c_left"]/a/img').extract()[0].split('"')[1]
        jieshao = ''.join(re.findall(
            u'[\u2E80-\u9FFF\u3002\uff1b\uff0c\uff1a\u201c\u201d\uff08\uff09\u3001\uff1f\u300a\uff01\u300ba-zA-Z0-9]+',
            ques))
        if not jieshao:
            item["introduce"] = None
        else:
            item["introduce"] = jieshao
        return item