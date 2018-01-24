# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html


from scrapy.item import Item, Field

class CpsecspidersItem(Item):
    title = Field()
    content = Field()
    url = Field()
    reply = Field()
    click = Field()
    uname = Field()
    source = Field()
    typeid = Field()
    datetime = Field()
    EmotionalScore =Field()