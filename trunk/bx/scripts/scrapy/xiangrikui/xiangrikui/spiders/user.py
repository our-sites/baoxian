#from newtest.items import DmozItem
#coding:utf-8
import scrapy
import urllib2
import json
from xiangrikui.items import  UserItem
import copy
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
province_dic={u"北京":34,u"天津":35,u"河北":11,u"山西":12,u"内蒙古":39,u"辽宁":13,u"吉林":14,u"黑龙江":15,u"上海":36,u"江苏":16,u"浙江":17,\
              u"安徽":18,u"福建":19,u"江西":20,u"山东":21,u"河南":22,u"湖北":23,u"湖南":24,u"广东":25,u"广西":38,u"海南":26,u"重庆":37,\
              u"四川":27,u"贵州":28,u"云南":29,u"西藏":40,u"陕西":30,u"甘肃":31,u"青海":32,u"宁夏":41,u"新疆":42,u"台湾":33,u"香港":43,u"澳门":44}
province_dic={u"北京":34}
province_dic={u"天津":35,u"河北":11,u"山西":12,u"内蒙古":39,u"辽宁":13,u"吉林":14,u"黑龙江":15,u"上海":36,u"江苏":16,u"浙江":17,\
              u"安徽":18,u"福建":19,u"江西":20,u"山东":21,u"河南":22,u"湖北":23,u"湖南":24,u"广东":25,u"广西":38,u"海南":26,u"重庆":37,\
              u"四川":27,u"贵州":28,u"云南":29,u"西藏":40,u"陕西":30,u"甘肃":31,u"青海":32,u"宁夏":41,u"新疆":42,u"台湾":33,u"香港":43,u"澳门":44}
area_info=[]
send_headers = {
 'Host':'common.xiangrikui.com',
 'User-Agent':'Mozilla/5.0 (Windows NT 6.2; rv:16.0) Gecko/20100101 Firefox/16.0',
 'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
 'Connection':'keep-alive'
}
for i in province_dic:
    url="http://common.xiangrikui.com/api/v1/locate/provinces/"+str(province_dic[i])+"/cities"
    try:
        proxy=urllib2.ProxyHandler({'http':'58.96.184.188:8088'})
        opener=urllib2.build_opener(proxy)
        urllib2.install_opener(opener)
        req=urllib2.Request(url,headers=send_headers)
        get_api_open=urllib2.urlopen(req)
        get_api_data=json.loads(get_api_open.read())
        get_api_open.close()
    except Exception,e:
        print e
    else:
        for country_info in get_api_data:
            area_info.append({"province_name":i,"province_id":province_dic[i],"city_name":country_info["city_name"],"city_id":country_info["id"]})
tmp_info={}
for i in area_info:
    tmp_info[i["city_id"]]=i["city_name"]
    tmp_info[i["province_id"]]=i["province_name"]
class XiangrikuiSpider(scrapy.Spider):
    name = "XiangrikuiSpider"
    allowed_domains = ["a.xiangrikui.com","bxr.im"]
    start_urls=[]
    for i in area_info:
            start_urls.append("http://a.xiangrikui.com/sf"+str(i["province_id"])+"-cs"+str(i["city_id"])+"/gs.html")
    def parse(self, response):
        province_id=int(response.url.split('sf')[-1].split('-')[0])
        city_id=int(response.url.split('cs')[-1].split('/')[0])
        print province_id,city_id
        for sel in response.xpath('//div[@class="paginage clearfix"]'):
            #item=UserItem()
            item={}
            item["city_name"]=tmp_info[city_id]
            item["province_name"]=tmp_info[province_id]
            item["area_url"]=response.url
            try:
                max_page=sel.xpath('a/@href').extract()[-1].split('page=')[-1]
            except:
                pass
            else:
                for i in range(1,int(max_page)+1):
                    yield scrapy.Request(response.url+"?page="+str(i), meta={'item':item},callback=self.parse_level2)

    def parse_level2(self,response):
        item = response.meta['item']
        name_info=[]
        items=[]
        for sel in response.xpath('//div[@id="agents"]'):
            url_info=sel.xpath('div[@class="agent-info border-org"]/div[@class="agent-header"]/div/a/@href').extract()
            for index,data in enumerate(url_info):
                ttt=copy.copy(item)
                ttt["murl"]=data
                ttt["url"]="http://pc."+data.split("//")[1]
                items.append(ttt)
        for tiem_data in items:
            yield scrapy.Request(tiem_data["url"], meta={'item':tiem_data},callback=self.parse_level3)

    def parse_level3(self,response):
        item = response.meta['item']
        #print item["name"],item["url"]
        item["des_url"]="http://pc.bxr.im"+response.xpath('//div[@class="agent-intro"]/p/a/@href').extract()[0]
        item["name"]=response.xpath('//span[@class="agent-name"]/text()').extract()[0]
        item["company_name"]=response.xpath('//p[@class="agent-company"]/text()').extract()[0].split()[-1]
        print item["company_name"]
        for sel in response.xpath('//div[@class="agent-cert fn-clear"]'):
            item["evelop_code"]="".join(sel.xpath('div/text()').extract()[1].split('：')[-1].split())
            item["certificate_code"]="".join(sel.xpath('div/text()').extract()[3].split('：')[-1].split())
        yield scrapy.Request(item["des_url"], meta={'item':item},callback=self.parse_level4)

    def parse_level4(self,response):
        item = response.meta['item']
        for sel in response.xpath('//div[@class="info-box"]'):
            try:
                content=sel.xpath('p/text()').extract()[0]
            except:
                pass
            else:
                item["introduce"]=content
            return item
