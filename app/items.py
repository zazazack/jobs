# -*- coding: utf-8 -*-
# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html
from datetime import datetime as dt
import json
from pathlib import Path
import re

import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose, TakeFirst, Identity


class JobLoader(ItemLoader):
    default_output_processor = TakeFirst()
    default_input_processor = MapCompose(str.strip)


class Job(scrapy.Item):
    city = scrapy.Field()
    company = scrapy.Field(input_processor=MapCompose(str.strip))
    country = scrapy.Field()
    data = scrapy.Field()
    description = scrapy.Field()
    easy_apply = scrapy.Field()
    file_urls = scrapy.Field()
    files = scrapy.Field()
    id = scrapy.Field(input_processor=Identity())
    image_url = scrapy.Field()
    images = scrapy.Field()
    location = scrapy.Field()
    post_age = scrapy.Field()
    post_dt = scrapy.Field()
    region = scrapy.Field()
    spider = scrapy.Field()
    state = scrapy.Field()
    timestamp = scrapy.Field(input_processor=Identity())
    title = scrapy.Field()
    url = scrapy.Field()
    zip_code = scrapy.Field()
