# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Field


class PaintItem(scrapy.Item):
    name = Field()
    address = Field()
    postal_code = Field()
    phone = Field()
