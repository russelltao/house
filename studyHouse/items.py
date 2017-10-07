# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class LianjiaCJItem(scrapy.Item):
    area = scrapy.Field()
    subarea = scrapy.Field()
    title = scrapy.Field()
    totalPrice = scrapy.Field()
    dealDate = scrapy.Field()
    houseInfo = scrapy.Field()
    positionInfo = scrapy.Field()
    source = scrapy.Field()
    unitPrice = scrapy.Field()

class LianjiaZSItem(scrapy.Item):
    area = scrapy.Field()
    subarea = scrapy.Field()
    title = scrapy.Field()
    totalPrice = scrapy.Field()
    houseInfo = scrapy.Field()
    positionInfo = scrapy.Field()
    source = scrapy.Field()
    unitPrice = scrapy.Field()
    followInfo = scrapy.Field()#15人关注 / 共2次带看 / 2个月以前发布