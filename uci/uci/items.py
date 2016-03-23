# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class UciItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    name = scrapy.Field()
    url = scrapy.Field()
    dset_characteristics = scrapy.Field()
    attr_characteristics = scrapy.Field()
    tasks = scrapy.Field()
    instances = scrapy.Field()
    attributes = scrapy.Field()
    missings = scrapy.Field()
    area = scrapy.Field()
    hits = scrapy.Field()
    date = scrapy.Field()

