# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ScrapyBangumiItem(scrapy.Item):
    chName = scrapy.Field() 
    oriName= scrapy.Field()
    info = scrapy.Field()
    href = scrapy.Field()
    imgUrl = scrapy.Field()