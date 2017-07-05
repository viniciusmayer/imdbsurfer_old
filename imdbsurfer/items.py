# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class Movie(scrapy.Item):
    index = scrapy.Field()
    year = scrapy.Field()
    link = scrapy.Field()
    name = scrapy.Field()
    genres = scrapy.Field()
    minutes = scrapy.Field()
    rate = scrapy.Field()
    metascore = scrapy.Field()
    votes = scrapy.Field()
    artistsa = scrapy.Field()
    artistsb = scrapy.Field()
    directors = scrapy.Field()
    stars = scrapy.Field()