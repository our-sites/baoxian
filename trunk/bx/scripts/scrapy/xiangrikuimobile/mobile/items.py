# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class UserItem(scrapy.Item):
    uid=scrapy.Field()
    starts = scrapy.Field()
    score = scrapy.Field()
    img_url = scrapy.Field()
    phone = scrapy.Field()
    qq = scrapy.Field()
    weixin = scrapy.Field()