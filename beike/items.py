# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Field,Item

class BeikeItem(Item):
    collection = table = 'beike'
    zone = Field()
    style = Field()
    village = Field()
    area = Field()
    house = Field()
    position = Field()
    layout = Field()
    price = Field()
    tags = Field()
    sale = Field()
    description = Field()
