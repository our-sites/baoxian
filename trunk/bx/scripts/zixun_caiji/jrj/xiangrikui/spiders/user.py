#from newtest.items import DmozItem
#coding:utf-8
import scrapy
import redis
import os.path
from xiangrikui.items import  UserItem
import re
import copy
import sys
import math
import time
reload(sys)
sys.setdefaultencoding('utf-8')
#r=redis.Redis(host='172.16.13.177')
script_pattern = re.compile(r'<script.*<\/script>')
p_pattern = re.compile(r'<p.*</p>')
p = re.compile(r'<a class="ot1".*?(</a>)')
def today_first_time():
    return int(time.time() - (time.time() % 86400) + time.timezone)


class XiangrikuiSpider(scrapy.Spider):
    name = "XiangrikuiSpider"
    allowed_domains = ["insurance.jrj.com.cn"]
    start_urls=["http://insurance.jrj.com.cn/list/hyzx.shtml"]
    def parse(self, response):
        for sel in response.xpath('//ul[@class="jrj-l1"]/li'):
            if not '''class="none"''' in str(sel):
                item={}
                des_url=sel.xpath('span/a/@href').extract()[0]
                item["publishtime"]=int(time.mktime(time.strptime(sel.xpath('i/text()').extract()[0], "%Y-%m-%d")))
                item["addtime"]=int(time.time())
                item["title"]=sel.xpath('span/a/text()').extract()[0]
                item["url"]=des_url
                yield scrapy.Request(des_url,meta={'item':item},callback=self.desc,dont_filter=True)


    def desc(self,response):
        item = response.meta['item']
        tmp_list=[i for i in response.xpath('//div[@class="texttit_m1"]//node()').extract() if p_pattern.match(i) and  not script_pattern.match(i)]
        for index,data in enumerate(tmp_list):
            if  '''<a class="ot1"''' in data or '''<span kwid="stock_''' in data or '''<span id="TrsStock"''' in data:
                ttt=re.sub("<[^<>]+>",'',tmp_list[index])
                tmp_list[index]="<p>  "+ttt+"</p>"
                #print "ttttttttttt"
        str_neirong="".join(tmp_list)
        item["content"]=str_neirong
        span_data=response.xpath('//div[@class="titmain"]/p[@class="inftop"]/span/text()').extract()
        print re.sub('\r\n','',span_data[0])
        item["publishtime"]=int(time.mktime(time.strptime(re.sub('\r\n','',span_data[0]), "%Y-%m-%d %H:%M:%S")))
        if len(span_data)>=5:
            item["writer"]=span_data[3]
        else:
            data=response.xpath('//div[@class="titmain"]/p[@class="inftop"]/span').extract()[1]
            tmp_dic={"91d1878d754c4fdd9669.png":"金融界保险","4e0a6d778bc1523862a5.png":"上海证券报",
                     "4e2d56fd8bc1523862a5.png":"中国证券报","4e2d5b8957287ebf202020202020202020202020.png":"中安在线",
                     "91d1878d754c4fdd966998919053.png":"金融界保险频道","71d58d75665a62a5.png":"燕赵晚报",
                     "8bc1523865f662a57f51.png":"证券时报网","4e2d56fd8bc152387f51.png":"中国证券网",
                     "4e2d56fd4fdd966962a500b74e2d4fdd7f51.png":"中国保险报·中保网",
                     "65b0534e7f51.png":"新华网","84dd9cb865b095fb.png":"蓝鲸新闻",
                     "4e2d56fd4fdd9669884c4e1a534f4f1a.png":"中国保险行业协会","8bc1523865e562a5.png":"证券日报"}
            if len(response.xpath('//div[@class="titmain"]/p[@class="inftop"]/span/a/text()').extract())==2:
                item["writer"]=response.xpath('//div[@class="titmain"]/p[@class="inftop"]/span/a/text()').extract()[0]
            else:
                 img_url=data.split("http://")[-1].split('">')[0]
                 img_name=os.path.basename(img_url)
                 img_list=tmp_dic.keys()
                 if img_name in img_list:
                    item["writer"]=tmp_dic[img_name]
                    #pass
                    #print item
                    return item
                 else:
                    print img_url,response.url,"0000000"
        #print "+++++++++++++++++++++++++++++++++"
        # for sel in response.xpath('//div[@class="titmain"]/p[@class="inftop"]/span/text()').extract():
        #     print sel