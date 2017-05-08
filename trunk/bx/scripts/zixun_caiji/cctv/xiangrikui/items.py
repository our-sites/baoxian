# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class UserItem(scrapy.Item):
    url = scrapy.Field()
    type = scrapy.Field()
    addtime = scrapy.Field()
    online_id = scrapy.Field()
    image_mark = scrapy.Field()
    keywords = scrapy.Field()
    summary = scrapy.Field()
    content= scrapy.Field()
    content_forged = scrapy.Field()
    publishtime = scrapy.Field()
    writer = scrapy.Field()
