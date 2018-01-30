# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import re
from datetime import datetime as dt

import dateparser
import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose, TakeFirst


def parse_age(age):
    """Parse a natural language string denoting age, e.g. '1+ day ago'."""
    age_string = re.sub('\+', '', str(age))
    # if the post is over 30 days old, it is denoted as '30+ days old'
    # strip the '+' sign
    parsed_age = dateparser.parse(age_string)
    return dt.isoformat(parsed_age)


class JobLoader(ItemLoader):
    default_output_processor = TakeFirst()
    default_input_processor = MapCompose(str.strip)


class Job(scrapy.Item):
    company = scrapy.Field()
    jobtitle = scrapy.Field()
    href = scrapy.Field()
    summary = scrapy.Field()
    date = scrapy.Field(input_processor=MapCompose(parse_age))
    sponsored = scrapy.Field()
