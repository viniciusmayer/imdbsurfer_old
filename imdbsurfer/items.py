# -*- coding: utf-8 -*-
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class Movie(scrapy.Item):
    genre = scrapy.Field()
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