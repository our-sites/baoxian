# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class UserItem(scrapy.Item):
    province_name = scrapy.Field()
    city_name = scrapy.Field()
    area_url = scrapy.Field()
    company_name = scrapy.Field()
    name = scrapy.Field()
    url = scrapy.Field()
    image_url = scrapy.Field()
    evelop_code = scrapy.Field()
    certificate_code= scrapy.Field()
    des_url = scrapy.Field()
    introduce = scrapy.Field()
    addtime = scrapy.Field()
    tag= scrapy.Field()
    info_url = scrapy.Field()
    qq = scrapy.Field()
    phone = scrapy.Field()
    mail = scrapy.Field()
    shenfen_code = scrapy.Field()
