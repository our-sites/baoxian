# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class InfoItem(scrapy.Item):
    name = scrapy.Field()
    url = scrapy.Field()
    address = scrapy.Field()
    city = scrapy.Field()
    area = scrapy.Field()
    area_name = scrapy.Field()
    phone = scrapy.Field()

