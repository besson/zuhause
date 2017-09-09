# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.item import Item, Field


class Home(scrapy.Item):
    location = Field()
    rent_price = Field()
    available_at = Field()
    allows_pets = Field()
    furnished = Field()
    min_time_to_stay = Field()
    deposit = Field()
    source_id = Field()
    description = Field()
    url = Field()
    title = Field()
    dimensions = Field()
    source = Field()
    updated_at = Field()
    address = Field()
    geolocation = Field()
    rooms = Field()
