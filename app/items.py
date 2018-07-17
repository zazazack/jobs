# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import re
from datetime import datetime as dt

# import dateparser
import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose, TakeFirst


def build_job_post_url_with_jobkey(jobkey):
    return f'https://www.indeed.com/viewjob?jk={jobkey}'


def is_sponsored(s):
    s = s.lower().strip()
    if 'sponsored' in s:
        return True
    else:
        return False


class JobLoader(ItemLoader):
    default_output_processor = TakeFirst()
    default_input_processor = MapCompose(str.strip)


class Job(scrapy.Item):
    company = scrapy.Field()
    id = scrapy.Field()
    job_type = scrapy.Field() # full-time, part-time, etc.
    jobtitle = scrapy.Field()
    location = scrapy.Field()
    post_age = scrapy.Field()
    post_url = scrapy.Field(input_processor=MapCompose(build_job_post_url_with_jobkey))
    sponsored = scrapy.Field(input_processor=MapCompose(is_sponsored))
    summary = scrapy.Field()

class Page(scrapy.Item):
    id = scrapy.Field()
    page_text = scrapy.Field()
    page_title = scrapy.Field()
    url = scrapy.Field()
